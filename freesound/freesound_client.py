"""
The module contains the definition of the FreeSoundClient, the core of the library	
"""
from datetime import datetime
from time import sleep
import traceback
from typing import Any, NoReturn
import json 
from io import BytesIO
import os
import sys
from requests import ReadTimeout, Response # type: ignore

import freesound.freesound_api as freesound_api
from .freesound_errors import FieldError, FreesoundError
from .freesound_requests import AuthorizationError
from .freesound_sound import FreeSoundSoundInstance
from .formatting import headline, separator,ask, warning,error,info,log,unpack_features


class FreeSoundClient:
	"""The core class of the library

	The `FreeSoundClient` is a wrapper around the [`freeesound_api`](api-fs-api.md).
	It facilitates the formulation of queries to make requests to the [Freesound Database](https://www.freesound.org).
	It handles bulk files download and can write `json` files from the queries.

	Check the [Tutorial](../tutorial.md) and [How-To](../how-to-guide.md) sections of this documentation for a detailed explanation of its usage.

	Args:
		user_id (str): the User id
		api_key (str): the API key
		download_folder (str | None, optional): the path where sound files should be downloaded.
		token_file_path (str, optional): the Path to a `json` file containing the user's access token.

	Usage:
		```
		>>> c = FreesoundClient('<your-user-id>','<your-api-key>', 'sound_lib', 'access_token.json')
		```
	"""
	def __init__(self, user_id:str, api_key:str, download_folder:str|None=None, token_file_path:str="access_token.json") -> None:
		self._user_id = user_id # private
		self._api_key = api_key # private
		self._access_token = "" # private
		self._token_file_path = token_file_path # private

		self._username = "" # read-only
		self._page_size = 15 # read-only
		self._results_page:dict[str,Any] = {} # read-only
		self._results_list:dict[str,Any] = {'results':[], 'timestamp':datetime.now().isoformat(), 'count':0} # read-only

		self._download_count = 15 # read-only
		self._download_list:dict[str,Any] = {'downloaded-files':[], 'timestamp':datetime.now().isoformat(), 'count':0} # read-only
		self._download_folder = download_folder # read-write

		try:
			token_data = self._load_token_from_file()
		except FileNotFoundError:
			print("No access token file found. Authorizing...")
			token_data = self._authorize()

		self._update_access_data(token_data)
		
		try:
			self._get_my_infos()
		except AuthorizationError:
			self._refresh_access_token()
			self._get_my_infos()
		
		print(f"FreeSound Client {self._username} Initialized")
		separator()

	"""
	AUTHORIZATION
	-------------
	"""	
	def _load_token_from_file(self) -> dict[str,str]:
		with open(self._token_file_path,"r") as file:
			print("Loading token from file")
			separator()

			return json.load(file)
		
	def _authorize(self) -> dict[str,str]:
		if self._user_id == "" and self._api_key == "":
			separator()
			print("You must provide a valid user id and API key")
			print("Visit https://freesound.org/help/developers/ for applying")
			separator()
			self.logout()
		# STEP 1
		params: dict[str,str] = {"client_id":self._user_id, "response_type":"code", "state": "xyz"}
		#use /logout_and_authorize/ if want the user to login before the authorization
		auth_url = "https://freesound.org/apiv2/oauth2/authorize/"
		authorization_url: str = auth_url+"?"+"&".join([f"{key}={value}" for key, value in params.items()])
		print(headline(f"Visit this page to authorize your user: {authorization_url}", centered=True))
		# STEP 2
		access_data:dict[str,Any] = {}
		authorization_code: str = input("Enter the authorization code from the redirect URL: ")
		access_data = freesound_api.get_access_token(self._user_id, self._api_key, authorization_code)
		
		print("Authorization succeded!")
		self._update_access_data(access_data)
		return access_data
	
	def _refresh_access_token(self) -> None:
		print('Refreshing Access Token')
		try:
			token_data = freesound_api.refresh_access_token(self._user_id, self._api_key, self._refresh_token)
			self._update_access_data(token_data)
		except Exception as e:
			self._handle_exception(e)
	
	def _update_access_data(self, access_data:dict[str,Any]) -> None:
		access_token: str | None = access_data.get('access_token')
		refresh_token: str | None = access_data.get('refresh_token')
		if access_token is not None and refresh_token is not None:
			self._access_token = access_token
			self._refresh_token = refresh_token
			self._save_access_token(access_data)
		else:
			print("The access data provided is not valid")
			self.logout()

	def _save_access_token(self,access_data:dict[str,Any]) -> None:
		with open(self._token_file_path, "w") as file:
			json.dump(access_data, file)

	"""
	API
	---
	"""	
	def search(self, query:str,filters:str='',fields:str='',descriptors:str='',sort_by:str='score',page_size:int=15, normalized:int=0) -> dict[str,Any]:
		"""wrapper around the [`search()`][freesound.freesound_api.search] function 

		see: <https://freesound.org/docs/api/resources_apiv2.html#search-resources> for details

		Args:
			query (str): a string of space-separated word to search into the [Freesound Database](https://www.freesound.org)
			filters (str, optional): a string of valid filter:value string (see: [`FreeSoundFilters`][freesound.freesound_filters.FreeSoundFilters] for help)
			fields (str, optional): a coma-separated string of valid `fields` (see: [`FreeSoundFields`][freesound.freesound_fields.FreeSoundFields] for help)
			descriptors (str, optional): a coma-separated string of valid `descriptors` (see: [`FreeSoundDescriptors`][freesound.freesound_descriptors.FreeSoundDescriptors] for help). This attribute must be used in combination with the field `analysis`
			sort_by (str, optional): a string defining how the search results should be organised (see: [`FreeSoundFilters`][freesound.freesound_filters.FreeSoundSort] for help)
			page_size (int, optional): the maximum count of items that should be returned by the search result
			normalized (int, optional): whether the sound `descriptors` values should be normalized or not

		Returns:
			a json object representing the Response from the freesound database <https://freesound.org/docs/api/resources_apiv2.html#response>
		"""
		if page_size > 150: # see documentation https://freesound.org/docs/api/resources_apiv2.html#response-sound-list
			warning(f"Page size {page_size} too big. Setting it to 150")
		print(f"Searching for {query}")
		self._page_size = min(page_size,150)
		try:
			search_data = freesound_api.search(query, self._access_token,fields,filters,descriptors,sort_by,self._page_size,normalized)
			self._results_page = search_data
			self._update_result_list(search_data)
			if search_data["count"] == 0:
				print("No results found")
			else:
				print(f"Found {search_data['count']} results")
		except Exception as e:
			self._handle_exception(e)
		
		return search_data
	
	def get_track_info(self, track_id:int|str, track_name:str|None=None, fields:str|None=None,descriptors:str|None=None) -> FreeSoundSoundInstance:
		"""a wrapper around the [`get_track_info()`][freesound.freesound_api.get_track_info] function 

		This function queries the database to get the infos of a sound identified by `id`.
		Check the documentation for more help: <https://freesound.org/docs/api/resources_apiv2.html#sound-instance>

		Args:
			track_id (Any): the `id` of the sound
			track_name (str | None, optional): the name of the sound track with the provided `id`
			fields (str | None, optional): a coma-separated string of valid `fields` (see: [`FreeSoundFields`][freesound.freesound_fields.FreeSoundFields] for help)
			descriptors (str | None, optional): a coma-separated string of valid `descriptors` (see: [`FreeSoundDescriptors`][freesound.freesound_descriptors.FreeSoundDescriptors] for help). This attribute must be used in combination with the field `analysis`

		Returns:
			an instance of a sound with default or specified `fields`
		"""
		if track_name is not None:
			print(f"Getting {track_name} infos")
		else:
			print(f"Getting track {track_id} infos")
		try:
			track_info = freesound_api.get_track_info(str(track_id),self._access_token,fields,descriptors)
			audio_track = FreeSoundSoundInstance(track_info)
		except Exception as e:
			self._handle_exception(e)
		return audio_track

	def download_track(self, url:str, filename:str, outfolder:str) -> None:
		"""a wrapper around the [`download_track()`][freesound.freesound_api.download_track] function 

		Downloads a track for a valid download `url` retrived from the [Freesound Database](https://www.freesound.org)
		
		See: <https://freesound.org/docs/api/resources_apiv2.html#download-sound-oauth2-required> for details
		

		Args:
			url (str): the download link for a specific sound
			filename (str): the name of the file to download
			outfolder (str): the folder where the file should be downloaded
		"""
		print(f"Downloading {filename}")
		try:
			file_response: Response = freesound_api.download_track(url, self._access_token)
			binary_data = BytesIO(file_response.content)
			self._write_audio_file(binary_data, filename, outfolder)
		except Exception as e:
			self._handle_exception(e)

	def get_next_page(self, url:str) -> dict[str,Any]:
		"""a wrapper around the [`get_next_page()`][freesound.freesound_api.get_next_page] function 

		Args:
			url (str): a url retrieved from a previous 'search' request

		Returns:
			a json object representing the Response from the freesound database <https://freesound.org/docs/api/resources_apiv2.html#response>
		"""
		print("Getting next page")
		separator()
		try:
			page = freesound_api.get_next_page(url, self._access_token)
			self._results_page = page
			self._update_result_list(page)
		except Exception as e:
			self._handle_exception(e)
		return page
	
	def _get_my_infos(self) -> dict[str, Any]:
		print("Getting Client Info")
		user_data = freesound_api.get_my_infos(self._access_token)
		try:
			self._parse_user_info(user_data)
		except Exception as e:
			self._handle_exception(e)
		return user_data

	"""
	PROPERTIES
	----------
	"""
	@property # read-only
	def username(self) -> str:
		"""read-only

		Returns:
			the username associated with this `FreeSoundClient` identified by `user_id`
		"""
		return self._username

	@property # read-only
	def page_size(self) -> int:
		"""read-only

		Returns:
			the maximum count of items that should be returned by the search result specified in the [`search`][freesound.freesound_client.FreeSoundClient.search] function.
		"""
		return self._page_size
	
	@property # read-only
	def results_list(self) -> dict[str,Any]:
		"""read-only

		Returns:
			a `json` object containing the response of a [`search`][freesound.freesound_client.FreeSoundClient.search] request.
		"""
		return self._results_list
	
	@property # read-only
	def download_count(self) -> int:
		"""read-only

		Returns:
			how many files have been downloaded
		"""
		return self._download_count
	
	@property
	def download_list(self) -> dict[str, list[dict[str, Any]]]:
		"""read-only

		Returns:
			a detailed list of the downloaded files in `json` format
		"""
		return self._download_list

	@property
	def download_folder(self) -> str|None:
		"""
		Returns:
			the name of the folder where audio files should be downladed
		"""
		return self._download_folder

	@download_folder.setter
	def download_folder(self,path:str) -> None:
		"""
		Args:
		 	path (str): the name of the folder where audio files should be downladed
		"""
		self._download_folder = path

	"""
	UTILITIES
	---------
	"""	
	def _set_download_count(self,count:int|None):
		max_value = self._results_page['count']
		if count is None:
			self._download_count = self._prompt_downloads(max_value)
		else:
			if count <= max_value:
				self._download_count = count
			else:
				warning(f"You want to download {count} files, but only {max_value} were found")
				self._download_count = max_value

	def download_results(self,output_folder_path:str|None=None,files_count:int|None=None) -> None:
		"""download `files_count` audio files into `output_folder_path`

		This function takes care of pagination automatically

		Args:
			output_folder_path (str | None, optional): The name of the output folder.
			files_count (int | None, optional): how many files should be downloaded. 
		"""
		self._set_download_count(files_count)
		if output_folder_path is not None:
			self._download_folder = output_folder_path
		else:
			if self._download_folder is None:
				self._download_folder = self._prompt_output_folder()
		
		print(f"Downloading {self._download_count} files of {self._results_page['count']}")
		separator()
		downloaded_count = 0
		while downloaded_count < self._download_count:
			for sound in self._results_page['results']:
				if downloaded_count < self._download_count:
					try:
						parsed_sound = FreeSoundSoundInstance(sound)
					except Exception as e:
						self._handle_exception(e)
					
					print(parsed_sound.name)
					filepath = os.path.join(self._download_folder,parsed_sound.name)
					
					if os.path.exists(filepath):
						warning(f"The file {parsed_sound.name} has already been downloaded...Skipping")
						separator()
						sleep(0.1) # avoid throttling
						pass
					else:
						try:
							self.download_track(parsed_sound.ensure_value('download'),parsed_sound.name, self._download_folder)
						except Exception as e:
							self._handle_exception(e)
						downloaded_count+=1
						self._update_download_list(sound, downloaded_count)
						info(f"Downloaded Files: {downloaded_count} of {self._download_count}")
						separator()
				else:
					break
			if downloaded_count < self._download_count:
				if not self._set_next_page():
					break
		info("Done Downloading")

	def write_download_list(self,filename:str="downloads.json", folder:str|None=None) -> None:
		"""save a detailed list of the downloaded files in a `json` file

		If `folder` is not provided the client will prompt the user for this information

		Args:
			filename (str, optional): the name of the file to save
			folder (str | None, optional): the name of the folder where to save the file
		"""
		self._write_json(self._download_list,filename, folder)
		
	def write_result_list(self,filename:str='results_list.json', folder:str|None=None) -> None:
		"""save a detailed list of the [`search`][freesound.freesound_client.FreeSoundClient.search] response in a `json` file

		If `folder` is not provided the client will prompt the user for this information

		Args:
			filename (str, optional): the file of the files where the list should be saved
			folder (str | None, optional): the name of the folder where to save the file
		"""
		self._write_json(self._results_list,filename, folder)
	def dump_results(self, data:dict[str,Any]|None=None):
		"""pretty print the result of a [`search`][freesound.freesound_client.FreeSoundClient.search]

		Args:
			data (dict[str,Any] | None, optional): a `dict` (for example the result of a [`search`][freesound.freesound_client.FreeSoundClient.search]). By default it will print the result of the last performed search.
		"""
		if data is None:
			data = self._results_list
		for key, values in data.items():
			if isinstance(values, list):
				for value in values: # type:ignore
					separator()
					for x,y in value.items(): # type:ignore
						if isinstance(y,dict):
						# 	for desc,desc_values in y.items(): # type:ignore
						# 		log(desc,values)
						# else:
							log(x, unpack_features(y))
						else:
							log(x, y)
			else:
				log(str(key),values)
			print('')

	def _prompt_downloads(self,downloadable:int)-> int:
		if downloadable == 0:
			warning("There is nothing to download")
			self.logout()
		max_download = None
		while True:
			try:
				max_download_input: str = ask("How many files do you want to download? [a number | all] ")
				if max_download_input == 'all' or max_download_input == '':
					max_download = downloadable
				else:
					max_download = int(max_download_input)
				break
			except ValueError:
				warning("You must insert a number or type 'all'")
				continue
		if max_download > downloadable:
			warning("You are trying to download more files that are actually available")
			warning(f"Setting {downloadable} as the number of files to download")
			max_download = downloadable
		return max_download
	
	def _prompt_output_folder(self) -> str:
		output_folder = ask("Please set an output folder: ")
		if output_folder != "":
			if output_folder.endswith("/"):
				return output_folder
			else:
				return output_folder+"/"
		else:
			return "./"

	def _update_result_list(self, list:dict[str,Any]):
		self._results_list['count'] += list['count']
		self._results_list['timestamp'] = datetime.now().isoformat()
		self._results_list['results'].extend(list['results'])

	def _update_download_list(self, sound_obj:dict[str,Any], count:int):
		self._download_list['count'] = count
		self._download_list['timestamp'] = datetime.now().isoformat()
		self._download_list['downloaded-files'].append(sound_obj)

	def _check_for_path(self,filename:str, folder:str|None) -> str:
		if folder is None:
			if self._download_folder is None:
				out_folder = self._prompt_output_folder()
			else:
				out_folder = self._download_folder
		else:
			if folder == "":
				out_folder = "."
			else:
				out_folder=folder
			self._download_folder = folder

		if not os.path.exists(out_folder):
			os.mkdir(out_folder)
		output_path = os.path.join(out_folder,filename)
		while os.path.exists(output_path):
			warning(f"The File {output_path} already exists")
			new_filename = ask("Press Enter to overwrite or set a new filename: ")
			if new_filename.strip() == "":
				info(f"Overwriting {filename}")
				break
			else:
				output_path = os.path.join(out_folder,new_filename)
		return output_path

	def _write_audio_file(self, data:BytesIO, file_name:str, folder:str) -> None:
		output_path = self._check_for_path(file_name,folder)
		with open(output_path,"wb") as file:
			file.write(data.read())

	def _write_json(self,data:dict[Any,Any], filename:str, folder:str|None):
		output_path = self._check_for_path(filename,folder)
		if ".json" not in output_path:
			filename += ".json"
		with open(output_path, "w") as outfile:
			json.dump(data, outfile, indent=4)
		info(f"File: {output_path} written!")

	def _set_next_page(self) -> bool:
		if self._results_page["next"] is not None:
			url:str = self._results_page["next"]
			self.get_next_page(url)
			return True
		else:
			return False

	def _parse_user_info(self,data:dict[str,Any]):
		# we could set more user's information in this function
		# check this page for more info: https://freesound.org/docs/api/resources_apiv2.html#user-instance
		self._username = data['username']

	def _handle_exception(self, e:Exception) -> NoReturn:
		if isinstance(e, FreesoundError):
			error(e.args[0])
		elif isinstance(e, AuthorizationError):
			error(e.args[0])
		elif isinstance(e, FieldError):
			error(e.args[0])
		else:
			if isinstance(e, ReadTimeout):
				error("Connection Timeout!")
			else:
				print("Caught a generic Exception. Copy the printed infos and inform the developers")
				print(traceback.format_exc())
		self.logout()

	def __repr__(self) -> str:
		return f"<freesound.freesound_client.FreeSounClient {self._username}>"

	def logout(self) -> NoReturn:
		"""Closes the program

		Should not normally need to be called explicitly

		Calls `sys.exit(0)`
		"""
		print(headline("Logging out"))
		sys.exit(0)

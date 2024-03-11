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
from .freesound_downloader import Downloader
from .freesound_errors import FieldError, FreesoundDownloadError, FreesoundError
from .freesound_requests import AuthorizationError
from .freesound_sound import FreeSoundSoundInstance
from .formatting import headline, separator,ask, separator_red, warning,error,info,log,unpack_features


class FreeSoundClient:
	"""The core class of the library

	The `FreeSoundClient` is a wrapper around the [`freeesound_api`](api-fs-api.md).
	It facilitates the formulation of queries to make requests to the [Freesound Database](https://www.freesound.org).
	It handles bulk files download and can write `json` files from the queries.

	Check the [Tutorial](../tutorials/tutorial-basics.md) and [How-To](../how-to-guide.md) sections of this documentation for a detailed explanation of its usage.

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

		self._downloader = Downloader(self)

		# self._download_count = 15 # read-only
		self._download_folder = download_folder # read-write

		try:
			token_data = self._load_token_from_file()
		except FileNotFoundError:
			print("No access token file found. Authorizing...")
			token_data = self._authorize()

		self._update_access_data(token_data)
		
		try:
			self.get_my_infos()
		except AuthorizationError:
			self._refresh_access_token()
			self.get_my_infos()
		
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
	def search(self, query:str,filter:str='',fields:str='',descriptors:str='',sort_by:str='score',page_size:int=15, normalized:int=0) -> dict[str,Any]:
		"""wrapper around the [`search()`][freesound.freesound_api.search] function 

		see: <https://freesound.org/docs/api/resources_apiv2.html#search-resources> for details

		Args:
			query (str): a string of space-separated word to search into the [Freesound Database](https://www.freesound.org)
			filter (str, optional): a string of valid filter:value string (see: [`FreeSoundFilters`][freesound.freesound_filters.FreeSoundFilters] for help)
			fields (str, optional): a coma-separated string of valid `fields` (see: [`FreeSoundFields`][freesound.freesound_fields.FreeSoundFields] for help)
			descriptors (str, optional): a coma-separated string of valid `descriptors` (see: [`FreeSoundDescriptors`][freesound.freesound_descriptors.FreeSoundDescriptors] for help). This attribute must be used in combination with the field `analysis`
			sort_by (str, optional): a string defining how the search results should be organised (see: [`FreeSoundFilters`][freesound.freesound_filters.FreeSoundSort] for help)
			page_size (int, optional): the maximum count of items that should be returned by the search result
			normalized (int, optional): whether the sound `descriptors` values should be normalized or not

		Returns:
			a json object representing the Response from the freesound database <https://freesound.org/docs/api/resources_apiv2.html#response-sound-list>
		"""
		if page_size > 150: # see documentation https://freesound.org/docs/api/resources_apiv2.html#response-sound-list
			warning(f"Page size {page_size} too big. Setting it to 150")
		print(f"Searching for {query}")
		self._page_size = min(page_size,150)
		try:
			search_data = freesound_api.search(query, self._access_token,fields,filter,descriptors,sort_by,self._page_size,normalized)
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
	
	def get_similar_track(self,track_id:int|str,track_name:str|None=None,fields:str|None=None,descriptors_filter:str|None=None,descriptors:str|None=None,page_size:int=15,normalized:int=0) -> dict[str, Any]:
		"""a wrapper around the [`get_similar()`][freesound.freesound_api.get_similar] function

		This function queries the Database to retrieve similar sound of another sound identified by `track_id`.
		It does not allow the use of filters but you can specify a `descriptors_filter`

		Args:
			track_id (int | str): the `id` of the sound
			track_name (str | None, optional):the name of the sound track with the provided `id`
			fields (str | None, optional): a coma-separated string of valid `fields` (see: [`FreeSoundFields`][freesound.freesound_fields.FreeSoundFields] for help)
			descriptors (str | None, optional): a coma-separated string of valid `descriptors` (see: [`FreeSoundDescriptors`][freesound.freesound_descriptors.FreeSoundDescriptors] for help). This attribute must be used in combination with the field `analysis`
			descriptors_filter (str | None, optional): a string of valid descriptor:value string (see: [`Filter.from_descriptor`][freesound.filter_types.Filter.from_descriptor] for help)
			page_size (int, optional): _description_. Defaults to 15.
			normalized (int, optional): _description_. Defaults to 0.

		Returns:
			a json object representing the Response from the freesound database <https://freesound.org/docs/api/resources_apiv2.html#response-sound-list>
		"""
		if track_name is not None:
			print(f"Getting tracks similar to {track_name}")
		else:
			print(f"Getting tracks similar to {track_id}")
		try:
			similar_tracks = freesound_api.get_similar(str(track_id),self._access_token,fields,descriptors_filter,descriptors,page_size,normalized)
			self._results_page = similar_tracks
			self._update_result_list(similar_tracks)
			if similar_tracks["count"] == 0:
				print("No results found")
			else:
				print(f"Found {similar_tracks['count']} results")
		except Exception as e:
			self._handle_exception(e)
		return similar_tracks


	def download_track(self, url:str, filename:str, outfolder:str|None=None, skip:bool=False) -> bool:
		"""a wrapper around the [`download_track()`][freesound.freesound_api.download_track] function 

		Downloads a track given a valid download `url` retrieved from the [Freesound Database](https://www.freesound.org)
		
		See: <https://freesound.org/docs/api/resources_apiv2.html#download-sound-oauth2-required> for details
		
		Args:
			url (str): the download link for a specific sound
			filename (str): the name of the file to download
			outfolder (str): the folder where the file should be downloaded
			skip (bool, optional): whether to skip a file if it already exists.
		
		Returns:
			bool: `True` if the file has been downloaded, `False` otherwise 
		"""
		if outfolder is not None:
			self._download_folder = outfolder
		print(f"Downloading {filename}")
		out_file = self._check_for_path(filename,skip)
		if  out_file is None:
			sleep(0.1) # avoid throttling
			return False
		else:
			try:
				file_response: Response = freesound_api.download_track(url, self._access_token)
				binary_data = BytesIO(file_response.content)
				self._write_audio_file(binary_data, out_file)
				return True
			except Exception as e:
				self._handle_exception(e)

	def download_analysis(self, url:str, filename:str, outfolder:str|None=None, skip:bool=False,timestamp:bool=True) -> bool:
		"""a wrapper around the [`download_analysis_data()`][freesound.freesound_api.download_analysis_data] function 

		download the frame-by-frame analysis file given a valid `analysis_frame` url file

		Args:
			url (str): the download link for the sound analysis
			filename (str): the name of the sound file
			outfolder (str | None, optional): the destination folder
			skip (bool, optional): whether to skip a file if it already exists.

		Returns:
			bool: `True` if the data file has been downloaded, `False` otherwise 
		"""
		filename += ".analysis.json"
		if outfolder is not None:
			self._download_folder = outfolder
		out_file = self._check_for_path(filename,skip)
		print(f"Downloading {filename} analysis data")
		if out_file is None:
			sleep(0.1)
			return False
		else:
			try:
				file_response: dict[str,Any] = freesound_api.download_analysis_data(url,self._access_token)
				self._write_json(file_response,out_file)
				return True
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
	
	def get_my_infos(self) -> dict[str, Any]:
		"""a wrapper around the [`get_my_infos()`][freesound.freesound_api.get_my_infos] function 

		this functions query information about my user. Visit: <https://freesound.org/docs/api/resources_apiv2.html#me-information-about-user-authenticated-using-oauth2-oauth2-required>

		Returns:
			a json object representing the basic information of the user that is logged in
		"""
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
	def results_page(self) -> dict[str,Any]:
		return self._results_page
	
	@property # read-only
	def download_count(self) -> int:
		"""read-only

		Returns:
			how many files have been downloaded
		"""
		return self._downloader.download_count
	
	@property
	def download_list(self) -> dict[str, list[dict[str, Any]]]:
		"""read-only

		Returns:
			a detailed list of the downloaded files in `json` format
		"""
		return self._downloader.download_list

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
		if path == "":
			path = "./"
		if not path.endswith("/"):
			path += "/"
		self._download_folder = path

	"""
	UTILITIES
	---------
	"""	
	
	def download_results(self,files_count:int|None=None, include_analysis:bool|None=None,output_folder:str|None=None) -> None:
		"""download `files_count` audio files into `output_folder_path`

		This function takes care of pagination automatically

		Args:
			files_count (int | None, optional): how many files should be downloaded. 
			include_analysis (bool | None, optional): whether to include the frame-by-frame analysis data file or not
			output_folder (str | None, optional):the destination folder.
		"""
		try:
			self._downloader.download_results(files_count,include_analysis,output_folder)
		except Exception as e:
			self._handle_exception(e)

	def download_analysis_results(self,files_count:int|None=None, include_sound:bool|None=None,output_folder:str|None=None) -> None:
		"""download `files_count` analysis files into `output_folder_path`

		This function takes care of pagination automatically

		Args:
			files_count (int | None, optional): how many files should be downloaded. 
			include_sound (bool | None, optional): whether to download the sound file or not
			output_folder (str | None, optional):the destination folder.
		"""
		try:
			self._downloader.download_analysis_results(files_count,include_sound,output_folder)
		except Exception as e:
			self._handle_exception(e)

	def write_download_list(self,filename:str="downloads.json", folder:str|None=None) -> None:
		"""save a detailed list of the downloaded files in a `json` file

		If `folder` is not provided the client will prompt the user for this information

		Args:
			filename (str, optional): the name of the file to save
			folder (str | None, optional): the name of the folder where to save the file
		"""
		if self._downloader.download_count == 0:
			warning("There are no download records to write because nothing has been downloaded")
		else:
			filename = self._set_timestamp(filename)
			if folder is not None:
				self._download_folder = folder
			out_file = self._check_for_path(filename,False)
			if out_file is not None:
				self._write_json(self._downloader.download_list,out_file)
		
	def write_results_list(self,filename:str='results_list.json', folder:str|None=None) -> None:
		"""save a simplified list of the [`search`][freesound.freesound_client.FreeSoundClient.search] response in a `json` file

		If `folder` is not provided the client will prompt the user for this information

		Args:
			filename (str, optional): the file of the files where the list should be saved
			folder (str | None, optional): the name of the folder where to save the file
		"""
		if self._results_list['count'] == 0:
			warning("There are no result records to write. Did you already performed a search and found something?")
		else:
			filename = self._set_timestamp(filename)
			if folder is not None:
				self._download_folder = folder
			out_file = self._check_for_path(filename,False)
			if out_file is not None:
				self._write_json(self._results_list,out_file)

	def load_results_list(self, json_file:str):
		"""load a json file produced from [`write_results_list`][freesound.freesound_client.FreeSoundClient.write_results_list]

		Args:
			json_file (str): a relative or an absolute path to a json file
		"""
		if os.path.exists(json_file):
			with open(json_file) as data_file:
				try:
					data = json.load(data_file)
					self._validate_data(data)
				except Exception as e:
					self._handle_exception(e)
		else:
			error(f"File {json_file} not found")
			self.logout()

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
							log(x, unpack_features(y))
						else:
							log(x, y)
			else:
				log(str(key),values)
			print('')	
	
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
		self._results_list['count'] += len(list['results'])
		self._results_list['timestamp'] = datetime.now().isoformat()
		self._results_list['results'].extend(list['results'])
	
	def _set_timestamp(self, filename:str) -> str:
		timestamp = datetime.fromisoformat(self._results_list['timestamp']).strftime("%y%m%dT%H%M")
		filename = timestamp + "_" + filename
		return filename
		
	def _check_for_path(self,filename:str,skip:bool) -> str|None:
		if self._download_folder is None:
			self._download_folder = self._prompt_output_folder()
		output_path = os.path.join(self._download_folder,filename)
		while os.path.exists(output_path):
			warning(f"The File {output_path} already exists...")
			if  skip:
				warning("Skipping")
				separator()
				return None
			else:
				new_filename = ask("Press Enter to overwrite or set a new filename: ")
				if new_filename.strip() == "":
					info(f"Overwriting {filename}")
					break
				else:
					output_path = os.path.join(self._download_folder,new_filename)
		if not os.path.exists(self._download_folder):
			os.mkdir(self._download_folder)
		return output_path

	def _write_audio_file(self, data:BytesIO, output_path:str) -> None:
		with open(output_path,"wb") as file:
			file.write(data.read())
		info(f"File: {output_path} written!")

	def _write_json(self,data:dict[Any,Any], output_path:str):
		with open(output_path, "w") as outfile:
			json.dump(data, outfile, indent=4)
		info(f"File: {output_path} written!")

	def _parse_user_info(self,data:dict[str,Any]):
		# we could set more user's information in this function
		# check this page for more info: https://freesound.org/docs/api/resources_apiv2.html#user-instance
		self._username = data['username']
	
	def _validate_data(self,data:dict[str,Any]):
		if 'results' not in data or 'count' not in data or 'timestamp' not in data:
			error(f"The json file you are trying to load is corrupted")
			self.logout()
		else:
			self._results_list = data

	def _handle_exception(self, e:Exception) -> NoReturn:
		if isinstance(e, FreesoundError):
			error(e.args[0])
		elif isinstance(e, AuthorizationError):
			error(e.args[0])
		elif isinstance(e, FieldError):
			error(e.args[0])
		elif isinstance(e, FreesoundDownloadError):
			warning(e.args[0])
		else:
			if isinstance(e, ReadTimeout):
				error("Connection Timeout!")
			else:
				separator_red()
				warning(traceback.format_exc())
				separator_red()
				error("Caught a generic Exception. Copy the above printed trace and inform the developers")
		self.logout()

	def __repr__(self) -> str:
		return f"<freesound.freesound.FreeSounClient {self._username}>"

	def logout(self) -> NoReturn:
		"""Closes the program

		Should not normally need to be called explicitly

		Calls `sys.exit(0)`
		"""
		print(headline("Logging out"))
		sys.exit(0)

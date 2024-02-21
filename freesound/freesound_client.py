from time import sleep
import traceback
from typing import Any, NoReturn
import json 
from io import BytesIO
from urllib.parse import urlparse, parse_qsl
import os
import sys
from requests import Response # type: ignore

import freesound.freesound_api as freesound_api
from .freesound_errors import FieldError, FreesoundError
from .freesound_requests import AuthorizationError
from .freesound_track import FreeSoundTrack
from .freesound_filters import *
from .formatting import headline, separator,ask, warning,error,info,log


class FreeSoundClient:
	def __repr__(self) -> str:
		return f"<freesound.freesound_client.FreeSounClient {self._username}>"
	
	def __init__(self, user_id:str, api_key:str, download_folder:str|None=None, token_file_path:str="access_token.json") -> None:
		self._user_id = user_id # private
		self._api_key = api_key # private
		self._access_token = "" # private
		self._token_file_path = token_file_path # private

		self._username = "" # read-only
		self._page_size = 15 # read-only
		self._result_page:dict[str,Any] = {} # read-only
		self._result_list:dict[str,list[dict[str,Any]]] = {'search-results':[]} # read-only

		self._download_count = 15 # read-only
		self._download_list:dict[str,list[dict[str,Any]]] = {'downloaded-files':[]} # read-only
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
			print(f"The access data provided is not valid")
			self.logout()

	def _save_access_token(self,access_data:dict[str,Any]) -> None:
		with open(self._token_file_path, "w") as file:
			json.dump(access_data, file)

	"""
	API
	---
	"""	
	# TODO check if it works with the descriptors
	def search(self, query:str,filters:str='',fields:str='',descriptors:str='',sort_by:str='score',page_size:int=15, normalized:int=0) -> dict[str,Any]:
		if page_size > 150: # see documentation https://freesound.org/docs/api/resources_apiv2.html#response-sound-list
			warning(f"Page size {page_size} too big. Setting it to 150")
		print(f"Searching for {query}")
		self._page_size = min(page_size,150)
		try:
			search_data = freesound_api.search(query, self._access_token,fields,filters,descriptors,sort_by,self._page_size,normalized)
			self._result_page = search_data
			self._update_result_list(search_data)
			if search_data["count"] == 0:
				print("No results found")
			else:
				print(f"Found {search_data['count']} results")
		except Exception as e:
			self._handle_exception(e)
		
		return search_data
	
	def get_track_info(self, track_id:Any, track_name:str, params:dict[str,str]) -> FreeSoundTrack:
		print(f"Getting {track_name} infos")
		try:
			track_info = freesound_api.get_track_info(str(track_id), params,self._access_token)
			audio_track = FreeSoundTrack(track_info)
		except Exception as e:
			self._handle_exception(e)
		return audio_track

	def download_track(self, url:str, filename:str, outfolder:str) -> BytesIO | None:
		print(f"Downloading {filename}")
		try:
			file_response: Response = freesound_api.download_track(url, self._access_token)
			# FIXME the response should be checked somehow
			binary_data = BytesIO(file_response.content)
			self._write_audio_file(binary_data, filename, outfolder)
			return binary_data
		# TODO handle Error
		except Exception as e:
			self._handle_exception(e)

	def get_next_page(self, query:dict[str,str]) -> dict[str,Any]:
		print("Getting next page")
		separator()
		try:
			page = freesound_api.get_next_page(query, self._access_token)
			self._result_page = page
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
		return self._username

	@property # read-only
	def page_size(self) -> int:
		return self._page_size
	
	@property # read-only
	def result_list(self) -> dict[str,Any]:
		return self._result_list
	
	@property # read-only
	def download_count(self) -> int:
		return self._download_count
	
	@property
	def download_list(self):
		return self._download_list

	@property
	def download_folder(self) -> str|None:
		return self._download_folder

	@download_folder.setter
	def download_folder(self,path:str) -> None:
		self._download_folder = path

	"""
	UTILITIES
	---------
	"""	
	def download_results(self,output_folder_path:str|None=None,count:int|None=None) -> None:
		if count is None:
			self._download_count = self._prompt_downloads(self._result_page['count'])
		else:
			self._download_count = count
		if output_folder_path is not None:
			self._download_folder = output_folder_path
		else:
			if self._download_folder is None:
				self._download_folder = self._prompt_output_folder()
		
		print(f"Downloading {self._download_count} files of {self._result_page['count']}")
		separator()
		downloaded_count = 0
		while downloaded_count < self._download_count:
			for sound in self._result_page['results']:
				if downloaded_count < self.download_count:
					try:
						parsed_sound = FreeSoundTrack(sound)
					except Exception as e:
						self._handle_exception(e)
						
					filepath = os.path.join(self._download_folder,parsed_sound.name)
					
					if os.path.exists(filepath):
						warning(f"The file {parsed_sound.name} has already been downloaded...Skipping")
						separator()
						sleep(0.1) # avoid throttling
						pass
					else:
						self.download_track(parsed_sound.ensure_value('download'),parsed_sound.name, self._download_folder)
						downloaded_count+=1
						self._update_download_list(sound)
						info(f"Downloaded Files: {downloaded_count} of {self._download_count}")
						separator()
				else:
					break
			if downloaded_count < self.download_count:
				self._set_next_page()

	def write_download_list(self,filename:str="downloads.json", folder:str|None=None) -> None:
		self._write_json(self._download_list,filename, folder)
		
	def write_result_list(self,filename:str='result_list.json', folder:str|None=None) -> None:
		self._write_json(self._result_list,filename, folder)

	def dump_result(self, result:dict[str,Any]):
		for key, values in result.items():
			if isinstance(values, list):
				for value in values: # type:ignore
					separator()
					for x,y in value.items(): # type:ignore
						log(x,y)
						
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
		if output_folder.endswith("/"):
			return output_folder
		else:
			return output_folder+"/"

	def _update_result_list(self, list:dict[str,Any]):
		self._result_list['search-results'].extend(list['results'])

	def _update_download_list(self, sound_obj:dict[str,Any]):
		self._download_list['downloaded-files'].append(sound_obj)

	def _check_for_path(self,filename:str, folder:str|None):
		if folder is None:
			if self._download_folder is None:
				out_folder = self._prompt_output_folder()
			else:
				out_folder = self._download_folder
		else:
			out_folder="./"

		output_path = os.path.join(out_folder,filename)
		while os.path.exists(output_path):
			warning(f"The File {output_path} already exists")
			new_filename = ask("Press Enter to overwrite or set a new filename: ")
			if new_filename.strip() == "":
				info(f"Overwriting {filename}")
				break
			else:
				output_path = os.path.join(out_folder,new_filename)
		
		if ".json" not in output_path:
			filename += ".json"
		return output_path

	def _write_audio_file(self, data:BytesIO, file_name:str, folder:str) -> None:
		if not os.path.exists(folder):
			os.makedirs(folder)
		with open(folder+file_name,"wb") as file:
			file.write(data.read())

	def _write_json(self,data:dict[Any,Any], filename:str, folder:str|None):
		output_path = self._check_for_path(filename,folder)
		with open(output_path, "w") as outfile:
			json.dump(data, outfile, indent=4)
		info(f"File: {output_path} written!")

	def _set_next_page(self) -> bool:
		url:str = self._result_page["next"]
		if url != 'null':
			query: str = urlparse(url).query
			query_dict = dict(parse_qsl(query))
			self.get_next_page(query_dict)
			return True
		else:
			raise DataError("The field 'next' in the search result is empty")

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
			print("Caught a generic Exception. Inform the developers")
			print(traceback.format_exc())
		self.logout()

	def logout(self) -> NoReturn:
		print(headline("Logging out"))
		sys.exit(1)

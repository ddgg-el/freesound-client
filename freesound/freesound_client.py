from typing import Any, NoReturn

from .freesound_errors import FreesoundError
from .freesound_requests import AuthorizationError
from .freesound_track import FreeSoundTrack
from .freesound_filters import *
from .formatting import headline, separator
import freesound.freesound_api as freesound_api
from requests import Response # type: ignore
import json 
from io import BytesIO
from urllib.parse import urlparse, parse_qsl
import os
import sys


class FreeSoundClient():
	def __init__(self, user_id:str, api_key:str, token_file_path:str="access_token.json") -> None:
		self.username = ""
		self._user_id = user_id
		self._api_key = api_key
		self._token_file_path = token_file_path
		self._access_token = ""
		try:
			token_data = self._load_token_from_file()
		except FileNotFoundError:
			print("No access token file found. Authorizing...")
			token_data = self._authorize_procedure()

		self._update_access_data(token_data)
		self._next_page_query:dict[str,str] | None = None
		
		try:
			self._get_self_info()
		except AuthorizationError:
			self._refresh_access_token()
			self._get_self_info()
		
		print(f"FreeSound Client {self.username} Initialized")
		separator()

	def _load_token_from_file(self) -> dict[str,str]:
		with open(self._token_file_path,"r") as file:
			print("Loading token from file")
			separator()

			return json.load(file)
		
	def _authorize_procedure(self) -> dict[str,str]:
		if self._user_id == "" and self._api_key == "":
			separator()
			print("You must provide a valid user id and API key")
			print("Visit https://freesound.org/help/developers/ for applying")
			separator()
			self.logout()
		# STEP 1
		params: dict[str, str] = {"client_id":self._user_id, "response_type":"code", "state": "xyz"}
		#use /logout_and_authorize/ if want the user to login before the authorization
		auth_url = "https://freesound.org/apiv2/oauth2/authorize/"
		authorization_url: str = auth_url+"?"+"&".join([f"{key}={value}" for key, value in params.items()])
		print(headline(f"Visit this page to authorize your user: {authorization_url}", centered=True))
		# STEP 2
		access_data:dict[Any,Any] = {}
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
	
	def _update_access_data(self, access_data:dict[Any,Any]) -> None:
		access_token: str | None = access_data.get('access_token')
		refresh_token: str | None = access_data.get('refresh_token')
		if access_token is not None and refresh_token is not None:
			self._access_token:str = access_token
			self._refresh_token:str = refresh_token
			self._save_access_token(access_data)
		else:
			print(f"The access data provided is not valid")
			self.logout()

	def _save_access_token(self,access_data:dict[Any,Any]) -> None:
		with open(self._token_file_path, "w") as file:
			json.dump(access_data, file)

	def _get_self_info(self) -> dict[Any, Any]:
		print("Getting Client Info")
		user_data = freesound_api.get_my_infos(self._access_token)
		try:
			self._parse_user_info(user_data)
		except Exception as e:
			self._handle_exception(e)
		return user_data
	
	def _parse_user_info(self,data:dict[Any,Any]):
		# check this page for more info: https://freesound.org/docs/api/resources_apiv2.html#user-instance
		self.username = data['username']

	def search(self, query:str,filters:str,fields:str='',sort_by:str='score',page_size:int=15, normalized:int=0) -> dict[Any, Any]:
		print(f"Searching for {query}")
		try:
			search_data = freesound_api.search(query, self._access_token,fields,filters,sort_by,page_size,normalized)
			if search_data["next"] != 'null':
				self._set_next_page(search_data["next"])
		except Exception as e:
			self._handle_exception(e)
		
		return search_data
	
	def get_track_info(self, track_id:Any, track_name:str, params:dict[str,str]) -> FreeSoundTrack:
		print(f"Getting {track_name} infos")
		try:
			track_info = freesound_api.get_track_info(str(track_id), params,self._access_token)
			audio_track = FreeSoundTrack(track_name,track_info)
		except Exception as e:
			self._handle_exception(e)
		return audio_track
	
	def download_track(self, url:str, filename:str, outfolder:str = "sound_lib/") -> BytesIO | None:
		print(f"Downloading {filename}")
		try:
			file_response: Response = freesound_api.download(url, self._access_token)
			# FIXME the response should be checked somehow
			binary_data = BytesIO(file_response.content)
			self.write_audio_file(binary_data, filename, outfolder)
			return binary_data
		# TODO handle Error
		except Exception as e:
			self._handle_exception(e)

	def get_next_page_result(self) -> dict[Any,Any]:
		if self._next_page_query is not None:
			try:
				page = freesound_api.get_next_page(self._next_page_query, self._access_token)
				if page["next"] != 'null':
					self._set_next_page(page["next"])
			except Exception as e:
				self._handle_exception(e)
			return page
		else:
			# TODO handle else case
			self.logout()
			# print("No page found")
	
	def write_audio_file(self, data:BytesIO, file_name:str, folder:str) -> None:
		if not os.path.exists(folder):
			os.makedirs(folder)
		with open(folder+file_name,"wb") as file:
			file.write(data.read())

	def _set_next_page(self, url:str) -> None:
		query: str = urlparse(url).query
		query_dict = dict(parse_qsl(query))
		self._next_page_query = query_dict

	def _handle_exception(self, e:Exception) -> NoReturn:
		if isinstance(e, FreesoundError):
			print(e)
		elif isinstance(e, AuthorizationError):
			print(e)
		else:
			print("Caught a generic Exception. Inform the developers")
			print(e)
		self.logout()

	def logout(self) -> NoReturn:
		print(headline("Logging out"))
		sys.exit(1)

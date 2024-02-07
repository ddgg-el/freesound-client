from typing import Any, NoReturn, Callable
from .utilities import separator, AuthorizationError,headline
from .track import FreeSoundTrack
import freesound.freesound_api as freesound_api
from requests import Response, ConnectionError, ConnectTimeout # type: ignore
import json 
from io import BytesIO
from urllib.parse import urlparse, parse_qsl
import os
import sys

token_file_path = "access_token.json" # change to absolute path

class FreeSoundClient():
	def __init__(self, user_id:str, api_key:str) -> None:
		self.user_id: str = user_id
		self.api_key:str = api_key
		self.next_page_query:dict[str,str] | None = None
		try:
			token_data: dict[str,str] = self.load_token_from_file()
		except:
			print("No existing access token found. Authorizing...")
			token_data = self.authorize_procedure()

		self.update_access_data(token_data)
		print("FreeSound Client Initialized")
		separator()

	def load_token_from_file(self) -> dict[str,str]:
		with open(token_file_path,"r") as file:
			print("Loading token from file")
			separator()
			return json.load(file)
	# STEP 1 -> STEP 2
	def authorize_procedure(self) -> dict[str,str]:
		# STEP 1
		params: dict[str, str] = {"client_id":self.user_id, "response_type":"code", "state": "xyz"}
		#use /logout_and_authorize/ if want the user to login before the authorization
		auth_url = "https://freesound.org/apiv2/oauth2/authorize/"
		authorization_url: str = auth_url+"?"+"&".join([f"{key}={value}" for key, value in params.items()])
		print(headline(f"Visit this page to authorize your user: {authorization_url}", centered=True))
		# STEP 2
		access_data:dict[Any,Any] = {}
		try:
			authorization_code: str = input("Enter the authorization code from the redirect URL: ")
			access_response: Response = freesound_api.get_access_token(self.user_id, self.api_key, authorization_code)
			access_data = self.parse_response( access_response)
		except KeyboardInterrupt as e:
			self.logout()
		except Exception as e:
			print(e)
			self.logout()
		print("Authorization succeded!")
		self.update_access_data(access_data)
		return access_data
		# Go on to STEP 3
	
	def refresh_access_token(self, caller:Callable[[str], str], *args:str, **kwargs:str) -> None:
		try:
			refresh_response: Response = freesound_api.refresh_access_token(self.user_id, self.api_key, self.refresh_token)
			token_data: dict[Any, Any] =self.parse_response(refresh_response)
			self.update_access_data(token_data)
		except Exception as e:
			print(e)
			self.logout()
		caller(*args, **kwargs)
	
	def update_access_data(self, access_data:dict[Any,Any]) -> None:
		self.token_data = access_data
		access_token: str | None = self.token_data.get('access_token')
		refresh_token: str | None = self.token_data.get('refresh_token')
		if access_token is not None and refresh_token is not None:
			self.access_token:str = access_token
			self.refresh_token:str = refresh_token
			self.save_access_token()
		else:
			print(f"No tokens found in {token_file_path}. Delete {token_file_path} and retry")
			self.logout()

	def save_access_token(self) -> None:
		with open(token_file_path, "w") as file:
			json.dump(self.token_data, file)

	def search(self, query:str) -> dict[Any, Any]|NoReturn:
		# search_data: dict[Any, Any] = {}
		try:
			response: Response = freesound_api.search(query, self.access_token)
			search_data = self.parse_response(response)
			if search_data["next"] != 'null':
				self.set_next_page(search_data["next"])
			
		except AuthorizationError as e:
			print(e)
			self.logout()
			# TODO: the access token should be refreshed somehow
			#self.refresh_access_token(self.search,query)
		except KeyboardInterrupt as e:
			self.logout()
		except ConnectTimeout as e:
			print('Connection to freesound.org timed out. Retry later')
			self.logout()
		except Exception as e:
			print("Connection Error - Are you connected to the Internet?")
			self.logout()
		return search_data
	
	def get_track_info(self, track_id:Any, track_name:str, params:dict[str,str]) -> FreeSoundTrack:
		print(f"Getting {track_name} infos")
		try:
			response: Response = freesound_api.get_track_info(str(track_id), params,self.access_token)
			track_info: dict[Any, Any] = self.parse_response(response)
			audio_track = FreeSoundTrack(track_name,track_info)
		except KeyboardInterrupt as e:
			self.logout()
		except ConnectionError as e:
			raise ConnectionError("SSL Error...skipping")
		except Exception as e:
			print(e)
			self.logout()
		return audio_track
	
	def download_track(self, url:str, filename:str) -> BytesIO | None:
		print(f"Downloading {filename}")
		try:
			file_response: Response = freesound_api.download(url, self.access_token)
			# TODO: the response should be checked somehow
			# removed parse response
			binary_data = BytesIO(file_response.content)
			self.write_audio_file(binary_data, filename)
			return binary_data
		except KeyboardInterrupt as e:
			self.logout()
		except Exception as e:
			print(e)
			self.logout()

	def get_next_page_result(self) -> dict[Any,Any]|NoReturn:
		# page: dict[Any,Any] = {}
		if self.next_page_query is not None:
			try:
				response:Response = freesound_api.get_next_page(self.next_page_query, self.access_token)
				page:dict[Any,Any] = self.parse_response(response)
				if page["next"] != 'null':
					self.set_next_page(page["next"])

			except Exception as e:
				self.handle_exception(e)
			return page
		else:
			# TODO: handle else case
			self.logout()
			# print("No page found")
	
	def write_audio_file(self, data:BytesIO, file_name:str, folder:str="sound_lib/") -> None:
		if not os.path.exists(folder):
			os.makedirs(folder)

		with open(folder+file_name,"wb") as file:
			file.write(data.read())

	def parse_response(self, response:Response) -> dict[Any,Any]:
		result: dict[Any,Any] = {}
		try:
			result = response.json()
		except json.JSONDecodeError:
			print("There was an error parsing the Reponse")
			self.logout()
		return result

	def set_next_page(self, url:str) -> None:
		query: str = urlparse(url).query
		query_dict = dict(parse_qsl(query))
		self.next_page_query = query_dict

	def handle_exception(self, e:Exception) -> NoReturn:
		print(type(e))
		self.logout()
			
	def logout(self) -> NoReturn:
		print(headline("Logging out"))
		sys.exit(1)

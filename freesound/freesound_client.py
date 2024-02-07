from typing import Any, NoReturn, Callable
from .utilities import separator, AuthorizationError,headline, ConnectionError
from .track import FreeSoundTrack
import freesound.freesound_api as freesound_api
from requests import Response, ConnectTimeout # type: ignore
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
		except Exception as e:
			print(f"Error Authorizing: {e}")
			self.logout()
		print("Authorization succeded!")
		self.update_access_data(access_data)
		return access_data
	
	def refresh_access_token(self, caller:Callable[[], dict[Any,Any]|None]) -> None:
		print('Refreshing Access Token')
		print(self.user_id, self.api_key, self.refresh_token)
		try:
			refresh_response: Response = freesound_api.refresh_access_token(self.user_id, self.api_key, self.refresh_token)
			token_data: dict[Any, Any] =self.parse_response(refresh_response)
			self.update_access_data(token_data)
		except Exception as e:
			print(f"Error Refreshing Access Token")
			self.handle_exception(e)
			self.logout()
		
		caller()
	
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

	def search(self, query:str) -> dict[Any, Any]|NoReturn|None:
		print(f"Searching for {query}")
		try:
			response: Response = freesound_api.search(query, self.access_token)
			search_data = self.parse_response(response)
			if search_data["next"] != 'null':
				self.set_next_page(search_data["next"])
			
		except AuthorizationError as e:
			# TODO: does this work?
			print(f"Authorization Error: {e}")
			self.refresh_access_token(lambda: self.search(query))
			return {'count': 0}
		except ConnectTimeout:
			print('Connection to freesound.org timed out. Retry later')
			self.logout()
		except Exception as e:
			print(f"Connection Error - {e}\nAre you connected to the Internet?")
			self.logout()
		return search_data
	
	def get_track_info(self, track_id:Any, track_name:str, params:dict[str,str]) -> FreeSoundTrack:
		print(f"Getting {track_name} infos")
		try:
			response: Response = freesound_api.get_track_info(str(track_id), params,self.access_token)
			track_info: dict[Any, Any] = self.parse_response(response)
			audio_track = FreeSoundTrack(track_name,track_info)
		except ConnectionError:
			raise ConnectionError("SSL Error...skipping")
		except Exception as e:
			print(e)
			self.logout()
		return audio_track
	
	def download_track(self, url:str, filename:str, outfolder:str = "sound_lib/") -> BytesIO | None:
		print(f"Downloading {filename}")
		try:
			file_response: Response = freesound_api.download(url, self.access_token)
			# TODO: the response should be checked somehow
			# removed parse response
			binary_data = BytesIO(file_response.content)
			self.write_audio_file(binary_data, filename, outfolder)
			return binary_data
		except Exception as e:
			print(e)
			self.logout()

	def get_next_page_result(self) -> dict[Any,Any]|NoReturn:
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
	
	def write_audio_file(self, data:BytesIO, file_name:str, folder:str) -> None:
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
		if isinstance(e, ConnectionError):
			print(f"Connection Error: Status {e}")
		self.logout()
			
	def logout(self) -> NoReturn:
		print(headline("Logging out"))
		sys.exit(1)

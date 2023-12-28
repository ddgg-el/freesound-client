from .utilities import separator, AuthorizationError,headline
import freesound.freesound_api as freesound_api
from requests import Response, ConnectionError
import json 
from typing import Any
from io import BytesIO
import os
import sys

token_file_path = "access_token.json" # change to absolute path

class FreeSoundClient():
	def __init__(self, user_id:str, api_key:str) -> None:
		self.user_id: str = user_id
		self.api_key:str = api_key
		try:
			self.token_data: dict[str,str] = self.load_token_from_file()
		except:
			print("No existing access token found. Authorizing...")
			self.token_data = self.authorize_procedure()

		self.update_access_data()
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
		self.update_access_data()
		return access_data
		# Go on to STEP 3
	
	def refresh_access_token(self, caller, *args, **kwargs) -> None:
		try:
			refresh_response: Response = freesound_api.refresh_access_token(self.user_id, self.api_key, self.refresh_token)
			token_data: dict[Any, Any] =self.parse_response(refresh_response)
			self.token_data = token_data
			print(token_data)
		except Exception as e:
			print(e)
			self.logout()
		self.update_access_data()
		caller(*args, **kwargs)
	
	def update_access_data(self) -> None:
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

	def search(self, query:str) -> dict[Any, Any]:
		search_data: dict[Any, Any] = {}
		try:
			response: Response = freesound_api.search(query, self.access_token)
			search_data = self.parse_response(response)
		except AuthorizationError as e:
			print(e)
			self.refresh_access_token(self.search,query)
		except KeyboardInterrupt as e:
			self.logout()
		except Exception as e:
			print("Connection Error - Are you connected to the Internet?")
			self.logout()
		return search_data
	
	def get_track_info(self, track_id:Any, track_name:str, params:dict[str,str]) -> dict[Any, Any]:
		print(f"Getting {track_name} infos")
		track_info:dict[Any,Any] = {}
		try:
			response: Response = freesound_api.get_track_info(str(track_id), params,self.access_token)
			track_info= self.parse_response(response)
		except KeyboardInterrupt as e:
			self.logout()
		except Exception as e:
			print(e)
			self.logout()
		return track_info
	
	def download_track(self, url:str, filename:str) -> BytesIO:
		try:
			file_response: Response = freesound_api.download(url, self.access_token)
			sound_file: dict[Any, Any] = self.parse_response(file_response)
			binary_data = BytesIO(sound_file.content)
			self.write_audio_file(binary_data, filename)
		except KeyboardInterrupt as e:
			self.logout()
		except:
			self.logout()
			# binary_data = BytesIO()
		return binary_data
	
	def write_audio_file(self, data:BytesIO, file_name:str, folder:str="sound_lib/") -> None:
		if not os.path.exists(folder):
			os.makedirs(folder)

		with open(folder+file_name,"wb") as file:
			file.write(data.read())

	def parse_response(self, response:Response) -> dict[Any,Any]:
		result: dict[Any,Any] = {}
		try:
			result = response.json()
		except json.JSONDecodeError as e:
			print("There was an error parsing the Reponse")
			self.logout()
		return result
			
	def logout(self) -> None:
		print(headline("Logging out"))
		sys.exit(1)

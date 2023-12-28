from requests import Response, get, post
import json
from typing import Any

class ConnectionError(Exception):
	def __init__(self, message:str) -> None:
		super().__init__(message)

class AuthorizationError(Exception):
	def __init__(self,message:str) -> None:
		super().__init__(message)

def handle_response(response:Response) -> bool:
	response_data = response.json()
	code = response.status_code
	if code != 200:
		if code == 401:
			raise AuthorizationError(f"{code} -> The credentials you provided are invalid (probably expired) Refreshing...")
		else:	
			detail = response_data.get('detail')
			raise ConnectionError(f"{code} -> {detail!r}")
	return True

def make_get_request(url:str, header:dict[str,str] = {},params:dict[str,str]={}) -> Response:
	response:Response = get(url, headers=header, params=params)
	handle_response(response)
	return response

def make_post_request(url:str, data:dict[str,str]) -> Response:
	response:Response = post(url,data)
	handle_response(response)
	return response

def headline(text: str, centered: bool = False) -> str:
	if not centered:
		return f"{text}\n{'-' * len(text)}"
	else:
		print("".center(50,"="))
		return f" {text} ".center(50, "o")
	
def separator(length:int=20)->None:
	print(f"{'-'*length}")
	
def get_file_info(set:dict[Any,Any], key:str) -> Any:
	value = set.get(key)
	if value is None:
		raise KeyError(key)
	return value 
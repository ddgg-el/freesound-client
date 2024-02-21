from requests import Response

from freesound.freesound_requests import make_get_request, make_post_request
from freesound.freesound_errors import DataError
# from multipledispatch import dispatch # type:ignore
from typing import Any
import json

def get_my_infos(token:str) -> dict[Any,Any]:
	header = {"Authorization": f"Bearer {token}"}
	user_url = "https://freesound.org/apiv2/me/"
	user_response:Response = make_get_request(user_url,header=header)
	user_info = parse_response(user_response)
	return user_info

def get_access_token(user_id:str, api_key:str, authorization_code:str) -> dict[Any,Any]:
	token_url = "https://freesound.org/apiv2/oauth2/access_token/"
	token_params: dict[str, str] = {
		"client_id": user_id,
		"client_secret": api_key,
		"code": authorization_code,
		"grant_type": "authorization_code",
	}
	token_resp: Response = make_post_request(token_url, data=token_params)
	token = parse_response(token_resp)
	return token

def refresh_access_token(user_id:str, api_key:str, refresh_token:str) -> dict[Any,Any]:
		token_url = "https://freesound.org/apiv2/oauth2/access_token/"
		token_params: dict[str, str] = {
			"client_id": user_id,
			"client_secret": api_key,
			"grant_type": "refresh_token",
			"refresh_token": refresh_token,
		}
		token_resp: Response = make_post_request(token_url, data=token_params)
		token = parse_response(token_resp)
		return token

# query "piano detuned"
# fields "id,samplerate,download"
# filters "tag:class type:wav"
def search(query:str, token:str,fields:str|None=None,filters:str|None=None,descriptors:str|None=None,sort_by:str='score',page_size:int=15,normalized:int=0) -> dict[Any,Any]:
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	fields_list = 'id,name'
	if fields is not None:
		fields_list += ',' + fields

	params: dict[str, str] = {"query":query,"fields":fields_list,"page_size":str(page_size), "sort":sort_by, "normalized":str(normalized)}
	
	if filters is not None and filters != '':
		params['filter'] = filters
	
	if descriptors is not None and descriptors != '':
		params['descriptors'] = descriptors
	
	search_url = "https://freesound.org/apiv2/search/text/"
	search_response: Response = make_get_request(search_url, header=headers, params=params)
	search = parse_response(search_response)
	return search

def get_track_info(track_id:str,params:dict[str,str], token:str) -> dict[Any,Any]:
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	track_info_url:str = f"https://freesound.org/apiv2/sounds/{track_id}/"
	file_type_response: Response = make_get_request(track_info_url, header=headers, params=params)
	file_type = parse_response(file_type_response)
	return file_type
	
def get_next_page(params:dict[str,str], token:str) -> dict[Any,Any]:
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	next_page_response:Response = make_get_request("https://freesound.org/apiv2/search/text/", header=headers, params=params)
	next_page = parse_response(next_page_response)
	return next_page
	
def download_track(track_url:str, token:str) -> Response:
	# TODO check the response and type
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	sound_file_response: Response = make_get_request(track_url, header=headers, params={})
	# print(sound_file_response)
	# if sound_file_response.status_code == 200:
	return sound_file_response

def parse_response(response:Response) -> dict[str,Any]:
	result:dict[str,Any] = {}
	try:
		result = response.json()
	except json.JSONDecodeError:
		raise DataError(f"There was an error parsing the Reponse from {response.url}")
	return result
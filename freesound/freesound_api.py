"""The Freesound API

This modules containts the basic functions that the `FreeSoundClient` uses to make GET and POST requests to <freesound.org>

It is anyway possible to use them directly providing the appropriate parameters

All requests require an OAuth2 access token
Examples:
	>>> from freesound.freesound_api import *
	>>> get_my_infos(access_token)
	{username: ...,about:...}
The module contains the following functions:
- `get_access_token` - see https://freesound.org/docs/api/authentication.html#token-authentication
- `refresh_access_token` - see https://freesound.org/docs/api/authentication.html#once-you-have-your-access-token
- `get_my_infos` - see https://freesound.org/docs/api/resources_apiv2.html#other-resources
- `search` - see https://freesound.org/docs/api/resources_apiv2.html#search-resources
- `get_track_info` - see https://freesound.org/docs/api/resources_apiv2.html#sound-resources
- `get_next_page` - https://freesound.org/docs/api/resources_apiv2.html#response-sound-list
- `download_track` - https://freesound.org/docs/api/resources_apiv2.html#download-sound-oauth2-required

All response from these requests are parsed as `dict[str,Any]`
"""
from requests import Response

from freesound.freesound_requests import make_get_request, make_post_request
from freesound.freesound_errors import DataError
from typing import Any
from urllib.parse import urlparse, parse_qsl
import json


def get_access_token(user_id:str, api_key:str, authorization_code:str) -> dict[str,Any]:
	"""A utlity function which covers Step 3 of the OAuth2 Authentication process 
		see: <https://freesound.org/docs/api/authentication.html#step-3>

	You can apply for API credentials here: <https://freesound.org/apiv2/apply/>

	You can save the response data in a file for future connections

	Args:
		user_id (str): the User id
		api_key (str): the API key
		authorization_code (str): the authorization code copied from the browser see: <https://freesound.org/docs/api/authentication.html#step-2>

	Returns:
		a `dict` containing the following keys: `"access_token"`, `"expires_in"`, `"token_type"`, `"scope"`, `"refresh_token"`
	"""
	token_url = "https://freesound.org/apiv2/oauth2/access_token/"
	token_params: dict[str, str] = {
		"client_id": user_id,
		"client_secret": api_key,
		"code": authorization_code,
		"grant_type": "authorization_code",
	}
	token_resp: Response = make_post_request(token_url, data=token_params)
	token = _parse_response(token_resp)
	return token

def refresh_access_token(user_id:str, api_key:str, refresh_token:str) -> dict[str,Any]:
	"""Refresh the User "access token" when expired

	see: <https://freesound.org/docs/api/authentication.html#once-you-have-your-access-token>
	
	Args:
		user_id (str): your the User id
		api_key (str): the API key
		refresh_token (str): the "refresh_token" saved from the [`get_access_token()`][freesound.freesound_api.get_access_token] Response

	Returns:
		a `dict` containing the following keys: `"access_token"`, `"expires_in"`, `"token_type"`, `"scope"`, `"refresh_token"`
	"""
	token_url = "https://freesound.org/apiv2/oauth2/access_token/"
	token_params: dict[str, str] = {
		"client_id": user_id,
		"client_secret": api_key,
		"grant_type": "refresh_token",
		"refresh_token": refresh_token,
	}
	token_resp: Response = make_post_request(token_url, data=token_params)
	token = _parse_response(token_resp)
	return token

def get_my_infos(token:str) -> dict[str,Any]:
	"""get the info about the User identified by `token`

	Args:
		token (str): a valid OAuth2 access token

	Returns:
		a `dict` containing data listed here: <https://freesound.org/docs/api/resources_apiv2.html#user-instance>
	"""
	#TODO implement the User class
	header = {"Authorization": f"Bearer {token}"}
	user_url = "https://freesound.org/apiv2/me/"
	user_response:Response = make_get_request(user_url,header=header)
	user_info = _parse_response(user_response)
	return user_info

def search(query:str, token:str,fields:str|None=None,filter:str|None=None,descriptors:str|None=None,sort_by:str='score',page_size:int=15,normalized:int=0) -> dict[str,Any]:
	"""Search in the FreeSound Database

	For a full documentation see: <https://freesound.org/docs/api/resources_apiv2.html#search-resources>

	Args:
		query (str): a space-separatad string of words to search in the FreeSound Database
		token (str): a valid OAuth2 access token
		fields (str | None, optional): a coma-separated string of fields of a SoundInstance
		filter (str | None, optional): a space-separated string of valid filter:value
		descriptors (str | None, optional): a coma-separated string of valid sound analysis descriptors
		sort_by (str, optional): a valid sort paramter
		page_size (int, optional): the max number of items inside the result array of the response
		normalized (int, optional): wheteher the analysis values are normalized or not either 0-1

	Returns:
		a sound list. See: <https://freesound.org/docs/api/resources_apiv2.html#response-sound-list>
	"""
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	fields_list = 'id,name'
	if fields is not None:
		fields_list += ',' + fields

	params: dict[str, str] = {"query":query,"fields":fields_list,"page_size":str(page_size), "sort":sort_by, "normalized":str(normalized)}
	
	if filter is not None and filter != '':
		params['filter'] = filter
	
	if descriptors is not None and descriptors != '':
		params['descriptors'] = descriptors
	
	search_url = "https://freesound.org/apiv2/search/text/"
	search_response: Response = make_get_request(search_url, header=headers, params=params)
	search = _parse_response(search_response)
	return search

def get_track_info(track_id:str,token:str,fields:str|None=None,descriptors:str|None=None) -> dict[str,Any]:
	"""Requests infos of a SoundInstance

	see: <https://freesound.org/docs/api/resources_apiv2.html#sound-instance>

	Args:
		track_id (str): a valid id of a sound in the freesound database
		token (str): a valid OAuth2 access token
		fields (str | None, optional): a coma-separated string of fields of a SoundInstance
		descriptors (str | None, optional): a coma-separated string of valid sound analysis descriptors

	Returns:
		a dict containing all the info of a SoundInstance. see <https://freesound.org/docs/api/resources_apiv2.html#sound-resources>
	"""
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	track_info_url:str = f"https://freesound.org/apiv2/sounds/{track_id}/"
	
	params:dict[str,Any] = {}
	if fields is not None and fields != '':
		params['fields'] = fields
	
	if descriptors is not None and descriptors != '':
		params['descriptors'] = descriptors

	file_type_response: Response = make_get_request(track_info_url, header=headers, params=params)
	file_type = _parse_response(file_type_response)
	return file_type
	
def get_next_page(url:str, token:str) -> dict[str,Any]:
	"""A utility function to handle pagination in sound results

	It performs a search form the a url parsed from the `'next'` field of a search result
	
	Args:
		url str: a url retrieved from a previous 'search' request
		token (str): a valid OAuth2 access token

	Returns:
		a sound list. See: <https://freesound.org/docs/api/resources_apiv2.html#response-sound-list>
	"""
	query: str = urlparse(url).query
	params = dict(parse_qsl(query))
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	next_page_response:Response = make_get_request("https://freesound.org/apiv2/search/text/", header=headers, params=params)
	next_page = _parse_response(next_page_response)
	return next_page
	
def download_track(track_url:str, token:str) -> Response:
	"""Download a track from a url

	Args:
		track_url (str): a valid download url retrieved from a SoundInstance
		token (str): a valid OAuth2 access token

	Returns:
		a `requests.Response` whose `content` can be loaded in a `ByteIO`
	"""
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	sound_file_response: Response = make_get_request(track_url, header=headers, params={})
	if sound_file_response.ok:
		return sound_file_response
	else:
		raise DataError(f"Could not Download File. Broken Data")

def _parse_response(response:Response) -> dict[str,Any]:
	result:dict[str,Any] = {}
	try:
		result = response.json()
	except json.JSONDecodeError:
		raise DataError(f"There was an error parsing the Reponse from {response.url}")
	return result

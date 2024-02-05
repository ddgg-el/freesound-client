from requests import Response
from .utilities import make_get_request, make_post_request

# STEP 3
def get_access_token(user_id:str, api_key:str, authorization_code:str) -> Response:
	token_url = "https://freesound.org/apiv2/oauth2/access_token/"
	token_params: dict[str, str] = {
		"client_id": user_id,
		"client_secret": api_key,
		"code": authorization_code,
		"grant_type": "authorization_code",
	}
	token_resp: Response = make_post_request(token_url, data=token_params)
	return token_resp

def refresh_access_token(user_id:str, api_key:str, refresh_token:str) -> Response:
		token_url = "https://freesound.org/apiv2/oauth2/access_token/"
		token_params: dict[str, str] = {
			"client_id": user_id,
			"client_secret": api_key,
			"grant_type": "refresh_token",
			"refresh_token": refresh_token,
		}

		token_resp: Response = make_post_request(token_url, data=token_params)
		return token_resp
	
def search(query:str, token:str) -> Response:
	print(f"Searching for {query}")
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	params: dict[str, str] = {"query":query} # "filter": "tag:prepared"}
	search_response: Response = make_get_request("https://freesound.org/apiv2/search/text/", header=headers, params=params)
	return search_response

def get_track_info(track_id:str,params:dict[str,str], token:str) -> Response:
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	url:str = f"https://freesound.org/apiv2/sounds/{track_id}/"
	file_type_response: Response = make_get_request(url, header=headers, params=params)
	return file_type_response
	
def get_next_page(url:str) -> Response:
	print(url)
	next_page:Response = make_get_request(url)
	return next_page
	
def download(track_url:str, token:str)-> Response:
	headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
	sound_file_response: Response = make_get_request(track_url, header=headers, params={})
	# print(sound_file_response)
	# if sound_file_response.status_code == 200:
	return sound_file_response
from requests import Response, get, post, exceptions # type:ignore
from .freesound_errors import AuthorizationError, FreesoundError

def handle_response(res:Response) -> None:
		print(res.url)
		# Guide: https://freesound.org/docs/api/overview.html#errors
		try:
			res.raise_for_status()
		except:
			err_code = res.status_code
			url = res.url
			if err_code == 400:
				# TODO write tests for error 400
				raise FreesoundError(f"The request at {url} is either missing parameters or there is an error with the API")
			elif err_code == 401:
				raise AuthorizationError("The crediantials you provided are invalid.")
			elif err_code == 403:
				raise FreesoundError(f"Visiting {url} should be done via 'https'")
			elif err_code == 404:
				raise FreesoundError(f"{url} not found. There are is nothing to retrieve at {url}")
			elif err_code == 405:
				raise FreesoundError(f"The method {res.request.method} is not allowed in this page")
			elif err_code == 409:
				# TODO check response for more information
				raise FreesoundError(f"The request is valid but it can not be processed because: {res}")
			elif err_code == 429:
				raise FreesoundError("Too many requests. Read https://freesound.org/docs/api/overview.html#throttling for more information")
			else:
				raise FreesoundError(f"Server error: contact the Freesound mailing list")

def make_get_request(url:str, header:dict[str,str] = {},params:dict[str,str]={}) -> Response:
	try:
		response:Response = get(url, headers=header, params=params, timeout=5)
		handle_response(response)
		return response
	except exceptions.ConnectionError:
		print("There are problems connecting to freesound.org")
		exit(0)

def make_post_request(url:str, data:dict[str,str]) -> Response:
	try:
		response:Response = post(url,data, timeout=5)
		handle_response(response)
		return response
	except ConnectionError:
		exit(0)
from typing import Dict
from requests import Response, get, post, exceptions, JSONDecodeError # type:ignore
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
				try:
					details = res.json()['detail']
					raise FreesoundError(f"There was an error with your request. Read the details carefully\n{details}")
				except JSONDecodeError:
					raise FreesoundError(f"The request at {url} is either missing parameters or there is an error with the API")
					# raise FreesoundError(e)
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
				raise FreesoundError("Server error: contact the Freesound mailing list")

def make_get_request(url:str, header:Dict[str,str] = {},params:Dict[str,str]={}) -> Response:
	try:
		response:Response = get(url, headers=header, params=params, timeout=5)
		handle_response(response)
		return response
	except exceptions.ConnectionError:
		print("There are problems connecting to freesound.org")
		exit(0)
	except exceptions.ReadTimeout:
		print("Connection to Freesound.org timed out after 5 seconds")
		exit(0)

def make_post_request(url:str, data:Dict[str,str]) -> Response:
	try:
		response:Response = post(url,data, timeout=5)
		handle_response(response)
		return response
	except ConnectionError:
		exit(0)
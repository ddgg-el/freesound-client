from requests import get, Response, JSONDecodeError # type:ignore
from typing import Any, NoReturn
from sys import exit

def logout() -> NoReturn:
	exit()

def get_page(url:str) -> dict[Any,Any] | NoReturn:
	try:
		response: Response = get(url)
		page: dict[Any,Any] = response.json()
	except JSONDecodeError as e:
		print(e)
		logout()
	return page

try:
	result: dict[Any, Any] = get_page("https://stackoverflow.com/")
except Exception as e:
	print(e)
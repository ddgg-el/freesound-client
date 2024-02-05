import os
from dotenv import load_dotenv

def prompt_keywords()->str:
	keywords: str = input("Enter your search keywords separated by a space [ex. piano detuned prepared ]: ")
	keywords = keywords.strip().lower()
	keywords = keywords.replace(" ", ",")
	return keywords

def prompt_downloads()->int:
	while True:
		try:
			max_download_input: str = input("How many files do you want to download? ")
			max_download = int(max_download_input)
			break
		except ValueError as e:
			print("You must insert a number")
			continue
	return max_download

def load_credentials()->tuple[str,str, str]:
	if load_dotenv():
		API_KEY = os.getenv('API_KEY')
		USER_ID = os.getenv('USER_ID')
		OUT_FOLDER = os.getenv('OUT_FOLDER')
	else:
		print(".env file not found")
		print("Please follow the instruction in the README.md file")
		exit()

	if API_KEY is not None and USER_ID is not None:
		if OUT_FOLDER is None:
			OUT_FOLDER = "sound_lib/"
		return API_KEY, USER_ID, OUT_FOLDER
	else:
		print("FreeSound Credentials not Found")
		exit()
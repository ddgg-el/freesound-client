import os
from dotenv import load_dotenv

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def warning(text:str)->None:
	print(colors.YELLOW + text + colors.END)

def ask(text:str)->str:
	return input(colors.BLUE + text + colors.END)

def error(text:str)->None:
	print(colors.RED + text + colors.END)

def info(text:str)->None:
	print(colors.GREEN + text + colors.END)


def prompt_keywords()->str:
	keywords: str = ask("Enter your search keywords separated by a space [ex. piano detuned prepared ]: ")
	keywords = keywords.strip().lower()
	keywords = keywords.replace(" ", ",")
	return keywords

def prompt_downloads(downloadable:int)->int:
	max_download = None
	while True:
		try:
			max_download_input: str = ask("How many files do you want to download? ")
			if max_download_input == 'all':
				max_download = downloadable
			else:
				max_download = int(max_download_input)
			break
		except ValueError:
			warning("You must insert a number or type 'all'")
			continue
	if max_download > downloadable:
		warning("You are trying to download more files that are actually available")
		warning(f"Setting {downloadable} as the number of files to download")
		max_download = downloadable
	return max_download

def load_credentials()->tuple[str,str, str]:
	if load_dotenv():
		api_key = os.getenv('API_KEY')
		user_id = os.getenv('USER_ID')
		out_folder = os.getenv('OUT_FOLDER')
	else:
		print(".env file not found")
		print("Please follow the instruction in the README.md file")
		exit()

	if api_key is not None and user_id is not None:
		if out_folder is None:
			out_folder = "sound_lib/"
		return api_key, user_id, out_folder
	else:
		error("FreeSound Credentials not Found")
		exit()
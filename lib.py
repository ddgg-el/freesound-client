import os
from dotenv import load_dotenv

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
		print("FreeSound Credentials not Found")
		exit()
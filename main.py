# As url parameter
# curl "https://freesound.org/apiv2/search/text/?query=piano&token=YOUR_API_KEY"

# as header
# curl -H "Authorization: Token YOUR_API_KEY" "https://freesound.org/apiv2/search/text/?query=piano"
# from authorize import authorize_procedure, 
from freesound.freesound_client import FreeSoundClient
from typing import Any
from freesound.utilities import separator, get_file_info
import os
from dotenv import load_dotenv
from io import BytesIO
from lib import *


API_KEY, USER_ID, OUT_FOLDER = load_credentials()

	

if  __name__ == "__main__":
	# Inizializzo il client di connessione al servizio
	client = FreeSoundClient(user_id=USER_ID,api_key=API_KEY)
	try:
		# chiedi le parole chiavi di ricerca
		query: str = 'piano' #prompt_keywords()
	except KeyboardInterrupt as e:
		exit()
	# cerca nel database freesound
	response_list: dict[Any, Any] = client.search(query);
	if response_list['count'] == 0:
		print("No files found")
		exit()
	else:
		print(f"{response_list['count']} files found!")

	separator()

	try:
		# quanti file si svolgiono scaricare?
		max_downloads: int = 99 #prompt_downloads()
	except KeyboardInterrupt as e:
		exit()

	print(f"Downloading: {max_downloads} files")

	separator()

	for i in range(max_downloads):
		try:
			sound = response_list['results'][i]
		except IndexError as e:
			print("Changing Page!")
			new_list = client.get_next_page_result()
			exit()

		track_id = str(sound['id'])
		file_name:str = sound['name'].replace(" ", "-")
		# Richiedi informazioni relative alla traccia individuata
		file_data: dict[Any, Any] = client.get_track_info(track_id, sound['name'], {"fields":"type,channels,bitdepth,samplerate,download"})
		# Assicurati che ci siano tutte le informazioni necessarie
		try:
			file_type = get_file_info(file_data,"type")
			num_channels = get_file_info(file_data,"channels")
			sample_rate = get_file_info(file_data,"samplerate")
			bit_depth = int(get_file_info(file_data,"bitdepth"))
			sound_url = get_file_info(file_data,"download")
			
			sample_width = int(bit_depth/8)
		except KeyError as e:
			print(f"The file {file_name} does not have a {e} value")
			print(f"Skipping")
			continue
		print(f"{file_name}, {num_channels}, {file_type},{sample_rate}, {bit_depth}, {sound_url}")

		file_extension:str = file_name + "." + file_type
		filepath: str = os.path.join(OUT_FOLDER,file_extension)
		# se il file audio non è già stato scaricato
		if not os.path.exists(filepath):
			# Scarica la traccia nella cartella definita all'inizio del programma
			print("Download")
	#		binary_data: BytesIO| None = client.download_track(str(sound_url), file_extension)
			
		else:
			print(f"The file {file_name} has already been downloaded...Skipping")
		separator()

	client.logout()
from freesound import FreeSoundClient
from freesound.formatting import separator, info
from typing import Any
import os
from lib import *


# Recupera le credenziali da .env
API_KEY, USER_ID, OUT_FOLDER = load_credentials()
# Inizializzo il client di connessione al servizio
client = FreeSoundClient(user_id=USER_ID,api_key=API_KEY)

def get_info_and_download(soundlist:dict[Any,Any]) -> bool:
	global count
	for sound in soundlist:
		if count < max_downloads_user:
			track_id = str(sound['id'])
			# Richiedi informazioni relative alla traccia individuata
			file_data = client.get_track_info(track_id, sound['name'])
			filepath = os.path.join(OUT_FOLDER,file_data.file_name)
			# se il file audio non è già stato scaricato...
			if not os.path.exists(filepath):
				# ...scarica la traccia nella cartella definita all'inizio del programma...
				client.download_track(str(file_data.sound_url), file_data.file_name, OUT_FOLDER)
				count+= 1
				info(f"Downloaded Files: {count}")
			# ...altrimenti ignora il file
			else:
				warning(f"The file {file_data.file_name} has already been downloaded...Skipping")
				pass
			separator()
			
		else: 
			return False
	return True

# Ctrl+C block
try:
	# chiedi le parole chiavi di ricerca
	query = prompt_keywords()
	# cerca nel database freesound
	response_list = client.search(query,fields=["type","channels","bitdepth","samplerate","download","tags"]);

	if response_list['count'] == 0:
		warning("No files found")
		client.logout()
	else:
		max_downloads = response_list['count']
		print(f"{max_downloads} files found!")

	separator()
	# quanti file si vogliono scaricare?
	max_downloads_user = prompt_downloads(max_downloads)
	print(f"Downloading: {max_downloads_user} files")

	separator()

	count = 0
	while count < max_downloads_user:
		if get_info_and_download(response_list['results']):
			print(f"Downloaded {count} files")
			print("Changing Page!")
			separator()
			response_list = client.get_next_page_result()
		else:
			info(f"Downloaded {count} files")
			break
			
	print("Done")
		
except KeyboardInterrupt:
	pass

client.logout()
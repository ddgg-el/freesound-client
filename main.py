# As url parameter
# curl "https://freesound.org/apiv2/search/text/?query=piano&token=YOUR_API_KEY"

# as header
# curl -H "Authorization: Token YOUR_API_KEY" "https://freesound.org/apiv2/search/text/?query=piano"
# from authorize import authorize_procedure, 
from freesound.freesound_client import FreeSoundClient, FreeSoundTrack
from typing import Any
from freesound.utilities import separator
import os
from io import BytesIO
from lib import *


# Recupera le credenziali da .env
API_KEY, USER_ID, OUT_FOLDER = load_credentials()
# Inizializzo il client di connessione al servizio
client = FreeSoundClient(user_id=USER_ID,api_key=API_KEY)
try:
	# chiedi le parole chiavi di ricerca
	query: str = prompt_keywords()
except KeyboardInterrupt as e:
	exit()
# cerca nel database freesound
response_list: dict[Any, Any] = client.search(query);
if response_list['count'] == 0:
	print("No files found")
	exit()
else:
	max_downloads = response_list['count']
	print(f"{max_downloads} files found!")

separator()


try:
	# quanti file si vogliono scaricare?
	max_downloads_user: int = prompt_downloads(max_downloads)
except KeyboardInterrupt as e:
	exit()

print(f"Downloading: {max_downloads_user} files")

separator()
try:
	for i in range(max_downloads_user):
		try:
			sound = response_list['results'][i]
			track_id = str(sound['id'])
			print(track_id)
		except IndexError as e:
			if len(response_list['results']) < max_downloads:
				print("Changing Page!")
				response_list = client.get_next_page_result()
				continue
			break
		
		
		# Richiedi informazioni relative alla traccia individuata
		try:
			file_data: FreeSoundTrack = client.get_track_info(track_id, sound['name'], {"fields":"type,channels,bitdepth,samplerate,download"})
			filepath: str = os.path.join(OUT_FOLDER,file_data.file_name)
			# se il file audio non è già stato scaricato
			if not os.path.exists(filepath):
				# Scarica la traccia nella cartella definita all'inizio del programma
				print("Download")
				binary_data: BytesIO| None = client.download_track(str(file_data.sound_url), file_data.file_name)
			else:
				print(f"The file {file_data.file_name} has already been downloaded...Skipping")
			separator()
		except KeyError as e:
			print(f"Skipping")
			pass
		
except KeyboardInterrupt as e:
	client.logout()
	exit()	
client.logout()
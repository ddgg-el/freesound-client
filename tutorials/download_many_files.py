import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"

c = FreeSoundClient(USER_ID,API_KEY)

filters = FreeSoundFilters(type="wav", samplerate=48000).aslist
c.search(query="piano", fields=Field.download, filter=filters, page_size=100)
c.download_results(output_folder="tutorials/sound_lib",files_count=100)
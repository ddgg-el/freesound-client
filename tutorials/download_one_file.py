import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"

c = FreeSoundClient(USER_ID,API_KEY)
result = c.get_track_info(382353)
c.download_track(result.download, result.name,outfolder='tutorials/sound_lib', skip=True)

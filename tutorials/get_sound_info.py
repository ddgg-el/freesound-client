import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"

c = FreeSoundClient(USER_ID,API_KEY)

result = c.get_track_info(382353)
print(result)
# print(result.as_dict())

t = FreeSoundSoundInstance({'id': 524545, 'name': 'Piano12 B Flat', 'tags': ['note', 'synthesizer', 'Piano'], 'type': 'mp3', 'download': 'https://freesound.org/apiv2/sounds/524545/download/'})
print(t.name)

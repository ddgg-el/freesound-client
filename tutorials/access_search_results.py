import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"

c = FreeSoundClient(USER_ID,API_KEY)

 # store the id of only those sounds that have a `pitch_centroid` lower than 0.4
result = c.search(query="piano detuned", fields=Field.analysis, descriptors=Descriptor.sfx_pitch_centroid, page_size=100)
results_list = result['results']

ids:list[int] = []

for i,snd in enumerate(results_list):
	centroid = snd['analysis']['sfx']['pitch_centroid']
	mean = centroid['mean']
	if mean <= 0.4:
		ids.append(snd['id'])

print(ids)
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"

c = FreeSoundClient(USER_ID,API_KEY)

fields = FreeSoundFields([Field.download, Field.analysis]).aslist
filters = FreeSoundFilters(type="wav", samplerate=44100, tag=["prepared"], ac_single_event=True).aslist
result = c.search(query="piano", fields=fields, filter=filters, descriptors=Descriptor.lowlevel_average_loudness, page_size=150)
print(c.results_list['count']) # 150

c.get_next_page(result['next'])
print(c.results_list['count']) # 151

c.write_results_list()
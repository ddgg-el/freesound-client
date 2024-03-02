import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

USER_ID = "<your-user-id>"
API_KEY = "<your-api-key>"

c = FreeSoundClient(USER_ID,API_KEY)

filters = FreeSoundFilters(type='wav',samplerate=44100,bitdepth=16,tag=['prepared','detuned'])
desc = FreeSoundDescriptors([Descriptor.lowlevel_average_loudness,Descriptor.lowlevel_dissonance])
fields = FreeSoundFields([Field.analysis, Field.download])

# you can use Field.all() to query all the data about a sound file at once
c.search(query="piano detuned", fields=fields.aslist, filter=filters.aslist, descriptors=desc.aslist)

# the same query using strings
# c.search(query="piano detuned", fields="analysis,download", filter="type:wav samplerate:44100 bitdepth:16 tag:prepared tag:detuned", descriptors="lowlevel.average_loudness,lowlevel.dissonance")

c.dump_results()
c.write_results_list()
# c.download_results() 

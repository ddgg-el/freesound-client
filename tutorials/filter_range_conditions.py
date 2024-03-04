import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"

c = FreeSoundClient(USER_ID,API_KEY)

filters = FreeSoundFilters(type=Filter.OR('wav','aiff'), duration=Filter.UP_TO(1),created=Filter.RANGE((datetime.now()-timedelta(weeks=20)),datetime.now())).aslist
result = c.search("music",fields=Field.duration,filter=filters)
c.dump_results()

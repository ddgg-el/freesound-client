import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"

c = FreeSoundClient(USER_ID,API_KEY)
c.load_results_list("tutorials/records/240301T2042_results_list.json")
c.dump_results()
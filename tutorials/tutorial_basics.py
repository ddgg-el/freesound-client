import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from freesound import *

USER_ID = "<your-user-id>"
API_KEY = "<your-api-key>"

c = FreeSoundClient(USER_ID,API_KEY)
c.search(query="piano detuned", fields="download")
# print(c.results_list)
c.dump_results()

c.download_results() 

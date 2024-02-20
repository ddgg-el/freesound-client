from freesound import *

API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"
# or use load-credentials from lib.py

c = FreeSoundClient(USER_ID,API_KEY)

try:
# handwritten
	result = c.search("piano detuned",fields="download,type,tags,ac_analysis",filters="type:mp3",sort_by='score',page_size=3)
	c.dump_result(result)
	# c.download_results("sound_lib/",2)
	# c.write_download_list()
	# c.write_result_list()
	
# with the help of the API 
	field:str = FreeSoundFields([fields.DOWNLOAD, fields.TYPE, fields.TAGS]).params
	filters:str = FreeSoundFilter(type="mp3").params
	sort_by:str = FreeSoundSort.SCORE
	# second_result = c.search("piano",filters=filters, fields=field,sort_by=sort_by,page_size=1)
	# c.dump_result(second_result)

except KeyboardInterrupt:
	print("\nStop")
	c.logout()

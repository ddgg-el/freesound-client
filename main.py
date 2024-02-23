from freesound import *

# You need to set these only before the file access_token.json is created
API_KEY = "<your-api-key>"
USER_ID = "<your-user-id>"
# or use load-credentials from lib.py

c = FreeSoundClient(USER_ID,API_KEY)

try:
# handwritten
	result = c.search("piano detuned",fields="download",filters="type:wav",sort_by='score',page_size=3)
	# result = c.search("piano detuned",fields="download,type,tags,analysis",filters="type:mp3",descriptors="lowlevel.spectral_complexity,lowlevel.spectral_entropy",sort_by='score',page_size=3)
	# print(result)
	# c.download_results("",files_count=2)
	# c.write_download_list()
	# c.write_result_list()
# 	print("=======================================")
# # with the help of the API 
	field:str = FreeSoundFields([Field.download, Field.tags, Field.analysis]).aslist
	filters:str = FreeSoundFilters(type="mp3").aslist
	sort_by:str = FreeSoundSort.SCORE
	descriptors = FreeSoundDescriptors([Descriptor.lowlevel_spectral_complexity,Descriptor.lowlevel_spectral_entropy]).aslist
# 	second_result = c.search("piano detuned",fields=field,filters=filters,sort_by=sort_by,page_size=3)
# 	c.dump_result(second_result)
	
except KeyboardInterrupt:
	print("\nStop")
	c.logout()


# TODO run radon black vulture
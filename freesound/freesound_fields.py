"""
Details at:
-----------
https://freesound.org/docs/api/resources_apiv2.html#response-sound-instance

EXAMPLE
-------
https://freesound.org/apiv2/search/text/?query=guitar&fields=id%2Cname%2Cfilesize
"""

from enum import Enum

class fields(Enum):
	ID = "id"
	URL = "url"
	NAME = "name"
	TAGS = "tags"
	DESCRIPTION = "description"
	GEOTAG = "geotag"
	CREATED = "created"
	LICENSE = "license"
	TYPE = "type"
	CHANNELS = "channels"
	FILESIZE = "filesize"
	BITRATE = "bitrate"
	BITDEPTH = "bitdepth"
	DURATION = "duration"
	SAMPLERATE = "samplerate"
	USERNAME = "username"
	PACK = "pack"
	DOWNLOAD = "download"
	BOOKMARKS = "bookmarks"
	PREVIEWS = "previews"
	IMAGES = "images"
	NUM_DOWNLOADS = "num_downloads"
	AVG_RATING = "avg_rating"
	NUM_RATINGS = "num_ratings"
	RATE = "rate"
	COMMENTS = "comments"
	NUM_COMMENTS = "num_comments"
	COMMENT = "comment"
	SIMILAR_SOUNDS = "similar_sounds"
	ANALYSIS = "analysis" # to use in combination with parameter 'descriptors'
	ANALYSIS_STATS = "analysis_stats" # link for the analysis file
	ANALYSIS_FRAMES = "analysis_frames" # link for full frame analysis report
	AC_ANALYSIS = "ac_analysis" # for full ac analysis

# Coma separated values
class FreeSoundFields:
	def __init__(self, fields:list[fields]):
		param_array = [field.value for field in fields]
		self._params = ",".join(param_array)

	@property
	def params(self) -> str:
		return self._params

if __name__ == "__main__":
	a = FreeSoundFields([fields.BITDEPTH,fields.SAMPLERATE])
	print(a.params)
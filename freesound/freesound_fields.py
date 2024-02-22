"""
Details at:
-----------
https://freesound.org/docs/api/resources_apiv2.html#response-sound-instance

EXAMPLE
-------
https://freesound.org/apiv2/search/text/?query=guitar&fields=id%2Cname%2Cfilesize
"""

from dataclasses import dataclass
from typing import Optional, Any

from freesound.freesound_list_maker import ListMaker

@dataclass
class FieldsBase():
	id:int
	name:str
	url: Optional[str]
	tags: Optional[str|list[str]] = None
	description: Optional[str] = None
	geotag: Optional[str] = None
	created: Optional[str] = None
	license: Optional[str] = None
	type: Optional[str] = None
	channels: Optional[int] = None
	filesize: Optional[int] = None
	bitrate: Optional[int] = None
	bitdepth: Optional[int] = None
	duration: Optional[float] = None
	samplerate: Optional[int] = None
	username: Optional[str] = None
	pack: Optional[str] = None
	download: Optional[str] = None
	bookmarks: Optional[str] = None
	previews: Optional[dict[str,Any]] = None
	images: Optional[dict[str,Any]] = None
	num_downloads: Optional[int] = None
	avg_rating: Optional[float] = None
	num_ratings: Optional[int] = None
	rate: Optional[int] = None
	comments: Optional[int] = None
	num_comments: Optional[int] = None
	comment: Optional[str] = None
	similar_sounds: Optional[str] = None
	analysis: Optional[dict[str,Any]] = None
	analysis_stats: Optional[str] = None
	analysis_frames: Optional[str] = None
	ac_analysis: Optional[dict[str,Any]] = None

	def _set_file_name(self,ext:str) -> str:
		file_name = self.name.strip().replace(" ","-")
		
		if ext not in file_name:
			file_name += "."+ext
		self.name = file_name
		return file_name

	
class FieldsMeta(FieldsBase):
	def __init__(self) -> None:
		for attribute,_ in self.__annotations__.items():
			setattr(self,attribute,str(attribute))

Field = FieldsMeta()

# Coma separated values
class FreeSoundFields(ListMaker):
	def __init__(self, fields:list[Any]) -> None:
		super().__init__(fields)

	@property
	def aslist(self) -> str:
		return self._make_coma_separated()
		

if __name__ == "__main__":
	a = FreeSoundFields([Field.tags,Field.samplerate])
	print(a.aslist)

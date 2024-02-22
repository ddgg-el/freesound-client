"""
The module contains the definitions of
- FieldsBase (the Base class for FreeSoundFields)
- FieldMeta
- Field (an instance of FieldMeta)
- FreeSoundFields

Relevant for the users are just the `Field` and `FreeSoundFields`, two utilitity structures which help users to build `fields` queries for the [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient] by providing lintering. 

Details at:
-----------
<https://freesound.org/docs/api/resources_apiv2.html#response-sound-instance>


Usage Example
-------------
`https://freesound.org/apiv2/search/text/?query=guitar&fields=id%2Cname%2Cfilesize`

This query contains 3 fields parameters

`id`, `name` and `filesize`

You can build this query taking advange of lintering when writing:
>>> print(FreeSoundFields([Field.id,Field.name,Field.filesize]).aslist)
id,name,filesize
"""

from dataclasses import dataclass
from typing import Optional, Any

from .freesound_list_maker import ListMaker

@dataclass
class FieldsBase():
	"""The Base class for [`FieldMeta`][freesound.freesound_fields.FieldMeta) and [`FreeSoundSoundInstance`][freesound.freesound_sound.FreeSoundSoundInstance]. Useful for lintering"""
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

	
class FieldMeta(FieldsBase):
	"""A class whose attributes are valid `fields` to query the [`freesound.org`](https://www.freesound.org) database"""
	def __init__(self) -> None:
		for attribute,_ in self.__annotations__.items():
			setattr(self,attribute,str(attribute))

Field = FieldMeta()
"""Field is an instance of `FieldsMeta` and provides lintering for valid `fields` to query the [`freesound.org`](https://www.freesound.org) database"""

# Coma separated values
class FreeSoundFields(ListMaker):
	"""A Utility Class that creates a coma-separated string from a list of [`Field`][freesound.freesound_fields.Field] calling the method `aslist`
	
	The result is a ready formatted `string` to be used in the `fields` parameter of [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient]

	For more information visit: <https://freesound.org/docs/api/resources_apiv2.html#response-sound-instance>

	Usage: 
		```
		>>> print(FreeSoundFields([Field.id,Field.filesize]).aslist)
		id,filesize
		```
	"""
	def __init__(self, fields:list[Any]) -> None:
		super().__init__(fields)

	@property
	def aslist(self) -> str:
		"""use this property to pass the list of [`Field`][freesound.freesound_fields.Field]to a [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient]

		Returns:
			str: a coma-separated string of valid fields
		"""
		return self._make_coma_separated()
		

if __name__ == "__main__":
	print(FreeSoundFields([Field.tags,Field.samplerate]).aslist)

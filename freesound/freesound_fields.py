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

# from dataclasses import dataclass
from typing import Any

from .freesound_list_maker import ListMaker

class Field():
	"""Field is a class that provides hints for valid `fields` to query the [`freesound.org`](https://www.freesound.org) database"""
	id = "id"
	name = "name"
	url = "url"
	tags = "tags"
	description = "description"
	geotag = "geotag"
	created = "created"
	license = "license"
	type = "type"
	channels = "channels"
	filesize = "filesize"
	bitrate = "bitrate"
	bitdepth = "bitdepth"
	duration = "duration"
	samplerate = "samplerate"
	username = "username"
	pack = "pack"
	download = "download"
	bookmarks = "bookmarks"
	previews = "previews"
	images = "images"
	num_downloads = "num_downloads"
	avg_rating = "avg_rating"
	num_ratings = "num_ratings"
	rate = "rate"
	comments = "comments"
	num_comments = "num_comments"
	comment = "comment"
	similar_sounds = "similar_sounds"
	analysis = "analysis"
	analysis_stats = "analysis_stats"
	analysis_frames = "analysis_frames"
	ac_analysis = "ac_analysis"

	def _set_file_name(self,name:str) :
		file_name = name.strip().replace(" ","-")
		return file_name
	
	@classmethod
	def all(cls):# -> list[Any]:
		fields:list[str] = []
		for attr_name, attr_value in cls.__dict__.items():
			if not isinstance(attr_value, classmethod) and not attr_name.startswith("__") and not callable(attr_value):
				fields.append(attr_value)
		return fields 

	
# class Field(FieldsBase):
# 	"""A class whose attributes are valid `fields` to query the [`freesound.org`](https://www.freesound.org) database"""
# 	def __init__(self) -> None:
# 		for attribute,_ in self.__annotations__.items():
# 			setattr(self,attribute,str(attribute))

# Field = FieldMeta()


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

"""
The module contains the definitions of the class FreeSoundSoundInstance
which represents an Object that stores the json data of a SoundInstance received from the freesound.org Database

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
from typing import Any

from .freesound_errors import DataError, FieldError
from .freesound_fields import FieldsBase

class FreeSoundSoundInstance(FieldsBase):
	"""A Utility class the stores the details of a SoundInstance request from the [`freesound.org`](https://www.freesound.org) database. 
		Notice that the name of the input SoundInstance will be manipulated automatically by calling `self._set_file_name`. A name such as `Piano12 B Flat`
		will be automatically transformed in `Piano12-B-Flat.mp3`
	
		for more information visit: <https://freesound.org/docs/api/resources_apiv2.html#sound-instance>

		Args:
			track_data (dict[Any,Any]): a dictionary of information about a SoundInstance

		Raises:
			AttributeError: if the passed dictonary does not contain the fields `id` and `name` it raises an error
			DataError: if the passed dictonary does not contain a valid `field` it raises an error

		Usage:
			```
			>>> t = FreeSoundSoundInstance({'id': 524545, 'name': 'Piano12', 'tags': ['note', 'synthesizer', 'Piano'], 'type': 'mp3', 'download': 'https://freesound.org/apiv2/sounds/524545/download/'})
			>>> print(t.name)
			Piano12
			```
	"""
	# FIXME not setting filename!
	def __init__(self, track_data:dict[str,Any]) -> None:
		valid_attributes = [member for member in FieldsBase.__annotations__]
		if 'id' not in track_data or 'name' not in track_data:
			raise AttributeError("No 'id' or 'name' provided")
		
		for field,value in track_data.items():
			if field not in valid_attributes:
				raise DataError(f"Could not create a FreeSoundTrack {field} is not a valid field")
			if field == 'name':
				value = self._set_file_name(str(value))
			if field == 'type':
				value = self._set_file_ext(str(value))
			setattr(self,field,value)
		
	def ensure_value(self,field:str)-> str:
		"""a utility function which ensure the presence of a field inside the input dictionary

		Args:
			field (str): which field must be store in this `FreeSoundSoundInstance`

		Raises:
			FieldError: raises an error if `field` is not store in this `FreeSoundSoundInstance`

		Returns:
			str: the value of the `field`
		
		Usage:
			```
			>>> t = FreeSoundSoundInstance({'id': 524545, 'name': 'Piano12', 'type': 'mp3'})
			>>> t.ensure_value('download')
			FieldError
			>>> t.ensure_value('type')
			mp3
			```
		"""
		value = getattr(self,field, None)
		if  value is None:
			raise FieldError(f"Attribute '{field}' not found! Please include the '{field}' keyword in your fields' search list and retry")
		return value
	
	
		# return file_name
	
	def _set_file_ext(self,ext:str) -> None:
		print("setting file ext")
		if ext not in self.name:
			self.name += "."+ext
		# self.name = file_name
		
	def __repr__(self) -> str:
		return f"<freesound.freesound_track.FreeSoundTrack {self.name}>"
	
if __name__ == "__main__":
	t = FreeSoundSoundInstance({'id': 524545, 'name': 'Piano12 B Flat', 'tags': ['note', 'synthesizer', 'Piano'], 'type': 'mp3', 'download': 'https://freesound.org/apiv2/sounds/524545/download/'})
	print(t)
	
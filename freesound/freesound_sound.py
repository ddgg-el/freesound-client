from typing import Any

from .freesound_errors import DataError, FieldError
from .freesound_fields import FieldsBase

class FreeSoundSoundInstance(FieldsBase):
	def __repr__(self):
		return f"<freesound.freesound_track.FreeSoundTrack {self.name}>"
	
	def __init__(self, track_data:dict[Any,Any]) -> None:
		valid_attributes = [member for member in FieldsBase.__annotations__]
		if 'id' not in track_data or 'name' not in track_data:
			raise AttributeError("No 'id' or 'name' provided")
		
		for field,value in track_data.items():
			if field not in valid_attributes:
				raise DataError(f"Could not create a FreeSoundTrack {field} is not a valid field")
			if field == 'type':
				value = self._set_file_name(value)
			setattr(self,field,value)
		
	def ensure_value(self,attribute:str):	
		value = getattr(self,attribute, None)
		if  value is None:
			raise FieldError(f"Attribute '{attribute}' not found! Please include the '{attribute}' keyword in your fields' search list and retry")
	
		return value
		
if __name__ == "__main__":
	t = FreeSoundSoundInstance({'id': 524545, 'name': 'Piano12', 'tags': ['note', 'synthesizer', 'Piano'], 'type': 'mp3', 'download': 'https://freesound.org/apiv2/sounds/524545/download/'})
	print(t.ac_analysis)
	
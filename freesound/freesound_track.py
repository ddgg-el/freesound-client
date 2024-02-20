from typing import Any

from .freesound_errors import DataError, FieldError
from .freesound_fields import fields

# TODO not all the attributes have type

class FreeSoundTrack:
	def __repr__(self):
		return f"<freesound.freesound_track.FreeSoundTrack {self.name}>"
	
	def __init__(self, track_data:dict[Any,Any], check_for_field:str|list[str]|None=None) -> None:
		valid_attributes = [member.value for member in fields]
		if 'id' not in track_data or 'name' not in track_data:
			raise AttributeError("No 'id' or 'name' provided")
		
		for field,value in track_data.items():
			if field not in valid_attributes:
				raise DataError(f"Could not create a FreeSoundTrack {field} is not a valid field")
			setattr(self,field,value)
			# property(lambda self: str(self.key())) 
			
		if check_for_field is not None:
			if isinstance(check_for_field, str):
				check_for_field = [check_for_field]
			for field in check_for_field:
				if field not in track_data:
					raise FieldError(f"Field '{field}' not found! Please include the '{field}' keyword in your fields' search list and retry")
		
	@property
	def name(self) -> str:
		file_name = getattr(self,'_name','')
		if self._type not in file_name:
			file_name += "."+self._type
		return file_name
	
	@name.setter
	def name(self, name:str):
		self._name = name.strip().replace(" ", "-")

	@property
	def id(self)->int:
		return getattr(self,'_id')
	
	@id.setter
	def id(self, id:int) -> None:
		self._id = id
	
	@property
	def download(self)->str:
		return getattr(self,'_download')

	@download.setter
	def download(self,url:str):
		self._download = url

	@property
	def type(self)->str:
		return getattr(self,'_type')
	
	@type.setter
	def type(self,ext:str):
		self._type = ext
	
if __name__ == "__main__":
	t = FreeSoundTrack({'id': 524545, 'name': 'Piano12', 'tags': ['note', 'synthesizer', 'Piano'], 'type': 'mp3', 'download': 'https://freesound.org/apiv2/sounds/524545/download/'})
	print(t.name)
	
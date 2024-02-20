from typing import Any

class FreeSoundTrack():
	def __init__(self, track_name:str, *args:dict[Any,Any]) -> None:
		self.original_name = track_name
		self.short_name:str = self.original_name.replace(" ", "-")
		self.parse_track_info(*args)

		self.file_name:str = self.short_name + "." + self.file_type

		print(f"{self.file_name}, {self.num_channels}, {self.file_type},{self.sample_rate}, {self.bit_depth}, {self.sound_url}")

	def parse_track_info(self, file_data:dict[Any,Any]) -> None:
		# Assicurati che ci siano tutte le informazioni necessarie
		try:
			self.file_type = self._get_file_info(file_data,"type")
			self.num_channels = self._get_file_info(file_data,"channels")
			self.sample_rate = self._get_file_info(file_data,"samplerate")
			self.bit_depth = int(self._get_file_info(file_data,"bitdepth"))
			self.sound_url = self._get_file_info(file_data,"download")
			
			self.sample_width = int(self.bit_depth/8)
		except KeyError as e:
			raise KeyError(f"The file {self.file_name} does not have a {e} value")

	def _get_file_info(self, set:dict[Any,Any], key:str) -> Any:
		value = set.get(key)
		if value is None:
			raise KeyError(key)
		return value 	
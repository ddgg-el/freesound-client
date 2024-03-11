from __future__ import annotations

from freesound.freesound_errors import FreesoundDownloadError
from .formatting import *
from .freesound_sound import FreeSoundSoundInstance
from datetime import datetime
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
	from .freesound_client import FreeSoundClient

class Downloader:
	"""a utility class which implements the bulk download of analysis data and sound file for the FreeSoundClient 
	and keeps records of the downloaded files
	"""
	def __init__(self, client:FreeSoundClient) -> None:
		self.client = client
		self._download_count = 15
		self._download_list:dict[str,Any] = {'downloaded-files':[], 'timestamp':datetime.now().isoformat(), 'count':0} # read-only
		pass

	def download_results(self,files_count:int|None=None, include_analysis:bool|None=None,output_folder:str|None=None) -> None:
		"""download `files_count` audio files into `output_folder_path`

		This function takes care of pagination automatically

		Args:
			files_count (int | None, optional): how many files should be downloaded. 
			include_analysis (bool | None, optional): whether to include the frame-by-frame analysis data file or not
			output_folder (str | None, optional):the destination folder.
		"""
		self._set_download_count(files_count)
		if self._download_count == 0:
			print("Nothing to Download")
			return
		else:			
			print(f"Downloading {self._download_count} files of {self.client.results_page['count']}")
			separator()
			if include_analysis is None:
				include_analysis = self._prompt_yes_no("Do you want to include the full frame-by-frame analysis data of each downloaded sound file? [yes|no:default]: ")
			separator()
			downloaded_count = 0
			while downloaded_count < self._download_count:
				for sound in self.client.results_page['results']:
					if downloaded_count >= self._download_count:
						break
					try:
						parsed_sound = FreeSoundSoundInstance(sound)
						
						if self._download_audio_file_step(parsed_sound,output_folder,include_analysis):
							downloaded_count+=1
							self._update_download_list(sound, downloaded_count)
							info(f"Downloaded Files: {downloaded_count} of {self._download_count}")
							separator()
					except Exception as e:
						raise e
						# self._handle_exception(e)
					
				if downloaded_count < self._download_count:
					if not self._set_next_page():
						break
			info("Done Downloading")

	def download_analysis_results(self,files_count:int|None=None, include_sound:bool|None=None,output_folder:str|None=None) -> None:
		"""download `files_count` analysis files into `output_folder_path`

		This function takes care of pagination automatically

		Args:
			files_count (int | None, optional): how many files should be downloaded. 
			include_sound (bool | None, optional): whether to download the sound file or not
			output_folder (str | None, optional):the destination folder.
		"""
		self._set_download_count(files_count)
		if self._download_count == 0:
			print("Nothing to Download")
			return
		else:			
			print(f"Downloading {self._download_count} files of {self.client.results_page['count']}")
			separator()
			if include_sound is None:
				include_sound = self._prompt_yes_no("Do you want to include the sound file data of each downloaded analysis data? [yes|no:default]: ")
			separator()
			downloaded_count = 0
			while downloaded_count < self._download_count:
				for sound in self.client.results_page['results']:
					if downloaded_count >= self._download_count:
						break
					try:
						parsed_sound = FreeSoundSoundInstance(sound)
						
						if self._download_data_file_step(parsed_sound,output_folder,include_sound):
							downloaded_count+=1
							info(f"Downloaded Files: {downloaded_count} of {self._download_count}")
							separator()
					except Exception as e:
						raise e 
						# self._handle_exception(e)
					
				if downloaded_count < self._download_count:
					if not self._set_next_page():
						break
			info("Done Downloading")

	def _download_audio_file_step(self,sound:FreeSoundSoundInstance, output_folder:str|None,include_analysis:bool|None)->bool:
		try:
			sound_download_successful = self.client.download_track(sound.ensure_value('download'),sound.name,output_folder,skip=True)
			if sound_download_successful and include_analysis:
				analysis_downloaded = self.client.download_analysis(sound.ensure_value('analysis_frames'),sound.name,output_folder,skip=True)
				if not analysis_downloaded:
					warning(f"No Analysis Data Saved for file {sound.name}")
			return sound_download_successful
		except Exception as e:
			raise(e)
			# self._handle_exception(e)

	def _download_data_file_step(self,sound:FreeSoundSoundInstance, output_folder:str|None,include_sound:bool|None)->bool:
		try:
			analysis_download_successful = self.client.download_analysis(sound.ensure_value('analysis_frames'),sound.name,output_folder,skip=True)
			if analysis_download_successful and include_sound:
				sound_downloaded = self.client.download_track(sound.ensure_value('download'),sound.name,output_folder,skip=True)
				if not sound_downloaded:
					warning(f"No sound file Data Saved for file {sound.name}")
			return analysis_download_successful
		except Exception as e:
			raise(e)
			# self._handle_exception(e)

	def _set_download_count(self,count:int|None):
		max_value = self.client.results_page['count']
		if count is None:
			self._download_count = self._prompt_downloads(max_value)
		else:
			if count <= max_value:
				self._download_count = count
			else:
				warning(f"You want to download {count} files, but only {max_value} were found")
				self._download_count = max_value

	def _prompt_yes_no(self, message:str) -> bool:
		while True:
			answer = ask(message).lower()
			if answer == 'no' or answer == '':
				return False
			elif answer == 'yes':
				return True
			else:
				warning("You must type 'yes' or 'no'")

	def _prompt_max_download(self, downloadable:int) -> int:
		while True:
			max_download_input: str = ask("How many files do you want to download? [a number | all] ")
			if max_download_input.lower() == 'all' or max_download_input == '':
				return downloadable
			elif max_download_input.isdigit():
				max_download = int(max_download_input)
				
				if max_download <= downloadable:
					return max_download
				else:
					warning("You are trying to download more files than are actually available")
					warning(f"Setting {downloadable} as the number of files to download")
					return downloadable		
			else:
				warning("You must insert a number or type 'all'")

	def _prompt_downloads(self,downloadable:int)-> int:
		if downloadable == 0:
			raise FreesoundDownloadError("There is nothing to download")
		max_download = self._prompt_max_download(downloadable)
		return max_download

	def _update_download_list(self, sound_obj:dict[str,Any], count:int):
		self._download_list['count'] = count
		self._download_list['timestamp'] = datetime.now().isoformat()
		self._download_list['downloaded-files'].append(sound_obj)

	def _set_next_page(self) -> bool:
		if self.client.results_page["next"] is not None:
			url:str = self.client.results_page["next"]
			self.client.get_next_page(url)
			return True
		else:
			return False

	@property
	def download_count(self)->int:
		return self._download_count
	
	@property
	def download_list(self):
		return self._download_list
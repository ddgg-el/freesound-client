"""
Details at:
-----------
https://freesound.org/docs/api/resources_apiv2.html#text-search

EXAMPLE
-------
https://freesound.org/apiv2/search/text/?query=guitar&fields=id%2Cname&filter=type:wav
https://freesound.org/apiv2/search/text/?query=guitar&fields=id%2Cname%2Cdownload%2Ctype%2Ctags&filter=tag%3Ablues+type%3Amp3+tag%3Ascale

Don't forget that you can use this sintax
-----------------------------------------
filter=fieldname:[start TO end]
filter=fieldname:[* TO end]
filter=fieldname:[start to \\*] # with only one '\'

DATES
-----
filter=created:[* TO NOW]
filter=created:[1976-03-06T23:59:59.999Z TO *]
filter=created:[1995-12-31T23:59:59.999Z TO 2007-03-06T00:00:00Z]
filter=created:[NOW-1YEAR/DAY TO NOW/DAY+1DAY]
filter=created:[1976-03-06T23:59:59.999Z TO 1976-03-06T23:59:59.999Z+1YEAR]
filter=created:[1976-03-06T23:59:59.999Z/YEAR TO 1976-03-06T23:59:59.999Z]

BOOLEAN
-------
filter=type:(wav OR aiff)
filter=description:(piano AND note)
"""

# TODO geotagging

from typing import Any, Unpack
from .filter_types import TypeFilter, TypeACFilter
from .freesound_errors import DataError

#"filter": "tag:plucked tag:fret type:wav"
class FreeSoundFilterBase:
	'''Utility Class to create different filters for FreeSound searches

	For more information visit: https://freesound.org/docs/api/resources_apiv2.html#text-search
	'''
	_parameters_list:dict[str,Any] = {}
	def __init__(self, **kwargs:Any) -> None:
		self._filters:list[str] = []
		for key,values in kwargs.items():
			if key in self._parameters_list:
				if isinstance(values,list):
					for value in values: # type: ignore
						self._filters.append(f"{key}:{value}")
				else:
					self._filters.append(f"{key}:{values}")
			else:
				raise DataError(f"'{key}' is not a valid filter. See the list of available filter at: https://freesound.org/docs/api/resources_apiv2.html#text-search")
		
		self._params = self._make_filter_list()
		
	@property
	def filters(self) -> list[str]:
		return self._filters
	
	@property
	def params(self) -> str:
		return self._params
	
	def _make_filter_list(self) -> str:
		return ' '.join(self._filters)
	
class FreeSoundFilter(FreeSoundFilterBase):
	'''Utility Class to create AudioCommons filters for FreeSound searches

	For more information visit: https://freesound.org/docs/api/resources_apiv2.html#text-search
	'''
	_parameters_list:dict[str,Any] = TypeFilter.__annotations__
	def __init__(self, **kwargs: Unpack[TypeFilter]) -> None:
		super().__init__(**kwargs)


class FreeSoundACFilter(FreeSoundFilterBase):
	'''Utility Class to create AudioCommons filters for FreeSound searches

	For more information visit: https://freesound.org/docs/api/resources_apiv2.html#text-search
	Check the audio common project at: http://www.audiocommons.org/
	'''
	_parameters_list:dict[str,Any] = TypeACFilter.__annotations__
	def __init__(self, **kwargs: Unpack[TypeACFilter]) -> None:
		super().__init__(**kwargs)

# TODO create helper class
class FreeSoundSort():
	SCORE = "score"
	DURATION_DESC = "duration_desc"
	DURATION_ASC = "duration_asc"
	CREATED_DESC = "created_desc"
	CREATED_ASC = "created_asc"
	DOWNLOADS_DESC = "downloads_desc"
	DOWNLOADS_ASC = "downloads_asc"
	RATING_DESC = "rating_desc"
	RATING_ASC = "rating_asc"
	
	
if __name__ == "__main__":
	#"filter": "tag:plucked tag:fret type:wav"
	try:
		filter = FreeSoundFilter(tag=['fret','plucked'], type="wav", samplerate=44100)
		ac_filter = FreeSoundACFilter(ac_hardness=30)
	except DataError as e:
		print(e)
	
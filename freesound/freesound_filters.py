"""
The module contains the definitions of
- Descriptor
- FreeSoundDescriptors

2 utilitity structures which help users to build `descriptors` queries for the [`FreeSoundClient`][freesound.freesound_client.FreesoundClient] by providing type hints. 
These queries are valid only if the parameter 'fields=analysis' is included in the https request 

Details at:
-----------
https://freesound.org/docs/api/resources_apiv2.html#text-search

Usage Example
-------------
`https://freesound.org/apiv2/search/text/?query=guitar&fields=id%2Cname%2Cdownload%2Ctype%2Ctags&filter=tag%3Ablues+type%3Amp3+tag%3Ascale`

This query contains 2 sound descriptors parameters

`lowlevel.spectral_complexity` and `lowlevel.average_loudness`

You can build this query taking advange of type hints writing:
>>> print(FreeSoundDescriptors([Descriptor.lowlevel_spectral_complexity, Descriptor.lowlevel_average_loudness]).aslist)
lowlevel.spectral_complexity,lowlevel.average_loudness

WARNING
-------
Complex queries such as the followings are not implemented yet

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
# TODO conditional queries

from typing import Any, Unpack

from .freesound_list_maker import ListMaker

from .filter_types import TypeFilter, TypeACFilter
from .freesound_errors import DataError

#"filter": "tag:plucked tag:fret type:wav"
class FreeSoundFilterBase(ListMaker):
	"""The Base class for [`FreeSoundFilter`](.FreeSoundFilter) and [`FreeSoundACFilter`](freesound.freesound_filters.FreeACSoundFilter). Useful for type hints"""
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
		
		super().__init__(self._filters)
		
	@property
	def aslist(self) -> str:
		"""use this property to pass the list of filters to a [`FreeSoundClient`][freesound.freesound_client.FreesoundClient]

		Returns:
			str: a space-separated string of valid filter:value
		"""
		return self._make_list()
	
	@property
	def filters(self) -> list[str]:
		return self._filters
	
class FreeSoundFilters(FreeSoundFilterBase):
	'''A Utility Class that creates a space-separated `string` of `filter:value` calling the method `aslist`

	It makes use of `TypeFilter` (a `TypeDict`) to provide type annotation for valid `filters` to query the [`freesound.org`](https://www.freesound.org) database
	
	The result is a ready formatted string to be used as a `filter` parameter in the [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient].

	For more information visit: <https://freesound.org/docs/api/resources_apiv2.html#text-search>

	Usage:
		```
		>>> print(FreeSoundFilters(tag=['fret','plucked'], type="wav", samplerate=44100).aslist)
		tag:fret tag:plucked type:wav samplerate:44100
		```
	'''
	_parameters_list:dict[str,Any] = TypeFilter.__annotations__
	def __init__(self, **kwargs: Unpack[TypeFilter]) -> None:
		super().__init__(**kwargs)

	def __repr__(self) -> str:
		return f'<FreeSoundFilters {self.filters}'

class FreeSoundACFilters(FreeSoundFilterBase):
	'''A Utility Class that creates a space-separated string of `ac_filter:value` calling the method `aslist`

	The result is a ready formatted string to be used as a `filter` parameter in the [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient].

	For more information visit: <https://freesound.org/docs/api/resources_apiv2.html#text-search>
	Check the audio common project at: http://www.audiocommons.org/

	Usage: 
		```
		>>> print(FreeSoundACFilters(ac_hardness=30).aslist)
		ac_hardness:30
		```
	'''
	_parameters_list:dict[str,Any] = TypeACFilter.__annotations__
	def __init__(self, **kwargs: Unpack[TypeACFilter]) -> None:
		super().__init__(**kwargs)

	def __repr__(self) -> str:
		return f'<FreeSoundACFilters {self.filters}'

class FreeSoundSort():
	"""A Utility Class that outputs a valid string to be used as a `sort` parameter in the [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient].
	Useful for linting

	Usage:
		```
		>>> print(FreeSoundSort.DURATION_DESC)
		duration_desc
		```
	"""
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
	try:
		filter = FreeSoundFilters(tag=['fret','plucked'], type="wav", samplerate=44100)
		ac_filter = FreeSoundACFilters(ac_hardness=30)
		print(filter.aslist)
		print(ac_filter.aslist)
	except DataError as e:
		print(e)
	
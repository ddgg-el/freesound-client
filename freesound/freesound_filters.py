"""
The module contains the definitions of
- FreeSoundFilters
- FreeSoundSort

2 utilitity structures which help users to build list of `filters` queries 
and the `sort` paramete respectevely for the [`FreeSoundClient`][freesound.freesound_client.FreesoundClient] by providing type hints. 

Details at:
-----------
https://freesound.org/docs/api/resources_apiv2.html#request-parameters-text-search-parameters

Usage Example
-------------
`https://freesound.org/apiv2/search/text/?query=piano&fields=id%2Cname%2Csamplerate%2Ctype&page_size=15&sort=score&normalized=0&filter=type%3Awav+samplerate%3A48000`

This query contains 2 sound filters:

`type` and `samplerate`

You can build this query taking advange of type hints writing:
>>> print(FreeSoundFilters(type="wav", samplerate=48000).aslist)
tag:detuned tag:prepared ac_brightness:80 ac_loudness:30

This class allows you to filter queries by AudioCommon features

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

from typing import Unpack

from .freesound_list_maker import ListMaker

from .filter_types import TypeFilter
from .freesound_errors import DataError

#"filter": "tag:plucked tag:fret type:wav"
class FreeSoundFilters(ListMaker):
	'''A Utility Class that creates a space-separated `string` of `filter:value` calling the method `aslist`

	It makes use of `TypeFilter` (a `TypeDict`) to provide type annotation for valid `filters` to query the [`freesound.org`](https://www.freesound.org) database
	The result is a ready formatted string to be used as a `filter` parameter in the [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient] including `ac_filter`

	For more information visit: <https://freesound.org/docs/api/resources_apiv2.html#text-search>
	Check the audio common project at: <http://www.audiocommons.org/>

	Usage:
		```py
		>>> print(FreeSoundFilters(tag=['fret','plucked'], type="wav", samplerate=44100).aslist)
		tag:fret tag:plucked type:wav samplerate:44100
		```
	'''
	def __init__(self, **kwargs:Unpack[TypeFilter]) -> None:
		self._filters:list[str] = []
		for key,values in kwargs.items():
			if key in kwargs:
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
		"""use this property to pass the list of filters to a [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient].

		Returns:
			str: a space-separated string of valid filter:value
		"""
		return self._make_list()
	
	@property
	def filters(self) -> List[str]:
		return self._filters
	
	def __repr__(self) -> str:
		return f'<FreeSoundFilters {self.filters}'


class FreeSoundSort():
	"""A Utility Class that outputs a valid string to be used as a `sort` parameter in the [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient].
	Useful for linting

	Usage:
		```py
		>>> print(FreeSoundSort.DURATION_DESC)
		duration_desc
		```
	"""
	score = "score"
	duration_desc = "duration_desc"
	duration_asc = "duration_asc"
	created_desc = "created_desc"
	created_asc = "created_asc"
	downloads_desc = "downloads_desc"
	downloads_asc = "downloads_asc"
	rating_desc = "rating_desc"
	rating_asc = "rating_asc"
	
	
if __name__ == "__main__":
	try:
		filter = FreeSoundFilters(tag=['fret','plucked'], type="wav", samplerate=44100, ac_brightness=80, ac_loudness=-30)
		print(filter.aslist)
	except DataError as e:
		print(e)
	
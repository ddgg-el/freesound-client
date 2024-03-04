from datetime import date
from typing import Optional, TypedDict, List, Union

class TypeFilter(TypedDict):
	id:Optional[int]
	username:Optional[str]
	created:Optional[date]
	original_filename:Optional[str]
	description:Optional[str]
	tag:Optional[Union[str,List[str]]]
	license:Optional[str]
	is_remix:Optional[bool]
	was_remixed:Optional[bool]
	pack:Optional[str]
	pack_tokenized:Optional[str]
	is_geotagged:Optional[bool]
	type:Optional[str]
	duration:Optional[Union[int,float]]
	bitdepth:Optional[int]
	bitrate:Optional[Union[int,float]]
	samplerate:Optional[int]
	filesize:Optional[int] # in bytes
	channels:Optional[int]
	md5:Optional[str]
	num_downloads:Optional[int]
	avg_rating:Optional[Union[int,float]]
	num_comments:Optional[int]
	# Audio Common
	ac_loudness:Optional[Union[int,float]]
	ac_dynamical_range:Optional[Union[int,float]]
	ac_temporal_centroid:Optional[Union[int,float]]
	ac_log_attack_time:Optional[Union[int,float]]
	ac_single_event:Optional[bool]
	ac_tonality:Optional[str]
	ac_tonality_confidence:Optional[float] # between 0 and 1
	ac_loop:Optional[bool]
	ac_tempo:Optional[int]
	ac_tempo_confidence:Optional[float] # between 0 and 1
	ac_note_midi:Optional[int]
	ac_note_name:Optional[str]
	ac_note_frequency:Optional[Union[int,float]]
	ac_note_confidence:Optional[float] # between 0 and 1
	ac_brightness:Optional[float] # between 0 and 100
	ac_depth:Optional[float] # between 0 and 100
	ac_hardness:Optional[float] # between 0 and 100
	ac_roughness:Optional[float] # between 0 and 100
	ac_boominess:Optional[float] # between 0 and 100
	ac_warmth:Optional[float] # between 0 and 100
	ac_sharpness:Optional[float] # between 0 and 100
	ac_reverb:Optional[bool]

class Filter:
	"""A utility class that allows you to create conditional and range filters
	"""
	@classmethod
	def OR(cls,val1:Any,val2:Any) -> str:
		"""conditional OR

		you should not use this class method outside the `FreeSoundFilters` class parameters.

		Usage:
			```
			>>> FreeSoundFilters(type=Filter.OR('wav','aiff')).aslist
			'type:(wav OR aiff)'
			```
		Args:
			val1 (Any): first value
			val2 (Any): second value

		Returns:
			str: a well-formatted string for the filter url parameter
		"""
		return f"^({val1} OR {val2})"
	@classmethod
	def AND(cls,val1:Any,val2:Any) -> str:
		"""conditional AND

		you should not use this class method outside the `FreeSoundFilters` class parameters.

		Usage:
			```
			>>> FreeSoundFilters(tag=Filter.AND('nature','soundscape')).aslist
			'tag:(nature AND soundscape)'
			```
		Args:
			val1 (Any): first value
			val2 (Any): second value

		Returns:
			str: a well-formatted string for the filter url parameter
		"""
		return f"^({val1} AND {val2})"
	@classmethod
	def RANGE(cls,minimum:Any,maximum:Any) -> str:
		"""range from minimum TO maximum

		you should not use this class method outside the `FreeSoundFilters` class parameters.

		Usage:
			```
			>>> FreeSoundFilters(duration=Filter.RANGE(3,5)).aslist
			'duration:[3 TO 5]'
			```
		Args:
			minimum (Any): range minimum
			maximum (Any): range maximum

		Returns:
			str: a well-formatted string for the filter url parameter
		"""
		if isinstance(minimum,datetime) and isinstance(maximum,datetime):
			minimum = minimum.isoformat()
			maximum = maximum.isoformat()
		return f"^[{minimum} TO {maximum}]"
	@classmethod
	def AT_LEAST(cls, minimum:Any) -> str:
		"""range from a minimum value

		you should not use this class method outside the `FreeSoundFilters` class parameters.

		Usage:
			```
			>>> FreeSoundFilters(duration=Filter.AT_LEAST(3)).aslist
			'duration:[3 TO *]'
			```
		Args:
			minimum (Any): the minimum value

		Returns:
			str: a well-formatted string for the filter url parameter
		"""
		if isinstance(minimum,datetime):
			minimum = minimum.isoformat()
		return f"^[{minimum} TO *]"
	@classmethod
	def UP_TO(cls,maximum:Any) -> str:
		"""range up to a maximum value

		you should not use this class method outside the `FreeSoundFilters` class parameters.

		Usage:
			```
			>>> FreeSoundFilters(duration=Filter.UP_TO(3)).aslist
			'duration:[* TO 3]'
			```
		Args:
			maximum (Any): the maximum value

		Returns:
			str: a well-formatted string for the filter url parameter
		"""
		if isinstance(maximum,datetime):
			maximum = maximum.isoformat()
		return f"^[* TO {maximum}]"
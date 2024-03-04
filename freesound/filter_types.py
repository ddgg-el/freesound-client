from datetime import date, datetime
from typing import Any, TypedDict, NotRequired

class TypeFilter(TypedDict):
	id:NotRequired[int]
	username:NotRequired[str]
	created:NotRequired[date|str]
	original_filename:NotRequired[str]
	description:NotRequired[str]
	tag:NotRequired[str|list[str]]
	license:NotRequired[str]
	is_remix:NotRequired[bool]
	was_remixed:NotRequired[bool]
	pack:NotRequired[str]
	pack_tokenized:NotRequired[str]
	is_geotagged:NotRequired[bool]
	type:NotRequired[str]
	duration:NotRequired[int|float|str]
	bitdepth:NotRequired[int|str]
	bitrate:NotRequired[int|float|str]
	samplerate:NotRequired[int|str]
	filesize:NotRequired[int|str] # in bytes
	channels:NotRequired[int|str]
	md5:NotRequired[str]
	num_downloads:NotRequired[int|str]
	avg_rating:NotRequired[int|float|str]
	num_comments:NotRequired[int|str]
	# Audio Common
	ac_loudness:NotRequired[int|float|str]
	ac_dynamical_range:NotRequired[int|float|str]
	ac_temporal_centroid:NotRequired[int|float|str]
	ac_log_attack_time:NotRequired[int|float|str]
	ac_single_event:NotRequired[bool|str]
	ac_tonality:NotRequired[str|str]
	ac_tonality_confidence:NotRequired[float|str] # between 0 and 1
	ac_loop:NotRequired[bool]
	ac_tempo:NotRequired[int|str]
	ac_tempo_confidence:NotRequired[float|str] # between 0 and 1
	ac_note_midi:NotRequired[int|str]
	ac_note_name:NotRequired[str]
	ac_note_frequency:NotRequired[int|float|str]
	ac_note_confidence:NotRequired[float|str] # between 0 and 1
	ac_brightness:NotRequired[float|str] # between 0 and 100
	ac_depth:NotRequired[float|str] # between 0 and 100
	ac_hardness:NotRequired[float|str] # between 0 and 100
	ac_roughness:NotRequired[float|str] # between 0 and 100
	ac_boominess:NotRequired[float|str] # between 0 and 100
	ac_warmth:NotRequired[float|str] # between 0 and 100
	ac_sharpness:NotRequired[float|str] # between 0 and 100
	ac_reverb:NotRequired[bool]

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
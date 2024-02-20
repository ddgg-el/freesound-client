from datetime import date
from typing import TypedDict, NotRequired

class TypeFilter(TypedDict):
	id:NotRequired[int]
	username:NotRequired[str]
	created:NotRequired[date]
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
	duration:NotRequired[int|float]
	bitdepth:NotRequired[int]
	bitrate:NotRequired[int|float]
	samplerate:NotRequired[int]
	filesize:NotRequired[int] # in bytes
	channels:NotRequired[int]
	md5:NotRequired[str]
	num_downloads:NotRequired[int]
	avg_rating:NotRequired[int|float]
	num_comments:NotRequired[int]

class TypeACFilter(TypedDict):
	ac_loudness:NotRequired[int|float]
	ac_dynamical_range:NotRequired[int|float]
	ac_temporal_centroid:NotRequired[int|float]
	ac_log_attack_time:NotRequired[int|float]
	ac_single_event:NotRequired[bool]
	ac_tonality:NotRequired[str]
	ac_tonality_confidence:NotRequired[float] # between 0 and 1
	ac_loop:NotRequired[bool]
	ac_tempo:NotRequired[int]
	ac_tempo_confidence:NotRequired[float] # between 0 and 1
	ac_note_midi:NotRequired[int]
	ac_note_name:NotRequired[str]
	ac_note_frequency:NotRequired[int|float]
	ac_note_confidence:NotRequired[float] # between 0 and 1
	ac_brightness:NotRequired[float] # between 0 and 100
	ac_depth:NotRequired[float] # between 0 and 100
	ac_hardness:NotRequired[float] # between 0 and 100
	ac_roughness:NotRequired[float] # between 0 and 100
	ac_boominess:NotRequired[float] # between 0 and 100
	ac_warmth:NotRequired[float] # between 0 and 100
	ac_sharpness:NotRequired[float] # between 0 and 100
	ac_reverb:NotRequired[bool]


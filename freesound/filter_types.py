from datetime import date
from typing import List, TypedDict, Union, Optional

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

class TypeACFilter(TypedDict):
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


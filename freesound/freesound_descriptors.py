"""
The module contains the definitions of
- Descriptor
- FreeSoundDescriptors

2 utilitity structures which help users to build `descriptors` queries for the `FreeSoundClient` by providing type hints. 
These queries are valid only if the parameter 'fields=analysis' is included in the https request 

Details at:
-----------
<https://freesound.org/docs/api/analysis_docs.html>

Usage Example
-------------
`https://freesound.org/apiv2/search/text/?query=guitar&fields=id%2Cname%2Canalysis&descriptors=lowlevel.spectral_complexity%2Clowlevel.average_loudness`

This query contains 2 sound descriptors parameters

`lowlevel.spectral_complexity` and `lowlevel.average_loudness`

You can build this query taking advange of type hints writing:
>>> print(FreeSoundDescriptors([Descriptor.lowlevel_spectral_complexity, Descriptor.lowlevel_average_loudness]).aslist)
lowlevel.spectral_complexity,lowlevel.average_loudness
"""

from typing import Any, List

from .freesound_list_maker import ListMaker

class Descriptor():
	"""A list of valid descriptors for FreeSound Analysis
	
	This should not be used outside a [`FreeSoundDescriptors`][freesound.freesound_descriptors.FreeSoundDescriptors]
	
	Usage: 
		```py
		>>> FreeSoundDescriptors([Descriptor.lowlevel.spectral_complexity])
		```
	"""
	# Metadata
	metadata_version = "metadata.version"
	# Low Level
	lowlevel_spectral_complexity = "lowlevel.spectral_complexity"
	lowlevel_silence_rate_20db = "lowlevel.silence_rate_20dB"
	lowlevel_erb_bands = "lowlevel.erb_bands"
	lowlevel_average_loudness = "lowlevel.average_loudness"
	lowlevel_spectral_rms = "lowlevel.spectral_rms"
	lowlevel_spectral_kurtosis = "lowlevel.spectral_kurtosis"
	lowlevel_barkbands_kurtosis = "lowlevel.barkbands_kurtosis"
	lowlevel_scvalleys = "lowlevel.scvalleys"
	lowlevel_spectral_spread = "lowlevel.spectral_spread"
	lowlevel_pitch = "lowlevel.pitch"
	lowlevel_dissonance = "lowlevel.dissonance"
	lowlevel_spectral_energyband_high = "lowlevel.spectral_energyband_high"
	lowlevel_gfcc = "lowlevel.gfcc"
	lowlevel_spectral_flux = "lowlevel.spectral_flux"
	lowlevel_silence_rate_30db = "lowlevel.silence_rate_30dB"
	lowlevel_spectral_contrast = "lowlevel.spectral_contrast"
	lowlevel_spectral_energyband_middle_high = "lowlevel.spectral_energyband_middle_high"
	lowlevel_barkbands_spread = "lowlevel.barkbands_spread"
	lowlevel_spectral_centroid = "lowlevel.spectral_centroid"
	lowlevel_pitch_salience = "lowlevel.pitch_salience"
	lowlevel_silence_rate_60db = "lowlevel.silence_rate_60dB"
	lowlevel_spectral_entropy = "lowlevel.spectral_entropy"
	lowlevel_spectral_rolloff = "lowlevel.spectral_rolloff"
	lowlevel_barkbands = "lowlevel.barkbands"
	lowlevel_spectral_energyband_low = "lowlevel.spectral_energyband_low"
	lowlevel_barkbands_skewness = "lowlevel.barkbands_skewness"
	lowlevel_pitch_instantaneous_confidence = "lowlevel.pitch_instantaneous_confidence"
	lowlevel_spectral_energyband_middle_low = "lowlevel.spectral_energyband_middle_low"
	lowlevel_spectral_strongpeak = "lowlevel.spectral_strongpeak"
	lowlevel_start_frame = "lowlevel.startFrame"
	lowlevel_spectral_decrease = "lowlevel.spectral_decrease"
	lowlevel_stop_frame = "lowlevel.stopFrame"
	lowlevel_mfcc = "lowlevel.mfcc"
	lowlevel_spectral_energy = "lowlevel.spectral_energy"
	lowlevel_spectral_flatness_db = "lowlevel.spectral_flatness_db"
	lowlevel_frequency_bands = "lowlevel.frequency_bands"
	lowlevel_zerocrossingrate = "lowlevel.zerocrossingrate"
	lowlevel_spectral_skewness = "lowlevel.spectral_skewness"
	lowlevel_hfc = "lowlevel.hfc"
	lowlevel_spectral_crest = "lowlevel.spectral_crest"
	# Rhythm
	rhythm_first_peak_bpm = "rhythm.first_peak_bpm"
	rhythm_onset_times = "rhythm.onset_times"
	rhythm_beats_count = "rhythm.beats_count"
	rhythm_beats_loudness = "rhythm.beats_loudness"
	rhythm_first_peak_spread = "rhythm.first_peak_spread"
	rhythm_second_peak_weight = "rhythm.second_peak_weight"
	rhythm_bpm = "rhythm.bpm"
	rhythm_bpm_intervals = "rhythm.bpm_intervals"
	rhythm_onset_count = "rhythm.onset_count"
	rhythm_second_peak_spread = "rhythm.second_peak_spread"
	rhythm_beats_loudness_band_ratio = "rhythm.beats_loudness_band_ratio"
	rhythm_second_peak_bpm = "rhythm.second_peak_bpm"
	rhythm_onset_rate = "rhythm.onset_rate"
	rhythm_beats_position = "rhythm.beats_position"
	rhythm_first_peak_weight = "rhythm.first_peak_weight"
	# Tonal
	tonal_hpcp_entropy = "tonal.hpcp_entropy"
	tonal_chords_scale = "tonal.chords_scale"
	tonal_chords_number_rate = "tonal.chords_number_rate"
	tonal_key_strength = "tonal.key_strength"
	tonal_chords_progression = "tonal.chords_progression"
	tonal_key_scale = "tonal.key_scale"
	tonal_chords_strength = "tonal.chords_strength"
	tonal_key_key = "tonal.key_key"
	tonal_chords_changes_rate = "tonal.chords_changes_rate"
	tonal_chords_count = "tonal.chords_count"
	tonal_hpcp_crest = "tonal.hpcp_crest"
	tonal_chords_histogram = "tonal.chords_histogram"
	tonal_chords_key = "tonal.chords_key"
	tonal_tuning_frequency = "tonal.tuning_frequency"
	tonal_hpcp_peak_count = "tonal.hpcp_peak_count"
	tonal_hpcp = "tonal.hpcp"
	# SFX
	sfx_temporal_decrease = "sfx.temporal_decrease"
	sfx_inharmonicity = "sfx.inharmonicity"
	sfx_pitch_min_to_total = "sfx.pitch_min_to_total"
	sfx_tc_to_total = "sfx.tc_to_total"
	sfx_der_av_after_max = "sfx.der_av_after_max"
	sfx_pitch_max_to_total = "sfx.pitch_max_to_total"
	sfx_temporal_spread = "sfx.temporal_spread"
	sfx_temporal_kurtosis = "sfx.temporal_kurtosis"
	sfx_logattacktime = "sfx.logattacktime"
	sfx_temporal_centroid = "sfx.temporal_centroid"
	sfx_tristimulus = "sfx.tristimulus"
	sfx_max_der_before_max = "sfx.max_der_before_max"
	sfx_strongdecay = "sfx.strongdecay"
	sfx_pitch_centroid = "sfx.pitch_centroid"
	sfx_duration = "sfx.duration"
	sfx_temporal_skewness = "sfx.temporal_skewness"
	sfx_effective_duration = "sfx.effective_duration"
	sfx_max_to_total = "sfx.max_to_total"
	sfx_oddtoevenharmonicenergyratio = "sfx.oddtoevenharmonicenergyratio"
	sfx_pitch_after_max_to_before_max_energy_ratio = "sfx.pitch_after_max_to_before_max_energy_ratio"


class FreeSoundDescriptors(ListMaker):
	"""A Utility Class that creates a coma-separated string from a list of [`Descriptor`][freesound.freesound_descriptors.Descriptor] calling the method `aslist`
	
	The result is a ready formatted `string` to be used in the `descriptors` parameter of the [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient]. 
	Don't forget to use this parameter in combination with the field `analysis`

	Args:
		fields (list[Any]): a `list` of [`Descriptor`][freesound.freesound_descriptors.Descriptor]

	Usage:
		```py
		>>> print(FreeSoundDescriptors([Descriptor.low_level_average_loudness,Descriptor.low_level_mfcc]).aslist)
		lowlevel.average_loudness,lowlevel.mfcc
		```
	"""
	def __init__(self, fields:List[Any]):
		# param_array = [field.value for field in fields]
		super().__init__(fields)
		
	@property
	def aslist(self) -> str:
		"""use this method to pass the list of [`Descriptor`][freesound.freesound_descriptors.Descriptor] to a [`FreeSoundClient`][freesound.freesound_client.FreeSoundClient]

		Returns:
			str: a coma-separated string of valid sound descriptors
		"""
		return self._make_coma_separated()
	

if __name__ == "__main__":
	print(FreeSoundDescriptors([Descriptor.lowlevel_average_loudness]).aslist)
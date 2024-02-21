"""
Details at:
-----------
https://freesound.org/docs/api/analysis_docs.html

EXAMPLE
-------
https://freesound.org/apiv2/search/text/?query=guitar&fields=id%2Cname%2Canalysis&descriptors=lowlevel.spectral_complexity
"""

from enum import Enum
from typing import Any, List

from .freesound_list_maker import ListMaker


class Descriptor(Enum):
    # Metadata
    metadata_version = "metadata.version"
    # Low Level
    low_level_spectral_complexity = "lowlevel.spectral_complexity"
    low_level_silence_rate_20db = "lowlevel.silence_rate_20dB"
    low_level_erb_bands = "lowlevel.erb_bands"
    low_level_average_loudness = "lowlevel.average_loudness"
    low_level_spectral_rms = "lowlevel.spectral_rms"
    low_level_spectral_kurtosis = "lowlevel.spectral_kurtosis"
    low_level_barkbands_kurtosis = "lowlevel.barkbands_kurtosis"
    low_level_scvalleys = "lowlevel.scvalleys"
    low_level_spectral_spread = "lowlevel.spectral_spread"
    low_level_pitch = "lowlevel.pitch"
    low_level_dissonance = "lowlevel.dissonance"
    low_level_spectral_energyband_high = "lowlevel.spectral_energyband_high"
    low_level_gfcc = "lowlevel.gfcc"
    low_level_spectral_flux = "lowlevel.spectral_flux"
    low_level_silence_rate_30db = "lowlevel.silence_rate_30dB"
    low_level_spectral_contrast = "lowlevel.spectral_contrast"
    low_level_spectral_energyband_middle_high = "lowlevel.spectral_energyband_middle_high"
    low_level_barkbands_spread = "lowlevel.barkbands_spread"
    low_level_spectral_centroid = "lowlevel.spectral_centroid"
    low_level_pitch_salience = "lowlevel.pitch_salience"
    low_level_silence_rate_60db = "lowlevel.silence_rate_60dB"
    low_level_spectral_entropy = "lowlevel.spectral_entropy"
    low_level_spectral_rolloff = "lowlevel.spectral_rolloff"
    low_level_barkbands = "lowlevel.barkbands"
    low_level_spectral_energyband_low = "lowlevel.spectral_energyband_low"
    low_level_barkbands_skewness = "lowlevel.barkbands_skewness"
    low_level_pitch_instantaneous_confidence = "lowlevel.pitch_instantaneous_confidence"
    low_level_spectral_energyband_middle_low = "lowlevel.spectral_energyband_middle_low"
    low_level_spectral_strongpeak = "lowlevel.spectral_strongpeak"
    low_level_start_frame = "lowlevel.startFrame"
    low_level_spectral_decrease = "lowlevel.spectral_decrease"
    low_level_stop_frame = "lowlevel.stopFrame"
    low_level_mfcc = "lowlevel.mfcc"
    low_level_spectral_energy = "lowlevel.spectral_energy"
    low_level_spectral_flatness_db = "lowlevel.spectral_flatness_db"
    low_level_frequency_bands = "lowlevel.frequency_bands"
    low_level_zerocrossingrate = "lowlevel.zerocrossingrate"
    low_level_spectral_skewness = "lowlevel.spectral_skewness"
    low_level_hfc = "lowlevel.hfc"
    low_level_spectral_crest = "lowlevel.spectral_crest"
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
	def __init__(self, fields:List[Any]):
		param_array = [field.value for field in fields]
		super().__init__(param_array)
		
	@property
	def aslist(self) -> str:
		return self._make_coma_separated()
	

if __name__ == "__main__":
    print(FreeSoundDescriptors([Descriptor.low_level_average_loudness]).aslist)
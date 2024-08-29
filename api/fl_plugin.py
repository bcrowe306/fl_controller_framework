from dataclasses import dataclass
from fl_controller_framework.api.fl_parameters import PluginParameter, PluginParameterType
from fl_controller_framework.api.fl_channel import channel_types_mapping, ChannelType
import plugins, channels, mixer, general, midi

def make_equal_discrete_regions(*, names) -> list[tuple]:
    """Returns a list of discrete regions as tuples (lower_boundary, name)
    where lower_boundary indicates the start of that region (inclusive)

    Note: Each region will have the same width, except the first and last region which are centered around
          zero and one respectively
    """
    return [
        ((1.0 / (len(names) - 1) / 2) * max(0, index * 2 - 1), name)
        for index, name in enumerate(names)
    ]
def make_discrete_regions_from_midpoints(*, names, midpoints) -> list[tuple]:
    """
    Makes a list of discrete regions as tuples (lower_boundary, name)
    where lower_boundary indicates the start of that region (inclusive)

    Args:
        names: The name of each region in order
        midpoints: The midpoint of each region in order
    """
    lower_boundaries = [midpoints[0]]
    lower_boundaries.extend(
        [
            (midpoints[index - 1] + midpoints[index]) / 2
            for index in range(1, len(midpoints))
        ]
    )
    return [
        (lower_boundary, name) for lower_boundary, name in zip(lower_boundaries, names)
    ]

__all__ = ["native_plugin_parameter_mappings"]

native_parameter_regions = {
    "3x_Osc_osc_shape": make_equal_discrete_regions(
        names=[
            "Sine Wave",
            "Triangle Wave",
            "Square Wave",
            "Saw Wave",
            "Rounded Saw Wave",
            "Noise Wave",
            "Custom Wave",
        ]
    ),
    "Channel_filter_type": make_discrete_regions_from_midpoints(
        names=["Fast LP", "LP", "BP", "HP", "BS", "LPx2", "SVF LP", "SVF LPx2"],
        midpoints=[
            0,
            0.142857142724097,
            0.285714285448194,
            0.42857142817229,
            0.57142857182771,
            0.714285714551806,
            0.857142857275903,
            1,
        ],
    ),
    "Fruity_Squeeze_relation": [
        (0, "None"),
        (0.173, "Preserve"),
        (0.5, "Preserve x2"),
        (0.83, "Preserve /2"),
    ],
}

native_plugin_parameter_mappings = {
    "Sampler": [
        PluginParameter(
            index=2, name="Filter Cutoff", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=3, name="Filter Resonance", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=5,
            name="Filter Type",
            parameter_type=PluginParameterType.Channel,
            discrete_regions=native_parameter_regions["Channel_filter_type"],
        ),
        PluginParameter(
            index=13, name="Sample Start", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=9, name="Gate Time", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=11, name="Time Shift", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=12, name="Swing Mix", parameter_type=PluginParameterType.Channel
        ),
    ],
    "AudioClip": [
        PluginParameter(
            index=19,
            name="Filter Cutoff",
            parameter_type=PluginParameterType.Channel,
            deadzone_centre=0.5,
        ),
        PluginParameter(
            index=20,
            name="Filter Resonance",
            parameter_type=PluginParameterType.Channel,
            deadzone_centre=0.5,
        ),
    ],
    "Layer": [
        PluginParameter(
            index=19,
            name="Filter Cutoff",
            parameter_type=PluginParameterType.Channel,
            deadzone_centre=0.5,
        ),
        PluginParameter(
            index=20,
            name="Filter Resonance",
            parameter_type=PluginParameterType.Channel,
            deadzone_centre=0.5,
        ),
    ],
    "FL Keys": [
        PluginParameter(index=1, name="Release", deadzone_centre=0.5),
        PluginParameter(index=7, name="Stereo", deadzone_centre=0.5),
        PluginParameter(index=14, name="Overdrive"),
        PluginParameter(index=11, name="Treble", deadzone_centre=0.5),
        PluginParameter(index=5, name="Vel > Muffle"),
        PluginParameter(index=4, name="Muffle"),
        PluginParameter(index=3, name="Vel > Hardness", deadzone_centre=0.5),
        PluginParameter(index=2, name="Hardness", deadzone_centre=0.5),
    ],
    "3x Osc": [
        PluginParameter(
            index=1,
            name="Osc 1 Shape",
            discrete_regions=native_parameter_regions["3x_Osc_osc_shape"],
        ),
        PluginParameter(
            index=8,
            name="Osc 2 Shape",
            discrete_regions=native_parameter_regions["3x_Osc_osc_shape"],
        ),
        PluginParameter(
            index=15,
            name="Osc 3 Shape",
            discrete_regions=native_parameter_regions["3x_Osc_osc_shape"],
        ),
        PluginParameter(index=9, name="Osc 2 Coarse"),
        PluginParameter(index=16, name="Osc 3 Coarse"),
        PluginParameter(
            index=2, name="Filter Cutoff", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=3, name="Filter Resonance", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=5,
            name="Filter Type",
            parameter_type=PluginParameterType.Channel,
            discrete_regions=native_parameter_regions["Channel_filter_type"],
        ),
    ],
    "FLEX": [
        PluginParameter(index=10),
        PluginParameter(index=11),
        PluginParameter(index=12),
        PluginParameter(index=13),
        PluginParameter(index=14),
        PluginParameter(index=15),
        PluginParameter(index=16),
        PluginParameter(index=17),
    ],
    "Harmless": [
        PluginParameter(index=31, name="Pluck"),
        PluginParameter(index=79, name="Harmonizer Mix"),
        PluginParameter(index=54, name="Filter Frequency"),
        PluginParameter(index=59, name="Filter Resonance"),
        PluginParameter(index=49, name="Filter Decay"),
        PluginParameter(index=52, name="Env > Filter", deadzone_centre=0.5),
        PluginParameter(index=71, name="Phaser Mix"),
        PluginParameter(index=65, name="Unison"),
    ],
    "Harmor": [
        PluginParameter(index=772, name="Modulation X"),
        PluginParameter(index=773, name="Modulation Y"),
        PluginParameter(index=774, name="Modulation Z"),
        PluginParameter(index=75, name="Pluck Decay Time"),
        PluginParameter(index=76, name="Phaser Mix"),
        PluginParameter(index=27, name="Harmonizer Mix"),
        PluginParameter(index=23, name="Harmonic Blur"),
        PluginParameter(index=52, name="Filter Cutoff"),
    ],
    "PoiZone": [
        PluginParameter(index=18, name="Filter Cutoff"),
        PluginParameter(index=19, name="Filter Resonance"),
        PluginParameter(index=23, name="Amp Decay"),
        PluginParameter(index=12, name="Envelope Decay"),
        PluginParameter(index=10, name="Envelope Amount", deadzone_centre=0.5),
        PluginParameter(index=8, name="Osc Balance"),
        PluginParameter(index=38, name="Delay Wet"),
        PluginParameter(index=42, name="Chorus Wet"),
    ],
    "Sytrus": [
        PluginParameter(index=18, name="Modulation X"),
        PluginParameter(index=19, name="Modulation Y"),
        PluginParameter(index=4, name="Volume Decay", deadzone_centre=0.5),
        PluginParameter(index=8, name="Filter Decay", deadzone_centre=0.5),
        PluginParameter(index=11, name="Unison Order"),
        PluginParameter(index=14, name="Unison Pitch"),
        PluginParameter(index=15, name="Unison Sub Level"),
        PluginParameter(index=1, name="Master LFO Level", deadzone_centre=0.5),
    ],
    "GMS": [
        PluginParameter(index=32, name="Filter Cutoff"),
        PluginParameter(index=33, name="Filter Resonance"),
        PluginParameter(index=40, name="Envelope Attack"),
        PluginParameter(index=41, name="Envelope Decay"),
        PluginParameter(index=42, name="Envelope Amount"),
        PluginParameter(index=45, name="LFO Rate"),
        PluginParameter(index=46, name="LFO Amount"),
        PluginParameter(index=65, name="Modulation"),
    ],
    "MiniSynth": [
        PluginParameter(index=8, name="Filter Frequency"),
        PluginParameter(index=9, name="Filter Peak"),
        PluginParameter(index=5, name="Osc Waveform"),
        PluginParameter(index=6, name="Osc Modifier"),
        PluginParameter(index=20, name="LFO Amount", deadzone_centre=0.5),
        PluginParameter(index=19, name="LFO Rate"),
        PluginParameter(index=18, name="LFO Destination"),
        PluginParameter(index=2, name="Slide Time"),
    ],
    "Sawer": [
        PluginParameter(index=27, name="Filter Cutoff"),
        PluginParameter(index=28, name="Filter Resonance"),
        PluginParameter(index=31, name="Filter Mode"),
        PluginParameter(index=45, name="LFO Amount"),
        PluginParameter(index=39, name="LFO Speed"),
        PluginParameter(index=19, name="Sub-Saw Level"),
        PluginParameter(index=18, name="Sub-Saw Harmonic"),
        PluginParameter(index=11, name="Glide Time"),
    ],
    "Transistor Bass": [
        PluginParameter(index=0, name="Tuning", deadzone_centre=0.5),
        PluginParameter(index=41, name="303 Pulse"),
        PluginParameter(index=1, name="Waveform"),
        PluginParameter(index=2, name="Filter Cutoff"),
        PluginParameter(index=4, name="Filter Resonance"),
        PluginParameter(index=5, name="Envelope Mod"),
        PluginParameter(index=6, name="Decay"),
        PluginParameter(index=7, name="Accent"),
    ],
    "MIDI Out": [
        PluginParameter(index=1),
        PluginParameter(index=2),
        PluginParameter(index=3),
        PluginParameter(index=4),
        PluginParameter(index=5),
        PluginParameter(index=6),
        PluginParameter(index=7),
        PluginParameter(index=8),
    ],
    "Morphine": [
        PluginParameter(index=30, name="Master Attack"),
        PluginParameter(index=31, name="Master Decay"),
        PluginParameter(index=32, name="Master Sustain"),
        PluginParameter(index=33, name="Master Release"),
        PluginParameter(index=17, name="Reverb Decay"),
        PluginParameter(index=19, name="Reverb Mix"),
        PluginParameter(index=52, name="Gen A: Pan Range"),
        PluginParameter(index=6, name="Overdrive"),
    ],
    "Ogun": [
        PluginParameter(index=3, name="Modulation X"),
        PluginParameter(index=4, name="Modulation Y"),
        PluginParameter(index=5, name="Timbre Pre-Decay"),
        PluginParameter(index=6, name="Timbre Decay"),
        PluginParameter(index=7, name="Timbre Release"),
        PluginParameter(index=8, name="Timbre Fullness"),
        PluginParameter(index=15, name="Unison Pitch"),
        PluginParameter(index=40, name="EQ Band 1 Level", deadzone_centre=0.5),
    ],
    "Sakura": [
        PluginParameter(index=2, name="Amp Attack"),
        PluginParameter(index=3, name="Amp Decay"),
        PluginParameter(index=4, name="Amp Sustain"),
        PluginParameter(index=5, name="Amp Release"),
        PluginParameter(index=6, name="String 1: Decay"),
        PluginParameter(index=9, name="String 1: Damp"),
        PluginParameter(index=11, name="String 2: Decay"),
        PluginParameter(index=14, name="String 2: Damp"),
    ],
    "ToxicBiohazard": [
        PluginParameter(index=110, name="Osc 2 > 1 FM"),
        PluginParameter(index=44, name="Osc 2 Freq Shift", deadzone_centre=0.5),
        PluginParameter(index=117, name="Osc 3 > 2 FM"),
        PluginParameter(index=45, name="Osc 3 Freq Shift", deadzone_centre=0.5),
        PluginParameter(index=15, name="Filter Cutoff"),
        PluginParameter(index=16, name="Filter Resonance"),
        PluginParameter(index=3, name="Master Attack"),
        PluginParameter(index=1, name="Distortion"),
    ],
    "SimSynth Live": [
        PluginParameter(index=11, name="Filter Cutoff"),
        PluginParameter(index=12, name="Filter Emphasis"),
        PluginParameter(index=15, name="Filter Highpass"),
        PluginParameter(index=16, name="Filter Bandpass"),
        PluginParameter(index=13, name="Env > Filter", deadzone_centre=0.5),
        PluginParameter(index=22, name="Filter Attack"),
        PluginParameter(index=23, name="Filter Decay"),
        PluginParameter(index=18, name="Amp Env Decay"),
    ],
    "DirectWave": [
        PluginParameter(index=32, name="Amp Env Attack"),
        PluginParameter(index=33, name="Amp Env Decay"),
        PluginParameter(index=34, name="Amp Env Sustain"),
        PluginParameter(index=35, name="Amp Env Release"),
        PluginParameter(index=83, name="Delay Send"),
        PluginParameter(index=84, name="Chorus Send"),
        PluginParameter(index=85, name="Reverb Send"),
        PluginParameter(index=1, name="Glide"),
    ],
    "FPC": [
        PluginParameter(index=256, name="Pad 1 Tune", deadzone_centre=0.5),
        PluginParameter(index=257, name="Pad 2 Tune", deadzone_centre=0.5),
        PluginParameter(index=258, name="Pad 3 Tune", deadzone_centre=0.5),
        PluginParameter(index=259, name="Pad 4 Tune", deadzone_centre=0.5),
        PluginParameter(index=260, name="Pad 5 Tune", deadzone_centre=0.5),
        PluginParameter(index=261, name="Pad 6 Tune", deadzone_centre=0.5),
        PluginParameter(index=262, name="Pad 7 Tune", deadzone_centre=0.5),
        PluginParameter(index=263, name="Pad 8 Tune", deadzone_centre=0.5),
    ],
    "Slicex": [
        PluginParameter(index=6, name="Modulation X"),
        PluginParameter(index=7, name="Modulation Y"),
        PluginParameter(index=5, name="Master Pitch", deadzone_centre=0.5),
        PluginParameter(index=8, name="Filter Env"),
        PluginParameter(index=9, name="Filter Cutoff"),
        PluginParameter(index=10, name="Filter Resonance"),
        PluginParameter(index=20, name="Volume Env Decay"),
        PluginParameter(index=28, name="Filter Env Decay"),
    ],
    "Fruity Slicer": [
        PluginParameter(
            index=2, name="Filter Cutoff", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=3, name="Filter Resonance", parameter_type=PluginParameterType.Channel
        ),
        PluginParameter(
            index=5,
            name="Filter Type",
            parameter_type=PluginParameterType.Channel,
            discrete_regions=native_parameter_regions["Channel_filter_type"],
        ),
    ],
    "BASSDRUM": [
        PluginParameter(index=6, name="Base"),
        PluginParameter(index=7, name="Peak"),
        PluginParameter(index=8, name="Slide Time"),
        PluginParameter(index=4, name="Drive"),
        PluginParameter(index=15, name="Click Amount"),
        PluginParameter(index=21, name="Noise Mix"),
        PluginParameter(index=17, name="Noise Decay"),
        PluginParameter(index=2, name="Duration"),
    ],
    "Fruity DrumSynth Live": [
        PluginParameter(index=460, name="Osc1 Frequency"),
        PluginParameter(index=461, name="Osc1 Sweep Start"),
        PluginParameter(index=462, name="Osc1 Sweep Time"),
        PluginParameter(index=463, name="Osc1 Env Decay"),
        PluginParameter(index=466, name="Osc2 Frequency"),
        PluginParameter(index=467, name="Osc2 Bandwidth"),
        PluginParameter(index=489, name="O1>O2 Ring Mod"),
        PluginParameter(index=469, name="Osc2 Env Decay"),
    ],
    "Drumaxx": [
        PluginParameter(index=0, name="Ch.1: Volume"),
        PluginParameter(index=44, name="Ch.2: Volume"),
        PluginParameter(index=88, name="Ch.3: Volume"),
        PluginParameter(index=132, name="Ch.4: Volume"),
        PluginParameter(index=176, name="Ch.5: Volume"),
        PluginParameter(index=220, name="Ch.6: Volume"),
        PluginParameter(index=264, name="Ch.7: Volume"),
        PluginParameter(index=308, name="Ch.8: Volume"),
    ],
    "Drumpad": [
        PluginParameter(index=3, name="Mallet Decay"),
        PluginParameter(index=5, name="Mallet Noise RP"),
        PluginParameter(index=6, name="Membrane Decay"),
        PluginParameter(index=8, name="Membrane Tension"),
        PluginParameter(index=12, name="Membrane Shape"),
        PluginParameter(index=13, name="Low Frequency"),
        PluginParameter(index=23, name="Mid Decay"),
        PluginParameter(index=29, name="Pitch", deadzone_centre=0.5),
    ],
    "SoundFont Player": [
        PluginParameter(index=5, name="Env 2 Attack"),
        PluginParameter(index=6, name="Env 2 Decay"),
        PluginParameter(index=7, name="Env 2 Sustain"),
        PluginParameter(index=8, name="Env 2 Release"),
        PluginParameter(index=12, name="Filter Cutoff"),
        PluginParameter(index=4, name="Modulation"),
        PluginParameter(index=2, name="Reverb Send"),
        PluginParameter(index=3, name="Chorus Send"),
    ],
    "Fruity Envelope Controller": [
        PluginParameter(index=88, name="Modulation X"),
        PluginParameter(index=89, name="Modulation Y"),
        PluginParameter(index=0, name="Base Level"),
        PluginParameter(index=1, name="Envelope Level"),
        PluginParameter(index=3, name="Attack Scale", deadzone_centre=0.5),
        PluginParameter(index=4, name="Decay Scale", deadzone_centre=0.5),
        PluginParameter(index=5, name="Sustain Offset", deadzone_centre=0.5),
        PluginParameter(index=6, name="Release Scale", deadzone_centre=0.5),
    ],
    "Fruity Keyboard Controller": [
        PluginParameter(index=0, name="Attack Smoothing"),
        PluginParameter(index=1, name="Release Smoothing"),
    ],
    "Fruit kick": [
        PluginParameter(index=0, name="Max Frequency"),
        PluginParameter(index=1, name="Min Frequency"),
        PluginParameter(index=2, name="Frequency Decay"),
        PluginParameter(index=3, name="Amp Decay"),
        PluginParameter(index=4, name="Click"),
        PluginParameter(index=5, name="Distortion"),
    ],
    "BooBass": [
        PluginParameter(index=0, name="Bass"),
        PluginParameter(index=1, name="Mid"),
        PluginParameter(index=2, name="Treble"),
    ],
    "Fruity granulizer": [
        PluginParameter(index=0, name="Grain Attack"),
        PluginParameter(index=1, name="Grain Hold"),
        PluginParameter(index=2, name="Grain Spacing", deadzone_centre=0.558),
        PluginParameter(index=3, name="Wave Spacing", deadzone_centre=0.805),
        PluginParameter(index=7, name="Pan"),
        PluginParameter(index=6, name="Randomness"),
        PluginParameter(index=10, name="Sample Start"),
        PluginParameter(index=9, name="Hold Sound"),
    ],
    "PLUCKED!": [
        PluginParameter(index=0, name="Decay"),
        PluginParameter(index=1, name="Color"),
        PluginParameter(index=2, name="Normalize Decay"),
        PluginParameter(index=3, name="Gate"),
        PluginParameter(index=4, name="Widen"),
    ],
    "BeepMap": [
        PluginParameter(index=0, name="Frequency Range"),
        PluginParameter(index=1, name="Pixel Length"),
        PluginParameter(index=2, name="Scale Type"),
        PluginParameter(index=3, name="Use Blue"),
        PluginParameter(index=4, name="Grainy"),
        PluginParameter(index=5, name="Loop"),
        PluginParameter(index=6, name="Widen (Stereo)"),
    ],
    "Fruity DX10": [
        PluginParameter(index=11, name="Waveform"),
        PluginParameter(index=21, name="Coarse"),
        PluginParameter(index=5, name="Mod 1 Init"),
        PluginParameter(index=6, name="Mod 1 Decay"),
        PluginParameter(index=3, name="Mod 1 Coarse"),
        PluginParameter(index=16, name="Mod 2 Init"),
        PluginParameter(index=17, name="Mod 2 Decay"),
        PluginParameter(index=14, name="Mod 2 Coarse"),
    ],
    "Autogun": [PluginParameter(index=0, name="Master Level")],
    "Kepler": [
        PluginParameter(index=19, name="VCF Cutoff"),
        PluginParameter(index=20, name="VCF Resonance"),
        PluginParameter(index=5, name="LFO Rate"),
        PluginParameter(index=23, name="VCF LFO"),
        PluginParameter(index=22, name="VCF Env"),
        PluginParameter(index=26, name="Attack"),
        PluginParameter(index=27, name="Decay"),
        PluginParameter(index=28, name="Sustain"),
    ],
    "Kepler Exo": [
        PluginParameter(index=37, name="VCF Cutoff"),
        PluginParameter(index=38, name="VCF Resonance"),
        PluginParameter(index=48, name="LFO Rate"),
        PluginParameter(index=45, name="VCF LFO"),
        PluginParameter(index=44, name="VCF Env"),
        PluginParameter(index=61, name="Attack"),
        PluginParameter(index=62, name="Decay"),
        PluginParameter(index=63, name="Sustain"),
    ],
    "Fruity Reeverb 2": [
        PluginParameter(index=0, name="Low Cut"),
        PluginParameter(index=1, name="High Cut"),
        PluginParameter(index=3, name="Room Size"),
        PluginParameter(index=4, name="Diffusion"),
        PluginParameter(index=13, name="Mod Speed"),
        PluginParameter(index=14, name="Mod Depth"),
        PluginParameter(index=10, name="Dry Level"),
        PluginParameter(index=12, name="Wet Level"),
    ],
    "Fruity Filter": [
        PluginParameter(index=0, name="Cutoff Frequency"),
        PluginParameter(index=1, name="Resonance"),
        PluginParameter(index=2, name="Low Pass"),
        PluginParameter(index=3, name="Band Pass"),
        PluginParameter(index=4, name="High Pass"),
        PluginParameter(index=5, name="X2"),
    ],
    "Fruity Blood Overdrive": [
        PluginParameter(index=0, name="Pre Band"),
        PluginParameter(index=1, name="Color"),
        PluginParameter(index=2, name="Pre Amp"),
        PluginParameter(index=3, name="x100"),
        PluginParameter(index=4, name="Post filter"),
        PluginParameter(index=5, name="Post gain"),
    ],
    "Fruity Delay 2": [
        PluginParameter(index=0, name="Input Panning", deadzone_centre=0.5),
        PluginParameter(index=1, name="Input Volume"),
        PluginParameter(index=6, name="Feedback Mode"),
        PluginParameter(index=3, name="Feedback Level"),
        PluginParameter(index=7, name="Feedback Cutoff"),
        PluginParameter(index=4, name="Time"),
        PluginParameter(index=5, name="Time Stereo Offset"),
        PluginParameter(index=2, name="Dry Level"),
    ],
    "Fruity Fast Dist": [
        PluginParameter(index=0, name="Pre Gain"),
        PluginParameter(index=1, name="Threshold"),
        PluginParameter(index=2, name="Type"),
        PluginParameter(index=3, name="Mix"),
        PluginParameter(index=4, name="Post Gain"),
    ],
    "Fruity Compressor": [
        PluginParameter(index=0, name="Threshold"),
        PluginParameter(index=1, name="Ratio"),
        PluginParameter(index=2, name="Gain"),
        PluginParameter(index=3, name="Attack"),
        PluginParameter(index=4, name="Release"),
        PluginParameter(index=5, name="Type"),
    ],
    "Fruity Convolver": [
        PluginParameter(index=0, name="Dry Level"),
        PluginParameter(index=1, name="Wet Level"),
        PluginParameter(index=2, name="Dry Stereo Separation"),
        PluginParameter(index=3, name="Wet Stereo Separation"),
    ],
    "Fruity Delay 3": [
        PluginParameter(index=0, name="Input"),
        PluginParameter(index=4, name="Delay Time"),
        PluginParameter(index=1, name="Delay Model"),
        PluginParameter(index=14, name="Feedback Level", deadzone_centre=0.8),
        PluginParameter(index=16, name="Feedback Cutoff"),
        PluginParameter(index=15, name="Filter Type"),
        PluginParameter(index=11, name="Diffusion Level"),
        PluginParameter(index=18, name="Distortion Level"),
    ],
    "Fruity delay bank": [
        PluginParameter(index=0, name="Dry Level"),
        PluginParameter(index=1, name="Wet Level"),
        PluginParameter(index=2, name="Input"),
        PluginParameter(index=3, name="Feedback"),
        PluginParameter(index=12, name="Delay 1 Time"),
        PluginParameter(index=28, name="Delay 2 TIme"),
        PluginParameter(index=48, name="Delay 3 Time"),
        PluginParameter(index=60, name="Delay 4 Time"),
    ],
    "LuxeVerb": [
        PluginParameter(index=0, name="Wet Gain"),
        PluginParameter(index=4, name="Decay"),
        PluginParameter(index=7, name="Brightness"),
        PluginParameter(index=9, name="Size"),
        PluginParameter(index=12, name="Diffusion"),
        PluginParameter(index=8, name="Character"),
        PluginParameter(index=34, name="Peak Freq"),
        PluginParameter(index=35, name="Peak Gain"),
    ],
    "Distructor": [
        PluginParameter(index=37, name="Mix Level (1)"),
        PluginParameter(index=38, name="Output Level (1)"),
        PluginParameter(index=86, name="Mix Level (2)"),
        PluginParameter(index=87, name="Output Level (2)"),
        PluginParameter(index=135, name="Mix Level (3)"),
        PluginParameter(index=136, name="Output Level (3)"),
        PluginParameter(index=184, name="Mix Level (4)"),
        PluginParameter(index=185, name="Output Level (4)"),
    ],
    "Multiband Delay": [
        PluginParameter(index=384, name="Delay Scale"),
        PluginParameter(index=386, name="Delay Feedback"),
        PluginParameter(index=387, name="Smoothing Time"),
        PluginParameter(index=389, name="Keep Pitch"),
        PluginParameter(index=390, name="Morph"),
        PluginParameter(index=395, name="Wet Sat Type"),
        PluginParameter(index=394, name="High Pass"),
        PluginParameter(index=391, name="Wet/Dry", deadzone_centre=0.5),
    ],
    "Fruity soft clipper": [
        PluginParameter(index=0, name="Threshold"),
        PluginParameter(index=1, name="Gain", deadzone_centre=0.5),
    ],
    "Fruity Squeeze": [
        PluginParameter(index=2, name="Steps Amount"),
        PluginParameter(index=6, name="Filter Cutoff"),
        PluginParameter(index=5, name="Filter Resonance"),
        PluginParameter(index=0, name="Gain", deadzone_centre=0.5),
        PluginParameter(index=10, name="Preserve"),
        PluginParameter(index=9, name="Impact"),
        PluginParameter(
            index=8,
            name="Relation",
            discrete_regions=native_parameter_regions["Fruity_Squeeze_relation"],
        ),
        PluginParameter(index=11, name="Amount"),
    ],
    "Fruity WaveShaper": [
        PluginParameter(index=0, name="Pre"),
        PluginParameter(index=1, name="Mix", deadzone_centre=0.5),
        PluginParameter(index=2, name="Post"),
    ],
    "Hardcore": [
        PluginParameter(index=3, name="EQ Band 125"),
        PluginParameter(index=4, name="EQ Band 250"),
        PluginParameter(index=5, name="EQ Band 500"),
        PluginParameter(index=6, name="EQ Band 1k"),
        PluginParameter(index=7, name="EQ Band 2k"),
        PluginParameter(index=8, name="EQ Band 4k"),
        PluginParameter(index=9, name="EQ Band 8k"),
        PluginParameter(index=10, name="EQ Band 16k"),
    ],
    "Fruity Limiter": [
        PluginParameter(index=0, name="Gain", deadzone_centre=0.5),
        PluginParameter(index=1, name="Saturation"),
        PluginParameter(index=2, name="Limiter Ceiling", deadzone_centre=0.5),
        PluginParameter(index=3, name="Limiter Attack"),
        PluginParameter(index=5, name="Limiter Release"),
        PluginParameter(index=7, name="Limiter Sustain"),
        PluginParameter(index=15, name="Noise Gain"),
        PluginParameter(index=16, name="Noise Threshold"),
    ],
    "Fruity Multiband Compressor": [
        PluginParameter(index=0, name="Gain", deadzone_centre=0.5),
        PluginParameter(index=23, name="Low Threshold"),
        PluginParameter(index=22, name="Low Gain", deadzone_centre=0.5),
        PluginParameter(index=15, name="Medium Threshold"),
        PluginParameter(index=14, name="Medium Gain", deadzone_centre=0.5),
        PluginParameter(index=6, name="High Threshold"),
        PluginParameter(index=5, name="High Gain", deadzone_centre=0.5),
    ],
    "Maximus": [
        PluginParameter(index=47, name="Master Pre", deadzone_centre=0.5),
        PluginParameter(index=48, name="Master Post", deadzone_centre=0.5),
        PluginParameter(index=50, name="Master Threshold", deadzone_centre=0.5),
        PluginParameter(index=51, name="Ceiling", deadzone_centre=0.5),
        PluginParameter(index=5, name="LMH Mix", deadzone_centre=0.5),
        PluginParameter(index=0, name="Low Frequency"),
        PluginParameter(index=2, name="High Frequency"),
        PluginParameter(index=6, name="Low Cut"),
    ],
    "Transient Processor": [
        PluginParameter(index=6, name="Split Freq"),
        PluginParameter(index=0, name="Attack"),
        PluginParameter(index=1, name="Drive"),
        PluginParameter(index=7, name="Split Balance"),
        PluginParameter(index=2, name="Release"),
        PluginParameter(index=3, name="Gain", deadzone_centre=0.5),
        PluginParameter(index=4, name="Attack Shape"),
        PluginParameter(index=5, name="Release Shape"),
    ],
    "EQUO": [
        PluginParameter(index=0, name="Shift"),
        PluginParameter(index=1, name="Mix"),
        PluginParameter(index=2, name="Morph"),
        PluginParameter(index=3, name="Smooth"),
        PluginParameter(index=4, name="Volume"),
    ],
    "Frequency Splitter": [
        PluginParameter(index=0, name="Low/Mid Freq", deadzone_centre=0.5),
        PluginParameter(index=1, name="Mid/High Freq", deadzone_centre=0.5),
        PluginParameter(index=11, name="Low Out", deadzone_centre=0.5),
        PluginParameter(index=12, name="Mid Out", deadzone_centre=0.5),
        PluginParameter(index=13, name="High Out", deadzone_centre=0.5),
        PluginParameter(index=8, name="Low", deadzone_centre=0.5),
        PluginParameter(index=9, name="Mid", deadzone_centre=0.5),
        PluginParameter(index=10, name="High", deadzone_centre=0.5),
    ],
    "Fruity Love Philter": [
        PluginParameter(index=6, name="Modulation X"),
        PluginParameter(index=7, name="Modulation Y"),
        PluginParameter(index=0, name="Master Level"),
        PluginParameter(index=1, name="Master LFO"),
        PluginParameter(index=2, name="EF Level"),
        PluginParameter(index=3, name="EF Attack"),
        PluginParameter(index=4, name="EF Release"),
    ],
    "Fruity Parametric EQ": [
        PluginParameter(index=0, name="Band 1 Level", deadzone_centre=0.5),
        PluginParameter(index=7, name="Band 1 Freq"),
        PluginParameter(index=2, name="Band 3 Level", deadzone_centre=0.5),
        PluginParameter(index=9, name="Band 3 Freq"),
        PluginParameter(index=4, name="Band 5 Level", deadzone_centre=0.5),
        PluginParameter(index=11, name="Band 5 Freq"),
        PluginParameter(index=6, name="Band 7 Level", deadzone_centre=0.5),
        PluginParameter(index=13, name="Band 7 Freq"),
    ],
    "Fruity Parametric EQ 2": [
        PluginParameter(index=0, name="Band 1 Level", deadzone_centre=0.5),
        PluginParameter(index=7, name="Band 1 Freq"),
        PluginParameter(index=2, name="Band 3 Level", deadzone_centre=0.5),
        PluginParameter(index=9, name="Band 3 Freq"),
        PluginParameter(index=4, name="Band 5 Level", deadzone_centre=0.5),
        PluginParameter(index=11, name="Band 5 Freq"),
        PluginParameter(index=6, name="Band 7 Level", deadzone_centre=0.5),
        PluginParameter(index=13, name="Band 7 Freq"),
    ],
    "Fruity Chorus": [
        PluginParameter(index=0, name="Delay"),
        PluginParameter(index=1, name="Depth"),
        PluginParameter(index=2, name="Stereo"),
        PluginParameter(index=3, name="LFO 1 Freq"),
        PluginParameter(index=4, name="LFO 2 Freq"),
        PluginParameter(index=5, name="LFO 3 Freq"),
        PluginParameter(index=10, name="Cross Cutoff"),
        PluginParameter(index=11, name="Wet Only"),
    ],
    "Fruity Flanger": [
        PluginParameter(index=0, name="Delay"),
        PluginParameter(index=1, name="Depth"),
        PluginParameter(index=2, name="Rate"),
        PluginParameter(index=3, name="Phase"),
        PluginParameter(index=6, name="Feed"),
        PluginParameter(index=9, name="Dry"),
        PluginParameter(index=10, name="Wet"),
        PluginParameter(index=11, name="Cross"),
    ],
    "Fruity Flangus": [
        PluginParameter(index=0, name="Order"),
        PluginParameter(index=1, name="Depth"),
        PluginParameter(index=2, name="Speed"),
        PluginParameter(index=3, name="Delay"),
        PluginParameter(index=4, name="Spread"),
        PluginParameter(index=5, name="Cross"),
        PluginParameter(index=6, name="Dry"),
        PluginParameter(index=7, name="Wet"),
    ],
    "Fruity Phaser": [
        PluginParameter(index=0, name="Sweep Freq"),
        PluginParameter(index=1, name="Min Depth"),
        PluginParameter(index=2, name="Max Depth"),
        PluginParameter(index=3, name="Freq Range"),
        PluginParameter(index=4, name="Stereo"),
        PluginParameter(index=6, name="Feedback"),
        PluginParameter(index=7, name="Dry-Wet", deadzone_centre=0.5),
        PluginParameter(index=8, name="Out Gain", deadzone_centre=0.5),
    ],
    "Vintage Chorus": [
        PluginParameter(index=5, name="Time 1"),
        PluginParameter(index=6, name="Time 2"),
        PluginParameter(index=10, name="Feedback"),
        PluginParameter(index=11, name="Hi Pass"),
        PluginParameter(index=2, name="Mod Speed"),
        PluginParameter(index=13, name="Noise"),
        PluginParameter(index=12, name="Gain"),
        PluginParameter(index=7, name="Mix", deadzone_centre=0.5),
    ],
    "Vintage Phaser": [
        PluginParameter(index=0, name="Min Freq"),
        PluginParameter(index=1, name="Max Freq"),
        PluginParameter(index=2, name="Feedback"),
        PluginParameter(index=6, name="Speed"),
        PluginParameter(index=14, name="Delay Mix", deadzone_centre=0.5),
        PluginParameter(index=16, name="Delay Time"),
        PluginParameter(index=23, name="Noise"),
        PluginParameter(index=21, name="Mix", deadzone_centre=0.5),
    ],
    "Fruity Balance": [
        PluginParameter(index=0, name="Balance", deadzone_centre=0.5),
        PluginParameter(index=1, name="Volume", deadzone_centre=0.8),
    ],
    "Fruity PanOMatic": [
        PluginParameter(index=0, name="Pan", deadzone_centre=0.5),
        PluginParameter(index=1, name="Volume"),
        PluginParameter(index=4, name="Amount", deadzone_centre=0.5),
        PluginParameter(index=5, name="Speed"),
        PluginParameter(index=2, name="LFO Shape"),
        PluginParameter(index=3, name="LFO Target"),
    ],
    "Fruity Send": [
        PluginParameter(index=2, name="Dry"),
        PluginParameter(index=0, name="Pan", deadzone_centre=0.5),
        PluginParameter(index=1, name="Volume"),
    ],
    "Fruity Stereo Enhancer": [
        PluginParameter(index=2, name="Stereo Sep", deadzone_centre=0.5),
        PluginParameter(index=3, name="Phase Offset", deadzone_centre=0.5),
        PluginParameter(index=4, name="Phase Position"),
        PluginParameter(index=5, name="Phase Inversion"),
        PluginParameter(index=0, name="Pan", deadzone_centre=0.5),
        PluginParameter(index=1, name="Volume"),
    ],
    "Fruity Stereo Shaper": [
        PluginParameter(index=0, name="R into L Vol", deadzone_centre=0.5),
        PluginParameter(index=1, name="Left Vol", deadzone_centre=0.5),
        PluginParameter(index=2, name="Right Vol", deadzone_centre=0.5),
        PluginParameter(index=3, name="L into R Vol", deadzone_centre=0.5),
        PluginParameter(index=4, name="L/R Delay", deadzone_centre=0.5),
        PluginParameter(index=5, name="L/R Phase", deadzone_centre=0.5),
    ],
    "Effector": [
        PluginParameter(
            index=3, name="Param X", deadzone_centre=0.5, deadzone_width=0.05
        ),
        PluginParameter(
            index=4, name="Param Y", deadzone_centre=0.5, deadzone_width=0.05
        ),
        PluginParameter(index=2, name="Dry/Wet", deadzone_centre=0.5),
        PluginParameter(index=7, name="Mod Amount X", deadzone_centre=0.5),
        PluginParameter(index=8, name="Mod Amount Y", deadzone_centre=0.5),
        PluginParameter(index=5, name="Mod Rate"),
        PluginParameter(index=9, name="Mod Shape"),
        PluginParameter(index=6, name="Tempo", deadzone_centre=0.5),
    ],
    "Frequency Shifter": [
        PluginParameter(index=2, name="Frequency", deadzone_centre=0.5),
        PluginParameter(index=4, name="Left Shape", deadzone_centre=0.5),
        PluginParameter(index=5, name="Right Shape", deadzone_centre=0.5),
        PluginParameter(index=9, name="Start Phase", deadzone_centre=0.5),
        PluginParameter(index=3, name="L/R Phase"),
        PluginParameter(index=6, name="Feedback", deadzone_centre=0.5),
        PluginParameter(index=0, name="Mix", deadzone_centre=0.5),
        PluginParameter(index=7, name="Stereo"),
    ],
    "Fruity Scratcher": [
        PluginParameter(index=0, name="Wave Position"),
        PluginParameter(index=4, name="Pan", deadzone_centre=0.5),
        PluginParameter(index=5, name="Volume"),
        PluginParameter(index=2, name="Speed"),
        PluginParameter(index=3, name="Acceleration"),
        PluginParameter(index=7, name="Sensitivity"),
    ],
    "Fruity Vocoder": [
        PluginParameter(index=4, name="Formant"),
        PluginParameter(index=0, name="Min"),
        PluginParameter(index=1, name="Max"),
        PluginParameter(index=6, name="Attack"),
        PluginParameter(index=7, name="Release"),
        PluginParameter(index=9, name="Modulation Level"),
        PluginParameter(index=10, name="Carrier Level"),
        PluginParameter(index=11, name="Wet Level"),
    ],
    "Pitch Shifter": [
        PluginParameter(index=0, name="Pitch", deadzone_centre=0.5),
        PluginParameter(index=4, name="Duration"),
        PluginParameter(index=5, name="Density"),
        PluginParameter(index=6, name="Jitter"),
        PluginParameter(index=7, name="Random"),
        PluginParameter(index=8, name="Delay"),
        PluginParameter(index=9, name="Feedback"),
        PluginParameter(index=3, name="Mix"),
    ],
    "Pitcher": [
        PluginParameter(index=0, name="Speed"),
        PluginParameter(index=3, name="Fine Tune"),
    ],
    "Hyper Chorus": [
        PluginParameter(index=0, name="Delay"),
        PluginParameter(index=1, name="Feedback"),
        PluginParameter(index=3, name="Mod Rate"),
        PluginParameter(index=2, name="Modulation"),
        PluginParameter(index=8, name="High Pass"),
        PluginParameter(index=7, name="Low Pass"),
        PluginParameter(index=10, name="LFO Phase Dif"),
        PluginParameter(index=9, name="Mix", deadzone_centre=0.5),
    ],
    "Spreader": [
        PluginParameter(index=0, name="Spread", deadzone_centre=0.5),
        PluginParameter(index=1, name="Separation", deadzone_centre=0.5),
        PluginParameter(index=2, name="Low Bypass"),
    ],
    "LowLifter": [
        PluginParameter(index=6, name="Pre-Gain"),
        PluginParameter(index=3, name="Slope"),
        PluginParameter(index=8, name="Depth"),
        PluginParameter(index=7, name="Mix", deadzone_centre=0.5),
        PluginParameter(index=2, name="Low Gain", deadzone_centre=0.5),
        PluginParameter(index=10, name="Crossover Cutoff"),
        PluginParameter(index=9, name="High Gain", deadzone_centre=0.5),
        PluginParameter(index=1, name="Dry/Wet", deadzone_centre=0.5),
    ],
}


@dataclass
class FLPlugin:
    is_valid: bool
    channel_index: int
    slot_index: int
    name: str
    parameters: list[PluginParameter]

    @staticmethod
    def from_selected_channel(slot_index: int = -1) -> "FLPlugin":
        channel_index = channels.selectedChannel()
        return FLPlugin.get_plugin(channel_index, slot_index)

    @staticmethod
    def get_plugin(channel_index: int, slot_index: int = -1) -> "FLPlugin":
        new_plugin = FLPlugin(
            is_valid=plugins.isValid(channel_index, slot_index),
            channel_index=channel_index,
            slot_index=slot_index,
            name=FLPlugin.get_plugin_name_for_channel(channel_index),
            parameters=[],
        )
        plug_params = native_plugin_parameter_mappings.get(new_plugin.name, None)
        new_plugin.parameters = plug_params if plug_params else []
        new_plugin.update_params()
        return new_plugin

    def update(self, channel_index:int, slot_index: int = -1) -> None:
        self.channel_index = channel_index
        self.slot_index = slot_index
        self.name = FLPlugin.get_plugin_name_for_channel(channel_index)
        plug_params = native_plugin_parameter_mappings.get(self.name, None)
        self.parameters = plug_params if plug_params else []
        self.update_params()

    def update_from_selected(self) -> None:
        self.update(channels.selectedChannel())

    def update_params(self) -> None:
        for param in self.parameters:
            param.value = self.get_parameter_value(param)

    @staticmethod
    def get_plugin_name_for_channel(group_channel) -> str:
        channel_type = channel_types_mapping[channels.getChannelType(group_channel)]
        if channel_type == ChannelType.Sampler:
            return "Sampler"
        if channel_type == ChannelType.AudioClip:
            return "AudioClip"
        if channel_type == ChannelType.Layer:
            return "Layer"
        if channel_type == ChannelType.GenPlug and plugins.isValid(group_channel):
            return plugins.getPluginName(group_channel)

        return None
    
    def __str__(self) -> str:
        return f"FLPlugin: {self.name}, ({self.channel_index}, {self.slot_index})"

    def __repr__(self) -> str:
        return self.__str__()

    def get_parameter_value(self, parameter: PluginParameter) -> float:
        if parameter.parameter_type == PluginParameterType.Channel:
            rec_event_parameter = parameter.index + channels.getRecEventId(
            channels.selectedChannel()
            )
            mask = midi.REC_GetValue
            # return general.processRECEvent(rec_event_parameter, 0, mask)
            return 0
        
        elif parameter.parameter_type == PluginParameterType.Plugin:
            return plugins.getParamValue(parameter.index, *self.get_selected_plugin_position())

    def get_parameter_value_as_string(self, parameter_index: int) -> str:
        return plugins.getParamValueString(
            parameter_index, *self.get_selected_plugin_position()
        )

    def get_selected_plugin_position(self):
        active_effect_index = mixer.getActiveEffectIndex()
        if active_effect_index is not None:
            return active_effect_index

        return self.channel_index, self.slot_index

    def set_sampler_parameter_value(self, parameter, value):
        rec_event_parameter = parameter + channels.getRecEventId(
            channels.selectedChannel()
        )
        value = int(value * midi.FromMIDI_Max)
        mask = midi.REC_MIDIController
        general.processRECEvent(rec_event_parameter, value, mask)

    def set_parameter_value(self, parameter: PluginParameter, value: float) -> None:
        if parameter.parameter_type == PluginParameterType.Channel:
            self.set_sampler_parameter_value(parameter.index, value)
        elif parameter.parameter_type == PluginParameterType.Plugin:
            plugins.setParamValue(
                value,
                parameter.index,
                *self.get_selected_plugin_position(),
                2,
            )
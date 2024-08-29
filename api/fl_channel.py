from dataclasses import dataclass
import channels
from fl_controller_framework.util.colors import BGRIntToRGB
from fl_controller_framework.api.fl_parameters import PluginParameter
# CT_Sampler	0	Internal sampler
# CT_Hybrid	1	generator plugin feeding internal sampler
# CT_GenPlug	2	generator plugin
# CT_Layer	3	Layer
# CT_AudioClip	4	Audio clip
# CT_AutoClip	5	Automation clip
class ChannelType:
    Sampler = 0
    Hybrid = 1
    GenPlug = 2
    Layer = 3
    AudioClip = 4
    AutoClip = 5
channel_types_mapping = {
    0: ChannelType.Sampler,
    1: ChannelType.Hybrid,
    2: ChannelType.GenPlug,
    3: ChannelType.Layer,
    4: ChannelType.AudioClip,
    5: ChannelType.AutoClip
}
@dataclass
class FLChannel:

    index: int
    name: str
    color: tuple[int, int, int]
    volume: float
    pan: float
    mute: bool
    solo: bool
    targetFxTrack: int
    midiInPort:int
    type: str
    pitch: float

    def __post_init__(self):
        self.parameters = [
            PluginParameter(index=0, name="Volume", value=self.volume),
            PluginParameter(index=1, name="Pan", value=self.pan),
            PluginParameter(index=2, name="Pitch", value=self.pitch),
        ]

    def get_selected(self):
        self.index = channels.selectedChannel()
        self.name = channels.getChannelName(self.index)
        self.color = BGRIntToRGB(channels.getChannelColor(self.index))
        self.volume = channels.getChannelVolume(self.index)
        self.pan = channels.getChannelPan(self.index)
        self.mute = channels.isChannelMuted(self.index)
        self.solo = channels.isChannelSolo(self.index)
        self.targetFxTrack = channels.getTargetFxTrack(self.index)
        self.midiInPort = channels.getChannelMidiInPort(self.index)
        self.type = channel_types_mapping[channels.getChannelType(self.index)]
        self.pitch = channels.getChannelPitch(self.index)

    def update(self, index):
        self.index = index
        self.name = channels.getChannelName(self.index)
        self.color = BGRIntToRGB(channels.getChannelColor(self.index))
        self.volume = channels.getChannelVolume(self.index)
        self.pan = channels.getChannelPan(self.index)
        self.mute = channels.isChannelMuted(self.index)
        self.solo = channels.isChannelSolo(self.index)
        self.targetFxTrack = channels.getTargetFxTrack(self.index)
        self.midiInPort = channels.getChannelMidiInPort(self.index)
        self.type = channel_types_mapping[channels.getChannelType(self.index)]
        self.pitch = channels.getChannelPitch(self.index)

    @staticmethod
    def from_selected():
        index: int = channels.selectedChannel()
        return FLChannel(
            index=index,
            name=channels.getChannelName(index),
            color=channels.getChannelColor(index),
            volume=channels.getChannelVolume(index),
            pan=channels.getChannelPan(index),
            mute=channels.isChannelMuted(index),
            solo=channels.isChannelSolo(index),
            targetFxTrack=channels.getTargetFxTrack(index),
            midiInPort=channels.getChannelMidiInPort(index),
            type=channel_types_mapping[channels.getChannelType(index)],
            pitch=channels.getChannelPitch(index)
        )
    
    def set_parameter(self, index: int, value: float) -> None:
        params = [
            self.set_volume,
            self.set_pan,
            self.set_pitch,
        ]
        if index < len(params) and index >= 0:
            set_param_func = params[index]
            set_param_func(value)
            
    def get_parameters(self):
        return [
            PluginParameter(index=0, name="Volume", value=self.volume),
            PluginParameter(index=1, name="Pan", value=self.pan),
            PluginParameter(index=2, name="Pitch", value=self.pitch),
        ]
    def set_volume(self, value: float) -> None:
        channels.setChannelVolume(self.index, value)

    def set_pan(self, value: float) -> None:
        channels.setChannelPan(self.index, value)

    def set_pitch(self, value: float) -> None:
        channels.setChannelPitch(self.index, value)
from dataclasses import dataclass
import channels
from fl_controller_framework.util.colors import BGRIntToRGB
# CT_Sampler	0	Internal sampler
# CT_Hybrid	1	generator plugin feeding internal sampler
# CT_GenPlug	2	generator plugin
# CT_Layer	3	Layer
# CT_AudioClip	4	Audio clip
# CT_AutoClip	5	Automation clip
fl_channel_types = {
    0: "Sampler",
    1: "Hybrid",
    2: "GenPlug",
    3: "Layer",
    4: "AudioClip",
    5: "AutoClip"
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
        self.type = fl_channel_types[channels.getChannelType(self.index)]
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
        self.type = fl_channel_types[channels.getChannelType(self.index)]
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
            type=fl_channel_types[channels.getChannelType(index)],
            pitch=channels.getChannelPitch(index)
        )

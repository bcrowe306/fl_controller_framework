__pdoc__ = {
    "playlist": False,
    "channels" : False, 
    "transport" : False, 
    "mixer": False, 
    "patterns": False, 
    "arrangement": False, 
    "ui": False, 
    "plugins": False, 
    "general": False, 
    "midi": False, 
    "device": False
}
import playlist, channels, transport, mixer, patterns, arrangement, ui, plugins, general, midi, device
from dataclasses import dataclass
from .util.colors import BGRIntToRGB

class _fl:
    """Class that hold a reference too all FL Studio modules."""
    playlist = playlist
    channels = channels
    transport = transport
    mixer = mixer
    patterns = patterns
    arrangement = arrangement
    ui = ui
    plugins = plugins
    general = general
    midi = midi
    device = device

class flMidiMsg:
    """Class the represents the midimsg that is sent by FL Studio OnMidiMsg"""
    handled:bool
    status:int
    data1:int
    data2:int
    port:int
    note:int
    velocity:int
    pressure:int
    progNum:int
    controlNum:int
    controlVal:int
    pitchBend:int
    sysex:bytes
    isIncrement:bool
    res:float
    inEv:int
    outEv:int
    midiId:int
    midiChan:int
    midiChanEx:int
    pmeFlags:int


@dataclass
class FLChannel:
    index: int
    name: str
    color: tuple[int, int, int]
    volume: float
    pan: float
    mute: bool
    solo: bool

    def get_selected(self):
        self.index = channels.selectedChannel()
        self.name = channels.getChannelName(self.index)
        self.color = BGRIntToRGB(channels.getChannelColor(self.index))
        self.volume = channels.getChannelVolume(self.index)
        self.pan = channels.getChannelPan(self.index)
        self.mute = channels.isChannelMuted(self.index)
        self.solo = channels.isChannelSolo(self.index)

    def update(self, index):
        self.index = index
        self.name = channels.getChannelName(self.index)
        self.color = BGRIntToRGB(channels.getChannelColor(self.index))
        self.volume = channels.getChannelVolume(self.index)
        self.pan = channels.getChannelPan(self.index)
        self.mute = channels.isChannelMuted(self.index)
        self.solo = channels.isChannelSolo(self.index)

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
            solo=channels.isChannelSolo(index)
        )


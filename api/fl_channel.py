from dataclasses import dataclass
import channels
from fl_controller_framework.util.colors import BGRIntToRGB

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
            solo=channels.isChannelSolo(index),
        )

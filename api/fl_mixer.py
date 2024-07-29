from dataclasses import dataclass
import mixer, utils
from fl_controller_framework.util.colors import ColorToRGB, BGRIntToRGB, RGBToColor
from fl_controller_framework.util.functions import limit_range


@dataclass
class FLMixerTrack:
    index: int
    name: str
    color: tuple[int, int, int]
    volume: float
    pan: float
    muted: bool
    soloed: bool

    def set_name(self, name: str) -> None:
        mixer.setTrackName(self.index, name)

    def set_volume(self, volume: float) -> None:
        self.volume = volume
        mixer.setTrackVolume(self.index, volume)

    def get_volume_as_db(self) -> float:
        return round(mixer.getTrackVolume(self.index, 1),2)
    
    def jog_volume(self, direction: int) -> None:
        current_volume = self.volume
        delta: float = 0.025
        if direction > 0:
            if self.volume < 1.0:
                current_volume = self.volume + delta
        elif direction < 0:
            if self.volume > 0.0:
                current_volume = self.volume - delta
                if current_volume < 0.0:
                    current_volume = 0.0
        self.set_volume(current_volume)

    def set_pan(self, pan: float) -> None:
        self.pan = limit_range(pan, -1.0, 1.0)
        mixer.setTrackPan(self.index, pan)
        
    def get_pan_as_percent(self) -> float:
        return round(self.pan * 100, 2)
    
    def jog_pan(self, direction: int) -> float:
        current_pan = self.pan
        delta: float = 0.025
        if direction > 0:
            if self.pan < 1.0:
                current_pan = self.pan + delta
        elif direction < 0:
            if self.pan > -1.0:
                current_pan = self.pan - delta
                if current_pan < -1.0:
                    current_pan = -1.0
        self.set_pan(current_pan)
        return current_pan

    def toggle_mute(self) -> None:
        self.muted = not self.muted
        mixer.muteTrack(self.index, int(self.muted))

    def toggle_solo(self) -> None:
        self.soloed = not self.soloed
        mixer.soloTrack(self.index, int(self.soloed))

    def set_color(self, color: tuple[int, int, int]) -> None:
        mixer.setTrackColor(self.index, RGBToColor(color))


class FLMixer:
    @staticmethod
    def scroll_track(direction: int) -> FLMixerTrack:
        current_track = mixer.trackNumber()
        if direction > 0:
            if mixer.trackNumber() < mixer.trackCount():
                current_track = mixer.trackNumber() + 1
        elif direction < 0:
            if mixer.trackNumber() > 0:
                current_track = mixer.trackNumber() - 1
        mixer.setTrackNumber(current_track)
        return FLMixer.get_track(current_track)

    @staticmethod
    def get_track(track_number: int) -> FLMixerTrack:
        return FLMixerTrack(
            index=track_number,
            name=mixer.getTrackName(track_number),
            color=BGRIntToRGB(mixer.getTrackColor(track_number)),
            volume=mixer.getTrackVolume(track_number),
            pan=mixer.getTrackPan(track_number),
            muted=mixer.isTrackMuted(track_number),
            soloed=mixer.isTrackSolo(track_number),
        )
    
    @staticmethod
    def get_selected_track() -> FLMixerTrack:
        return FLMixer.get_track(mixer.trackNumber())
    
    @staticmethod
    def select_track(track_number: int) -> FLMixerTrack:
        mixer.selectTrack(track_number)

from dataclasses import dataclass
import mixer, utils
from fl_controller_framework.util.colors import ColorToRGB, BGRIntToRGB, RGBToColor
from fl_controller_framework.util.functions import limit_range


@dataclass
class FLMixerTrack:
    """
    Represents a mixer track in FL Studio.
    """

    index: int
    name: str
    color: tuple[int, int, int]
    volume: float
    pan: float
    muted: bool
    soloed: bool

    def set_name(self, name: str) -> None:
        """
        Sets the name of the mixer track.

        Args:
            name (str): The new name for the track.
        """
        mixer.setTrackName(self.index, name)

    def set_volume(self, volume: float) -> None:
        """
        Sets the volume of the mixer track.

        Args:
            volume (float): The new volume value.
        """
        self.volume = volume
        mixer.setTrackVolume(self.index, volume)

    def get_volume_as_db(self) -> float:
        """
        Returns the volume of the mixer track in decibels.

        Returns:
            float: The volume in decibels.
        """
        return round(mixer.getTrackVolume(self.index, 1), 2)
    
    def jog_volume(self, direction: int) -> None:
        """
        Adjusts the volume of the mixer track by a small increment.

        Args:
            direction (int): The direction of adjustment. Positive values increase the volume, negative values decrease it.
        """
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
        """
        Sets the pan (stereo position) of the mixer track.

        Args:
            pan (float): The new pan value. Must be between -1.0 (left) and 1.0 (right).
        """
        self.pan = limit_range(pan, -1.0, 1.0)
        mixer.setTrackPan(self.index, pan)
        
    def get_pan_as_percent(self) -> float:
        """
        Returns the pan of the mixer track as a percentage.

        Returns:
            float: The pan as a percentage.
        """
        return round(self.pan * 100, 2)
    
    def jog_pan(self, direction: int) -> float:
        """
        Adjusts the pan of the mixer track by a small increment.

        Args:
            direction (int): The direction of adjustment. Positive values move the pan to the right, negative values move it to the left.

        Returns:
            float: The new pan value.
        """
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
        """
        Toggles the mute state of the mixer track.
        """
        self.muted = not self.muted
        mixer.muteTrack(self.index, int(self.muted))

    def toggle_solo(self) -> None:
        """
        Toggles the solo state of the mixer track.
        """
        self.soloed = not self.soloed
        mixer.soloTrack(self.index, int(self.soloed))

    def set_color(self, color: tuple[int, int, int]) -> None:
        """
        Sets the color of the mixer track.

        Args:
            color (tuple[int, int, int]): The RGB color values as a tuple of integers.
        """
        mixer.setTrackColor(self.index, RGBToColor(color))


class FLMixer:
    """
    Represents the FL Studio mixer and provides methods to interact with it.
    """

    @staticmethod
    def scroll_track(direction: int) -> FLMixerTrack:
        """
        Scrolls the current track in the specified direction.

        Args:
            direction (int): The direction to scroll the track. Positive values scroll forward, negative values scroll backward.

        Returns:
            FLMixerTrack: The FLMixerTrack object representing the new current track.
        """
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
        """
        Retrieves information about a specific track in the mixer.

        Args:
            track_number (int): The index of the track to retrieve information for.

        Returns:
            FLMixerTrack: The FLMixerTrack object representing the specified track.
        """
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
        """
        Retrieves information about the currently selected track in the mixer.

        Returns:
            FLMixerTrack: The FLMixerTrack object representing the currently selected track.
        """
        return FLMixer.get_track(mixer.trackNumber())
    
    @staticmethod
    def select_track(track_number: int) -> FLMixerTrack:
        """
        Selects a specific track in the mixer.

        Args:
            track_number (int): The index of the track to select.

        Returns:
            FLMixerTrack: The FLMixerTrack object representing the newly selected track.
        """
        mixer.selectTrack(track_number)

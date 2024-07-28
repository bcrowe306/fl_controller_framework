from dataclasses import dataclass
import mixer, utils
from fl_controller_framework.util.colors import ColorToRGB, BGRIntToRGB, RGBToColor

# trackNumber	-	int	Returns the index of the currently selected mixer track.	1
# getTrackInfo	int trackType	int	Returns track info.	1
# setTrackNumber	int index, (int flags = -1)	-	Sets the currently selected mixer track.	1
# trackCount	-	int	Returns the number of tracks.	1
# getTrackName	int index, (int maxLen = -1)	string	Returns the name of the track at index.	1
# setTrackName	int index, string name	-	Changes the name of the track at index to "name".	1
# getTrackColor	int index	int	Returns the color of the track at index.	1
# setTrackColor	int index, int color	-	Changes the color of the track at index to "color".	1
# getSlotColor	int index, int slot	int	Returns the color of the slot of the track at index as an RGBA value.	32
# setSlotColor	int index, int slot, int color	-	Changes the color of the slot track at index to the value of "color".	32
# isTrackArmed	int index	int	Returns True if the track at index is armed.	1
# armTrack	int index	-	Toggle the armed state of the track at index.	1
# isTrackSolo	int index	int	Returns True if the track at index is soloed.	1
# soloTrack	int index, (int value = -1), (int mode = -1)	-	without value this function will toggle the solo state of the track at index - set optional 'value' to 1 to solo track or to 0 unsolo track
# 1
# isTrackEnabled	int index	-	Returns True if the track at index is enabled.	1
# isTrackAutomationEnabled	int index, int plugIndex	-	Returns True if the track at index has automation enabled.	1
# enableTrack	int index	-	Toggle the enabled state of the track at index.	1
# isTrackMuted	int index	-	Returns True if the track at index is muted.	2
# muteTrack	int index, (int value* = -1)	-	Toggles the Mute status of the track at index if value is default. Otherwise mutes track if value is 1 and unmutes if value is 0.	2, *30
# isTrackMuteLock	int index	int	Returns True if the Mute for track at index is locked.	13
# getTrackPluginId	int index, int plugIndex	int	Returns plugin id of plugin with plugIndex on the track at index.	1
# isTrackPluginValid	int index, int plugIndex	int	Returns True if plugin with plugIndex on the track at index. is valid	1
# getTrackVolume	int index, (int mode* = 0)	float	Returns the normalized volume (between 0 and 1.0) of the track at index - set optional mode to 1 to get volume in dB	1, *14
# setTrackVolume	int index, float volume, (int pickupMode* = PIM_None)	-	Changes the volume of the track at index - volume is value between 0 and 1.0
# use optional pickupMode to override FL default pickup option	1, 13(pickup)
# getTrackPan	int index	float	Returns the pan value (between -1.0 and 1.0) for the track at index.	1
# setTrackPan	int index, float pan, (int pickupMode* = PIM_None)	-	Changes the panning for the track at index.
# pan value is between -1.0 and 1.0 - use optional pickupMode to override FL default pickup option	1, 13(pickup)
# getTrackStereoSep	int index	float	Returns the stereo separation value (between -1.0 and 1.0) for the track at index - set optional 'pickup' to 1 to use pickup function, or to 2 to follow FL global pickup setting	12, 13(pickup)
# setTrackStereoSep	int index, float sep, (int pickupMode = 0)	-	Changes the stereo separation for the track at index.
# sep value is between -1.0 and 1.0.	12
# isTrackSelected	int index	int	Returns True if the track at index is selected.	1
# selectTrack	int index	-	Toggle selection of the track at index.	1
# setActiveTrack	int index	-	Exclusively select the track at index.	27
# selectAll	-	-	Select all mixer tracks.	1
# deselectAll	-	-	Deselect all mixer tracks.	1
# setRouteTo	int index, int destIndex, int value, (bool updateUI* = False)	-	Set route for track at index to "destIndex". Set optional updateUI to true to update mixer UI (same as afterRoutingChanged)	1, *36
# setRouteToLevel	int index, int destIndex, float level	-	Set routeTo level, level is normalized value	36
# getRouteToLevel	int index, int destIndex	float	Get routeTo levelas normalized value	36
# getRouteSendActive	int index, int destIndex	int	Returns True if route sends from track at index to "destIndex" is active.	1
# afterRoutingChanged	-	-	Notify FL about routing changes.	1
# getEventValue	int index, (int value = MaxInt), (int smoothTarget = 1)	int	Returns event value from MIDI.	1
# remoteFindEventValue	int index, (int flags = 0)	float	Returns event value.	1
# getEventIDName	int index, (int shortName = 0)	str	Returns event name (set shortName to True for short name).	1
# getEventIDValueString	int index, int value	string	Returns event value as string.	1
# getAutoSmoothEventValue	int index, (int locked = 1)	int	Returns auto smooth event value.	1
# automateEvent	int index, int value, int flags, (int speed = 0), (int isIncrement = 0), (float res = EKRes)	int	Automate event	1
# getTrackPeaks	int index, int mode	float	Returns peaks for track at "index"
# returned value is between 0 (silence) and 1 (0db) or < 1 (clipping)	1
# getTrackRecordingFileName	int index	string	Returns recording file name for track at "index"	1
# linkTrackToChannel	int mode	-	Link track to channel
# "mode" can be one of the: ROUTE_ToThis = 0, ROUTE_StartingFromThis = 1	1
# linkChannelToTrack	int channel, int track, (int select = 0)	-	Link channel to track
# "channel" is channel index respecting groups, set optional 'select' to 1 to make track selected	23
# getSongStepPos	-	int	Returns song step position.	1
# getCurrentTempo	(int asInt = 0)	int/float	Returns current tempo - set optional "asInt" to True to get result as int	1
# getRecPPS	-	int	Returns recording pps.	1
# getSongTickPos	(int mode = ST_Int)	int/float	Returns song ticks pos.	1
# getLastPeakVol	int audioChannel	float	Returns last peak volume. Set audioChannel to 0 for left volume or to 1 for right volume.	9
# getTrackDockSide	int index	int	Returns dock side of the mixer track (index). (0 = left, 1 = center, 2 = right)
# listen to OnRefresh event (HW_Dirty_Mixer_Controls) flag to update on dock changes	13
# isTrackSlotsEnabled	int index	int	Returns state of mixer track (index) 'Enable effect slots' option.	19
# enableTrackSlots	int index, (int value = -1)	int	Toggle mixer track (index) 'Enable effect slots' option. (value: -1 = toggle, 0 = disable, 1 = enable)	19
# isTrackRevPolarity	int index	int	Returns state of mixer track (index) 'reverse polarity' option.	19
# revTrackPolarity	int index, (int value = -1)	int	Toggle mixer track (index) 'reverse polarity' option. (value: -1 = toggle, 0 = disable, 1 = enable)	19
# isTrackSwapChannels	int index	int	Returns state of mixer track (index) 'swap l/r channels' option.	19
# swapTrackChannels	int index, (int value = -1)	int	Toggle mixer track (index) 'swap l/r channels' option. (value: -1 = toggle, 0 = disable, 1 = enable)	19
# focusEditor	int index, int plugIndex	-	Focus editor (plugin window) for plugIndex on the track at "index".	25
# getActiveEffectIndex	-	tuple[int index, int plugIndex] | None	Returns tracks index and pluIndex for focused effect editor or none of no effect editor is focused.	25
# getEqBandCount	-	int	Returns number of Eq bands	35
# getEqGain	int index, int band, (int mode)	float	Returns Eq gain for band in track (index) as normalized value. Set optional mode to 1 to get value in Db.	35
# setEqGain	int index, int band, float value	-	Set Eq gain for band in track (index) as normalized value.	35
# getEqFrequency	int index, int band, (int mode)	float	Returns Eq frequency for band in track (index) as normalized value. Set optional mode to 1 to get value in Hz.	35
# setEqFrequency	int index, int band, float value	-	Set Eq frequency for band in track (index) as normalized value.	35
# getEqBandwidth	int index, int band	float	Returns Eq bandwidth for band in track (index) as normalized value.	35
# setEqBandwidth	int index, int band, float value	-	Set Eq bandwidth for band in track (index) as normalized value.


@dataclass
class FLMixerTrack:
    index: int
    name: str
    color: tuple[int, int, int]
    volume: float
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

    def toggle_mute(self) -> None:
        mixer.muteTrack(self.index, int(not self.muted))

    def toggle_solo(self) -> None:
        mixer.soloTrack(self.index, int(not self.soloed))

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
            muted=mixer.isTrackMuted(track_number),
            soloed=mixer.isTrackSolo(track_number),
        )
    
    @staticmethod
    def get_selected_track() -> FLMixerTrack:
        return FLMixer.get_track(mixer.trackNumber())
    
    @staticmethod
    def select_track(track_number: int) -> FLMixerTrack:
        mixer.selectTrack(track_number)

"""event.py: This module contains the essential event/observer building blocks from the rest of the .. 
    Essentially, this whole framework is a bidirectional observer pattern with builtin state. Most classes in this framework inherit from EventObject class.
"""

class EventObject(object):
    """This object is a base class that implements the basic observer patter. """
    def __init__(self, *a, **k):
        super(EventObject, self).__init__(*a, **k)
        self.observers: dict[str,list] = dict()
        """dictionary instance variable that houses the registry of observer functions. 
        They key for this dictionary is a str of the event_id. Events are referenced by this key and the list of observers are called by it."""

    def subscribe(self, event_id: str, func):
        """Subscribe to an event by event_id. This function add the supplied observer func to the list identified by event_id."""
        if self.observers.get(event_id) == None:
            self.observers[event_id] = []
        if(func not in self.observers[event_id]):
            self.observers[event_id].append(func)
            
    def unsubscribe(self, event_id: str, func):
        """Unsubscribe removed the supplied function from the list of observers by event_id."""
        handlers: list = self.observers[event_id]
        if handlers != None:
            for f in handlers:
                if f == func:
                    handlers.remove(f)
    
    def notify_listeners(self, event_id: str, *a, **k):
        """This function is called whenever a new event(event_id) is received. All functions registered by subscribe are called by the specified event_id."""
        _listeners = self.observers.get(event_id)
        if _listeners != None:
            for func in _listeners:
                if hasattr(func, '__call__'):
                    func(*a, **k)

class GlobalEventObject(EventObject):
    """This is a global event registry. This class inherits from EventObject and is used to receive the events from FL Studio. 
        It is a singleton object, and is attached to Component, and Control classes as instance variables.
        This allows Component, Controls, and Control Surface to subscribe-to and react to FL Studio events. 
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GlobalEventObject, cls).__new__(
                cls, *args, **kwargs)
        return cls.instance

    def __init__(self) -> None:
        super(GlobalEventObject, self).__init__()

class FLEvents:
    HW_Dirty_Mixer_Sel : str = "HW_Dirty_Mixer_Sel"
    """mixer selection changed"""

    HW_Dirty_Mixer_Display : str = "HW_Dirty_Mixer_Display"
    """mixer display changed"""
    HW_Dirty_Mixer_Controls : str = "HW_Dirty_Mixer_Controls"
    """mixer controls changed"""

    HW_Dirty_RemoteLinks : str = "HW_Dirty_RemoteLinks"
    """remote links (linked controls) has been added/removed"""

    HW_Dirty_FocusedWindow : str = "HW_Dirty_FocusedWindow"
    """channel selection changed"""

    HW_Dirty_Performance : str = "HW_Dirty_Performance"
    """performance layout changed"""

    HW_Dirty_LEDs : str = "HW_Dirty_LEDs"
    """various changes in FL which require update of controller leds
update status leds (play/stop/record/active window/.....) on this flag"""

    HW_Dirty_RemoteLinkValues : str = "HW_Dirty_RemoteLinkValues"
    """remote link (linked controls) value is changed"""

    HW_Dirty_Patterns : str = "HW_Dirty_Patterns"
    """pattern changes"""

    HW_Dirty_Tracks : str = "HW_Dirty_Tracks"
    """	track changes"""

    HW_Dirty_ControlValues : str = "HW_Dirty_ControlValues"
    """plugin control value changes"""

    HW_Dirty_Colors : str = "HW_Dirty_Colors"
    """plugin colors changes"""

    HW_Dirty_Names : str = "HW_Dirty_Names"
    """plugin names changes"""

    HW_Dirty_ChannelRackGroup : str = "HW_Dirty_ChannelRackGroup"
    """	Channel rack group changes"""

    HW_ChannelEvent : str = "HW_ChannelEvent"
    """channel changes"""

    OnInit: str = "OnInit"
    """Called when the script has been started."""

    OnMidiMsg: str = "OnMidiMsg"
    """Called for all MIDI messages that were not handled by OnMidiIn."""

    OnMidiOutMsg: str = "OnMidiOutMsg"
    """Called for short MIDI out messages sent from MIDI Out plugin - (event properties are limited to: handled, status, data1, data2, port, midiId, midiChan, midiChanEx)"""

    OnRefresh: str = "OnRefresh"
    """Called when something changed that the script might want to respond to."""

    OnIdle: str = "OnIdle"
    """Called from time to time. Can be used to do some small tasks, mostly UI related. For example: update activity meters."""

    OnUpdateMeters: str = "OnUpdateMeters"
    """Called when peak meters needs to be updated
call device.setHasMeters() in onInit to use this event!"""

    OnDeInit: str = "OnDeInit"
    """Called before the script will be stopped."""

    OnUpdateBeatIndicator: str = "OnUpdateBeatIndicator"
    """Called when the beat indicator has changes - "value" can be off = 0, bar = 1 (on), beat = 2 (on)"""

    OnProjectLoad: str = "OnProjectLoad"
    """Called when project is loaded"""

    OnDoFullRefresh: str = "OnDoFullRefresh"
    """Same as OnRefresh, but everything should be updated."""

    OnDisplayZone: str = "OnDisplayZone"
    """Called when playlist zone changed"""

    OnUpdateLiveMode: str = "OnUpdateLiveMode"
    """Called when something about performance mode has changed."""

    OnDirtyMixerTrack: str = "OnDirtyMixerTrack"
    """Called on mixer track(s) change, 'index' indicates track index of track that changed or -1 when all tracks changed
collect info about 'dirty' tracks here but do not handle track(s) refresh, wait for OnRefresh event with HW_Dirty_Mixer_Controls flag"""

    OnDirtyChannel: str = "OnDirtyChannel"
    """
        Called on channel rack channel(s) change, 'index' indicates channel that changed or -1 when all channels changed
collect info about 'dirty' channels here but do not handle channels(s) refresh, wait for OnRefresh event with HW_ChannelEvent flag
    """
    OnFirstConnect: str = "OnFirstConnect"
    """Called when device is connected for the first time (ever)"""

    OnWaitingForInput: str = "OnWaitingForInput"
    """ Called when peak meters needs to be updated call device.setHasMeters() in onInit to use this event!"""

    OnSendTempMsg: str = "OnSendTempMsg"
    """
        Called when hint message (to be displayed on controller display) is sent to the controller duration of message is in ms
    """
    class channels:
        selectedChannel: str = "channels.selectedChannel"
        """Returns 'index' (respecting groups) of the first selected channel
When there is no selection, function will return 0 (or -1 if canBeNone is 1)
Use optional 'offset' parameter to find other selected channels
Set optional 'indexGlobal' to 1 to return global channel index instead of index respecting groups"""

        getChannelName: str = "channels.getChannelName"
        """	Returns the name of the channel at "index"."""

        getChannelColor: str = "channels.getChannelColor"
        """	Returns the color of the channel at "index". """

        isChannelMuted: str = "channels.isChannelMuted"
        """int	Returns True if the channel at "index" is muted."""

        getChannelVolume: str = "channels.getChannelVolume"
        """	Returns the normalized volume (between 0 and 1.0) of the channel at "index" - set optional useDb to 1 to get volume in dB"""

        getChannelPan: str = "channels.getChannelPan"
        """Returns the pan value for the channel at "index", as a value between -1.0 and +1.0."""

        getChannelPitch: str = "channels.getChannelPitch"
        """	Returns the pitch value for the channel at "index", as a value between -1.0 and +1.0 - use optional mode parameter to return pitch in semitones (mode = 1) or to return pitch range (mode = 2)"""

        getChannelType: str = "channels.getChannelType"
        """	Returns the type of channel, can be one of the following values"""

        isChannelSelected: str = "channels.isChannelSelected"
        """Returns True if the channel at "index" is selected."""

        getChannelIndex: str = "channels.getChannelIndex"
        """Returns 'indexGlobal' for channel at "index" (respecting the groups)."""

        getTargetFxTrack: str = "channels.getTargetFxTrack"
        """	Returns target FX track for channel at "index"."""

        isHighLighted: str = "channels.isHighLighted"
        """Returns True when red highlight rectangle is active in channel rack."""

        getRecEventId: str = "channels.getRecEventId"
        """	Returns eventID for channel at "index".
            Use this eventID in processRECEvent.
            Example (to get eventId for volume of first channel):

            eventId = midi.REC_Chan_Vol + channels.getRecEventId(0)"""

        isGridBitAssigned: str = "channels.isGridBitAssigned"
        """Returns 1 when grid bit for channel at "index" is assigned."""

        getGridBit: str = "channels.getGridBit"
        """	Returns grid bit at "position" for channel at "index"."""

        getStepParam: str = "channels.getStepParam"
        """	Get step parameter for step at "step" """

        getCurrentStepParam: str = "channels.getCurrentStepParam"
        """Get current step parameter for channel at "index" and for step at "step"."""

        getGridBitWithLoop: str = "channels.getGridBitWithLoop"
        """Get grid bit with loop for channel at index."""

        isGraphEditorVisible: str = "channels.isGraphEditorVisible"
        """	Returns whether the graph editor is currently visible."""

        getActivityLevel: str = "channels.getActivityLevel"
        """Returns activity level for channel at "index"."""
    class mixer:
        trackNumber: str = "mixer.trackNumber"
        getTrackInfo: str = "mixer.getTrackInfo"
        trackCount: str = "mixer.trackCount"
        getTrackName: str = "mixer.getTrackName"
        getTrackColor: str = "mixer.getTrackColor"
        getSlotColor: str = "mixer.getSlotColor"
        isTrackArmed: str = "mixer.isTrackArmed"
        isTrackSolo: str = "mixer.isTrackSolo"
        isTrackEnabled: str = "mixer.isTrackEnabled"
        isTrackAutomationEnabled: str = "mixer.isTrackAutomationEnabled"
        isTrackMuted: str = "mixer.isTrackMuted"
        isTrackMuteLock: str = "mixer.isTrackMuteLock"
        getTrackPluginId: str = "mixer.getTrackPluginId"
        getTrackVolume: str = "mixer.getTrackVolume"
        getTrackPan: str = "mixer.getTrackPan"
        getTrackStereoSep: str = "mixer.getTrackStereoSep"
        isTrackSelected: str = "mixer.isTrackSelected"
        getRouteToLevel: str = "mixer.getRouteToLevel"
        getRouteSendActive: str = "mixer.getRouteSendActive"
        getEventValue: str = "mixer.getEventValue"
        getEventIDName: str = "mixer.getEventIDName"
        getEventIDValueString: str = "mixer.getEventIDValueString"
        getAutoSmoothEventValue: str = "mixer.getAutoSmoothEventValue"
        getTrackPeaks: str = "mixer.getTrackPeaks"
        getTrackRecordingFileName: str = "mixer.getTrackRecordingFileName"
        getSongStepPos: str = "mixer.getSongStepPos"
        getCurrentTempo: str = "mixer.getCurrentTempo"
        getRecPPS: str = "mixer.getRecPPS"
        getSongTickPos: str = "mixer.getSongTickPos"
        getLastPeakVol: str = "mixer.getLastPeakVol"
        getTrackDockSide: str = "mixer.getTrackDockSide"
        isTrackSlotsEnabled: str = "mixer.isTrackSlotsEnabled"
        isTrackRevPolarity: str = "mixer.isTrackRevPolarity"
        isTrackSwapChannels: str = "mixer.isTrackSwapChannels"
        getActiveEffectIndex: str = "mixer.getActiveEffectIndex"
        getEqBandCount: str = "mixer.getEqBandCount"
        getEqGain: str = "mixer.getEqGain"
        getEqFrequency: str = "mixer.getEqFrequency"
        getEqBandwidth: str = "mixer.getEqBandwidth"
    class playlist:
        trackCount: str = "playlist.trackCount"
        """Returns the current track count.	1"""

        getTrackName: str = "playlist.getTrackName"
        """Returns the name of the track at "index".	1"""

        setTrackName: str = "playlist.setTrackName"
        """Changes the name of the track at "index" to "name".	1"""

        getTrackColor: str = "playlist.getTrackColor"
        """Returns the color of the track at "index" as an RGBA value.	1"""

        setTrackColor: str = "playlist.setTrackColor"
        """Changes the color of the track at "index" to the value of "color".	1"""

        isTrackMuted: str = "playlist.isTrackMuted"
        """Returns True if the track at "index" is muted.	1"""

        muteTrack: str = "playlist.muteTrack"
        """Toggle whether the track at index is muted. An unmuted track will become muted and a muted track will become unmuted.Set optional value to 1(mute) or to 0(unmute) track.Set                     optional 'inGroup' to 1 to mute/unmute track group (alt + click in FL)	1, *30, *33"""

        isTrackMuteLock: str = "playlist.isTrackMuteLock"
        """Returns True if the Mute for track at "index" is locked.	2"""

        muteTrackLock: str = "playlist.muteTrackLock"
        """Toggles the Mute lock status of the track at "index".	2"""

        isTrackSolo	: str = "playlist.isTrackSolo"
        """Returns True if the track at "index" is currently solo'd.	1"""

        soloTrack: str = "playlist.soloTrack"
        """toggle the solo state of the track at "index"set optional 'value' to 1 to solo track or to 0 unsolo track set optional 'inGroup' to 1 to solo/unsolo track group (alt + right click in FL)	1, *30"""

        isTrackSelected: str = "playlist.isTrackSelected"
        """Returns True if the track at "index" is selected.	12"""

        selectTrack	: str = "playlist.selectTrack"
        """Toggle selection of the track at "index".	12"""

        selectAll: str = "playlist.selectAll"
        """Select all playlist tracks.	12"""

        deselectAll: str = "playlist.deselectAll"
        """Deselect all playlist tracks.	12"""

        getTrackActivityLevel: str = "playlist.getTrackActivityLevel"
        """Returns the activity level of the track at "index" (zero if not active, > 0 if active).	1"""

        getTrackActivityLevelVis: str = "playlist.getTrackActivityLevelVis"
        """Returns the visual activity level of the track at "index" as a normalized value.	1"""

        getDisplayZone: str = "playlist.getDisplayZone"
        """Returns current display zone in the playlist or zero if none.	1"""

        lockDisplayZone: str = "playlist.lockDisplayZone"
        """Lock display zone at "index".	1"""

        liveDisplayZone: str = "playlist.liveDisplayZone"
        """Set the display zone in the playlist to the specified co-ordinates - use optional 'duration' parameter to make display zone temporary	1"""

        getLiveLoopMode: str = "playlist.getLiveLoopMode"
        """Get live loop mode.	1"""

        getLiveTriggerMode: str = "playlist.getLiveTriggerMode"
        """Get live trigger mode - Result is one of the constants	1"""

        getLivePosSnap: str = "playlist.getLivePosSnap"
        """Get live pos snap - Result is one of the constants	1"""

        getLiveTrigSnap	: str = "playlist.getLiveTrigSnap"
        """Get live trig snap - Result is one of the constants	1"""

        getLiveStatus: str = "playlist.getLiveStatus"
        """Get live status for track at "index" - Result depends on mode.	1"""

        getLiveBlockStatus: str = "playlist.getLiveBlockStatus"
        """Get live block status for track at "index" and for block "blockNum" Result depends on mode -	1"""

        getLiveBlockColor: str = "playlist.getLiveBlockColor"
        """Get live block color for track at "index" and for block "blockNum"	1"""

        triggerLiveClip: str = "playlist.triggerLiveClip"
        """Trigger live clip for track at "index" and for block "blockNum". Set blockNum to -1 and use the TLC_Fill flag to stop live clips on this track.	1"""

        refreshLiveClips: str = "playlist.refreshLiveClips"
        """Refresh live clips for track at "index".	1"""

        incLivePosSnap: str = "playlist.incLivePosSnap"
        """Increase live pos snap for track at "index"	1"""

        incLiveTrigSnap: str = "playlist.incLiveTrigSnap"
        """Increase live trig snap for track at "index".	1"""

        incLiveLoopMode: str = "playlist.incLiveLoopMode"
        """Increase live loop mode for track at "index"	1"""

        incLiveTrigMode: str = "playlist.incLiveTrigMode"
        """Increase live trig mode for track at "index"	1"""

        getVisTimeBar: str = "playlist.getVisTimeBar"
        """Get time bar.	1"""

        getVisTimeTick: str = "playlist.getVisTimeTick"
        """Get time tick.	1"""

        getVisTimeStep: str = "playlist.getVisTimeStep"
        """Get time step.	1"""

        getPerformanceModeState: str = "playlist.getPerformanceModeState"
        """Returns 1 when the PL is in performance mode, 0 when it's not.	21"""
    class patterns:
        patternNumber:str = "patterns.patternNumber"
        patternCount: str  = "patterns.patternCount"
        patternMax: str = "patterns.patternMax"

    class transport:
        isRecording: str = "transport.isRecording"
        isPlaying: str = "transport.isPlaying"
        getSongPosHint: str = "transport.getSongPosHint"
        getLoopMode: str = "transport.getLoopMode"
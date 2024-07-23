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

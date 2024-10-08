class MIDI_STATUS:
    NOTE_ON_STATUS = 144
    NOTE_OFF_STATUS = 128
    CC_STATUS = 176
    PB_STATUS = 224
    AFTERTOUCH= 0xA0
    SYSEX_START = 240
    SYSEX_START_HEX = 240
    SYSEX_END = 247
    SYSEX_GENERAL_INFO = 6
    SYSEX_NON_REALTIME = 126
    SYSEX_IDENTITY_REQUEST_ID = 1
    SYSEX_IDENTITY_RESPONSE_ID = 2
    SYSEX_IDENTITY_REQUEST_MESSAGE = (SYSEX_START,
        SYSEX_NON_REALTIME,
        127,
        SYSEX_GENERAL_INFO,
        SYSEX_IDENTITY_REQUEST_ID,
        SYSEX_END)

class STATUS_BYTE:
    NOTE_ON=0x90
    NOTE_OFF=0x80
    AFTERTOUCH=0xA0
    CC=0xB0
    PROGRAM_CHANGE=0xC0
    CHANNEL_AFTERTOUCH=0xD0
    PTICH_BEND=0xE0

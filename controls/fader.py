from ..control import Control
from ..util.midi import MIDI_STATUS
from ..fl_class import flMidiMsg

class FaderControl(Control):
    @staticmethod
    def generate_event(on_msg_status: int, off_msg_status: int, event_data: flMidiMsg) -> dict[str: any]:
        events: dict[str: any] = dict()
        if event_data.status == on_msg_status:
            events['toggled'] = None
            events['pressed'] = True

        elif event_data.status == off_msg_status:
            events['pressed'] = False
            events['released'] = True
        return events
    def __init__(self, name: str, channel: int, identifier: int, status: int = MIDI_STATUS.CC_STATUS, playable=False, feedback=False, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super().__init__(name, channel, identifier, playable, status,
                         feedback, feedback_process, default_color, blackout_color, skin)

    def _on_value(self, e):
        print('override on_value')
        # self.notify('value', e)
    

from ..control import Control
from ..util.midi import MIDI_STATUS
from ..fl_class import flMidiMsg

class FaderControl(Control):
    """This control type is for knobs on your midi controller. It accepts the same parameters as the base Control Type, but emmits special events along with the value of the fader.
    Events:
        * unit_value: This event is emitted with the fader position represented as a float from 0 - 1.0.
        * inverse_value: this event is emitted with fader position reverse, so value of 127 is 0 and 0 is 127.
        * inverse_unit_value: this event is emitted with fader position reversed, but in unit form from 0 - 1.0.
        * symmetry_value: this event is emitted with the fader position represented in symetry from -64 - 64.
        * symmetry_unit_value: this event is emitted with the fader position represented in symetry from -1.0 - 1.0
    """
    @staticmethod
    def generate_event(event_data: flMidiMsg) -> dict[str: any]:
        """This static method generates the additional events for this control."""
        events: dict[str: any] = dict()
        value: int = 0
        try:
            value = int(event_data.data2)
        except:
            value = 0

        events['unit_value']  = value / 127
        events['inverse_value']  = 127 - value
        events['inverse_unit_value']  = (127 - value) / 127
        events['symmetry_value'] = value - 64
        events['symmetry_unit_value'] = (value - 64) / 64

        return events
    def __init__(self, name: str, channel: int, identifier: int, status: int = MIDI_STATUS.CC_STATUS, playable=False, feedback=False, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super().__init__(name, channel, identifier, playable, status,
                         feedback, feedback_process, default_color, blackout_color, skin)

    def _on_value(self, e):
        events: list = FaderControl.generate_event(e)
        for event in events:
            setattr(self, "_{}".format(event), events[event])
            self.notify(event, events[event])

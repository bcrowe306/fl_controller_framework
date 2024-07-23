from ..control import Control
from ..util.midi import MIDI_STATUS
from ..fl_class import flMidiMsg

class JogControl(Control):

    @staticmethod
    def generate_jog_events(status, inc_value, dec_value, event_data: flMidiMsg):
        events: dict[str: any] = dict()
        if event_data.status == status:
            if event_data.data2 == inc_value:
                events['inc'] = True
                events['jogged'] = True
            if event_data.data2 == dec_value:
                events['dec'] = True
                events['jogged'] = False
                
            
        return events
    def __init__(self, name: str, channel: int, identifier: int, status: int = MIDI_STATUS.CC_STATUS, inc_value: int = 1, dec_value: int = 127, playable=False, feedback=False, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super().__init__(name, channel, identifier, playable, status,
                         feedback, feedback_process, default_color, blackout_color, skin)
        self.inc_value = inc_value
        self.dec_value = dec_value
        self.status = status

    def _on_value(self, event_data: flMidiMsg):
        events = JogControl.generate_jog_events(
            self.status, self.inc_value, self.dec_value, event_data)
        for event in events:
            self.notify(event, events[event])
    

from ..control import Control
from ..util.midi import MIDI_STATUS
from ..fl_class import flMidiMsg

class JogControl(Control):
    """
    Represents a Jog control that generates events based on MIDI input.

    Args:
        name (str): The name of the control.
        channel (int): The MIDI channel of the control.
        identifier (int): The MIDI identifier of the control.
        status (int, optional): The MIDI status byte of the control. Defaults to MIDI_STATUS.CC_STATUS.
        inc_value (int, optional): The MIDI value for the increment action. Defaults to 1.
        dec_value (int, optional): The MIDI value for the decrement action. Defaults to 127.
        playable (bool, optional): Indicates if the control is playable. Defaults to False.
        feedback (bool, optional): Indicates if the control provides feedback. Defaults to False.
        feedback_process (function, optional): The feedback processing function. Defaults to None.
        default_color (str, optional): The default color of the control. Defaults to 'Default'.
        blackout_color (str, optional): The color when the control is in blackout mode. Defaults to 'Off'.
        skin (object, optional): The skin object associated with the control. Defaults to None.
    """

    @staticmethod
    def generate_jog_events(status, inc_value, dec_value, event_data: flMidiMsg):
        """
        Generates jog events based on the MIDI input.

        Args:
            status (int): The MIDI status byte to match.
            inc_value (int): The MIDI value for the increment action.
            dec_value (int): The MIDI value for the decrement action.
            event_data (flMidiMsg): The MIDI message data.

        Returns:
            dict: A dictionary containing the generated events.
        """
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
    

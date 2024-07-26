# from ..util.midi import MIDI_STATUS
from ..util.midi import MIDI_STATUS
from ..fl_class import flMidiMsg
from ..control import Control

class ButtonControl(Control):
    """
    Represents a button control for a MIDI controller.

    Args:
        name (str): The name of the button control.
        channel (int): The MIDI channel of the button control.
        identifier (int): The MIDI identifier of the button control.
        playable (bool, optional): Whether the button control is playable. Defaults to False.
        status (int, optional): The MIDI status of the button control. Defaults to MIDI_STATUS.NOTE_ON_STATUS.
        feedback (bool, optional): Whether the button control provides feedback. Defaults to False.
        feedback_process (callable, optional): The feedback process function for the button control. Defaults to None.
        default_color (str, optional): The default color of the button control. Defaults to 'Default'.
        blackout_color (str, optional): The blackout color of the button control. Defaults to 'Off'.
        skin (any, optional): The skin of the button control. Defaults to None.
        on_value (int, optional): The MIDI value when the button is turned on. Defaults to 127.
        off_value (int, optional): The MIDI value when the button is turned off. Defaults to 0.
        on_msg_type (int, optional): The MIDI message type when the button is turned on. Defaults to MIDI_STATUS.NOTE_ON_STATUS.
        off_msg_type (int, optional): The MIDI message type when the button is turned off. Defaults to MIDI_STATUS.NOTE_OFF_STATUS.
        hold_time (int, optional): The hold time in milliseconds for the button control. Defaults to 10.

    Attributes:
        isToggled (bool): Whether the button control is toggled.
        isHold (bool): Whether the button control is being held.
        isPressed (bool): Whether the button control is currently pressed.

    """

    @staticmethod
    def generate_button_events(on_msg_status: int, off_msg_status: int, event_data: flMidiMsg) -> dict[str: any]:
        """
        Generates button events based on the MIDI message status.

        Args:
            on_msg_status (int): The MIDI status for turning the button on.
            off_msg_status (int): The MIDI status for turning the button off.
            event_data (flMidiMsg): The MIDI message data.

        Returns:
            dict[str: any]: A dictionary containing the generated button events.

        """
        events: dict[str: any] = dict()
        if event_data.status == on_msg_status:
            events['toggled'] = None
            events['pressed'] = True
        elif event_data.status == off_msg_status:
            events['pressed'] = False
            events['released'] = True
        return events
        
    def __init__(
        self, name, channel, identifier,
        playable=False,
        status=MIDI_STATUS.NOTE_ON_STATUS,
        feedback=False, 
        feedback_process=None, 
        default_color='Default', 
        blackout_color='Off', 
        skin=None,
        on_value=127, 
        off_value=0, 
        on_msg_type=MIDI_STATUS.NOTE_ON_STATUS, 
        off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS, 
        hold_time=10, *a, **k):
        """
        Initializes a new instance of the ButtonControl class.

        Args:
            name (str): The name of the button control.
            channel (int): The MIDI channel of the button control.
            identifier (int): The MIDI identifier of the button control.
            playable (bool, optional): Whether the button control is playable. Defaults to False.
            status (int, optional): The MIDI status of the button control. Defaults to MIDI_STATUS.NOTE_ON_STATUS.
            feedback (bool, optional): Whether the button control provides feedback. Defaults to False.
            feedback_process (callable, optional): The feedback process function for the button control. Defaults to None.
            default_color (str, optional): The default color of the button control. Defaults to 'Default'.
            blackout_color (str, optional): The blackout color of the button control. Defaults to 'Off'.
            skin (any, optional): The skin of the button control. Defaults to None.
            on_value (int, optional): The MIDI value when the button is turned on. Defaults to 127.
            off_value (int, optional): The MIDI value when the button is turned off. Defaults to 0.
            on_msg_type (int, optional): The MIDI message type when the button is turned on. Defaults to MIDI_STATUS.NOTE_ON_STATUS.
            off_msg_type (int, optional): The MIDI message type when the button is turned off. Defaults to MIDI_STATUS.NOTE_OFF_STATUS.
            hold_time (int, optional): The hold time in milliseconds for the button control. Defaults to 10.

        """
        super().__init__(name, channel, identifier, playable, status,
                         feedback, feedback_process, default_color, blackout_color, skin)
        self.on_value = on_value
        self.off_value = off_value
        self.on_msg_type = on_msg_type
        self.off_msg_type = off_msg_type
        self._toggled = False
        self._pressed = False
        self._hold = False
        self._hold_counter = 0
        self.hold_time = hold_time
        

    @property
    def isToggled(self):
        """
        bool: Whether the button control is toggled.
        """
        return self._toggled


    def _on_idle(self):
        """
        Handles the idle event of the button control.
        """
        pass
        if self._pressed:
          self.hold_counter += 1
          if self.hold_counter > self.hold_time:
            if self.isChanged('_hold', True):
                self._set_hold(True)
        else:
            self.hold_counter = 0
            if self.isChanged('_hold', False):
                self._set_hold(False)


    def _set_hold(self, hold):
        """
        Sets the hold state of the button control.

        Args:
            hold (bool): Whether the button control is being held.

        """
        self._hold = hold
        self.notify('hold', self._hold)

    @property
    def isHold(self) -> bool:
        """
        bool: Whether the button control is being held.
        """
        return self._hold

    def activate(self):
        """
        Activates the button control.

        Returns:
            bool: True if the activation is successful, False otherwise.

        """
        self.event_object.subscribe('idle', self._on_idle)
        return super().activate()

    @property
    def isPressed(self) -> bool:
        """
        bool: Whether the button control is currently pressed.
        """
        return self._pressed
        
    def _set_toggled(self):
        """
        Toggles the state of the button control.
        """
        self._toggled = not self._toggled
        self.notify('toggled', self._toggled)

    def _set_pressed(self, value):
        """
        Sets the pressed state of the button control.

        Args:
            value (bool): Whether the button control is pressed.

        """
        self._pressed = value
        self.notify('pressed', self._pressed)

    def _set_released(self, value):
        """
        Sets the released state of the button control.

        Args:
            value (bool): Whether the button control is released.

        """
        self._released = value
        self.notify('released', self._released)

    def _on_value(self, event_data):
        """
        Handles the value change event of the button control.

        Args:
            event_data (flMidiMsg): The MIDI message data.

        """
        events = ButtonControl.generate_button_events(self.on_msg_type, self.off_msg_type, event_data)
        for event in events:
            setattr(self, '_{}'.format(event), events[event])
            self.notify(event, events[event])

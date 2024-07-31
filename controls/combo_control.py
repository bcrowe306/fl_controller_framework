from .control import ControlBase, Control
from ..api.fl_class import flMidiMsg
from ..util.midi import MIDI_STATUS
from .button import ButtonControl
from .jog_control import JogControl
from .fader import FaderControl
from .knob import KnobControl
from .encoder import EncoderControl

class CC(ControlBase):
    def __init__(self, name: str, channel: int, identifier: int, status=MIDI_STATUS.NOTE_ON_STATUS, playable=False, *a, **k):
        super().__init__(name, channel, identifier, status, playable, *a, **k)

class ComboControl(ControlBase):
    """
    Represents a combo control that combines a primary control with a modifier button.

    Args:
        name (str): The name of the combo control.
        primary_control (Control): The primary control to be combined with the modifier button.
        modifier_button (ButtonControl): The modifier button control.
        modifier_button_event (str, optional): The event type of the modifier button. Defaults to 'pressed'.

    Attributes:
        name (str): The name of the combo control.
        channel (int): The MIDI channel of the primary control.
        identifier (int): The MIDI identifier of the primary control.
        primary_control (Control): The primary control.
        modifier_button (ButtonControl): The modifier button control.
        modifier_button_event (str): The event type of the modifier button.
        _toggled (bool): Flag indicating if the combo control is toggled.
        _pressed (bool): Flag indicating if the combo control is pressed.
        _hold (bool): Flag indicating if the combo control is being held.
        _hold_counter (int): Counter for hold duration.
        hold_time (int): The duration threshold for a hold event.

    Methods:
        _on_modifier_button_event(event_data): Handles the modifier button event.
        _set_jogged(value): Sets the jogged value and notifies subscribers.
        _on_modified_primary_value(event_data): Handles the modified primary value event.
        activate(): Activates the combo control.

    """

    def __init__(self, name: str, primary_control: Control, modifier_button: ButtonControl, modifier_button_event: str = 'pressed', *a, **k):
        super(ComboControl, self).__init__(name, modifier_button.channel, modifier_button.identifier, status=primary_control.status, *a, **k)
        self.name: str = name
        self.channel: int = primary_control.channel
        self.identifier: int = primary_control.identifier
        self.primary_control: Control = primary_control
        self.modifier_button: ButtonControl = modifier_button
        self.modifier_button_event: str = modifier_button_event
        self._toggled: bool = False
        self._pressed: bool = False
        self._hold: bool = False
        self._hold_counter: int = 0
        self.hold_time: int = 10

    def __str__(self) -> str:
        return f"{self.name} {self.status}:{self.channel}:{self.identifier}"

    def __repr__(self) -> str:
        return (
            f"{self.name} {self.status}:{self.channel}:{self.identifier}"
        )

    def _on_modifier_button_event(self, event_data):
        """
        Handles the modifier button event.

        Args:
            event_data: The event data for the modifier button.

        Returns:
            None
        """
        if event_data:
            # self.registry.activate_control(self)
            self.registry.add_modifier(self, self.primary_control)
        else:
            # self.registry.deactivate_control(self)
            self.registry.remove_modifier(self, self.primary_control)

    def _set_jogged(self, value):
        """
        Sets the jogged value and notifies subscribers.

        Args:
            value: The jogged value.

        Returns:
            None
        """
        self.notify('jogged', value)
        self.notify('inc', value) if value else self.notify('dec', value)

    def _on_modified_primary_value(self, event_data: flMidiMsg):
        """
        Handles the modified primary value event.

        Args:
            event_data (flMidiMsg): The event data containing the MIDI message.

        Returns:
            None
        """
        if isinstance(self.primary_control, JogControl):
            events = JogControl.generate_jog_events(
                self.primary_control.status, self.primary_control.inc_value, self.primary_control.dec_value, event_data)
            for event in events:
                self.notify(event, events[event])

        elif isinstance(self.primary_control, ButtonControl):
            button_events = ButtonControl.generate_button_events(
                self.primary_control.on_msg_type, self.primary_control.off_msg_type, event_data)
            for event in button_events:
                setattr(self, '_{}'.format(event), button_events[event])
                self.notify(event, button_events[event])

        elif isinstance(self.primary_control, FaderControl):
            events = FaderControl.generate_event(event_data)
            for event in events:
                setattr(self, '_{}'.format(event), events[event])
                self.notify(event, events[event])

        elif isinstance(self.primary_control, KnobControl):
            events = KnobControl.generate_event(event_data)
            for event in events:
                setattr(self, '_{}'.format(event), events[event])
                self.notify(event, events[event])

        elif isinstance(self.primary_control, EncoderControl):
            events = EncoderControl.generate_encoder_events(event_data)
            for event in events:
                setattr(self, '_{}'.format(event), events[event])
                self.notify(event, events[event])

    def activate(self):
        """
        Activates the combo control.

        Returns:
            None
        """
        self.modifier_button.activate()
        self.event_object.subscribe('{}.{}'.format(self.name, 'value'), self._on_modified_primary_value)
        self.event_object.subscribe('{}.{}'.format(self.modifier_button.name, self.modifier_button_event), self._on_modifier_button_event)
        return super().activate()

    def deactivate(self):
        self.modifier_button.deactivate()
        self.event_object.unsubscribe(
            "{}.{}".format(self.name, "value"), self._on_modified_primary_value
        )
        self.event_object.unsubscribe(
            "{}.{}".format(self.modifier_button.name, self.modifier_button_event),
            self._on_modifier_button_event,
        )
        return super().deactivate()

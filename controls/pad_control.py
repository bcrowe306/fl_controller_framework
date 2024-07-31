from ..util.midi import MIDI_STATUS
from ..core.event import GlobalEventObject
from ..core.control_registry import ControlRegistry
from .control import ControlBase

class cc(ControlBase):
    def __init__(self, name: str, channel: int, identifier: int, status=MIDI_STATUS.NOTE_ON_STATUS, playable=False, *a, **k):
        """
        Represents a control change (CC) MIDI message.

        Args:
            name (str): The name of the control.
            channel (int): The MIDI channel of the control.
            identifier (int): The MIDI CC number of the control.
            status (int, optional): The MIDI status byte of the control. Defaults to MIDI_STATUS.NOTE_ON_STATUS.
            playable (bool, optional): Whether the control is playable. Defaults to False.
            *a: Variable length argument list.
            **k: Arbitrary keyword arguments.
        """
        super().__init__(name, channel, identifier, status, playable, *a, **k)


class PadControl(ControlBase):
    def __init__(self, name, channel, identifier, 
    number: int,
    color: tuple = None,
    playable=True, 
    on_msg_type: int = MIDI_STATUS.NOTE_ON_STATUS,
    off_msg_type: int = MIDI_STATUS.NOTE_OFF_STATUS,
    feedback=None, 
    translation=None
    ):
        """
        Represents a pad control.

        Args:
            name (str): The name of the control.
            channel (int): The MIDI channel of the control.
            identifier (int): The MIDI note number of the control.
            number (int): The pad number of the control.
            color (tuple, optional): The color of the pad. Defaults to None.
            playable (bool, optional): Whether the pad is playable. Defaults to False.
            on_msg_type (int, optional): The MIDI status byte for note on messages. Defaults to MIDI_STATUS.NOTE_ON_STATUS.
            off_msg_type (int, optional): The MIDI status byte for note off messages. Defaults to MIDI_STATUS.NOTE_OFF_STATUS.
            feedback (None, optional): Feedback function for the pad. Defaults to None.
            translation (None, optional): Translation function for the pad. Defaults to None.
        """
        super(PadControl, self).__init__(name or f'pad_{number}_{identifier}', channel, identifier, on_msg_type, playable)
        self.number: int = number
        self.color: tuple = color
        self.on_msg_type: int = on_msg_type
        self.off_msg_type: int = off_msg_type
        self.feedback = feedback
        self.translation = translation
        self.registry.register_control(self) 

    
    def __del__(self):
        self.registry.unregister_control(self)
    
    def set_light(self, *a, **k):
        """
        Sets the light of the pad.

        Args:
            *a: Variable length argument list.
            **k: Arbitrary keyword arguments.
        """
        if hasattr(self.draw, '__call__'):
            self.draw(self, *a, **k)

class PadsControl(ControlBase):
    def __init__(self, name: str, channel: int, pad_mapping: dict[int: int], on_msg_type: int = MIDI_STATUS.NOTE_ON_STATUS,
                 off_msg_type: int = MIDI_STATUS.NOTE_OFF_STATUS, hold_time=10, short_press_time=2, playable=True, feedback=None, translation=None, draw=None):
        """
        Represents a group of pad controls.

        Args:
            name (str): The name of the control.
            channel (int): The MIDI channel of the control.
            pad_mapping (dict[int: int]): The mapping of pad IDs to pad numbers.
            on_msg_type (int, optional): The MIDI status byte for note on messages. Defaults to MIDI_STATUS.NOTE_ON_STATUS.
            off_msg_type (int, optional): The MIDI status byte for note off messages. Defaults to MIDI_STATUS.NOTE_OFF_STATUS.
            hold_time (int, optional): The hold time in milliseconds. Defaults to 10.
            short_press_time (int, optional): The short press time in milliseconds. Defaults to 2.
            playable (bool, optional): Whether the pads are playable. Defaults to True.
            feedback (None, optional): Feedback function for the pads. Defaults to None.
            translation (None, optional): Translation function for the pads. Defaults to None.
            draw (None, optional): Draw function for the pads. Defaults to None.
        """
        self.event_object: GlobalEventObject = GlobalEventObject()
        self.registry: ControlRegistry = ControlRegistry()
        self.name: str = name
        self.channel: int = channel
        self.on_msg_type: int = on_msg_type
        self.off_msg_type: int = off_msg_type
        self.pad_mapping: dict[int: int] = pad_mapping
        self.playable = playable
        self.feedback = feedback
        self.translation = translation
        self.draw = draw
        self.shift = 24
        self.pads: list[PadControl] = []
        self.hold_time = hold_time
        self.short_press_time = short_press_time
        self.pad_state = dict()
        self.multi_hold = dict()
        for pad_id in self.pad_mapping:
            pad_number = self.pad_mapping[pad_id]
            self.pad_state[pad_number] = dict()
            self.pad_state[pad_number]['hold_counter'] = 0
            self.pad_state[pad_number]['hold'] = False
            self.pads.append(self.__generate_pad_control(pad_id))

    def size(self) -> int:
        """
        Returns the amount of pads in this PadsControl Control.

        Returns:
            int: The number of pads.
        """
        return len(self.pads)

    def _pad_state_is_changed(self, pad_number, event_name, value):
        """
        Checks if the state of a pad has changed.

        Args:
            pad_number (int): The pad number.
            event_name (str): The name of the event.
            value: The value of the event.

        Returns:
            bool: True if the state has changed, False otherwise.
        """
        changed = False
        current_state = self.pad_state[pad_number].get(event_name)
        if current_state == None:
            changed = True
            self.pad_state[pad_number][event_name] = value
        else:
            if value != current_state:
                changed = True
        self.pad_state[pad_number][event_name] = value
        return changed

    def get_pad_event_state(self, pad_number, event_name):
        """
        Gets the event state of a pad.

        Args:
            pad_number (int): The pad number.
            event_name (str): The name of the event.

        Returns:
            Any: The event state.
        """
        return self.pad_state[pad_number].get(event_name)

    def set_pad_event_state(self, pad_number, event_name, value):
        """
        Sets the event state of a pad.

        Args:
            pad_number (int): The pad number.
            event_name (str): The name of the event.
            value: The value of the event.
        """
        self.pad_state[pad_number][event_name] = value

    def _on_idle(self):
        """
        Event handler for idle event.
        """
        for pad_number in self.pad_state:
            if self.get_pad_event_state(pad_number, 'pressed'):
                self.pad_state[pad_number]['hold_counter'] += 1
                if self.pad_state[pad_number]['hold_counter'] > self.hold_time:
                    if self._pad_state_is_changed(pad_number, 'hold', True):
                        self._set_hold(pad_number, True)
            else:
                self.pad_state[pad_number]['hold_counter'] = 0
                if self._pad_state_is_changed(pad_number, 'hold', False):
                    self._set_hold(pad_number, False)

    def _set_multi_hold(self, pad_number, hold):
        """
        Sets the multi-hold state of a pad.

        Args:
            pad_number (int): The pad number.
            hold (bool): Whether the pad is in multi-hold state.
        """
        self.multi_hold[pad_number] = hold
        self.notify('multi_hold', self.multi_hold)

    def _set_hold(self, pad_number, hold):
        """
        Sets the hold state of a pad.

        Args:
            pad_number (int): The pad number.
            hold (bool): Whether the pad is in hold state.
        """
        self.notify('hold', pad_number, hold)
        self._set_multi_hold(pad_number, hold)  

    def _set_pressed(self, pad_number: int, pressed: bool, event):
        """
        Sets the pressed state of a pad.

        Args:
            pad_number (int): The pad number.
            pressed (bool): Whether the pad is pressed.
            event: The event object.
        """
        self.set_pad_event_state(pad_number, 'pressed', pressed)
        self.notify('pressed', pad_number, pressed, event)

    def _set_released(self, pad_number: int, released: bool, event):
        """
        Sets the released state of a pad.

        Args:
            pad_number (int): The pad number.
            released (bool): Whether the pad is released.
            event: The event object.
        """
        hold_counter = self.pad_state[pad_number]['hold_counter']
        if hold_counter > 0 and hold_counter < self.short_press_time:
            self.notify('short_press', pad_number, True)
        self.set_pad_event_state(pad_number, 'released', released)
        self.notify('released', pad_number, released, event)

    def _on_value(self, event):
        """
        Event handler for value event.

        Args:
            event: The event object.
        """
        self.notify('value', event)
        pad_number = self.pad_mapping[event.data1]
        self.notify('pad', pad_number, event)
        if event.status == (self.on_msg_type + self.channel):
            self.notify('toggled', pad_number, event)
            self._set_pressed(pad_number, True, event)
        elif event.status == (self.off_msg_type + self.channel):
            self._set_pressed(pad_number, False, event)
            self._set_released(pad_number, True, event)

    def __generate_pad_control(self, pad_id):
        """
        Generates a pad control.

        Args:
            pad_id: The pad ID.

        Returns:
            PadControl: The generated pad control.
        """
        pad_name = '{}_{}_{}'.format(
            self.name, self.pad_mapping[pad_id], pad_id)
        return PadControl(
            name=pad_name,
            channel=self.channel,
            identifier=pad_id,
            on_msg_type= self.on_msg_type,
            off_msg_type=self.off_msg_type,
            number=self.pad_mapping[pad_id],
            playable=self.playable,
            translation=self.translation,
            feedback=self.feedback,
        )

    def set_feedback(self, feedback_func):
        """
        Sets the feedback function for the pads.

        Args:
            feedback_func: The feedback function.
        """
        for pad in self.pads:
            pad.feedback = feedback_func

    def set_translation(self, translation_func):
        """
        Sets the translation function for the pads.

        Args:
            translation_func: The translation function.
        """
        for pad in self.pads:
            pad.translation = translation_func
    def set_playable(self, playable: bool):
        """
        Sets the pads to be playable.

        Args:
            playable (bool): Whether the pads are playable.
        """
        for pad in self.pads:
            pad.playable = playable
    def activate(self):
        """
        Activates the pads control.
        """
        self.event_object.subscribe('idle', self._on_idle)
        for pad in self.pads:
            self.event_object.subscribe('{}.value'.format(pad.name), self._on_value)
            self.registry.activate_control(pad)

    def deactivate(self):
        """
        Deactivates the pads control.
        """
        for pad in self.pads:
            self.event_object.unsubscribe('{}.value'.format(pad.name), self._on_value)
            self.registry.deactivate_control(pad)

    def _initialize(self):
        """
        Initializes the pads control.
        """
        self.set_light(self.default_color)

    def reset(self):
        """
        Resets the pads control.
        """
        self.set_light(self.default_color)

    def blackout(self):
        """
        Turns off the lights of the pads control.
        """

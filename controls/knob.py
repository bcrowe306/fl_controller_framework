"""knob.py: This module contains classes for Knob Controls
"""

from .control import Control
from ..util.midi import MIDI_STATUS
from ..api.fl_class import flMidiMsg
from dataclasses import dataclass


class KnobControl(Control):
    """This control type is for knobs on your midi controller. It accepts the same parameters as the base Control Type, but emmits special events along with the value of the fader.
    Events:
        * unit_value: This event is emitted with the fader position represented as a float from 0 - 1.0.
        * inverse_value: this event is emitted with fader position reverse, so value of 127 is 0 and 0 is 127.
        * inverse_unit_value: this event is emitted with fader position reversed, but in unit form from 0 - 1.0.
        * symentry_value: this event is emitted with the fader position represented in symetry from -64 - 64.
        * symentry_unit_value: this event is emitted with the fader position represented in symetry from -1.0 - 1.0
    """
    @dataclass
    class KnobEvent:
        """This dataclass represents the event generated by the Knob control."""
        value: int
        """Knob value event."""

        unit_value: float
        """Knob unit value event. Knob position represented as a float from 0 - 1.0."""
        inverse_value: int
        """Knob inverse value event. Knob position reverse, so value of 127 is 0 and 0 is 127."""
        inverse_unit_value: float
        """Knob inverse unit value event. Knob position reversed, but in unit form from 0 - 1.0."""
        symmetry_value: int
        """Knob symmetry value event. Knob position represented in symetry from -64 - 64."""
        symmetry_unit_value: float
        """Knob symmetry unit value event. Knob position represented in symetry from -1.0 - 1.0"""
        direction: int
        """Knob direction event. 1 for up, -1 for down, 0 for no change."""

    class Events:
        """Represents the events generated by the Knob control."""
        UNIT_VALUE: str = 'unit_value'
        """Knob unit value event."""
        INVERSE_VALUE: str = 'inverse_value'
        """Knob inverse value event."""
        INVERSE_UNIT_VALUE: str = 'inverse_unit_value'
        """Knob inverse unit value event."""
        SYMMETRY_VALUE: str = 'symmetry_value'
        """Knob symmetry value event."""
        SYMMETRY_UNIT_VALUE: str = 'symmetry_unit_value'
        """Knob symmetry unit value event."""
        DIRECTION: str = 'direction'
        ALL: str = 'all'

    def generate_event(self, event_data: flMidiMsg) -> dict[str: any]:
        """This static method generates the additional events for this control."""
        events: dict[str: any] = dict()
        value: int = 0
        try:
            value = int(event_data.data2)
        except:
            value = 0
        half_value: float = 127/2

        direction: int = 0
        if value > self.prev_value:
            direction = 1
        elif value < self.prev_value:
            direction = -1
        self.prev_value = value

        knob_event: KnobControl.KnobEvent = KnobControl.KnobEvent(
            value,
            unit_value=float(value) / 127,
            inverse_value=127 - value,
            inverse_unit_value=(127 - float(value)) / 127,
            symmetry_value=value - 127 // 2,
            symmetry_unit_value=(value - half_value) / half_value,
            direction=direction
        )
        events[KnobControl.Events.ALL] = knob_event
        events[KnobControl.Events.UNIT_VALUE] = knob_event.unit_value
        events[KnobControl.Events.INVERSE_VALUE] = knob_event.inverse_value
        events[KnobControl.Events.INVERSE_UNIT_VALUE] = knob_event.inverse_unit_value
        events[KnobControl.Events.SYMMETRY_VALUE] = knob_event.symmetry_value
        events[KnobControl.Events.SYMMETRY_UNIT_VALUE] = knob_event.symmetry_unit_value
        events[KnobControl.Events.DIRECTION] = knob_event.direction

        return events
    def __init__(self, name: str, channel: int, identifier: int, status: int = MIDI_STATUS.CC_STATUS, playable=False, feedback=False, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super().__init__(name, channel, identifier, playable, status,
                         feedback, feedback_process, default_color, blackout_color, skin)
        self.prev_value: int = 0

    def _on_value(self, e):
        events: list = self.generate_event(e)
        for event in events:
            setattr(self, "_{}".format(event), events[event])
            self.notify(event, events[event])

    def __str__(self) -> str:
        return f"{self.name} {self.status}:{self.channel}:{self.identifier}"

    def __repr__(self) -> str:
        return f"{self.name} {self.status}:{self.channel}:{self.identifier}"

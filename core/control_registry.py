from dataclasses import dataclass
from typing import List, Tuple, Dict
from .event import GlobalEventObject
from ..util.midi import MIDI_STATUS
from .state import StateBase
from ..util.functions import contains, get_index
from ..api.fl_class import flMidiMsg

ControlID = Tuple[int, int, int]

@dataclass
class ControlEntry:
    id: ControlID
    control: any
    active: bool = False

Registry = Dict[ControlID, List[ControlEntry]]

class ControlRegistry(StateBase):
    map: Registry = dict()
    modifiers: dict = dict()
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ControlRegistry, cls).__new__(
                cls, *args, **kwargs)
        return cls.instance

    def __init__(self) -> None:
        super(ControlRegistry, self).__init__()
        self.event_object = GlobalEventObject()

    def _create_control_id(self, control) -> ControlID:
        return (control.channel, control.identifier, (control.status + control.channel))

    def add_modifier(self, modifier, control):
        ControlRegistry.modifiers[control.name] = modifier

    def remove_modifier(self, modifier, control):
        mod = ControlRegistry.modifiers.get(control.name, None)
        if mod is not None and mod == modifier:
            del ControlRegistry.modifiers[control.name]

    def _create_control_ids(self, control) -> List[ControlID]:
        id_list = []
        id_list.append( self._create_control_id(control))
        if control.status == MIDI_STATUS.NOTE_ON_STATUS:
            id_list.append((control.channel, control.identifier, (control.channel + MIDI_STATUS.NOTE_OFF_STATUS)))
        return id_list

    def activate_control(self, control):
        for id_tuple in self._create_control_ids(control):
            if ControlRegistry.map.get(id_tuple) == None:
                return
            for entry in ControlRegistry.map[id_tuple]:
                if entry.control.name == control.name:
                    entry.active = True

    def get_modifer_from_control(self, control):
        for modifier in ControlRegistry.modifiers:
            if modifier['control'] == control:
                return modifier['modifier']
        return None

    def deactivate_control(self, control):
        for id_tuple in self._create_control_ids(control):
            if ControlRegistry.map.get(id_tuple) == None:
                return
            for entry in ControlRegistry.map[id_tuple]:
                if entry.control.name == control.name:
                    entry.active = False

    def register_control(self, control):
        for id_tuple in self._create_control_ids(control):
            control_entry = ControlEntry(id_tuple, control)
            if ControlRegistry.map.get(id_tuple) == None:
                ControlRegistry.map[id_tuple] = []
            if not contains(ControlRegistry.map[id_tuple], lambda cEntry: cEntry == control_entry):
                ControlRegistry.map[id_tuple].insert(0, control_entry)

    def unregister_control(self, control):
        for id_tuple in self._create_control_ids(control):
            control_entry = ControlEntry(id_tuple, control)
            if ControlRegistry.map.get(id_tuple) == None:
                return
            control_entries: list[ControlEntry] = ControlRegistry.map[id_tuple]
            if contains(control_entries, lambda cEntry: cEntry == control_entry):
                c_index = control_entries.index(control_entry)
                del control_entries[c_index]

    def is_control_modified(self, control):
        return ControlRegistry.modifiers.get(control.name, None)

    def HandleMidiMsg(self, event: flMidiMsg):
        id_tuple = (event.midiChan, event.data1, event.status)
        controls: list = ControlRegistry.map.get(id_tuple)
        # Get the control on the top of the registry stack for this event_id(channel, identifier)
        # Notify the listeners in the event registry and execute feedback, translation and playable.
        if controls and len(controls) > 0:

            control_entry = controls[0]
            control = control_entry.control
            if control_entry.active:

                modifier_control = self.is_control_modified(control)
                if modifier_control is not None:
                    event_id = "{}.{}".format(modifier_control.name, "value")
                    event.handled = not modifier_control.playable
                    self.event_object.notify_listeners(event_id, event)
                else:
                    event_id = '{}.{}'.format(control.name, 'value')
                    event.handled = not control.playable
                    self.event_object.notify_listeners(event_id, event)

                    if hasattr(control, 'feedback'):
                        if hasattr(control.feedback, '__call__'):
                            control.feedback(event, control)

                    if hasattr(control, 'translation'):
                        if hasattr(control.translation, '__call__'):
                            control.translation(event)
            else:
                print(f"Control {control.name} is not active")
                event.handled = not control.playable

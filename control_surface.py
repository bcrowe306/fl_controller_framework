from .event import GlobalEventObject, EventObject
from .component import Component
from .control_registry import ControlRegistry
from .control import ControlBase
from .state import UIState
from .fl_class import _fl

class ControlSurface(Component):
    def __init__(self, name: str,  meters: bool = False, *a, **k):
        super().__init__(name, *a, **k)
        self.meters = meters
        self.fl = _fl
        self.global_event_object = GlobalEventObject()
        self.control_registry = ControlRegistry()
        self.ui_state = UIState(self.global_event_object)

    def OnInit(self):
        self.activate()

    def OnMidiMsg(self, event):
        self.control_registry.HandleMidiMsg(event)

    def OnIdle(self):
        self.ui_state.HandleState()

    def OnUpdateBeatIndicator(self, event):
        self.global_event_object.notify_listeners('beat', event)

    def OnDeInit(self):
        self.deactivate()

    def OnRefresh(self, event):
        self.global_event_object.notify_listeners('OnRefresh', event)

    def OnUpdateMeters(self):
        self.global_event_object.notify_listeners('OnUpdateMeters')

    def _get_components(self) -> dict[str, Component]:
        components : dict[str, Component] = dict()
        for attr in dir(self):
            component = getattr(self, attr)
            if isinstance(component, Component):
                components[attr] = component
        return components

    def activate(self) -> None:
        """Activates this control surface and all member components of this control surface where component.auto_active = True"""
        super().activate()
        components = self._get_components()
        for component in components:
            if components[component].auto_active:
                components[component].activate()

    def deactivate(self):
        super().deactivate()
        components = self._get_components()
        for component in components:
            components[component].deactivate()

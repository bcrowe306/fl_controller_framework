from .core.event import GlobalEventObject
from .components.component import Component
from .core.control_registry import ControlRegistry
from .core.state import UIState
from .api.fl_class import _fl

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
        self.global_event_object.notify_listeners("OnUpdateBeatIndicator", event)

    def OnDeInit(self):
        self.deactivate()
        self._blackout()

    def _blackout(self):
        components = self._get_components()
        for component in components:
            components[component].blackout()
        controls = self._get_controls()
        for control in controls:
            controls[control].blackout()
        
    def OnRefresh(self, event):
        on_refresh_event_flags :dict[int:str] = {
            1: "HW_Dirty_Mixer_Sel",
            2: "HW_Dirty_Mixer_Display",
            4: "HW_Dirty_Mixer_Controls",
            16: "HW_Dirty_RemoteLinks",
            32: "HW_Dirty_FocusedWindow",
            64: "HW_Dirty_Performance",
            256: "HW_Dirty_LEDs",
            512: "HW_Dirty_RemoteLinkValues",
            1024: "HW_Dirty_Patterns",
            2048: "HW_Dirty_Tracks",
            4096: "HW_Dirty_ControlValues",
            8192: "HW_Dirty_Colors",
            16384: "HW_Dirty_Names",
            32768: "HW_Dirty_ChannelRackGroup",
            65536: "HW_ChannelEvent",
        }
        events: list[str] = []
        for i in range(16):
            bit_position = 1 << i
            event_flag = event & bit_position
            event_name = on_refresh_event_flags.get(event_flag)
            if event_name is not None:
                events.append(event_name)
        for event_name in events:
            self.global_event_object.notify_listeners(event_name, event)
        self.global_event_object.notify_listeners('OnRefresh', event)
        print(f"Refresh event: {event}")

    def OnUpdateMeters(self):
        self.global_event_object.notify_listeners('OnUpdateMeters')

    def OnProjectLoad(self, status: int):
        self.global_event_object.notify_listeners("OnProjectLoad", status)

    def OnDoFullRefresh(self):
        self.global_event_object.notify_listeners("OnDoFullRefresh")

    def OnDisplayZone(self):
        self.global_event_object.notify_listeners("OnDisplayZone")

    def OnUpdateLiveMode(self, lastTrack: int):
        self.global_event_object.notify_listeners("OnUpdateLiveMode", lastTrack)

    def OnDirtyMixerTrack(self, index: int):
        self.global_event_object.notify_listeners("OnDirtyMixerTrack", index)

    def OnDirtyChannel(self, index: int, flag: int):
        self.global_event_object.notify_listeners("OnDirtyChannel", index, flag)

    def OnFirstConnect(self):
        self.global_event_object.notify_listeners("OnFirstConnect")

    def OnWaitingForInput(self):
        self.global_event_object.notify_listeners("OnWaitingForInput")

    def OnSendTempMsg(self, message: str, duration: int):
        self.global_event_object.notify_listeners("OnSendTempMsg", message, duration)

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

        components = self._get_components()
        for component in components:
            components[component].deactivate()
        super().deactivate()

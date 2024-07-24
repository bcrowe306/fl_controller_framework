from .control import Control
from .component import Component
from .event import EventObject
from .state import StateBase

class Mode(EventObject, StateBase):
    """This class represents a Mode and is used to give your controller varying functionality with the same controls. Modes can have multiple components attached to them and controls that active the mode."""
    def __init__(self, name: str, components: list[Component], active_color='Default', inactive_color='Off',  *a, **k):
        super().__init__(*a, **k)
        self.name: str = name
        """Name must be unique to for Modes component it will exist."""

        self.active_color: str = active_color
        """This is the name of the color sent to the control when the mode is active. This is used to send lighting to your controller to show which mode is active. """
        self.inactive_color: str = inactive_color
        """This is the name of the color sent to the control when the mode is inactive. This is used to send lighting to your controller to show which mode is inactive. """
        self.components: list[Component] = components or []
        """A list of components to activate or deactivate with the mode."""
    
    def activate(self):
        """Activate all components. This method goes though the self.components list and runs that activate method on each component."""
        if self.isChanged('active', True):
            for component in self.components:
                component.activate()

    def deactivate(self):
        """Deactivate all components. This method goes though the self.components list and runs that deactivate method on each component."""
        if self.isChanged('active', False):
            for component in self.components:
                component.deactivate()

class ModesComponent(Component):
    """This class houses many Modes. It is used to implement different Modes for your controller. Use this along with Mode class and Components class to create different modes."""
    def __init__(self, name: str, cycle_control: Control = None, default_mode: str =None, *a, **k):
        super(ModesComponent, self).__init__(name=name, *a, **k)
        self.name: str = name
        """The name of the Component. Must be unique."""

        self.cycle_control: Control = cycle_control
        """The control used to cycle through the modes. This is useful if you only want one Button to switch modes, you can cycle through them with this control."""

        self.default_mode: str = default_mode
        """The default mode to activate with the ModeComponent is activated."""

        self.modes: dict[str, Mode] = {}
        """A dictionary of str, Mode. This attaches each mode to a string. The string can then be used to activate the mode."""

        self._controls = dict()
        self._active_mode: Mode = None
        self._previous_mode: Mode = None

    def _get_components(self):
        """Gets all controls on this Component instance"""
        member_components = dict()
        for attr in dir(self):
            member_component = getattr(self, attr)
            if isinstance(member_component, Component):
                member_components[attr] = member_component
        return member_components

    def add_mode(self, mode: Mode, behavior: str ='default'):
        """Add a mode to the collection"""
        self.modes[mode.name] = mode

    def add_control(self, mode_name: str, control: Control, event_name: str ='pressed') -> None:
        """Add controls to activate a specified mode. The event that is passed here is used to switch to the mode specified by mode_name arg."""
        setattr(self, control.name, control)
        self._controls[mode_name] = (control, event_name)

    def _get_ctrl_from_mode_name(self, mode_name: str) -> Control:
        control_tuple = self._controls.get(mode_name)
        if control_tuple:
            return control_tuple[0]

    def set_active_mode(self, mode_name: str) -> None:
        """Sets the active mode using the mode_name arg."""
        if self.isChanged('active_mode', mode_name):
            if self._active_mode:
                self.__deactivate_current_mode()
                self._previous_mode = self._active_mode
            self.__activate_mode(mode_name)
            self.fl.ui.setHintMsg('Active Mode: {}'.format(mode_name))
            self.notify('mode_changed', mode_name)
        else:
            if not self._active_mode.getValue('active'):
                self.__activate_mode(mode_name)

    def __activate_mode(self, mode_name: str) -> None:
        self._active_mode = self.modes[mode_name]
        self._active_mode.activate()
        control: Control = self._get_ctrl_from_mode_name(mode_name)
        if control is not None:
            control.set_light(self._active_mode.active_color)

    def __deactivate_current_mode(self) -> None:
        self._active_mode.deactivate()
        control: Control = self._get_ctrl_from_mode_name(self._active_mode.name)
        if control is not None:
            control.set_light(self._active_mode.inactive_color)

    def _generate_mode_name(self, mode_name: str):
        def call_mode(*a, **k):
            self._on_control_event(mode_name)
        return call_mode

    def activate(self) -> None:
        """Activates this Mode Component. This will activate the default mode specified during object instantiation."""            
        super(ModesComponent, self).activate()
        for mode_name in self._controls:
            (control, event_name) = self._controls[mode_name]
            event_id = '{}.{}'.format(control.name, event_name)
            self.global_event_object.subscribe( event_id, self._generate_mode_name(mode_name) )
            setattr(self, control.name, control)
        if self.default_mode is not None and self.default_mode != "":
            self.set_active_mode(self.default_mode)

    def _on_control_event(self, mode_name) -> None:
        self.set_active_mode(mode_name)

    def deactivate(self) -> None:
        """Deactivates the Modes Component."""
        for mode_name in self._controls:
            control_tuple = self._controls[mode_name]
            control: Control = control_tuple[0]
            event_name = control_tuple[1]
            event_id = '{}.{}'.format(control.name, event_name)
            self.global_event_object.unsubscribe(
                event_id, self._generate_mode_name(mode_name))
        if self._active_mode:
            self._active_mode.deactivate()
        super(ModesComponent, self).deactivate()

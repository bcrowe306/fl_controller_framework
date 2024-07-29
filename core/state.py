__pdoc__ = {
    "_fl": False,
}
from .event import EventObject
from ..util.functions import safe_getattr
from ..api.fl_class import _fl

class StateBase():
    """This is a base class the implements a basic state pattern. It has one method that checks the change of state, using a instance dictionary."""
    def __init__(self) -> None:
        self._state = dict()

    def isChanged(self, state: str, value: any) -> bool:
        """This is the method that checks for state changes. It takes the state represented as a string, and the value for comparison.
            It returns true is the value passed into the function is different from the value stored in the dictionary. It also updates the value in the dictionary with the one passed into the function.
        """
        changed = False
        current_state = self._state.get(state)
        if current_state == None:
            changed = True
            self._state[state] = value
        else:
            if value != current_state:
                changed = True
        self._state[state] = value
        return changed
    def getValue(self, state: str) -> any:
        return  self._state.get(state)

class StateObject(object):
    def __init__(self, event_object: EventObject) -> None:
        super(StateObject, self).__init__()
        self.event_object = event_object
        self.state = dict()

    def HandleState(self, event_id: str, value: any):
        if self.state.get(event_id) == None:
            self.event_object.notify_listeners(event_id, value)
        else:
            if value != self.state.get(event_id):
                self.event_object.notify_listeners(event_id, value)
        self.state[event_id] = value


class UIState(StateObject):
    """This class handles the UI events sent from FL Studio."""
    def __init__(self, event_object: EventObject) -> None:
        super(UIState, self).__init__(event_object)
        self.fl = _fl

    def HandleState(self):
        """This method handles the UI events sent from FL Studio. It is patched into the onIdle function.
            When onIdel is called, this method loops through the registered observers in the global event object. For every event_id that is registered, it calls that list of observer functions.
            These event registration is called in the components/controls. The pattern for event_ids is [module_name].[function].
            Example... If a component wants to listen for a selected channel change, the event id is "channels.selectedChannel".
            This function will split that event_id, call the corresponding FL Studio module function, check the state to see if it was changed, and if it was changed from the last onIdle call, notify the list of observer functions. 
        """
        # Loop through subscriber_map object to find what state we are listening to
        self.event_object.notify_listeners('idle')
        for event_id in list(self.event_object.observers):

            # Get the state by the event_id string
            path_list = event_id.split('.')

            # This checks to see if this event_id is for the UI state.
            module = safe_getattr(self.fl, path_list[0])
            if module != None: 
                new_state = getattr(module, path_list[1])()
                # Check to see if we have tracked this state before. If not, state has changed, call all functions subscribed
                old_state = self.state.get(event_id)
                if old_state == None:
                    self.event_object.notify_listeners(event_id, new_state)
                else:
                    # Check to see if state has changed. If so call all subscribed functions with value
                    if new_state != old_state:
                        self.event_object.notify_listeners(
                            event_id, new_state)
                self.state[event_id] = new_state
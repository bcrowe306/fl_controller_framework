"""event.py: This module contains the essential event/observer building blocks from the rest of the .. 
    Essentially, this whole framework is a bidirectional observer pattern with builtin state. Most classes in this framework inherit from EventObject class.
"""
# from .fl_class import FL
# fl = FL()

class EventObject(object):
    """This object is a base class that implements the basic observer patter. """
    def __init__(self, *a, **k):
        super(EventObject, self).__init__(*a, **k)
        self.observers: dict[str,list] = dict()
        """dictionary instance variable that houses the registry of observer functions. 
        They key for this dictionary is a str of the event_id. Events are referenced by this key and the list of observers are called by it."""

    def subscribe(self, event_id: str, func):
        """Subscribe to an event by event_id. This function add the supplied observer func to the list identified by event_id."""
        if self.observers.get(event_id) == None:
            self.observers[event_id] = []
        if(func not in self.observers[event_id]):
            self.observers[event_id].append(func)
        # if event_id == 'erase_button.pressed':
        #     for f in self.observers[event_id]:
        #         print(f.__name__)

    def unsubscribe(self, event_id: str, func):
        """Unsubscribe removed the supplied function from the list of observers by event_id."""
        handlers: list = self.observers[event_id]
        if handlers != None:
            for f in handlers:
                if f == func:
                    handlers.remove(f)
    
    def notify_listeners(self, event_id: str, *a, **k):
        """This function is called whenever a new event(event_id) is received. All functions registered by subscribe are called by the specified event_id."""
        _listeners = self.observers.get(event_id)
        if _listeners != None:
            for func in _listeners:
                if hasattr(func, '__call__'):
                    func(*a, **k)

class GlobalEventObject(EventObject):
    """This is a global event registry. This class inherits from EventObject and is used to receive the events from FL Studio. 
        It is a singleton object, and is attached to Component, and Control classes as instance variables.
        This allows Component, Controls, and Control Surface to subscribe-to and react to FL Studio events. 
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GlobalEventObject, cls).__new__(
                cls, *args, **kwargs)
        return cls.instance

    def __init__(self) -> None:
        super(GlobalEventObject, self).__init__()

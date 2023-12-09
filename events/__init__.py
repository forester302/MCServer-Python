from enums import Event
from .event import BasicEvent

from .join import JoinEvent
from .leave import LeaveEvent
from .chat import ChatEvent
from .move import MoveEvent




class EventManager():
    def __init__(self):
        self.listeners: dict[Event, list] = {}

    def add_listener(self, event: Event, listener):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)

    def remove_listener(self, event: Event, listener):
        if event not in self.listeners:
            return
        self.listeners[event].remove(listener)
        if len(self.listeners[event]) == 0:
            self.listeners.pop(event)

    def dispatch(self, event: BasicEvent):
        if event.event_type not in self.listeners:
            return
        for listener in self.listeners[event.event_type]:
            listener(event)

event_manager = EventManager()
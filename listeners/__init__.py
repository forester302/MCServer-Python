# register all listeners here
from events import event_manager
from enums import Event

from .move import move
event_manager.add_listener(Event.MOVE, move)
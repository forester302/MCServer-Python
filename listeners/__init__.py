# register all listeners here
from events import event_manager
from enums import Event

from .move import move
from .join import join
from .leave import leave
event_manager.add_listener(Event.MOVE, move)
event_manager.add_listener(Event.JOIN, join)
event_manager.add_listener(Event.LEAVE, leave)
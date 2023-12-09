from .event import BasicEvent
from enums import Event

from data import Player

class LeaveEvent(BasicEvent):
    event_type = Event.LEAVE
    def __init__(self, player: Player):
        self.player = player
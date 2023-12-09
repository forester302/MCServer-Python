from .event import BasicEvent
from enums import Event

from data import Player

class JoinEvent(BasicEvent):
    event_type = Event.JOIN
    def __init__(self, player: Player):
        self.player = player
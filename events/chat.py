from .event import BasicEvent
from enums import Event

from data import Player

class ChatEvent(BasicEvent):
    event_type = Event.CHAT
    def __init__(self, player: Player, message: str):
        self.player = player
        self.message = message
from .event import BasicEvent
from enums import Event

from data import Player

class MoveEvent(BasicEvent):
    event_type = Event.MOVE
    def __init__(self, player: Player, pos: tuple[int, int, int] = None, rot: tuple[int, int] = None, on_ground: bool = None):
        self.player = player
        self.pos = pos
        self.rot = rot
        self.on_ground = on_ground
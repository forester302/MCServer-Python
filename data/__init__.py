from .player import Player
from .connection import Connection
import uuid

config = None

connections: dict[tuple[str, int]: Connection] = {}
players: dict[uuid: Player] = {}
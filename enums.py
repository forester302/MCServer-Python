from enum import Enum

class State(Enum):
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    CONFIG = 3
    PLAY = 4

class Event(Enum):
    JOIN = 0
    LEAVE = 1
    CHAT = 2
    MOVE = 3
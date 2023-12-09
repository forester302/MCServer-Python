from typing import Any
from enums import Event

class BasicEvent:
    event_type: Event = None

    def is_set(self, name):
        return self.__getattribute__(name) is not None
    
    def get(self, name):
        return self.__getattribute__(name)
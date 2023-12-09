import asyncio
from enums import State

class Connection:
    def __init__(self, ip: str, port: int, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, state: State):
        self.ip = ip
        self.port = port
        self.reader = reader
        self.writer = writer
        self.state = state
        self.player = None

        self.open = True
        self.last_recieved_keep_alive = None
        self.keep_alive_task = None

    def set_state(self, state: State):
        if state in State:
            print(f"Changing State to {state}")
            self.state = state

    def set_player(self, player):
        self.player = player
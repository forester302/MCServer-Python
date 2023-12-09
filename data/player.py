from .connection import Connection
class Player:
    def __init__(self, connection, uuid, username, x, y, z, yaw, pitch):
        self.uuid = uuid
        self.username = username
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = True
        self.connection: Connection = connection

    def get_position(self):
        return (self.x, self.y, self.z)
    def get_rotation(self):
        return (self.yaw, self.pitch)
    
    def set_position(self, pos: tuple[float, float, float]):
        self.x, self.y, self.z = pos
    def set_rotation(self, rot: tuple[float, float]):
        self.yaw, self.pitch = rot
    def set_on_ground(self, on_ground: bool):
        self.on_ground = on_ground

    def set_connection(self, connection):
        self.connection = connection
    
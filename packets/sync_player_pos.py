from .packets import Packet
from .datatypes import Double, Float, Byte, VarInt

class SynchronizePlayerPositionPacket(Packet):
    packet_id = 0x3e
    def __init__(self):
        self.x: float = 0
        self.y: float = 0
        self.z: float = 0
        self.yaw: float = 0
        self.pitch: float = 0
        self.flags: int = 0
        self.teleport_id: int = 0

        super().__init__()
    
    def decode(self, data):
        self.x, data = Double(data).get_data_and_remaining()
        self.y, data = Double(data).get_data_and_remaining()
        self.z, data = Double(data).get_data_and_remaining()
        self.yaw, data = Float(data).get_data_and_remaining()
        self.pitch, data = Float(data).get_data_and_remaining()
        self.flags, data = Byte(data).get_data_and_remaining()
        self.teleport_id, data = VarInt(data).get_data_and_remaining()

    def construct(self):
        self.packet = Double(self.x).get_enc_data()
        self.packet += Double(self.y).get_enc_data()
        self.packet += Double(self.z).get_enc_data()
        self.packet += Float(self.yaw).get_enc_data()
        self.packet += Float(self.pitch).get_enc_data()
        self.packet += Byte(self.flags).get_enc_data()
        self.packet += VarInt(self.teleport_id).get_enc_data()

        return super().construct()
    
    def set_position(self, position: tuple[float, float, float]):
        self.x, self.y, self.z = position

    def get_position(self):
        return (self.x, self.y, self.z)

    def set_rotation(self, rotation: tuple[float, float]):
        self.yaw, self.pitch = rotation

    def get_rotation(self):
        return (self.yaw, self.pitch)

    def set_position_and_rotation(self, position: tuple[float, float, float], rotation: tuple[float, float]):
        self.x, self.y, self.z = position
        self.yaw, self.pitch = rotation

    def get_position_and_rotation(self):
        return (self.x, self.y, self.z), (self.yaw, self.pitch)

    def set_flags(self, flags: int):
        self.flags = flags

    def set_teleport_id(self, teleport_id: int):
        self.teleport_id = teleport_id
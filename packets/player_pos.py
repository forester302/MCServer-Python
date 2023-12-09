from .packets import Packet
from .datatypes import Double, Float, Boolean

class SetPlayerPositionPacket(Packet):
    packet_id = 0x16
    def __init__(self, data: bytes = None):
        self.x: float = None
        self.y: float = None
        self.z: float = None
        self.on_ground: bool = None
        super().__init__(data)
    
    def decode(self, data: bytes):
        self.x, data = Double(data).get_data_and_remaining()
        self.y, data = Double(data).get_data_and_remaining()
        self.z, data = Double(data).get_data_and_remaining()
        self.on_ground, data = Boolean(data).get_data_and_remaining()

    def construct(self):
        self.packet = Double(self.x).get_enc_data()
        self.packet += Double(self.y).get_enc_data()
        self.packet += Double(self.z).get_enc_data()
        self.packet += Boolean(self.on_ground).get_enc_data()
        return super().construct()
    
    def get_position(self):
        return (self.x, self.y, self.z)
    
    def set_position(self, position: tuple[float, float, float]):
        self.x, self.y, self.z = position
    

class SetPlayerPositionAndRotationPacket(Packet):
    packet_id = 0x17
    def __init__(self, data: bytes = None):
        self.x: float = None
        self.y: float = None
        self.z: float = None
        self.yaw: float = None
        self.pitch: float = None
        self.on_ground: bool = None
        super().__init__(data)

    def decode(self, data: bytes):
        self.x, data = Double(data).get_data_and_remaining()
        self.y, data = Double(data).get_data_and_remaining()
        self.z, data = Double(data).get_data_and_remaining()
        self.yaw, data = Float(data).get_data_and_remaining()
        self.pitch, data = Float(data).get_data_and_remaining()
        self.on_ground, data = Boolean(data).get_data_and_remaining()

    def construct(self):
        self.packet = Double(self.x).get_enc_data()
        self.packet += Double(self.y).get_enc_data()
        self.packet += Double(self.z).get_enc_data()
        self.packet += Float(self.yaw).get_enc_data()
        self.packet += Float(self.pitch).get_enc_data()
        self.packet += Boolean(self.on_ground).get_enc_data()
        return super().construct()
    
    def get_position(self):
        return (self.x, self.y, self.z)
    
    def set_position(self, position: tuple[float, float, float]):
        self.x, self.y, self.z = position

    def get_rotation(self):
        return (self.yaw, self.pitch)
    
    def set_rotation(self, rotation: tuple[float, float]):
        self.yaw, self.pitch = rotation
    

class SetPlayerRotationPacket(Packet):
    packet_id = 0x18
    def __init__(self, data: bytes = None):
        self.yaw: float = None
        self.pitch: float = None
        self.on_ground: bool = None
        super().__init__(data)

    def decode(self, data: bytes):
        self.yaw, data = Float(data).get_data_and_remaining()
        self.pitch, data = Float(data).get_data_and_remaining()
        self.on_ground, data = Boolean(data).get_data_and_remaining()

    def construct(self):
        self.packet = Float(self.yaw).get_enc_data()
        self.packet += Float(self.pitch).get_enc_data()
        self.packet += Boolean(self.on_ground).get_enc_data()
        return super().construct()
    
    def get_rotation(self):
        return (self.yaw, self.pitch)
    
    def set_rotation(self, rotation: tuple[float, float]):
        self.yaw, self.pitch = rotation
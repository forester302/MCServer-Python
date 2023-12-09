from ...packets import Packet
from ...datatypes import Byte, Float

class PlayerAbilitiesPacket(Packet):
    packet_id = 0x36
    def __init__(self, data: bytes = None):
        self.flags: int = None
        self.flying_speed: float = None
        self.fov_modifier: float = None
        super().__init__(data)

    def decode(self, data: bytes):
        self.flags, data = Byte(data[0]).get_data_and_remaining()
        self.flying_speed, data = Float(data[1:5]).get_data_and_remaining()
        self.fov_modifier, data = Float(data[5:9]).get_data_and_remaining()

    def construct(self):
        self.packet = Byte(self.flags).get_enc_data()
        self.packet += Float(self.flying_speed).get_enc_data()
        self.packet += Float(self.fov_modifier).get_enc_data()
        return super().construct()
    
    def set_flags(self, invulnerable: bool, flying: bool, allow_flying: bool, creative_mode: bool):
        self.flags = 1*invulnerable + 2*flying + 4*allow_flying + 8*creative_mode

    def set_flying_speed(self, flying_speed: float):
        self.flying_speed = flying_speed

    def set_fov_modifier(self, fov_modifier: float):
        self.fov_modifier = fov_modifier
    
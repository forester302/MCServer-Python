from ...packets import Packet
from ...datatypes import Position, Float

class SetDefaultSpawnPositionPacket(Packet):
    packet_id = 0x52
    def __init__(self):
        self.position: tuple[int, int, int] = (0, 0, 0)
        self.angle: float = 0
        super().__init__()

    def decode(self, data):
        self.position, data = Position(data).get_data_and_remaining()
        self.angle, data = Float(data).get_data_and_remaining()

    def construct(self):
        self.packet = Position(self.position).get_enc_data()
        self.packet += Float(self.angle).get_enc_data()

        return super().construct()
    
    def set_position(self, position: tuple[int, int, int]):
        self.position = position

    def set_angle(self, angle: float):
        self.angle = angle
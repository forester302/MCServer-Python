from ...packets import Packet
from ...datatypes import Long

class KeepAlivePacket(Packet):
    def __init__(self, data: bytes = None):
        self.id = None
        super().__init__(data)
    def decode(self, data: bytes):
        self.id, data = Long(data).get_data_and_remaining()
    def construct(self):
        self.packet = Long(self.id).get_enc_data()
        return super().construct()
    def set_id(self, id: int):
        self.id = id

class ClientboundKeepAlivePacket(KeepAlivePacket):
    packet_id = 0x24
    
class ServerboundKeepAlivePacket(KeepAlivePacket):
    packet_id = 0x14
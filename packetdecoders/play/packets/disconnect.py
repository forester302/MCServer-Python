from ...packets import Packet
from ...datatypes import String

class DisconnectPacket(Packet):
    packet_id = 0x1b
    def __init__(self, data: bytes = None):
        self.reason: str = None
        super().__init__(data)
    def decode(self, data: bytes):
        self.reason, data = String(data).get_data_and_remaining()
    def construct(self):
        self.packet = String(self.reason).get_enc_data()
        return super().construct()
    def set_reason(self, reason: str):
        self.reason = reason
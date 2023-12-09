from .packets import Packet
from .datatypes import VarInt, UUID

class PlayerInfoRemovePacket(Packet):
    packet_id = 0x3b
    def __init__(self):
        self.uuids = []

    def construct(self):
        self.packet = VarInt(len(self.uuids)).get_enc_data()
        for uuid in self.uuids:
            self.packet += UUID(uuid).get_enc_data()
        return super().construct()
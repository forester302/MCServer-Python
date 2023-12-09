from .datatypes import VarInt
class Packet:
    protocol_version = 764
    packet_id = 0xff
    def __init__(self, data: bytes = None):
        if data is not None:
            self.decode(data)
        self.packet = b''

    def decode(self, data: bytes):
        # default to no encoding
        self.data = data

    def construct(self):
        packet_id = VarInt(self.packet_id).get_enc_data()
        return VarInt(len(self.packet) + len(packet_id)).get_enc_data() + packet_id  + self.packet
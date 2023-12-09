from ..packets import Packet
from ..datatypes import VarInt, String, Short, Byte

class HandshakePacket(Packet):
    packet_id = 0x00
    def __init__(self, data: bytes = None):
        self.client_protocol_version = None
        self.server_address = None
        self.server_port = None
        self.next_state = None
        super().__init__(data)

    def decode(self, data):
        self.client_protocol_version, data = VarInt(data).get_data_and_remaining()
        self.server_address, data = String(data).get_data_and_remaining()
        self.server_port, data = Short(data).get_data_and_remaining()
        self.next_state, data = Byte(data).get_data_and_remaining()

    def construct(self):
        self.packet += VarInt(self.client_protocol_version).get_enc_data()
        self.packet += String(self.server_address).get_enc_data()
        self.packet += Short(self.server_port).get_enc_data()
        self.packet += Byte(self.next_state).get_enc_data()

        return super().construct()  
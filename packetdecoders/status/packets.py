from ..packets import Packet
from ..datatypes import VarInt, JSON, Long

class StatusPacket(Packet):
    packet_id = 0x00
    def __init__(self, data: bytes = None):
        self.json = None
        super().__init__(data)
    def decode(self, data):
        self.json, data = JSON(data).get_data_and_remaining()
    def construct(self):
        self.packet = JSON(self.json).get_enc_data()

        return super().construct()
    

    def set_json(self, json):
        self.json = json

class PingPacket(Packet):
    packet_id = 0x01
    def __init__(self, data: bytes = None):
        self.payload = None
        super().__init__(data)
    def decode(self, data):
        self.payload, data = Long(data).get_data_and_remaining()

    def construct(self):
        self.packet = Long(self.payload).get_enc_data()
        return super().construct()
    

    def set_payload(self, payload):
        self.payload = payload
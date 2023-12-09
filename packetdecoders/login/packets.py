from ..packets import Packet
from ..datatypes import String, UUID, VarInt

class LoginStartPacket(Packet):
    packet_id = 0x00
    def __init__(self, data: bytes = None):
        self.username = None
        self.uuid = None
        super().__init__(data)
    def decode(self, data):
        self.username, data = String(data).get_data_and_remaining()
        self.uuid, data = UUID(data).get_data_and_remaining()
    def construct(self):
        self.packet = UUID(self.uuid).get_enc_data()
        return super().construct()
    
class LoginSuccessPacket(Packet):
    packet_id = 0x02
    def __init__(self, data: bytes = None):
        self.uuid = None
        self.username = None
        self.properties = 0
        super().__init__(data)
    def decode(self, data):
        self.uuid, data = UUID(data).get_data_and_remaining()
        self.username, data = String(data).get_data_and_remaining()
        self.properties, data = VarInt(data).get_data_and_remaining()
    def construct(self):
        self.packet = UUID(self.uuid).get_enc_data()
        self.packet += String(self.username).get_enc_data()
        self.packet += VarInt(self.properties).get_enc_data()
        return super().construct()
    
    def set_uuid(self, uuid):
        self.uuid = uuid
    def set_username(self, username):
        self.username = username
from .packets import Packet

class FinishConfigPacket(Packet):
    packet_id = 0x02


class SendRegistryDataPacket(Packet):
    packet_id = 0x05
    def __init__(self, registry):
        self.registry: bytes = registry
    def construct(self):
        self.packet = self.registry
        return super().construct()
from .packets import SendRegistryDataPacket, FinishConfigPacket
from ..play import play_start
from enums import State

packets = {
    0x02: lambda packet, connection: config_end(connection),
}

def decode_packet(packet_type, connection, packet):
    if packet_type in packets:
        return packets[packet_type](packet, connection)
    else:
        return {"error": "Unknown packet type"}
    
def config_start(connection):
    print("Sending Config")
    # send registry data
    with open("packetdecoders\\config\\registry_data.nbt", "rb") as f:
        registry = f.read()
    packet = SendRegistryDataPacket(registry)
    connection.writer.write(packet.construct())

    # send end config packet
    packet = FinishConfigPacket()
    connection.writer.write(packet.construct())


def config_end(connection):
    play_start(connection)
    connection.set_state(State.PLAY)
    return {}
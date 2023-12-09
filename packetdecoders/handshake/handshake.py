from packets import HandshakePacket
from enums import State

packets = {
    0x00: lambda packet, connection: handshake(HandshakePacket(packet), connection),
}

def decode_packet(packet_type, connection, packet):
    if packet_type in packets:
        return packets[packet_type](packet, connection)
    else:
        return {"error": "Unknown packet type"}
    
def handshake(packet, connection):
    #print(f"        Protocol Version: {packet.client_protocol_version}")
    #print(f"        Server Address: {packet.server_address}")
    #print(f"        Server Port: {packet.server_port}")
    #print(f"        Next State: {packet.next_state}")
    if packet.next_state == 1:
        connection.set_state(State.STATUS)
    if packet.next_state == 2:
        connection.set_state(State.LOGIN)
    return {}
from enums import State
from .util import get_length, get_packet_type
from data import Connection

from .handshake import handshake_decode
from .status import status_decode
from .login import login_decode
from .config import config_decode
from .play import play_decode


import traceback

statuses = {
    State.HANDSHAKE: handshake_decode,
    State.STATUS: status_decode,
    State.LOGIN: login_decode,
    State.CONFIG: config_decode,
    State.PLAY: play_decode
}

def decode_packet(packet, connection: Connection):
    #loop while there is still data to be decoded
    while len(packet) > 0:
        
        if packet[:2] == b"\xfe\x01":
            #handle legacy ping
            handle_legacy_server_list_ping(connection, packet)
            return
        
        #remove next packet if exists
        length, packet = get_length(packet)
        if len(packet) < length:
            #not enough data to decode packet
            return {"error": f"Packet length {length} is longer than packet of length {len(packet)} for packet {packet}"}

        #seperate next packet out
        cur_packet, packet = packet[:length], packet[length:]

        #print(cur_packet)
        #decode packet
        packet_type, cur_packet = get_packet_type(cur_packet)

        #print(f"Packet type: {hex(packet_type)}") # printed in hex for comparison to wiki

        #handle packet based on status
        try:
            return_data = statuses[connection.state](packet_type, connection, cur_packet)
        except KeyError:
            return {"error": f"Unknown state {connection.state}"} # should never happen
        except Exception as e:
            traceback.print_exc()
            return {"error": f"Error decoding packet {packet_type}: {e} for Packet {packet_type.to_bytes() + cur_packet}"}
        
        #deal with return data
        if return_data is None:
            return None
        if return_data == {}:
            continue
        if "error" in return_data:
            return {"error": f"Error decoding packet {packet_type}: {return_data['error']} for Packet {packet_type.to_bytes() + cur_packet}, State={connection.state}"}
        if "close" in return_data:
            return {"close": True}
    return {}


def handle_legacy_server_list_ping(connection: Connection, packet):
    print("Legacy server list ping")
    connection.writer.write(b"\xff\x00\x03\x00\xa7\x00\x31\x00\x00")
    connection.writer.close()
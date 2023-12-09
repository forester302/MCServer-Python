from enums import State
from .packets import LoginStartPacket, LoginSuccessPacket
from ..config import config_start

from data import config, players
from data import Player, Connection

packets = {
    0x00: lambda packet, connection: login_start(LoginStartPacket(packet), connection),
    0x01: lambda packet, connection: {"error": "Encryption not implemented"},
    0x02: lambda packet, connection: {"error": "Plugin Response not implemented"},
    0x03: lambda packet, connection: login_success(connection)
}

def decode_packet(packet_type, connection, packet):
    if packet_type in packets:
        return packets[packet_type](packet, connection)
    else:
        return {"error": "Unknown packet type"}
    
def login_start(packet: LoginStartPacket, connection: Connection):
    username = packet.username
    uuid = packet.uuid
    print(f"Username: {username}")
    print(f"UUID: {uuid}")

    # Construct Player Object
    spawn_config = config["spawn"]
    if uuid not in players:
        player = Player(connection, uuid, username, 
                        spawn_config["x"],
                        spawn_config["y"], 
                        spawn_config["z"], 
                        spawn_config["yaw"], 
                        spawn_config["pitch"])
        players[uuid] = player
    else:
        player = players[uuid]
        player.set_connection(connection)
    connection.set_player(player)
    #TODO: put encryption / compression here

    #send login success
    response = LoginSuccessPacket()
    response.set_uuid(uuid)
    response.set_username(username)
    connection.writer.write(response.construct())
    return {}

def login_success(connection):
    print("Login success packet received")
    config_start(connection)
    connection.set_state(State.CONFIG)
    return {}
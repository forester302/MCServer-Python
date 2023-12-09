from packets import LoginPlayPacket, SynchronizePlayerPositionPacket, SetDefaultSpawnPositionPacket, ClientboundKeepAlivePacket
from packets import ServerboundKeepAlivePacket, DisconnectPacket, SetPlayerPositionPacket, SetPlayerPositionAndRotationPacket
from packets import SetPlayerRotationPacket, PlayerAbilitiesPacket

from util import run_every
from data import players, Player, Connection
import asyncio
import time

from events import event_manager, MoveEvent, JoinEvent

from enums import Event

import traceback

packets = {
    0x00: lambda packet, connection: confirm_teleport(packet, connection),
    0x14: lambda packet, connection: recieved_keep_alive(ServerboundKeepAlivePacket(packet), connection),
    0x16: lambda packet, connection: set_player_position(SetPlayerPositionPacket(packet), connection),
    0x17: lambda packet, connection: set_player_position_and_rotation(SetPlayerPositionAndRotationPacket(packet), connection),
    0x18: lambda packet, connection: set_player_rotation(SetPlayerRotationPacket(packet), connection),
    0x1f: lambda packet, connection: player_abilities(packet, connection)
}

def decode_packet(packet_type, writer, packet):
    if packet_type in packets:
        return packets[packet_type](packet, writer)
    else:
        return {"error": "Unknown packet type"}
    
def play_start(connection: Connection):

    print("Initialising Play")

    # Login(Play) Packet
    packet = LoginPlayPacket()
    packet.set_entity_id(119)
    packet.set_is_hardcore(False)
    packet.set_dimensions(["minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"])
    packet.set_max_players(20)
    packet.set_view_distance(10)
    packet.set_simulation_distance(10)
    packet.set_reduced_debug_info(False)
    packet.set_enable_respawn_screen(True)
    packet.set_do_limited_crafting(False)
    packet.set_dimension_type("minecraft:overworld")
    packet.set_dimension_name("minecraft:overworld")
    packet.set_hashed_seed(1)
    packet.set_game_mode(1)
    packet.set_previous_game_mode(3)
    packet.set_is_debug(False)
    packet.set_is_flat(False)
    packet.set_has_death_loc(False)
    packet.set_portal_cooldown(0)

    connection.writer.write(packet.construct())

    # Player Abilities Packet (start flying)
    packet = PlayerAbilitiesPacket()
    packet.set_flags(False, True, True, False)
    packet.set_flying_speed(0.05)
    packet.set_fov_modifier(0.1)

    connection.writer.write(packet.construct())

    # Syncronize Player Position Packet

    position = connection.player.get_position()
    rotation = connection.player.get_rotation()

    packet = SynchronizePlayerPositionPacket()
    packet.set_position(position)
    packet.set_rotation(rotation)
    packet.set_flags(0)
    packet.set_teleport_id(0)

    connection.writer.write(packet.construct())

    rounded_position = (round(position[0]), round(position[1]), round(position[2]))

    # Set Default Spawn Position Packet
    packet = SetDefaultSpawnPositionPacket()
    packet.set_position(rounded_position)
    packet.set_angle(connection.player.yaw)

    connection.writer.write(packet.construct())

    a = asyncio.get_event_loop()
    connection.keep_alive_task = a.create_task(run_every(1, keep_alive, connection))
    event_manager.dispatch(JoinEvent(connection.player))

async def keep_alive(connection: Connection, i):
    data = b"\x00"
    if i%10 == 0:
        packet = ClientboundKeepAlivePacket()
        packet.set_id(round(time.time()))
        data = packet.construct()
    if connection.last_recieved_keep_alive is not None and connection.last_recieved_keep_alive + 30 < round(time.time()):
        # the client hasnt responded to keep_alives for more than 30 seconds
        # disconnect them
        packet = DisconnectPacket()
        packet.set_reason("Timed out")
        connection.writer.write(packet.construct())
        connection.writer.close()
        print(f"Disconnected from {connection.writer.get_extra_info('peername')} because they timed out")
        return False
    try:
        connection.writer.write(data)
        await connection.writer.drain()
    except ConnectionResetError as e:
        print(f"Disconnected from {connection.writer.get_extra_info('peername')}")
        connection.open = False
        connection.writer.close()
        return False
    return i + 1

def recieved_keep_alive(packet: ServerboundKeepAlivePacket, connection):
    connection.last_recieved_keep_alive = packet.id
    return {}

def confirm_teleport(packet, connection):
    # Client Confirm Teleport Packet
    # Can be ignored
    return {}

def set_player_position(packet: SetPlayerPositionPacket, connection: Connection):
    event = MoveEvent(connection.player, pos=packet.get_position(), on_ground=packet.on_ground)
    event_manager.dispatch(event)
    return {}

def set_player_position_and_rotation(packet, connection):
    # Set Player Position And Rotation Packet
    player: Player = connection.player
    player.set_position((packet.x, packet.y, packet.z))
    player.set_rotation((packet.yaw, packet.pitch))
    player.set_on_ground(packet.on_ground)
    return {}

def set_player_rotation(packet, connection):
    # Set Player Rotation Packet
    player: Player = connection.player
    player.set_rotation((packet.yaw, packet.pitch))
    player.set_on_ground(packet.on_ground)
    return {}

def player_abilities(packet, connection):
    # Player Abilities Packet
    # Sent When a player starts/stops flying
    # Can be ignored for now
    return {}
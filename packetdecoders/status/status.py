from enums import State
from .packets import StatusPacket, PingPacket

packets = {
    0x00: lambda packet, connection: status_request(connection),
    0x01: lambda packet, connection: ping(PingPacket(packet), connection)
}

def decode_packet(packet_type, connection, packet):
    if packet_type in packets:
        return packets[packet_type](packet, connection)
    else:
        return {"error": "Unknown packet type"}
    
def status_request(connection):
    status = StatusPacket()
    status.set_json(status_json)
    packet = status.construct()
    connection.writer.write(packet)
    return {}

def ping(packet: PingPacket, connection):
    payload = packet.payload
    packet = PingPacket()
    packet.set_payload(payload)
    connection.writer.write(packet.construct())
    return {"close": True}





status_json = {"version": {
                        "name": "1.20.2",
                        "protocol": 764
                    },
                    "players": {
                        "max": 100,
                        "online": 5,
                        "sample": [
                            {
                            "name": "Minecraft Server",
                            "id": "40b22ba3-9d02-4d69-8a98-3e5fcd16ed92"
                            },
                            {
                            "name": "By",
                            "id": "40b22ba3-9d02-4d69-8a98-3e5fcd16ed92"
                            },
                            {
                            "name": "Forester302",
                            "id": "40b22ba3-9d02-4d69-8a98-3e5fcd16ed92"
                            },
                            {
                            "name": "Working on Joining",
                            "id": "40b22ba3-9d02-4d69-8a98-3e5fcd16ed92"
                            },
                            {
                            "name": "🐒👍",
                            "id": "40b22ba3-9d02-4d69-8a98-3e5fcd16ed92"
                            }
                        ]
                    },
                    "description": {
                        "text": "Minecraft Server Written In Python\nCurrently unable to join"
                    },
                    "enforcesSecureChat": True,
                    "previewsChat": True
                }
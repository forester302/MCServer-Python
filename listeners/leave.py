from events import LeaveEvent
from data import Player, online_players

from packets import PlayerInfoRemovePacket


def leave(event: LeaveEvent):
    online_players.remove(event.player)

    playerremovepacket = PlayerInfoRemovePacket()
    playerremovepacket.uuids.append(event.player.uuid)

    for player in online_players:
        player.connection.writer.write(playerremovepacket.construct())

from events import JoinEvent
from packets import PlayerInfoUpdatePacket, PlayerAction
from data import Player, online_players

import requests

def make_player_action(player: Player):
    playeraction = PlayerAction()
    playeraction.uuid = player.uuid
    playeraction.name = player.username
    if player.profile is None:
        json = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{player.uuid}").json()
        player.profile = json
    for property in player.profile["properties"]:
            playeraction.properties.append({
                "name": property["name"],
                "value": property["value"],
                "signed": False
            })
    # TODO: Add properties
    playeraction.has_signature_data = False
    playeraction.game_mode = 1
    playeraction.listed = True
    playeraction.ping = 0
    playeraction.display_name = False
    return playeraction

def join(event: JoinEvent):
    online_players.append(event.player)
    playerinfoupdatepacket = PlayerInfoUpdatePacket()

    otherplayerinfoupdatepacket = PlayerInfoUpdatePacket()
    otherplayerinfoupdatepacket.add_player_action(make_player_action(event.player))
    
    for player in online_players:
        playerinfoupdatepacket.add_player_action(make_player_action(player))
        player.connection.writer.write(otherplayerinfoupdatepacket.construct())

    event.player.connection.writer.write(playerinfoupdatepacket.construct())
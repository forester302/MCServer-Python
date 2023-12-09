from events import MoveEvent
from data import Player
def move(event: MoveEvent):
    # Handle Event
    player: Player = event.player
    if event.is_set("pos"):
        player.set_position(event.pos)
    if event.is_set("rot"):
        player.set_rotation(event.rot)
    if event.is_set("on_ground"):
        player.set_on_ground(event.on_ground)

    # TODO: message all other players that this player has moved
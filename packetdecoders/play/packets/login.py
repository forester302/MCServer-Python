from ...packets import Packet
from ...datatypes import Int, Boolean, Array, VarInt, String, Long, Byte, Position

class LoginPlayPacket(Packet):
    packet_id = 0x29
    def __init__(self, data: bytes = None):
        self.entity_id: int = None
        self.is_hardocre: bool = None
        self.dimensions: list[str] = None
        self.max_players: int = None
        self.view_distance: int = None
        self.simulation_distance: int = None
        self.reduced_debug_info: bool = None
        self.enable_respawn_screen: bool = None
        self.do_limited_crafting: bool = None
        self.dimension_type: str = None
        self.dimension_name: str = None
        self.hashed_seed: int = None
        self.game_mode: int = None
        self.previous_game_mode: int = None
        self.is_debug: bool = None
        self.is_flat: bool = None
        self.has_death_loc: bool = None
        self.death_dimension_name: str = None
        self.death_location: tuple[int, int, int] = None
        self.portal_cooldown: int = None

        super().__init__(data)

    def decode(self, data):
        self.entity_id, data = Int(data).get_data_and_remaining()
        self.is_hardcore, data = Boolean(data).get_data_and_remaining()
        self.dimensions, data = Array(["string"], data).get_data_and_remaining()
        self.max_players, data = VarInt(data).get_data_and_remaining()
        self.view_distance, data = VarInt(data).get_data_and_remaining()
        self.simulation_distance, data = VarInt(data).get_data_and_remaining()
        self.reduced_debug_info, data = Boolean(data).get_data_and_remaining()
        self.enable_respawn_screen, data = Boolean(data).get_data_and_remaining()
        self.do_limited_crafting, data = Boolean(data).get_data_and_remaining()
        self.dimension_type, data = String(data).get_data_and_remaining()
        self.dimension_name, data = String(data).get_data_and_remaining()
        self.hashed_seed, data = Long(data).get_data_and_remaining()
        self.game_mode, data = Byte(data).get_data_and_remaining()
        self.previous_game_mode, data = Byte(data).get_data_and_remaining()
        self.is_debug, data = Boolean(data).get_data_and_remaining()
        self.is_flat, data = Boolean(data).get_data_and_remaining()
        self.has_death_loc, data = Boolean(data).get_data_and_remaining()
        if self.has_death_loc:
            self.death_dimension_name, data = String(data).get_data_and_remaining()
            self.death_location, data = Position(data).get_data_and_remainBooleanself.ing()
        self.portal_cooldown, data = VarInt(data).get_data_and_remaining()

    def construct(self):
        self.packet = Int(self.entity_id).get_enc_data()
        self.packet += Boolean(self.is_hardcore).get_enc_data()
        self.packet += Array(["string"], self.dimensions).get_enc_data()
        self.packet += VarInt(self.max_players).get_enc_data()
        self.packet += VarInt(self.view_distance).get_enc_data()
        self.packet += VarInt(self.simulation_distance).get_enc_data()
        self.packet += Boolean(self.reduced_debug_info).get_enc_data()
        self.packet += Boolean(self.enable_respawn_screen).get_enc_data()
        self.packet += Boolean(self.do_limited_crafting).get_enc_data()
        self.packet += String(self.dimension_type).get_enc_data()
        self.packet += String(self.dimension_name).get_enc_data()
        self.packet += Long(self.hashed_seed).get_enc_data()
        self.packet += Byte(self.game_mode).get_enc_data()
        self.packet += Byte(self.previous_game_mode).get_enc_data()
        self.packet += Boolean(self.is_debug).get_enc_data()
        self.packet += Boolean(self.is_flat).get_enc_data()
        self.packet += Boolean(self.has_death_loc).get_enc_data()
        if self.has_death_loc:
            self.packet += String(self.death_dimension_name).get_enc_data()
            self.packet += Position(self.death_location).get_enc_data()
        self.packet += VarInt(self.portal_cooldown).get_enc_data()

        return super().construct()

    def set_entity_id(self, entity_id: int):
        self.entity_id = entity_id
    
    def set_is_hardcore(self, is_hardcore: bool):
        self.is_hardcore = is_hardcore
    
    def set_dimensions(self, dimensions: list[str]):
        self.dimensions = [[dimension] for dimension in dimensions]

    def set_max_players(self, max_players: int):
        self.max_players = max_players

    def set_view_distance(self, view_distance: int):
        self.view_distance = view_distance

    def set_simulation_distance(self, simulation_distance: int):
        self.simulation_distance = simulation_distance

    def set_reduced_debug_info(self, reduced_debug_info: bool):
        self.reduced_debug_info = reduced_debug_info

    def set_enable_respawn_screen(self, enable_respawn_screen: bool):
        self.enable_respawn_screen = enable_respawn_screen

    def set_do_limited_crafting(self, do_limited_crafting: bool):
        self.do_limited_crafting = do_limited_crafting

    def set_dimension_type(self, dimension_type: str):
        self.dimension_type = dimension_type

    def set_dimension_name(self, dimension_name: str):
        self.dimension_name = dimension_name

    def set_hashed_seed(self, hashed_seed: int):
        self.hashed_seed = hashed_seed

    def set_game_mode(self, game_mode: int):
        self.game_mode = game_mode

    def set_previous_game_mode(self, previous_game_mode: int):
        self.previous_game_mode = previous_game_mode

    def set_is_debug(self, is_debug: bool):
        self.is_debug = is_debug

    def set_is_flat(self, is_flat: bool):
        self.is_flat = is_flat

    def set_has_death_loc(self, has_death_loc: bool):
        self.has_death_loc = has_death_loc

    def set_death_dimension_name(self, death_dimension_name: str):
        self.death_dimension_name = death_dimension_name

    def set_death_location(self, death_location: tuple[int, int, int]):
        self.death_location = death_location

    def set_portal_cooldown(self, portal_cooldown: int):
        self.portal_cooldown = portal_cooldown
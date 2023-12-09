from .packets import Packet
from .datatypes import VarInt, UUID, String, Boolean

class PlayerInfoUpdatePacket(Packet):
    packet_id = 0x3c
    def __init__(self): 
        self.actions_mask = "00111111"
        self.player_actions_list = []

    def construct(self):
        self.packet = VarInt(int(self.actions_mask, 2)).get_enc_data()
        self.packet += VarInt(len(self.player_actions_list)).get_enc_data()
        for player_action in self.player_actions_list:
            self.packet += player_action.construct(self.actions_mask)
        return super().construct()
    
    def set_mask(self, mask):
        self.actions_mask = mask

    def add_player_action(self, player_action):
        self.player_actions_list.append(player_action)
        
class PlayerAction:
    def __init__(self):
        self.uuid = None
        self.name = None
        self.properties: list[dict] = []

        #initialise chat
        self.has_signature_data = False
        self.chat_session_id = None
        self.public_key_expiry = None
        self.public_key_size = None
        self.public_key = None
        self.public_key_sig_size = None
        self.public_key_sig = None

        self.game_mode = 0
        self.listed = True
        self.ping = 0

        self.has_display_name = False
        self.display_name = None


    def construct(self, actions_mask):
        data = UUID(self.uuid).get_enc_data()
        if actions_mask[-1] == "1":
            data += String(self.name).get_enc_data()
            data += VarInt(len(self.properties)).get_enc_data()
            for property in self.properties:
                data += String(property["name"]).get_enc_data()
                data += String(property["value"]).get_enc_data()
                data += Boolean(property["signed"]).get_enc_data()
                if property["signed"]:
                    data += String(property["signature"]).get_enc_data()
        if actions_mask[-2] == "1":
            data += Boolean(self.has_signature_data).get_enc_data()
            if self.has_signature_data:
                # TODO: I am not adding this now
                pass
        if actions_mask[-3] == "1":
            data += VarInt(self.game_mode).get_enc_data()
        if actions_mask[-4] == "1":
            data += Boolean(self.listed).get_enc_data()
        if actions_mask[-5] == "1":
            data += VarInt(self.ping).get_enc_data()
        if actions_mask[-6] == "1":
            data += Boolean(self.has_display_name).get_enc_data()
            # TODO: encode name as nbt
        return data


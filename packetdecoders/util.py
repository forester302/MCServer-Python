from .datatypes import VarInt
# assign get_packet_type to get_length
get_packet_type = get_length = lambda data: VarInt(data).get_data_and_remaining()
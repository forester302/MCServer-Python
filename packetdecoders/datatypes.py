import json
import uuid
import struct

datatypes = {
    "varint": lambda data: VarInt(data),
    "short": lambda data: Short(data),
    "int": lambda data: Int(data),
    "long": lambda data: Long(data),
    "byte": lambda data: Byte(data),
    "boolean": lambda data: Boolean(data),
    "string": lambda data: String(data),
    "json": lambda data: JSON(data),
    "uuid": lambda data: UUID(data),
    "array": lambda data: Array(data),
    "position": lambda data: Position(data),
}

class DataType:
    def __init__(self, data):
        self.remaining_data: bytes = None
        self.enc_data: bytes = None
        self.data = None
        self.length: int = None

        # if data is bytes decode it
        if isinstance(data, bytes):
            self.decode(data)
        
        #if data is not bytes assume it is decoded
        else:
            self.data = data
            self.encode()
    def decode(self, data):
        # decode before setting enc_data so that remaining data can be removed
        self.enc_data = data
        # default to no encoding
        self.data = data
        self.remaining_data = b""
    def encode(self):
        # default to no encoding
        self.enc_data = self.data
        self.length = len(self.enc_data)
    def get_length(self):
        return self.length
    
    def get_data(self):
        return self.data
    def get_enc_data(self):
        return self.enc_data
    def get_remaining_data(self):
        remaining_data = self.remaining_data
        self.remaining_data = b""
        return remaining_data
    def get_data_and_remaining(self):
        return self.data, self.get_remaining_data()

class VarInt(DataType):
    def decode(self, data):
        result = 0
        shift = 0

        for i, byte in enumerate(data):
            result |= (byte & 0x7F) << shift
            shift += 7

            if not byte & 0x80:
                break

        self.data = result
        self.enc_data = data[:i+1]
        self.remaining_data = data[i+1:]
        self.length = i+1
    
    def encode(self):
        encoded_bytes = bytearray()
        value = self.data

        while True:
            byte = value & 0x7F  # Extract the lowest 7 bits of the value
            value >>= 7  # Right shift by 7 bits to prepare the next byte
            
            if value:
                byte |= 0x80  # Set the high bit to indicate more bytes
            encoded_bytes.append(byte)
            
            if value == 0:
                break
        
        self.enc_data = bytes(encoded_bytes)


class Short(DataType):
    length = 2
    def decode(self, data):
        self.data = int.from_bytes(data[:2])
        self.enc_data = data[:2]
        self.remaining_data = data[2:]

    def encode(self):
        self.enc_data = self.data.to_bytes(2)

class Int(DataType):
    length = 4
    def decode(self, data):
        self.data = int.from_bytes(data[:4])
        self.enc_data = data[:4]
        self.remaining_data = data[4:]

    def encode(self):
        self.enc_data = self.data.to_bytes(4)

class Long(DataType):
    length = 8
    def decode(self, data):
        self.data = int.from_bytes(data[:8])
        self.enc_data = data[:8]
        self.remaining_data = data[8:]

    def encode(self):
        self.enc_data = self.data.to_bytes(8)

class Float(DataType):
    length = 4
    def decode(self, data):
        self.data = struct.unpack(">f", data[:4])[0]
        self.enc_data = data[:4]
        self.remaining_data = data[4:]

    def encode(self):
        self.enc_data = struct.pack(">f", self.data)

class Double(DataType):
    length = 8
    def decode(self, data):
        self.data = struct.unpack(">d", data[:8])[0]
        self.enc_data = data[:8]
        self.remaining_data = data[8:]

    def encode(self):
        self.enc_data = struct.pack(">d", self.data)

class Byte(DataType):
    length = 1
    def decode(self, data):
        self.data = data[0]
        self.enc_data = data[0:1]
        self.remaining_data = data[1:]

    def encode(self):
        self.enc_data = self.data.to_bytes(1) 

class Boolean(DataType):
    length = 1
    def decode(self, data):
        self.data = data[0] == 1
        self.enc_data = data[0:1]
        self.remaining_data = data[1:]
    
    def encode(self):
        self.enc_data = self.data.to_bytes(1)

class String(DataType):
    def decode(self, data):
        self.length, data = VarInt(data).get_data_and_remaining()
        self.data = bytes(data[:self.length]).decode("utf-8")
        self.enc_data = bytes(data[:self.length])
        self.remaining_data = bytes(data[self.length:])

    def encode(self):
        self.enc_data = VarInt(len(self.data)).get_enc_data() + self.data.encode("utf-8")

class JSON(DataType):
    def decode(self, data):
        string = String(data)
        self.length = string.get_length()
        self.data = json.loads(string.get_data())
        self.enc_data = string.get_enc_data()
        self.remaining_data = string.get_remaining_data()

    def encode(self):
        self.enc_data = String(json.dumps(self.data)).get_enc_data()

class UUID(DataType):
    length = 16
    def decode(self, data):
        self.data = uuid.UUID(bytes=data[:16])
        self.enc_data = data[:16]
        self.remaining_data = data[16:]
    
    def encode(self):
        self.enc_data = self.data.bytes

class Position(DataType):
    length = 26 + 26 + 12
    def decode(self, data):
        # 26 bits for x and z
        # 12 bits for y
        # 8 bytes overall
        data = data[:8]
        self.remaining_data = data[8:]

        x = (data >> 38) & 0x3FFFFFF # 26 bits?
        z = (data >> 12) & 0x3FFFFFF # 26 bits?
        y = data & 0xFFF # 12 bits?

        self.data = (x, y, z)
    
    def encode(self):
        x, y, z = self.data
        self.enc_data = (((x & 0x3FFFFFF) << 38) | ((z & 0x3FFFFFF) << 12) | (y & 0xFFF)).to_bytes(8)


# Array of single datatype / repeated datatype sequence (doesnt work with chained arrays)
class Array(DataType):
    def __init__(self, datatype: list[str], data):
        self.datatype = datatype
        if isinstance(data, list):
            self.length = len(data)
        super().__init__(data)
    def decode(self, data):
        array = []
        self.length, data = VarInt(data).get_data_and_remaining()
        for _ in range(self.length):
            current_section = []
            for type in self.datatype:
                data_item: DataType = datatypes[type](data)
                current_section.append(data_item.get_data())
                data = data_item.get_remaining_data()
            array.append(current_section)
        self.data = array
        self.enc_data = self.encode()
        self.remaining_data = data

    def encode(self):
        enc_data = VarInt(len(self.data)).get_enc_data()
        for current_section in self.data:
            for i, d_item in enumerate(current_section):
                data_item: DataType = datatypes[self.datatype[i]](d_item)
                enc_data += data_item.get_enc_data()
        self.enc_data = enc_data
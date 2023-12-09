import struct

class TAG:
    typeid = 0
    def __init__(self, name: str = None, value = None):
        self.name: str = name
        self.value = value
    def encode(self) -> bytes:
        if self.name is None:
            return self.typeid.to_bytes()
        return self.typeid.to_bytes() + len(self.name).to_bytes(2) + self.name.encode()
    def __repr__(self):
        return f"{self.__class__.__name__}()"
    

class TAG_Byte(TAG):
    typeid = 1
    def __init__(self, name: str = None, value: int = None):
        self.name: str = name
        self.value: int = value
    def encode(self) -> bytes:
        return super().encode() + self.value.to_bytes(1)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    

class TAG_Short(TAG):
    typeid = 2
    def __init__(self, name: str = None, value: int = None):
        self.name: str = name
        self.value: int = value
    def encode(self) -> bytes:
        return super().encode() + self.value.to_bytes(2)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    
    
class TAG_Int(TAG):
    typeid = 3
    def __init__(self, name: str = None, value: int = None):
        self.name: str = name
        self.value: int = value
    def encode(self) -> bytes:
        return super().encode() + self.value.to_bytes(4)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    
    
class TAG_Long(TAG):
    typeid = 4
    def __init__(self, name: str = None, value: int = None):
        self.name: str = name
        self.value: int = value
    def encode(self) -> bytes:
        return super().encode() + self.value.to_bytes(8)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    
    
class TAG_Float(TAG):
    typeid = 5
    def __init__(self, name: str = None, value: float = None):
        self.name: str = name
        self.value: int = value
    def encode(self) -> bytes:
        return super().encode() + struct.pack(">f", self.value)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    

class TAG_Double(TAG):
    typeid = 6
    def __init__(self, name: str = None, value: float = None):
        self.name: str = name
        self.value: int = value
    def encode(self) -> bytes:
        return super().encode() + struct.pack(">d", self.value)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    

class TAG_Byte_Array(TAG):
    typeid = 7
    def __init__(self, name: str = None, value: bytes = None):
        self.name: str = name
        self.value: bytes = value
    def encode(self) -> bytes:
        return super().encode() + len(self.value).to_bytes(4) + self.value
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    

class TAG_String(TAG):
    typeid = 8
    def __init__(self, name: str = None, value: str = None):
        self.name: str = name
        self.value: str = value
    def encode(self) -> bytes:
        return super().encode() + len(self.value).to_bytes(2) + self.value.encode()
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    

class TAG_List(TAG):
    typeid = 9
    def __init__(self, subtypeid: int, length: int, name: str = None, ):
        self.children = []
        self.name = name
        self.subtypeid = subtypeid
        self.length = length
    def encode(self) -> bytes:
        bytestring = b''
        for child in self.children:
            bytestring += child.encode()
        return super().encode() + self.subtypeid.to_bytes() + self.length.to_bytes(4) + bytestring
    def add_child(self, child):
        self.children.append(child)
    

class TAG_Compound(TAG):
    typeid = 10
    def __init__(self, name: str = None):
        self.children = []
        self.name = name
    def encode(self):
        bytestring = b''
        for child in self.children:
            bytestring += child.encode()
        bytestring += b'\x00'
        return super().encode() + bytestring[1:]
    def add_child(self, child):
        self.children.append(child)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

class TAG_Int_Array(TAG):
    typeid = 11
    def __init__(self, name: str = None, value: list[int] = None):
        self.name: str = name
        self.value: list[int] = value
    def encode(self) -> bytes:
        return super().encode() + len(self.value).to_bytes(4) + b''.join([i.to_bytes(4) for i in self.value])
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    
class TAG_Long_Array(TAG):
    typeid = 12
    def __init__(self, name: str = None, value: list[int] = None):
        self.name: str = name
        self.value: list[int] = value
    def encode(self) -> bytes:
        return super().encode() + len(self.value).to_bytes(4) + b''.join([i.to_bytes(8) for i in self.value])
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.value})"
    

def encode_nbt(json):
    """works as long as the data is all dicts and strings"""
    json = {"name": "Bananrama"}
    root = TAG_Compound()
    for key in json:
        #if isinstance(json[key], int):
        if isinstance(json[key], str):
            root.add_child(TAG_String(key, json[key]))
    print(root.encode())

def decode_nbt(data):
    """decode nbt data into TAGs, works most of the time"""
    data = data[1:]
    root = TAG_Compound()
    tag_stack: list[TAG_Compound] = [root]

    listlengthrem = 0
    listtype = 0

    while len(data) > 0:
        print(tag_stack)
        if isinstance(tag_stack[-1], TAG_List):
            if listlengthrem == 0:
                tag_stack.pop()
                typeid = data[0]
                data = data[1:]
            else:
                typeid = listtype
                listlengthrem -= 1
        else:
            typeid = data[0]
            data = data[1:]

            if typeid == 0:
                tag_stack.pop()
                print("TAG_END()")
                if len(tag_stack) == 0:
                    break
                continue

            length = int.from_bytes(data[0:2])
            name = data[2:2+length]
            data = data[2+length:]

        if typeid == 0:
            # end
            tag_stack.pop()
            print("TAG_END()")
            if len(tag_stack) == 0:
                break
            continue
        elif typeid == 1:
            # byte
            value = int.from_bytes(data[0:1])
            data = data[1:]
            byte_tag = TAG_Byte(name.decode(), value)
            tag_stack[-1].add_child(byte_tag)
            print(byte_tag)
        elif typeid == 2:
            # short
            value = int.from_bytes(data[0:2])
            data = data[2:]
            int_tag = TAG_Int(name.decode(), value)
            tag_stack[-1].add_child(int_tag)
            print(int_tag)
        elif typeid == 3:
            # int
            value = int.from_bytes(data[0:4])
            data = data[4:]
            int_tag = TAG_Int(name.decode(), value)
            tag_stack[-1].add_child(int_tag)
            print(int_tag)
        elif typeid == 4:
            # long
            value = int.from_bytes(data[0:8])
            data = data[8:]
            long_tag = TAG_Long(name.decode(), value)
            tag_stack[-1].add_child(long_tag)
            print(long_tag)
        elif typeid == 5:
            # float
            value = struct.unpack(">f", data[0:4])[0]
            data = data[4:]
            float_tag = TAG_Float(name.decode(), value)
            tag_stack[-1].add_child(float_tag)
            print(float_tag)
        elif typeid == 6:
            # double
            value = struct.unpack(">d", data[0:8])[0]
            data = data[8:]
            double_tag = TAG_Double(name.decode(), value)
            tag_stack[-1].add_child(double_tag)
            print(double_tag)
        elif typeid == 7:
            # byte array
            length = int.from_bytes(data[0:4])
            data = data[4:]
            byte_array = data[0:length]
            data = data[length:]
            tag_byte_array = TAG_Byte_Array(name.decode(), byte_array)
            tag_stack[-1].add_child(tag_byte_array)
        elif typeid == 8:
            # string
            length = int.from_bytes(data[0:2])
            string = data[2:2+length]
            data = data[2+length:]

            string = TAG_String(name.decode(), string.decode())
            print(string)
            tag_stack[-1].add_child(string)
        elif typeid == 9:
            # list
            subtypeid = data[0]
            length = int.from_bytes(data[1:5])
            data = data[5:]

            list_tag = TAG_List(subtypeid, length, name.decode())
            print(list_tag)
            tag_stack[-1].add_child(list_tag)
            tag_stack.append(list_tag)
            listlengthrem = length
            listtype = subtypeid
        elif typeid == 10:
            compound_tag = TAG_Compound(name.decode())
            print(compound_tag)
            tag_stack[-1].add_child(compound_tag)
            tag_stack.append(compound_tag)
        elif typeid == 11:
            # int array
            length = int.from_bytes(data[0:4])
            data = data[4:]
            int_array = []
            for i in range(length):
                int_array.append(int.from_bytes(data[0:4]))
                data = data[4:]
            tag_int_array = TAG_Int_Array(name.decode(), int_array)
            tag_stack[-1].add_child(tag_int_array)
        elif typeid == 12:
            # long array
            length = int.from_bytes(data[0:4])
            data = data[4:]
            long_array = []
            for i in range(length):
                long_array.append(int.from_bytes(data[0:8]))
                data = data[8:]
            tag_long_array = TAG_Long_Array(name.decode(), long_array)
            tag_stack[-1].add_child(tag_long_array)
            pass
        else:
            print(data)
            raise Exception(f"Unknown NBT type {typeid}")
    return root

def to_json(root):
    """convert TAGs to json"""
    json = {}
    for child in root.children:
        if isinstance(child, TAG_Compound):
            json[child.name] = to_json(child)
            continue
        if isinstance(child, TAG_List):
            json[child.name] = []
            if child.subtypeid == TAG_Compound.typeid:
                for listchild in child.children:
                    json[child.name].append(to_json(listchild))
            else:
                for listchild in child.children:
                    json[child.name].append(listchild.value)
            continue
        json[child.name] = child.value
    return json

if __name__ == "__main__":
    with open("packetdecoders\\nbt\\registry_data.nbt", "rb") as f:
        data = f.read()
    registry_data = decode_nbt(data)
    print(to_json(decode_nbt(registry_data)))
    




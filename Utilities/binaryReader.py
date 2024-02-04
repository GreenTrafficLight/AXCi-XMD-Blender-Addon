import struct
import numpy as np

class BinaryReader:

    def __init__(self, data, endian="<"):
        self.data = data
        self.endian = endian
        
        self.seek(0)

    def seek(self, offset, option=0):
        if option == 1:
            self.data.seek(offset, 1)
        elif option == 2:
            self.data.seek(offset, 2)
        else:
            self.data.seek(offset, 0)

    def tell(self):
        return self.data.tell()

    def read(self, size):
        return self.data.read(size)

    def read_char(self):
        return struct.unpack(self.endian + "c", self.read(1))[0]

    def read_byte(self):
        return struct.unpack(self.endian + "b", self.read(1))[0]
    
    def read_bytes(self, size):
        ret = bytearray()
        for i in range(size):
            ret.append(self.read_byte())
        return bytes(ret)

    def read_ubyte(self):
        return struct.unpack(self.endian + "B", self.read(1))[0]
    
    def read_ubytes(self, size):
        ubytes = []
        for i in range(size):
            ubytes.append(self.read_ubyte())
        return ubytes

    def read_short(self):
        return struct.unpack(self.endian + "h", self.read(2))[0]

    def read_ushort(self):
        return struct.unpack(self.endian + "H", self.read(2))[0]
    
    def read_ushorts(self, n):
        ushorts = []
        for i in range(n):
            ushorts.append(self.read_ushort())
        return ushorts

    def read_int(self):
        return struct.unpack(self.endian + "i", self.read(4))[0]
    
    def read_ints(self, n):
        ints = []
        for i in range(n):
            ints.append(self.read_int())
        return ints

    def read_uint(self):
        return struct.unpack(self.endian + "I", self.read(4))[0]

    def read_long(self):
        return struct.unpack(self.endian + "q", self.read(8))[0]

    def read_ulong(self):
        return struct.unpack(self.endian + "Q", self.read(8))[0]

    def read_float(self):
        return struct.unpack(self.endian + "f", self.read(4))[0]
    
    def read_floats(self, n):
        floats = []
        for i in range(n):
            floats.append(self.read_float())
        return floats

    def read_half_float(self):
        return float(np.frombuffer(self.read(2), dtype="<e")[0])
    
    def read_half_floats(self, n):
        half_floats = []
        for i in range(n):
            half_floats.append(self.read_half_float())
        return half_floats

    def read_double(self):
        return struct.unpack(self.endian + "d", self.read(8))[0]


    def read_string(self, encoding="utf-8"):
        string = ""

        while True:
            character = self.readChar()
            if character == b"\x00":
                break
            else:
                try:
                    string += str(character, encoding)
                except:
                    pass

        return string

    def bytes_to_string(self, byteArray, encoding="utf-8"):
        try:
            return byteArray.decode(encoding)
        except:
            string = ""
            for b in byteArray:
                if b < 127:
                    string += chr(b)
            return string

    def get_boolean(self, offset):
        save_position = self.tell()
        self.seek(offset)
        boolean = self.read_byte() == 1
        self.seek(save_position)

        return boolean


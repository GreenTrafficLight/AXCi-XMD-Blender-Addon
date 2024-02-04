from ..Utilities import *

class MESH:

    def __init__(self) -> None:
        self.size = 0
        self.name = ""
        self.face_buffer = []
        self.vertex_buffer = {
            "positions" : [],
            "colors" : [],
            "normals" : [],
            "texCoords" : []
            }

    def read(self, br, filepath):
        position = br.tell() - 4
        print(br.tell())
        self.size = br.read_int()
        self.name = br.bytes_to_string(br.read_bytes(56)).replace("\0", "")
        Vector((br.read_floats(3)))
        br.read_int()
        br.read_int()
        stride = br.read_int()
        print(stride)
        br.read_int()
        br.read_int()
        br.read_int()
        face_buffer_offset = br.read_int()
        face_buffer_size = br.read_int()
        br.read_int()
        vertex_buffer_count = br.read_int()
        vertex_buffer_offset = br.read_int()
        vertex_buffer_size = br.read_int()
        br.read_int()
        br.read_int()
        size = br.read_int()
        br.read_int()
        br.read_int()

        self.read_face_buffer(br, position, face_buffer_offset, face_buffer_size)

        self.read_vertex_buffer(br, position, vertex_buffer_offset, vertex_buffer_count, vertex_buffer_size, stride)

    def read_face_buffer(self, br, position, face_buffer_offset, face_buffer_size):
        br.seek(position + face_buffer_offset, 0)
        self.face_buffer = br.read_ushorts(face_buffer_size // 2)

    def read_vertex_buffer(self, br, position, vertex_buffer_offset, vertex_buffer_count, vertex_buffer_size, stride):
        br.seek(position + vertex_buffer_offset, 0)
        for i in range(vertex_buffer_count):
            self.vertex_buffer["positions"].append([br.read_float(), br.read_float(), br.read_float()])
            if stride > 12:
                self.vertex_buffer["normals"].append([br.read_float(), br.read_float(), br.read_float()])
            if stride > 24:
                self.vertex_buffer["texCoords"].append([br.read_short() / 32767, br.read_short() / 32767])
            if stride > 28:
                br.seek(4, 1)
        
        br.seek(position + vertex_buffer_offset + vertex_buffer_size, 0)

        
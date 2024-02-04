from ..Utilities import *

class MESH:

    def __init__(self) -> None:
        self.size = 0
        self.mesh_name = ""
        self.face_buffer = []
        self.vertex_buffer = {
            "positions" : [],
            "colors" : [],
            "normals" : [],
            "texCoords" : []
            }

    def read(self, br, filepath):
        position = br.tell()
        br.seek(4, 0) # Header
        self.size = br.read_int()
        self.mesh_name = br.bytesToString(br.readBytes(56)).replace("\0", "")
        Vector((br.read_floats(3)))
        br.read_int()
        stride = br.read_int()
        br.read_int()
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

        self.read_vertex_buffer(br, position, vertex_buffer_offset, vertex_buffer_count, stride)

    def read_face_buffer(self, br, position, face_buffer_offset, face_buffer_size):
        br.seek(position + face_buffer_offset, 0)
        self.face_buffer = br.read_ushorts(face_buffer_size / 2)

    def read_vertex_buffer(self, br, position, vertex_buffer_offset, vertex_buffer_count, stride):
        br.seek(position + vertex_buffer_offset, 0)
        for i in range(vertex_buffer_count):
            self.vertex_buffer["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
            if stride == 28:
                br.seek(16, 1)

        
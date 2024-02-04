from ..Utilities import *

from .MESH import *

class XMD:

    def __init__(self) -> None:
        self.meshes = []

    def read(self, br, filepath, file_size):
        br.seek(4, 0) # Header
        br.seek(4, 1)
        br.read_int()
        model_data_offset = br.read_int()

        br.seek(model_data_offset, 0)
        while br.tell() != file_size:
            header = br.bytes_to_string(br.read_bytes(4)).replace("\0", "")
            if header == "Mesh":
                self.read_mesh(br, filepath)
            elif header == "Node":
                break

        print(br.tell())

    def read_mesh(self, br, filepath):
        mesh = MESH()
        mesh.read(br, filepath)
        self.meshes.append(mesh)

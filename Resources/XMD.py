from ..Utilities import *

from .MESH import *

class XMD:

    def __init__(self) -> None:
        self.meshes = []

    def read(self, br, filepath):
        br.seek(4, 0) # Header
        br.seek(4, 0)
        br.read_int()
        meshes_offset = br.read_int()

        self.read_meshes(br, filepath, meshes_offset)

    def read_meshes(self, br, filepath, meshes_offset):
        br.seek(meshes_offset, 0)
        for i in range(5):
            mesh = MESH()
            mesh.read(br, filepath)

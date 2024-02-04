bl_info = {
	"name": "Import AXCi XMD Models format",
	"description": "Import AXCi XMD Model",
	"author": "GreenTrafficLight",
	"version": (1, 0),
	"blender": (4, 0, 0),
	"location": "File > Import > AXCi XMD Importer",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator

class ImportBin(Operator, ImportHelper):
    bl_idname = "import_scene.bin_data"
    bl_label = "Import AXCi XMD Data"

    filename_ext = ".xmd"
    filter_glob: StringProperty(default="*.xmd", options={'HIDDEN'}, maxlen=255,)

    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)

    clear_scene: BoolProperty(
        name="Clear scene",
        description="Clear everything from the scene",
        default=False,
    )

    def execute(self, context):
        from . import  import_bin
        import_bin.main(self.filepath, self.files, self.clear_scene)
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportBin.bl_idname, text="AXCi XMD")


def register():
    bpy.utils.register_class(ImportBin)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportBin)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
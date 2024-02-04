import bpy
import bmesh

import os

from math import *
from mathutils import *
from bpy_extras import image_utils

from .Utilities import *
from .Blender import*
from .Resources import *

def build_xmd(filename, data):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.name = str(filename)

    armature = ob.data
    armature.name = str(filename)

    bone_mapping = []

    for index, bfmdlnode in enumerate(data.bfmdlnodes):

        bone_mapping.append(data.bfmdlnodes_sort.names[index])

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bone = armature.edit_bones.new(data.bfmdlnodes_sort.names[index])

        bone.head = (0, 0, 0)
        bone.tail = (0, 1, 0)

        bone.matrix = bfmdlnode.compute_world_transform()
        
        if bfmdlnode.parent_index != -1:

            bone.parent = armature.edit_bones[data.bfmdlnodes_sort.names[bfmdlnode.parent_index]]
            bone.matrix = armature.edit_bones[data.bfmdlnodes_sort.names[bfmdlnode.parent_index]].matrix @ bone.matrix


    bpy.ops.object.mode_set(mode='OBJECT')

    for index, bfmdlmesh in enumerate(data.bfmdlmeshs):

        bfmdlmesh_name = data.bfmdlnodes_sort.names[bfmdlmesh.name_index]

        bfmdlmesh_empty = add_empty(bfmdlmesh_name)
        bfmdlmesh_empty.parent = ob

        for i in range(bfmdlmesh.start_index, bfmdlmesh.start_index + bfmdlmesh.submeshs_count):

            mesh = bpy.data.meshes.new(bfmdlmesh_name + "_" + str(i))
            obj = bpy.data.objects.new(bfmdlmesh_name + "_" + str(i), mesh)

            bpy.context.collection.objects.link(obj)

            modifier = obj.modifiers.new(armature.name, type="ARMATURE")
            modifier.object = ob

            obj.parent = bfmdlmesh_empty

            vertexList = {}
            facesList = []
            normals = []

            bm = bmesh.new()
            bm.from_mesh(mesh)

            bfmdlsubmesh = data.bfmdlsubmeshs[i]

            for j in range(len(bfmdlsubmesh.vtx.positions)):

                vertex = bm.verts.new(bfmdlsubmesh.vtx.positions[j])
                
                vertex.index =  j

                vertexList[j] = vertex

            # Set faces
            faces = bfmdlsubmesh.vtx.face_indices
            for j in range(0, len(bfmdlsubmesh.vtx.face_indices)):
                try:
                    face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
                    face.smooth = True
                    facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
                except:
                    pass

            if bfmdlsubmesh.vtx.uvs != []:

                uv_name = "UV1Map"
                uv_layer1 = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)

                for f in bm.faces:
                    for l in f.loops:
                        l[uv_layer1].uv = [bfmdlsubmesh.vtx.uvs[l.vert.index][0], 1 - bfmdlsubmesh.vtx.uvs[l.vert.index][1]]


            bm.to_mesh(mesh)
            bm.free()

            for i in range(len(bfmdlsubmesh.vtx.bone_indices)):
                if bfmdlsubmesh.vtx.bone_indices != []:
                    vg_name = str(bfmdlsubmesh.vtx.bone_indices[i]) # bone_mapping[data.test[vg]]
                    if not vg_name in obj.vertex_groups:
                        group = obj.vertex_groups.new(name=vg_name)
                    else:
                        group = obj.vertex_groups[vg_name]
                    weight = 1.0
                    if weight > 0.0:
                        group.add([i], weight, 'REPLACE')
                    # for k, vg in enumerate(bfmdlsubmesh.vtx.bone_indices[i]):
                    #     vg_name = str(vg) # bone_mapping[data.test[vg]]
                    #     if not vg_name in obj.vertex_groups:
                    #         group = obj.vertex_groups.new(name=vg_name)
                    #     else:
                    #         group = obj.vertex_groups[vg_name]
                    #     weight = 1.0
                    #     if weight > 0.0:
                    #         group.add([i], weight, 'REPLACE')

            # Set normals
            mesh.use_auto_smooth = True

            if normals != []:
                try:
                    mesh.normals_split_custom_set_from_vertices(normals)
                except:
                    pass

    ob.rotation_euler = ( radians(90), 0, 0 )


def main(filepath, files, clear_scene):
    if clear_scene:
        clearScene()

    folder = (os.path.dirname(filepath))

    for i, j in enumerate(files):

        path_to_file = (os.path.join(folder, j.name))

        file = open(path_to_file, 'rb')
        filename =  path_to_file.split("\\")[-1]
        file_extension =  os.path.splitext(path_to_file)[1]
        file_size = os.path.getsize(path_to_file)

        br = BinaryReader(file, "<")
        if file_extension == ".xmd":
            xmd = XMD()
            xmd.read(br, filepath)


    
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

    for xmd_mesh in data.meshes:

        mesh = bpy.data.meshes.new(xmd_mesh.name)
        obj = bpy.data.objects.new(xmd_mesh.name, mesh)

        bpy.context.collection.objects.link(obj)

        modifier = obj.modifiers.new(armature.name, type="ARMATURE")
        modifier.object = ob

        obj.parent = ob

        vertexList = {}
        facesList = []
        normals = []

        faces = StripToTriangle(xmd_mesh.face_buffer)

        bm = bmesh.new()
        bm.from_mesh(mesh)

        for j in range(len(xmd_mesh.vertex_buffer["positions"])):

            vertex = bm.verts.new(xmd_mesh.vertex_buffer["positions"][j])

            if xmd_mesh.vertex_buffer["normals"] != []:
                vertex.normal = xmd_mesh.vertex_buffer["normals"][j]
                normals.append(xmd_mesh.vertex_buffer["normals"][j])
            
            vertex.index =  j

            vertexList[j] = vertex

        # Set faces
        for j in range(0, len(faces)):
            try:
                face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
                face.smooth = True
                facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
            except:
                pass

        if xmd_mesh.vertex_buffer["texCoords"] != []:

            uv_name = "UV1Map"
            uv_layer1 = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)

            for f in bm.faces:
                for l in f.loops:
                    l[uv_layer1].uv = [xmd_mesh.vertex_buffer["texCoords"][l.vert.index][0], 1 - xmd_mesh.vertex_buffer["texCoords"][l.vert.index][1]]

        bm.to_mesh(mesh)
        bm.free()

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
            xmd.read(br, filepath, file_size)
            build_xmd(filename, xmd)


    
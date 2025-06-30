import sys
import types

bpy = types.ModuleType('bpy')
bpy.types = types.SimpleNamespace(Object=object)

mathutils = types.ModuleType('mathutils')
class Vector(list):
    pass
mathutils.Vector = Vector

sys.modules.setdefault('bpy', bpy)
sys.modules.setdefault('bmesh', types.ModuleType('bmesh'))
sys.modules.setdefault('mathutils', mathutils)

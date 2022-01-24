import bpy

def toggle_modifier_drawer(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("modhelper.toggle_modifiers")

def register():
    bpy.types.VIEW3D_MT_object.append(toggle_modifier_drawer)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(toggle_modifier_drawer)
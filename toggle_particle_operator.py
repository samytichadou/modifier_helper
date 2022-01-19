import bpy

class PARTHELPER_OT_toggle_particles(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "parthelper.toggle_particles"
    bl_label = "Toggles Particle Systems"
    bl_options = {"REGISTER", "UNDO"}
    
    selected : bpy.props.BoolProperty(name = "Only Selected Objects", default = True)
    toggle_particles_items = [
        ('VIEWPORT', 'Change Viewport Visibility', ""),
        ('RENDER', 'Change Render Visibility', ""),
        ('BOTH', 'Change Viewport and Render Visibility', ""),
        ]
    behavior : bpy.props.EnumProperty(name = "Behavior", items = toggle_particles_items, default = 'VIEWPORT')
    show_viewport : bpy.props.BoolProperty(name = "Show Viewport")
    show_render : bpy.props.BoolProperty(name = "Show Render")
    exclude_toggle : bpy.props.BoolProperty(name = "Use Exclusion Pattern for Object/Modifier name")
    exclude_pattern : bpy.props.StringProperty(name = "Exclusion Pattern", default = "Exclusion Pattern")
    selected_number : bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True
    
    def invoke(self, context, event):
        self.selected_number = len(context.selected_objects)
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="%i objects selected" % self.selected_number)
        row.prop(self, "selected")

        layout.prop(self, "exclude_toggle")

        row = layout.row()
        if self.exclude_toggle:
            row.enabled = True
        else:
            row.enabled = False

        row.prop(self, "exclude_pattern", text="")

        layout.prop(self, "behavior")

        row = layout.row()
        if self.behavior == 'RENDER':
            row.enabled = False
        else:
            row.enabled = True
        row.prop(self, "show_viewport", icon="RESTRICT_VIEW_OFF")

        row = layout.row()
        if self.behavior == 'VIEWPORT':
            row.enabled = False
        else:
            row.enabled = True
        row.prop(self, "show_render", icon="RESTRICT_RENDER_OFF")

    def execute(self, context):
        if self.selected:
            objects = context.selected_objects
        else:
            objects = context.scene.objects

        for ob in objects:
            if ob.type == 'MESH':
                if self.exclude_toggle and self.exclude_pattern.lower() in ob.name.lower():
                    continue
                for mod in ob.modifiers:
                    if self.exclude_toggle and self.exclude_pattern.lower() in mod.name.lower():
                        continue
                    if mod.type == "PARTICLE_SYSTEM":
                        if self.behavior in {"VIEWPORT", "BOTH"}:
                            mod.show_viewport = self.show_viewport 
                        if self.behavior in {"RENDER", "BOTH"}:
                            mod.show_render = self.show_render

        return {'FINISHED'}


def register():
    bpy.utils.register_class(PARTHELPER_OT_toggle_particles)

def unregister():
    bpy.utils.unregister_class(PARTHELPER_OT_toggle_particles)
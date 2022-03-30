import bpy

class MODHELPER_OT_toggle_modifiers(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "modhelper.toggle_modifiers"
    bl_label = "Toggles Modifiers"
    bl_options = {"REGISTER", "UNDO"}
    
    modifier_type_items = [
        ('PARTICLE_SYSTEM', 'Particle System', ""),
        ('SUBSURF', 'Subdivision Surface', ""),
        ('DISPLACE', 'Displace', ""),
        ('ARMATURE', 'Armature', ""),
        ]
    modifier_type : bpy.props.EnumProperty(name = "Type", items = modifier_type_items, default = 'PARTICLE_SYSTEM')
    selected : bpy.props.BoolProperty(name = "Only Selected Objects", default = True)
    toggle_modifiers_items = [
        ('VIEWPORT', 'Change Viewport Visibility', ""),
        ('RENDER', 'Change Render Visibility', ""),
        ('BOTH', 'Change Viewport and Render Visibility', ""),
        ]
    behavior : bpy.props.EnumProperty(name = "Behavior", items = toggle_modifiers_items, default = 'VIEWPORT')
    show_viewport : bpy.props.BoolProperty(name = "Show Viewport")
    show_render : bpy.props.BoolProperty(name = "Show Render")
    exclude_toggle : bpy.props.BoolProperty(name = "Use Exclusion Pattern for Object/Modifier name")
    exclude_pattern : bpy.props.StringProperty(name = "Exclusion Pattern", default = "Exclusion Pattern")
    include_toggle : bpy.props.BoolProperty(name = "Use Inclusion Pattern for Object/Modifier name")
    include_pattern : bpy.props.StringProperty(name = "Inclusion Pattern", default = "Inclusion Pattern")
    selected_number : 0

    @classmethod
    def poll(cls, context):
        return True
    
    def invoke(self, context, event):
        self.selected_number = len(context.selected_objects)
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout

        layout.prop(self, "modifier_type")

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

        layout.prop(self, "include_toggle")
        row = layout.row()
        if self.include_toggle:
            row.enabled = True
        else:
            row.enabled = False
        row.prop(self, "include_pattern", text="")

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
                #exclusion pattern obj name
                if self.exclude_toggle and self.exclude_pattern.lower() in ob.name.lower():
                    continue
                #inclusion pattern obj name
                chk_include = False
                if self.include_toggle and self.include_pattern.lower() in ob.name.lower():
                    chk_include = True
                for mod in ob.modifiers:
                    #exclusion pattern mod name
                    if self.exclude_toggle and self.exclude_pattern.lower() in mod.name.lower():
                        continue
                    #inclusion pattern mod name
                    if self.include_toggle and self.include_pattern.lower() not in mod.name.lower() and not chk_include:
                        continue
                    if mod.type == self.modifier_type:
                        if self.behavior in {"VIEWPORT", "BOTH"}:
                            mod.show_viewport = self.show_viewport 
                        if self.behavior in {"RENDER", "BOTH"}:
                            mod.show_render = self.show_render

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MODHELPER_OT_toggle_modifiers)

def unregister():
    bpy.utils.unregister_class(MODHELPER_OT_toggle_modifiers)
import bpy
from bl_ext.blender_org.ucupaint.common import get_active_ypaint_node

addon_keymaps = []


class ICELAYERS_OT_next_layer(bpy.types.Operator):
    bl_idname = "icelayers.next_layer"
    bl_label = "Next Layer"

    def execute(self, context):

        node = get_active_ypaint_node()

        if not node:
            self.report({'WARNING'}, "No active Ucupaint node")
            return {'CANCELLED'}

        yp = node.node_tree.yp

        if len(yp.layers) == 0:
            return {'CANCELLED'}

        yp.active_layer_index += 1

        if yp.active_layer_index >= len(yp.layers):
            yp.active_layer_index = 0

        self.report(
            {'INFO'},
            f"Layer: {yp.layers[yp.active_layer_index].name}"
        )

        return {'FINISHED'}


class ICELAYERS_OT_prev_layer(bpy.types.Operator):
    bl_idname = "icelayers.prev_layer"
    bl_label = "Previous Layer"

    def execute(self, context):

        node = get_active_ypaint_node()

        if not node:
            self.report({'WARNING'}, "No active Ucupaint node")
            return {'CANCELLED'}

        yp = node.node_tree.yp

        if len(yp.layers) == 0:
            return {'CANCELLED'}

        yp.active_layer_index -= 1

        if yp.active_layer_index < 0:
            yp.active_layer_index = len(yp.layers) - 1

        self.report(
            {'INFO'},
            f"Layer: {yp.layers[yp.active_layer_index].name}"
        )

        return {'FINISHED'}


classes = (
    ICELAYERS_OT_next_layer,
    ICELAYERS_OT_prev_layer,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:

        km = kc.keymaps.new(
            name='Image Paint',
            space_type='EMPTY'
        )

        kmi = km.keymap_items.new(
            "icelayers.next_layer",
            'R',
            'PRESS'
        )
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            "icelayers.prev_layer",
            'R',
            'PRESS',
            alt=True
        )
        addon_keymaps.append((km, kmi))

    print("IceLayers Registered")


def unregister():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("IceLayers Unregistered")


if __name__ == "__main__":
    register()
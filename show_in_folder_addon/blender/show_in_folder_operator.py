import os
import bpy

from show_in_folder_addon.core import FileExplorerLauncher

class WM_OT_ShowInFolderOperator(bpy.types.Operator):

    bl_idname = "wm.show_in_folder"
    bl_label = "Show in Folder"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved
    
    def execute(self, context):
        if not bpy.data.is_saved:
            return {"CANCELED"}

        launcher = FileExplorerLauncher(os.path.dirname(bpy.data.filepath))
        launcher.start()
        return {"FINISHED"}
    

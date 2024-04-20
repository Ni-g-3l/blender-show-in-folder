bl_info = {
    "name": "Show in Folder",
    "author": "Nig3l",
    "version": (0, 1, 0),
    "blender": (3, 5, 1),
    "location": "Interface",
    "description": "Show current file in it's folder",
    "warning": "",
    "doc_url": "",
    "category": "Interface",
}

import bpy

from show_in_folder_addon.blender.show_in_folder_operator import WM_OT_ShowInFolderOperator

RECOVER_MENU_CODE = '    layout.menu("TOPBAR_MT_file_recover")\n'


class DrawFuncStore:
    bpy_type = "TOPBAR_MT_file" # Adjust this to the correct menu type
    bpy_type_class = getattr(bpy.types, bpy_type)
    draw = None

def register():
    bpy.utils.register_class(WM_OT_ShowInFolderOperator)
    DrawFuncStore.draw = DrawFuncStore.bpy_type_class.draw

    filepath = DrawFuncStore.bpy_type_class.draw.__code__.co_filename
    if filepath == "<string>":
        return
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except:
        return

    line_start = DrawFuncStore.bpy_type_class.draw.__code__.co_firstlineno - 1

    for i in range(line_start, len(lines)):
        line = lines[i]
        if not line[0].isspace() and line.lstrip()[0] not in ("#", "\n", "\r"):
            break

    line_end = i

    # Unindent draw func by one level, since it won't sit inside a class
    lines = [l[4:] for l in lines[line_start:line_end]]

    # Find the line where you want to insert your operator
    insert_after = RECOVER_MENU_CODE
    insert_code = '    layout.operator("wm.show_in_folder", text="Show in Folder", icon=\'FILE_FOLDER\')\n'

    for i, line in enumerate(lines, 1):
        if insert_after in line:
            lines.insert(i, insert_code)
            break
    
    lines.insert(1, "    from bpy.app.translations import contexts as i18n_contexts\n")
    l = {}
    exec("".join(lines), {}, l)

    DrawFuncStore.bpy_type_class.draw = l['draw']

def unregister():
    bpy.utils.unregister_class(WM_OT_ShowInFolderOperator)

    if DrawFuncStore.draw is not None:
        DrawFuncStore.bpy_type_class.draw = DrawFuncStore.draw
        DrawFuncStore.draw = None

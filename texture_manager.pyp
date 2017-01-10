# -*- coding: utf-8 -*-
import c4d
import os
from ctypes import pythonapi, c_void_p, py_object

# localimport-v1.5_b64_lw=99
if bool(1):
    exec("""import base64 as b, zlib as z; s={}; blob=b"\
    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";exec(z.decompress(b.b64decode(blob)), s);localimport=s["localimport"]; del blob, b, z, s;""")

with localimport('class/') as importer:
    importer.disable(['Utility'])
    importer.disable(['Constant'])

    from Utility import Utility
    from Constant import Constant

const = Constant()


class MyThread(c4d.threading.C4DThread):
    utility = Utility()

    texture_found = list()
    texture_to_relocate = list()
    texture_not_found = list()

    create_ui = None


    def Main(self):
        c4d.StatusSetSpin()
        self.texture_found, self.texture_to_relocate, self.texture_not_found = self.utility.get_texture_data(self.Get())
        c4d.StatusClear()

        if self.create_ui:
            self.create_ui = False
            c4d.SpecialEventAdd(const.PLUGIN_ID, p1=1)
        else:
            c4d.SpecialEventAdd(const.PLUGIN_ID, p1=2)


class Dialog(c4d.gui.GeDialog):
    utility = Utility()

    texture_found = list()
    texture_to_relocate = list()
    texture_not_found = list()

    can_be_closed = False
    thread_get_texture = None

    def get_all_textures(self, is_update):
        self.can_be_closed = False
        c4d.StatusSetSpin()

        if self.thread_get_texture is None:
            self.thread_get_texture = MyThread()
            self.thread_get_texture.Start(c4d.THREADMODE_ASYNC)
        else:
            self.thread_get_texture.End(True)
            self.thread_get_texture = MyThread()
            self.thread_get_texture.Start(c4d.THREADMODE_ASYNC)

        if is_update:
            self.thread_get_texture.create_ui = False
        else:
            self.thread_get_texture.create_ui = True

    def create_bitmap(self, bmp, ui_id, x, y):
        if isinstance(bmp, (str, unicode)):
            path, fn = os.path.split(__file__)
            buffer_bmp = c4d.bitmaps.BaseBitmap()
            if buffer_bmp.InitWith(os.path.join(path, "res/", bmp))[0] != c4d.IMAGERESULT_OK:
                return
            bmp = buffer_bmp
        else:
            bmp = self.utility.resize_bmp(bmp, x, y)


        bc = c4d.BaseContainer()
        bc.SetLong(c4d.BITMAPBUTTON_BORDER, c4d.BORDER_NONE)
        myBitButton = self.AddCustomGui(ui_id, c4d.CUSTOMGUI_BITMAPBUTTON, "Button",
                                        c4d.BFH_CENTER | c4d.BFV_CENTER, x, y, bc)
        myBitButton.SetImage(bmp)

    def create_texture_line(self, texture_data, state, ui_id):
        icon_size = 20
        if self.GroupBegin(id=ui_id, flags=c4d.BFH_SCALEFIT | c4d.BFV_TOP, cols=10, rows=1):
            self.GroupBorderSpace(5, -2, 5, -2)

            if state == const.MISSING:
                self.create_bitmap("not_found.png", ui_id + 1, icon_size - 5, icon_size - 5)
                self.AddStaticText(ui_id + 4, c4d.BFH_LEFT, initw=300, name=texture_data["tex_name"])
                self.SetDefaultColor(ui_id + 4, c4d.COLOR_TEXT, c4d.Vector(0.79, 0, 0))

            elif state == const.RELOCATE:
                self.create_bitmap("relocate.png", ui_id + 2, icon_size - 5, icon_size - 5)
                self.AddStaticText(ui_id + 4, c4d.BFH_LEFT, initw=300, name=texture_data["tex_name"])
                self.SetDefaultColor(ui_id + 4, c4d.COLOR_TEXT, c4d.Vector(0.91, 0.622, 0))

            else:
                self.create_bitmap("found.png", ui_id + 3, icon_size - 5, icon_size - 5)
                self.AddStaticText(ui_id + 4, c4d.BFH_LEFT, initw=300, name=texture_data["tex_name"])
                self.SetDefaultColor(ui_id + 4, c4d.COLOR_TEXT, c4d.Vector(0.297, 0.72, 0.13))



            buffer_bmp = texture_data["material"].GetPreview()
            bmp = self.utility.resize_bmp(buffer_bmp, icon_size, icon_size)
            self.create_bitmap(bmp, ui_id + 5, icon_size, icon_size)

            self.AddButton(ui_id + 6, c4d.BFH_LEFT, initw=100, name=texture_data["material"].GetName())

            self.AddButton(ui_id + 7, c4d.BFH_LEFT, initw=100, name=texture_data["shader"].GetName())

            self.AddButton(ui_id + 8, c4d.BFH_LEFT, initw=100, name="replace")

            self.AddStaticText(ui_id + 9, c4d.BFH_SCALEFIT, initw=50, name=texture_data["relative_path"])

            self.AddStaticText(ui_id + 10, c4d.BFH_SCALEFIT, initw=50, name=texture_data["absolute_path"])

        self.GroupEnd()
        self.AddSeparatorH(0)

    def create_all_texture_lines(self, redraw=False):
        missing_ui_id = 0
        relocate_ui_id = 0
        found_ui_id = 0

        if redraw:
            self.LayoutFlushGroup(const.UI_MAIN_GRP)
        else:
            self.GroupBegin(const.UI_MAIN_GRP, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=1)

        if self.GroupBegin(const.UI_TEXT_GRP, flags=c4d.BFH_SCALEFIT | c4d.BFV_TOP, cols=10, rows=1):
                self.AddStaticText(const.UI_TEXT_STATE, c4d.BFH_CENTER, initw=100, name="State")
                self.AddStaticText(const.UI_TEXT_TEXNAME, c4d.BFH_CENTER, initw=300, name="Texture name")
                self.AddStaticText(const.UI_TEXT_MAT, c4d.BFH_CENTER, initw=125, name="Mat")
                self.AddStaticText(const.UI_TEXT_SHA, c4d.BFH_CENTER, initw=150, name="Shader")
                self.AddStaticText(const.UI_TEXT_REPLACE, c4d.BFH_CENTER, initw=125, name="Replace")
                self.AddStaticText(const.UI_TEXT_REL_PATH, c4d.BFH_SCALEFIT, initw=50, name="Relative path")
                self.AddStaticText(const.UI_TEXT_ABS_PATH, c4d.BFH_SCALEFIT, initw=50, name="Absolute path")
                self.AddSeparatorH(0)

        self.GroupEnd()

        if self.ScrollGroupBegin(const.UI_SCROLL_GRP, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, c4d.SCROLLGROUP_HORIZ | c4d.SCROLLGROUP_VERT, 100, 100):
            if self.GroupBegin(const.UI_GRP, flags=c4d.BFH_SCALEFIT | c4d.BFV_TOP, cols=1, rows=100000):
                for i in xrange(len(self.texture_not_found)):
                    missing_ui_id = const.MISSING * 10000 + const.STEP * i
                    self.create_texture_line(self.texture_not_found[i], const.MISSING, missing_ui_id)

                for i in xrange(len(self.texture_to_relocate)):
                    relocate_ui_id = const.RELOCATE * 10000 + const.STEP * i
                    self.create_texture_line(self.texture_to_relocate[i], const.RELOCATE, relocate_ui_id)

                for i in xrange(len(self.texture_found)):
                    found_ui_id = const.FOUND * 10000 + const.STEP * i
                    self.create_texture_line(self.texture_found[i], const.FOUND, found_ui_id)

            self.GroupEnd()
        self.GroupEnd()
        self.GroupEnd()

        self.LayoutChanged(const.UI_MAIN_GRP)

    def create_bottom_menu(self, redraw=False):
        nb_missing = len(self.texture_not_found)
        nb_relocate = len(self.texture_to_relocate)
        nb_found = len(self.texture_found)
        total_tex = nb_found + nb_missing + nb_relocate
        text = "Textures : "+str(total_tex)+" - Missing : "+str(nb_missing)+" - Need relocation : "+str(nb_relocate)

        if redraw:
            self.LayoutFlushGroup(const.UI_BOTTOM_GRP)
        else:
            self.GroupBegin(const.UI_BOTTOM_GRP, flags=c4d.BFH_SCALEFIT | c4d.BFV_BOTTOM, cols=1)

        self.AddSeparatorH(0)
        self.AddStaticText(const.UI_TEXT_BOTTOM, c4d.BFH_SCALEFIT, name=text)

        self.GroupEnd()

        self.LayoutChanged(const.UI_BOTTOM_GRP)

    def create_content(self):
        self.create_all_texture_lines()

        self.create_bottom_menu()

    def CreateLayout(self):
        self.SetTitle("Texture Manager - v" + str(const.VERSION))

        self.MenuFlushAll()
        self.GroupBeginInMenuLine()
        self.AddButton(const.MENU_BUTTON_RELOCATE_ALL, c4d.BFH_LEFT, 100, 10, name="Relocate all")
        self.AddButton(const.MENU_BUTTON_REFRESH, c4d.BFH_LEFT, 100, 10, name="Refresh")
        self.GroupEnd()

        self.get_all_textures(False)
        return True

    def refresh_ui(self, little_update=False):
        if not little_update:
            self.get_all_textures(True)
        self.create_all_texture_lines(True)
        self.create_bottom_menu(True)

    def AskClose(self):
        if self.can_be_closed:
            return False
        else:
            return True

    def CoreMessage(self, id, msg):
        if id == const.PLUGIN_ID:
            P1MSG_UN = msg.GetVoid(c4d.BFM_CORE_PAR1)

            pythonapi.PyCObject_AsVoidPtr.restype = c_void_p
            pythonapi.PyCObject_AsVoidPtr.argtypes = [py_object]
            P1MSG_EN = pythonapi.PyCObject_AsVoidPtr(P1MSG_UN)

            #1 = create content
            if P1MSG_EN == 1:
                self.texture_found = self.thread_get_texture.texture_found
                self.texture_to_relocate = self.thread_get_texture.texture_to_relocate
                self.texture_not_found = self.thread_get_texture.texture_not_found

                self.create_content()
                self.can_be_closed = True

            #Update Content
            elif P1MSG_EN == 2:
                self.texture_found = self.thread_get_texture.texture_found
                self.texture_to_relocate = self.thread_get_texture.texture_to_relocate
                self.texture_not_found = self.thread_get_texture.texture_not_found

                self.refresh_ui(True)
                self.can_be_closed = True
        return True

    def Command(self, id, msg):
        texture_list = list()
        list_id = 0
        controller_id = 0
        state = None

        if not self.can_be_closed:
            return True

        if id == const.MENU_BUTTON_REFRESH:
            self.refresh_ui()
            return True

        if id == const.MENU_BUTTON_RELOCATE_ALL:
            c4d.StopAllThreads()
            doc = c4d.documents.GetActiveDocument()

            doc.StartUndo()
            for i in reversed(xrange(len(self.texture_to_relocate))):
                shader = self.texture_to_relocate[i]["shader"]
                mat = self.texture_to_relocate[i]["material"]

                doc.AddUndo(c4d.UNDOTYPE_CHANGE, mat)
                shader[c4d.BITMAPSHADER_FILENAME] = self.texture_to_relocate[i]["absolute_path"].encode('utf8')
                mat.Update(True, True)

                self.texture_to_relocate[i]["relative_path"] = None
                self.texture_found.insert(0, self.texture_to_relocate[i])
                self.texture_to_relocate.pop(i)

            doc.EndUndo()
            c4d.EventAdd()
            self.refresh_ui(True)

            return True

        #missing
        if id > const.MISSING * 10000 and id < const.RELOCATE * 10000:
            controller_id = (id % (const.MISSING * 10000)) % const.STEP
            list_id = (id - const.MISSING * 10000) / const.STEP
            texture_list = self.texture_not_found
            state = const.MISSING

        #relocate
        elif id > const.RELOCATE * 10000 and id < const.FOUND * 10000:
            controller_id = (id % (const.RELOCATE * 10000)) % const.STEP
            list_id = (id - const.RELOCATE * 10000) / const.STEP
            texture_list = self.texture_to_relocate
            state = const.RELOCATE

        #found
        elif id > const.FOUND * 10000:
            controller_id = (id % (const.FOUND * 10000)) % const.STEP
            list_id = (id - const.FOUND * 10000) / const.STEP
            texture_list = self.texture_found
            state = const.FOUND

        #relocate
        if controller_id == 2:
            c4d.StopAllThreads()
            doc = c4d.documents.GetActiveDocument()
            shader = texture_list[list_id]["shader"]
            mat = texture_list[list_id]["material"]

            doc.StartUndo()
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, mat)
            shader[c4d.BITMAPSHADER_FILENAME] = texture_list[list_id]["absolute_path"].encode('utf8')
            mat.Update(True, True)

            doc.EndUndo()
            c4d.EventAdd()

            texture_list[list_id]["relative_path"] = None
            self.texture_found.insert(0, texture_list[list_id])
            self.texture_to_relocate.pop(list_id)
            self.refresh_ui(True)

            return True

        #remplace
        elif controller_id == 8 or controller_id == 1:
            new_file = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_IMAGES, c4d.FILESELECT_LOAD)
            if new_file is None:
                return True

            buffer_bmp = c4d.bitmaps.BaseBitmap()
            if buffer_bmp.InitWith(new_file)[0] != c4d.IMAGERESULT_OK:
                return True

            c4d.StopAllThreads()
            doc = c4d.documents.GetActiveDocument()
            shader = texture_list[list_id]["shader"]
            mat = texture_list[list_id]["material"]

            doc.StartUndo()
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, mat)
            shader[c4d.BITMAPSHADER_FILENAME] = new_file
            mat.Update(True, True)

            doc.EndUndo()
            c4d.EventAdd()

            texture_list[list_id]["tex_name"] = os.path.split(new_file.decode('utf8'))[1]
            texture_list[list_id]["relative_path"] = None
            texture_list[list_id]["absolute_path"] = new_file.decode('utf8')

            if state == const.MISSING:
                self.texture_found.insert(0, texture_list[list_id])
                self.texture_not_found.pop(list_id)

            elif state == const.RELOCATE:
                self.texture_found.insert(0, texture_list[list_id])
                self.texture_to_relocate.pop(list_id)

            elif state == const.RELOCATE:
                self.texture_found.insert(list_id, texture_list[list_id])
                self.texture_to_relocate.pop(list_id+1)

            self.refresh_ui(True)

            return True

        #select mat
        elif controller_id == 5 or controller_id == 6:
            c4d.StopAllThreads()
            doc = c4d.documents.GetActiveDocument()
            doc.SetActiveMaterial(texture_list[list_id]["material"], c4d.SELECTION_NEW)
            c4d.gui.ActiveObjectManager_SetObject(c4d.ACTIVEOBJECTMODE_MATERIAL,
                                                  texture_list[list_id]["material"],
                                                  c4d.ACTIVEOBJECTMANAGER_SETOBJECTS_OPEN)
            c4d.EventAdd()

        #select shader
        elif controller_id == 7:
            c4d.StopAllThreads()
            c4d.gui.ActiveObjectManager_SetObject(c4d.ACTIVEOBJECTMODE_SHADER,
                                                  texture_list[list_id]["shader"],
                                                  c4d.ACTIVEOBJECTMANAGER_SETOBJECTS_OPEN)
            c4d.EventAdd()


        return True

class Launcher(c4d.plugins.CommandData):
    dialog = None

    def Execute(self, doc):
        if self.dialog is None:
            self.dialog = Dialog()
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=const.PLUGIN_ID, defaultw=200, defaulth=50, xpos=-1,
                                ypos=-1)

    def RestoreLayout(self, sec_ref):
        if self.dialog is None:
            self.dialog = Dialog()
        return self.dialog.Restore(pluginid=const.PLUGIN_ID, secret=sec_ref)


if __name__ == "__main__":
    c4d.plugins.RegisterCommandPlugin(const.PLUGIN_ID, "00 - Texture Manager", 0, None, None, Launcher())

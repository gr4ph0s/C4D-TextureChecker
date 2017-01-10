# -*- coding: utf-8 -*-
import os
import c4d
import operator


class Utility(object):
    @staticmethod
    def __is_texture_relative(texture_path):
        if not len(os.path.split(texture_path)[0]):
            return False

        else:
            if texture_path[:1] == "." or texture_path[:1] == os.path.sep or texture_path[:1] == "/":
                return True

            return False

    def __get_all_texture(self):
        doc = c4d.documents.GetActiveDocument()
        all_texture = []
        mat = doc.GetFirstMaterial()
        while mat:
            sha = mat.GetFirstShader()
            all_texture += self.__recurse_find_bitmap(sha)
            mat = mat.GetNext()

        return all_texture

    def __get_tex_path_from_bmp_shader(self, sha):
        doc = c4d.documents.GetActiveDocument()
        path_tex = sha[c4d.BITMAPSHADER_FILENAME]
        if path_tex:
            if len(path_tex):
                if self.__is_texture_relative(path_tex):
                    return os.path.join(doc.GetDocumentPath(), path_tex)

                else:
                    if len(os.path.split(path_tex)):
                        return path_tex.decode('utf8')

        return None

    def __recurse_find_bitmap(self, op):
        tex = []
        while op:
            if op.CheckType(c4d.Xbitmap):
                buffer_path = self.__get_tex_path_from_bmp_shader(op)
                if buffer_path:
                    buffer_tex = {}
                    buffer_tex["path"] = buffer_path
                    buffer_tex["material"] = op.GetMain()
                    buffer_tex["shader"] = op

                    tex.append(buffer_tex)
            tex += self.__recurse_find_bitmap(op.GetDown())
            op = op.GetNext()
        return tex

    def __test_valid_picture(self, picture_path):
        bmp = c4d.bitmaps.BaseBitmap()
        result = bmp.InitWith(picture_path.encode('utf8'))
        if result[0] == c4d.IMAGERESULT_OK:
            return True
        else:
            return False

    def get_texture_data(self, thread):
        all_tex = self.__get_all_texture()

        texture_found = []
        texture_to_relocate = []
        texture_not_found = []

        doc = c4d.documents.GetActiveDocument()
        docpath = doc.GetDocumentPath()
        suggestedfolder = str()
        c4d.StatusClear()
        for tex in all_tex:
            if thread.TestBreak():
                c4d.StatusNetClear()
                break

            current_id = all_tex.index(tex)
            percent = current_id * 100 / len(all_tex)
            color = c4d.utils.MixVec(c4d.Vector(0.79, 0, 0), c4d.Vector(0.297, 0.72, 0.13), percent/100.00)
            c4d.StatusSetNetBar(percent, color)

            texture = c4d.GenerateTexturePath(docpath, tex["path"], suggestedfolder, bt=thread)
            if texture:
                texture = texture.decode('utf8')

            #Si le nom dans la texture et le meme que celui retourné c'est bon.
            if texture and texture == tex["path"]:
                #Si c'est un preset on check si c'est un preset valid
                if texture[:6] == "preset":
                    if self.__test_valid_picture(texture):
                        buffer_tex = {}
                        buffer_tex["absolute_path"] = texture
                        buffer_tex["tex_name"] = os.path.split(texture)[1]
                        buffer_tex["relative_path"] = None
                        buffer_tex["material"] = tex["material"]
                        buffer_tex["shader"] = tex["shader"]

                        texture_found.append(buffer_tex)

                    #Si l'image est corrompu
                    else:
                        buffer_tex = {}
                        buffer_tex["absolute_path"] = None
                        buffer_tex["tex_name"] = os.path.split(tex["path"])[1]
                        buffer_tex["relative_path"] = tex["path"]
                        buffer_tex["material"] = tex["material"]
                        buffer_tex["shader"] = tex["shader"]
                        texture_not_found.append(buffer_tex)

                else:
                    buffer_tex = {}
                    buffer_tex["absolute_path"] = texture
                    buffer_tex["tex_name"] = os.path.split(texture)[1]
                    buffer_tex["relative_path"] = None
                    buffer_tex["material"] = tex["material"]
                    buffer_tex["shader"] = tex["shader"]

                    texture_found.append(buffer_tex)

            #Si le nom n'est pas le même mais qu'on a trouvé une texture
            elif texture and texture != tex["path"]:

                #Si c'est pas dans les search path c'est qu'il faut relocate
                if not c4d.IsInSearchPath(tex["path"], docpath):
                    buffer_tex = {}
                    buffer_tex["absolute_path"] = texture
                    buffer_tex["tex_name"] = os.path.split(tex["path"])[1]
                    buffer_tex["relative_path"] = tex["path"]
                    buffer_tex["material"] = tex["material"]
                    buffer_tex["shader"] = tex["shader"]

                    texture_to_relocate.append(buffer_tex)

                else:
                    if self.__test_valid_picture(texture):
                        buffer_tex = {}
                        buffer_tex["absolute_path"] = texture
                        buffer_tex["tex_name"] = os.path.split(texture)[1]
                        buffer_tex["relative_path"] = None
                        buffer_tex["material"] = tex["material"]
                        buffer_tex["shader"] = tex["shader"]

                        texture_found.append(buffer_tex)
                    else:
                        buffer_tex = {}
                        buffer_tex["absolute_path"] = None
                        buffer_tex["tex_name"] = os.path.split(tex["path"])[1]
                        buffer_tex["relative_path"] = tex["path"]
                        buffer_tex["material"] = tex["material"]
                        buffer_tex["shader"] = tex["shader"]
                        texture_not_found.append(buffer_tex)

            else:
                buffer_tex = {}
                buffer_tex["absolute_path"] = None
                buffer_tex["tex_name"] = os.path.split(tex["path"])[1]
                buffer_tex["relative_path"] = tex["path"]
                buffer_tex["material"] = tex["material"]
                buffer_tex["shader"] = tex["shader"]
                texture_not_found.append(buffer_tex)

        texture_found.sort(key=operator.itemgetter('tex_name'))
        texture_to_relocate.sort(key=operator.itemgetter('tex_name'))
        texture_not_found.sort(key=operator.itemgetter('tex_name'))
        c4d.StatusNetClear()
        return texture_found, texture_to_relocate, texture_not_found

    @staticmethod
    def select_material(mats):
        doc = c4d.documents.GetActiveDocument()
        for tex in mats:
            doc.SetActiveMaterial(tex["material"], c4d.SELECTION_ADD)
            c4d.EventAdd()

    @staticmethod
    def resize_bmp(bmp, x, y):
        if bmp is None:
            return

        final_bmp = c4d.bitmaps.BaseBitmap()
        final_bmp.Init(x, y)
        bmp.ScaleBicubic(final_bmp, 0, 0, bmp.GetBw() - 1, bmp.GetBh() - 1, 0, 0, final_bmp.GetBw() - 1, final_bmp.GetBh() - 1)

        return final_bmp

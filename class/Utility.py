import os
import c4d


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

    def get_texture_data(self, thread):
        all_tex = self.__get_all_texture()

        texture_found = []
        texture_to_relocate = []
        texture_not_found = []

        doc = c4d.documents.GetActiveDocument()
        docpath = doc.GetDocumentPath()
        suggestedfolder = str()
        for tex in all_tex:
            texture = c4d.GenerateTexturePath(docpath, tex["path"], suggestedfolder, bt=thread)
            if texture:
                texture = texture.decode('utf8')

            if texture and texture == tex["path"]:
                buffer_tex = {}
                buffer_tex["absolute_path"] = texture
                buffer_tex["tex_name"] = os.path.split(texture)[1]
                buffer_tex["relative_path"] = None
                buffer_tex["material"] = tex["material"]
                buffer_tex["shader"] = tex["shader"]

                texture_found.append(buffer_tex)
            elif texture and texture != tex["path"]:
                if c4d.IsInSearchPath(tex["path"], docpath):
                    buffer_tex = {}
                    buffer_tex["absolute_path"] = texture
                    buffer_tex["tex_name"] = os.path.split(texture)[1]
                    buffer_tex["relative_path"] = None
                    buffer_tex["material"] = tex["material"]
                    buffer_tex["shader"] = tex["shader"]

                    texture_found.append(buffer_tex)
                else:
                    buffer_tex = {}
                    buffer_tex["absolute_path"] = texture
                    buffer_tex["tex_name"] = os.path.split(tex["path"])[1]
                    buffer_tex["relative_path"] = tex["path"]
                    buffer_tex["material"] = tex["material"]
                    buffer_tex["shader"] = tex["shader"]

                    texture_to_relocate.append(buffer_tex)
            else:
                buffer_tex = {}
                buffer_tex["absolute_path"] = None
                buffer_tex["tex_name"] = os.path.split(tex["path"])[1]
                buffer_tex["relative_path"] = tex["path"]
                buffer_tex["material"] = tex["material"]
                buffer_tex["shader"] = tex["shader"]
                texture_not_found.append(buffer_tex)

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

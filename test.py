# -*- coding: utf-8 -*-
import c4d
import os
import time


class Utility(object):
    @staticmethod
    def is_texture_relative(texture_path):
        if not len(os.path.split(texture_path)[0]):
            return False

        else:
            if texture_path[:1] == "." or texture_path[:1] == os.path.sep or texture_path[:1] == "/":
                return True

            return False


class TextureSearch(Utility):
    def __init__(self, doc=c4d.documents.GetActiveDocument()):
        self.doc = doc

    def set_doc(self, doc=False):
        try:
            if not doc:
                self.doc = c4d.documents.GetActiveDocument()
            else:
                self.doc = doc
            return True
        except:
            return False

    def get_doc(self, doc):
        return self.doc

    def get_all_texture(self):
        all_texture = []
        mat = self.doc.GetFirstMaterial()
        while mat:
            sha = mat.GetFirstShader()
            all_texture += self.__recurse_find_bitmap(sha)
            mat = mat.GetNext()

        return all_texture

    def __get_tex_path_from_bmp_shader(self, sha):
        path_tex = sha[c4d.BITMAPSHADER_FILENAME]
        if path_tex:
            if len(path_tex):
                if self.is_texture_relative(path_tex):
                    return os.path.join(self.doc.GetDocumentPath(), path_tex)

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


class DocPath(Utility):
    def __init__(self, doc=c4d.documents.GetActiveDocument()):
        self.doc = doc

    def set_doc(self, doc=False):
        try:
            if not doc:
                self.doc = c4d.documents.GetActiveDocument()
            else:
                self.doc = doc
            return True
        except:
            return False

    def get_doc(self, doc):
        return self.doc

    def get_all_path_to_search(self):
        buffer_all_path = []

        buffer_path = self.__get_doc_path()
        if buffer_path:
            buffer_all_path.append(buffer_path)

        buffer_path = self.__get_startup_write_path()
        if buffer_path:
            buffer_all_path.append(buffer_path)

        buffer_path = self.__get_startup_path()
        if buffer_path:
            buffer_all_path.append(buffer_path)

        buffer_path = self.__get_global_path()
        if buffer_path:
            buffer_all_path += buffer_path

        buffer_path = self.__get_xref_path()
        if buffer_path:
            buffer_all_path += buffer_path

        return set(list(buffer_all_path))

    def __recurse_find_xref(self, op):
        xref = []
        while op:
            if op.CheckType(c4d.Oxref):
                xref.append(op)
            xref += self.__recurse_find_xref(op.GetDown())
            op = op.GetNext()
        return xref

    def __get_xref_path(self):
        all_xrefs = self.__recurse_find_xref(self.doc.GetFirstObject())
        all_xrefs_path = []
        doc_path = self.__get_doc_path()

        # Pour chaque Xref
        for xref in all_xrefs:
            path_xref = xref[c4d.ID_CA_XREF_FILE]
            if path_xref:
                if len(path_xref):
                    if self.is_texture_relative(path_xref):
                        all_xrefs_path.append(os.path.split(os.path.join(doc_path, path_xref))[0])

                    else:
                        if len(os.path.split(path_xref)[0]):
                            all_xrefs_path.append(os.path.split(path_xref)[0])

        return all_xrefs_path

    def __get_doc_path(self):
        buffer_path = self.doc.GetDocumentPath()
        return buffer_path

    def __get_startup_write_path(self):
        buffer_path = c4d.storage.GeGetStartupWritePath()
        return buffer_path

    def __get_startup_path(self):
        buffer_path = c4d.storage.GeGetStartupPath()
        return buffer_path

    def __get_global_path(self):
        buffer_path = []
        for i in xrange(9):
            path = c4d.GetGlobalTexturePath(i)
            if path:
                buffer_path.append(path)

        if not len(buffer_path):
            return None

        return buffer_path


t = time.time()
a = DocPath()
all_path = a.get_all_path_to_search()

b = TextureSearch()
all_tex = b.get_all_texture()
all_relative = []
all_relative_path = []
texture_found = []
texture_not_found = []

for tex in all_tex:
    if os.path.exists(tex["path"]) and Utility.is_texture_relative(tex["path"]):
        buffer_tex = {}
        buffer_tex["absolute_path"] = tex["path"]
        buffer_tex["relative_path"] = None
        buffer_tex["material"] = tex["material"]
        buffer_tex["shader"] = tex["shader"]

        texture_found.append(buffer_tex)
    else:
        buffer_tex = {}
        buffer_tex["absolute_path"] = None
        buffer_tex["relative_path"] = tex["path"]
        buffer_tex["material"] = tex["material"]
        buffer_tex["shader"] = tex["shader"]
        all_relative.append(buffer_tex)
        all_relative_path.append(tex["path"].lower())

# on liste l'ensemble de nos (il ne dois rester que les relatives not found et les presets)
for relative in reversed(all_relative):
    if not len(all_relative):
        break

    # Si c'est un preset
    if relative["relative_path"][:7] == "preset:":
        src = c4d.bitmaps.BaseBitmap()
        if src.InitWith(relative["relative_path"].encode('utf8'))[0] == c4d.IMAGERESULT_OK:
            relative["absolute_path"] = relative["relative_path"]
            texture_found.append(relative)
            all_relative.remove(relative)
            continue

for tex_path in all_path:
    if not len(all_relative):
        break

    for (path, dirs, files) in os.walk(tex_path.decode('utf8')):
        if not len(all_relative):
            break

        # pour chaque fichier
        for name in files:

            # on check si le ficheir est dans notre liste de chemin
            if name.lower() in all_relative_path:

                # on liste l'ensemble de nos textures
                for relative in reversed(all_relative):

                    # on evite de faire un osplit pour rien
                    if name.lower() in relative["relative_path"].lower():
                        # On recup le nom du fichier
                        filename = os.path.split(relative["relative_path"])[1]

                        if name.lower() == filename.lower():
                            relative["absolute_path"] = os.path.join(path, name)
                            texture_found.append(relative)
                            all_relative.remove(relative)
                            continue

texture_not_found = all_relative
print "====================================="
print "texture found"
print texture_found
print "====================================="
print "texture not found"
for tex in texture_not_found:
    doc.SetActiveMaterial(tex["material"], c4d.SELECTION_ADD)
    print tex
print "====================================="
c4d.EventAdd()

print time.time() - t
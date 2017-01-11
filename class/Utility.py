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

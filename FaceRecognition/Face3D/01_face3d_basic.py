# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / Face3D
# 01_face3d_basic.py
#
# Basic Face 3D Network demo.
# It detects a face, generates a 3D face mesh, and draws the mesh on OSD.
#
# Required shared library on K230:
# /sdcard/libs/face3d_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
from libs.face3d_common import create_face_mesh_app
import time
import gc

fm = None


def exce_demo(pl):
    global fm
    try:
        fm = create_face_mesh_app(pl)
        print("Face3D model is large. The first detection may take a few seconds.")
        while True:
            with ScopedTiming("total", 0):
                img = pl.get_frame()
                det_boxes, mesh_res = fm.run(img)
                fm.draw_result(pl, det_boxes, mesh_res)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face3D basic demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    global fm
    if fm:
        fm.deinit()
        fm = None
    gc.collect()


if __name__ == "__main__":
    rgb888p_size = [640, 480]
    display_size = [640, 480]
    display_mode = "lcd"

    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    try:
        pl.create()
        exce_demo(pl)
    finally:
        exit_demo()
        try:
            pl.destroy()
        except Exception:
            pass

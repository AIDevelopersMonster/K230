# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / FaceOrientationDetection
# 01_face_orientation_basic.py
#
# Basic face orientation detection demo.
# It detects faces, estimates face pose, and draws a 3D cube over each face.
#
# Copy face_pose_common.py to the same folder on the TF card:
# /sdcard/FaceRecognition/FaceOrientationDetection/face_pose_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
import time
import gc

try:
    import sys
    sys.path.append("/sdcard/FaceRecognition/FaceOrientationDetection")
except Exception:
    pass

from face_pose_common import create_pose_app

fp = None


def exce_demo(pl):
    global fp
    try:
        fp = create_pose_app(pl)
        while True:
            with ScopedTiming("total", 1):
                img = pl.get_frame()
                det_boxes, pose_res = fp.run(img)
                fp.draw_result(pl, det_boxes, pose_res)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face orientation demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    global fp
    if fp:
        fp.deinit()
        fp = None
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

# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / AIvision
# 01_face_detection_basic.py
#
# What it demonstrates:
# - creates one PipeLine instance;
# - loads face_detection_320.kmodel and anchors;
# - configures AI2D preprocessing;
# - runs inference in a loop;
# - draws face rectangles on the OSD layer.
#
# Required library on K230:
# /sdcard/libs/face_aivision_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
import time
import gc

from libs.face_aivision_common import create_face_detection_app, safe_deinit

face_det = None


def exce_demo(pl):
    """Execute the current AI routine using an existing PipeLine instance."""
    global face_det
    try:
        face_det = create_face_detection_app(pl)

        while True:
            with ScopedTiming("total", 0):
                img = pl.get_frame()
                dets = face_det.run(img)
                face_det.draw_result(pl, dets)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)

    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face detection demo exit:", e)
    finally:
        safe_deinit(face_det)
        face_det = None


def exit_demo():
    """Release the current AI routine instance."""
    global face_det
    safe_deinit(face_det)
    face_det = None


if __name__ == "__main__":
    # Use the same AI image size and display size.
    # This keeps the face rectangle aligned with the camera image on the LCD.
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

# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / AIvision
# 03_face_detection_external_call.py
#
# What it demonstrates:
# - one global PipeLine can be shared by an external program;
# - the AI routine is kept in a small class with start/stop methods;
# - this is the same idea as exce_demo(pl) and exit_demo(), but wrapped
#   so beginners can clearly see the lifecycle.
#
# Required library on K230:
# /sdcard/libs/face_aivision_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
import time
import gc

from libs.face_aivision_common import create_face_detection_app, safe_deinit


class FaceDetectionRoutine:
    """Small wrapper that can be called from another program."""

    def __init__(self):
        self.app = None

    def start(self, pl):
        self.app = create_face_detection_app(pl)

    def run_once(self, pl):
        img = pl.get_frame()
        dets = self.app.run(img)
        self.app.draw_result(pl, dets)
        pl.show_image()
        return dets

    def stop(self):
        safe_deinit(self.app)
        self.app = None


# Names used in the PDF-style demos.
face_routine = FaceDetectionRoutine()


def exce_demo(pl):
    try:
        face_routine.start(pl)
        while True:
            with ScopedTiming("total", 0):
                face_routine.run_once(pl)
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("External call demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    face_routine.stop()


def main():
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
        gc.collect()


if __name__ == "__main__":
    main()

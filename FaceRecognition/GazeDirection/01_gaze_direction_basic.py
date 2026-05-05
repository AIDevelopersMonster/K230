# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / GazeDirection
# 01_gaze_direction_basic.py
#
# Basic gaze direction detection demo.
# It detects a face, estimates eye gaze pitch/yaw, and draws an arrow.
#
# Required shared library on K230:
# /sdcard/libs/gaze_direction_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
from libs.gaze_direction_common import create_eye_gaze_app, safe_deinit
import time
import gc

eg = None


def exce_demo(pl):
    global eg
    try:
        eg = create_eye_gaze_app(pl)
        while True:
            with ScopedTiming("total", 0):
                img = pl.get_frame()
                det_boxes, eye_gaze_res = eg.run(img)
                eg.draw_result(pl, det_boxes, eye_gaze_res)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Gaze direction demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    global eg
    safe_deinit(eg)
    eg = None


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

# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / GazeDirection
# 02_gaze_direction_uart.py
#
# Gaze direction detection with UART output.
# The serial packet format is: $x0,y0,x1,y1#
# x0,y0: arrow start. x1,y1: arrow end.
#
# Required shared library on K230:
# /sdcard/libs/gaze_direction_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
from libs.gaze_direction_common import create_eye_gaze_app, init_uart, safe_deinit
import time
import gc

eg = None
uart = None
pto = None


def exce_demo(pl):
    global eg, uart, pto
    uart, pto = init_uart()
    try:
        eg = create_eye_gaze_app(pl)
        while True:
            with ScopedTiming("total", 0):
                img = pl.get_frame()
                det_boxes, eye_gaze_res = eg.run(img)
                eg.draw_result(pl, det_boxes, eye_gaze_res, send_uart=True, uart=uart, pto=pto)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Gaze direction UART demo exit:", e)
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

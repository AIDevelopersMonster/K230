# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / RegisterFace
# 03_face_recognition_uart.py
#
# Live face recognition demo with UART output.
# Unknown packet: $x,y,w,h,unknown#
# Known packet:   $x,y,w,h,name,score#
#
# Required shared library on K230:
# /sdcard/libs/register_face_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
from libs.register_face_common import create_recognition_app, init_uart, safe_deinit
import time
import gc

fr = None
uart = None
pto = None

CONFIG = {
    "FACE_DET_KMODEL_PATH": "/sdcard/kmodel/face_detection_320.kmodel",
    "FACE_RECOGNITION_KMODEL_PATH": "/sdcard/kmodel/face_recognition.kmodel",
    "ANCHORS_PATH": "/sdcard/utils/prior_data_320.bin",
    "DATABASE_DIR": "/data/face_database/register/",
    "CONFIDENCE_THRESHOLD": "0.50",
    "NMS_THRESHOLD": "0.20",
    "FACE_RECOGNITION_THRESHOLD": "0.65"
}


def exce_demo(pl):
    global fr, uart, pto
    uart, pto = init_uart()
    try:
        fr = create_recognition_app(pl, CONFIG)
        while True:
            with ScopedTiming("total", 1):
                img = pl.get_frame()
                det_boxes, recg_res = fr.run(img)
                fr.draw_result(pl, det_boxes, recg_res, send_uart=True, uart=uart, pto=pto)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face recognition UART demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    global fr
    safe_deinit(fr)
    fr = None


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

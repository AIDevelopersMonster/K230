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
# - one global PipeLine can be shared by several demos;
# - the AI routine is started through exce_demo(pl);
# - the routine can be released through exit_demo();
# - this is the structure recommended for calling a routine from another file.
# ============================================

from libs.PipeLine import PipeLine
import gc

# Import the demo as a module. It contains exce_demo(pl) and exit_demo().
import 01_face_detection_basic as face_demo


def main():
    rgb888p_size = [640, 360]
    display_size = [640, 480]
    display_mode = "lcd"

    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    try:
        pl.create()
        face_demo.exce_demo(pl)
    finally:
        face_demo.exit_demo()
        try:
            pl.destroy()
        except Exception:
            pass
        gc.collect()


if __name__ == "__main__":
    main()

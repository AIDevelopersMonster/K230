# ============================================================
# Камера: классификация линий (горизонтальные / вертикальные / наклонные)
#
# Использование:
# 1. Откройте mixed_lines.png на экране
# 2. Наведите камеру K230
# 3. Увидите:
#    - зелёные линии (горизонтальные)
#    - красные линии (вертикальные)
#    - синие линии (наклонные)
# ============================================================

import time, math, gc, os
import image
from media.sensor import *
from media.display import *
from media.media import *
from libs.PipeLine import PipeLine

PICTURE_WIDTH = 160
PICTURE_HEIGHT = 120
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
ANGLE_TOLERANCE_DEG = 12


def scale_line(l):
    x1,y1,x2,y2 = l[:4]
    return (round(x1*DISPLAY_WIDTH/PICTURE_WIDTH),
            round(y1*DISPLAY_HEIGHT/PICTURE_HEIGHT),
            round(x2*DISPLAY_WIDTH/PICTURE_WIDTH),
            round(y2*DISPLAY_HEIGHT/PICTURE_HEIGHT))


def angle(l):
    x1,y1,x2,y2 = l[:4]
    a = math.degrees(math.atan2(y2-y1, x2-x1))
    return a+180 if a<0 else a


def is_h(l): return angle(l)<=ANGLE_TOLERANCE_DEG or angle(l)>=180-ANGLE_TOLERANCE_DEG

def is_v(l): return abs(angle(l)-90)<=ANGLE_TOLERANCE_DEG


def main():
    pl = PipeLine(rgb888p_size=[640,360], display_size=[DISPLAY_WIDTH,DISPLAY_HEIGHT], display_mode="LCD")
    pl.create(ch1_frame_size=[PICTURE_WIDTH,PICTURE_HEIGHT])

    try:
        while True:
            os.exitpoint()
            frame = pl.sensor.snapshot(chn=CAM_CHN_ID_1)
            lines = frame.find_line_segments(merge_distance=15, max_theta_diff=10)

            overlay = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
            overlay.clear()

            h=v=o=0
            for ln in lines:
                c = ln.line()
                if is_h(c):
                    overlay.draw_line(scale_line(c), color=(0,255,0), thickness=5); h+=1
                elif is_v(c):
                    overlay.draw_line(scale_line(c), color=(255,0,0), thickness=5); v+=1
                else:
                    overlay.draw_line(scale_line(c), color=(0,128,255), thickness=5); o+=1

            overlay.draw_string(5,5,f"H:{h} V:{v} O:{o}", color=(255,255,0), scale=2)
            Display.show_image(overlay,0,0,Display.LAYER_OSD3)
            time.sleep_us(1)

    finally:
        try: pl.destroy()
        except: pass
        gc.collect()


if __name__ == "__main__": main()

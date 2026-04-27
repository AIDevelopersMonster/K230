# ============================================================
# Камера: поиск ТОЛЬКО вертикальных линий
#
# Использование:
# - откройте vertical_lines.png на экране
# - наведите камеру K230
# - увидите красные линии (вертикальные)
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


def is_vertical(l): return abs(angle(l)-90)<=ANGLE_TOLERANCE_DEG


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

            count=0
            for ln in lines:
                if is_vertical(ln.line()):
                    overlay.draw_line(scale_line(ln.line()), color=(255,0,0), thickness=6)
                    count+=1

            overlay.draw_string(5,5,f"CAM vertical: {count}", color=(255,255,0), scale=2)
            Display.show_image(overlay,0,0,Display.LAYER_OSD3)
            time.sleep_us(1)

    finally:
        try: pl.destroy()
        except: pass
        gc.collect()


if __name__ == "__main__": main()

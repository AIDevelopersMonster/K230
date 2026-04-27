# Rectangle Detection live camera demo for Yahboom K230 / CanMV
# RU: Запустите в CanMV IDE. Наведите камеру на черный лист с белыми прямоугольниками.
# EN: Run in CanMV IDE. Point the camera at a black sheet with white rectangle outlines.

import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

PICTURE_WIDTH = 400
PICTURE_HEIGHT = 240
DISPLAY_MODE = "LCD"  # "LCD" or "VIRT"
RECT_THRESHOLD = 8000
MIN_AREA = 250

sensor = None

if DISPLAY_MODE == "VIRT":
    DISPLAY_WIDTH = ALIGN_UP(1920, 16)
    DISPLAY_HEIGHT = 1080
elif DISPLAY_MODE == "LCD":
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 480
else:
    raise ValueError("DISPLAY_MODE must be 'LCD' or 'VIRT'")

clock = time.clock()

try:
    sensor = Sensor(id=2)
    sensor.reset()
    sensor.set_framesize(width=PICTURE_WIDTH, height=PICTURE_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    if DISPLAY_MODE == "VIRT":
        Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=60)
    else:
        Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

    MediaManager.init()
    sensor.run()

    while True:
        os.exitpoint()
        clock.tick()
        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        count = 0
        for r in img.find_rects(threshold=RECT_THRESHOLD):
            x, y, w, h = r.rect()
            if w * h < MIN_AREA:
                continue
            count += 1
            img.draw_rectangle(r.rect(), color=(255, 255, 255), thickness=2)
            for p in r.corners():
                img.draw_circle(p[0], p[1], 5, color=(255, 0, 0), thickness=2)
            img.draw_string(x, max(0, y - 14), "R%d %dx%d" % (count, w, h), color=(0, 255, 0), scale=1)
            print("RECT", count, "rect=", r.rect(), "corners=", r.corners())

        img.draw_string(2, 2, "rects:%d fps:%.1f" % (count, clock.fps()), color=(0, 255, 0), scale=1)
        x0 = int((DISPLAY_WIDTH - PICTURE_WIDTH) / 2)
        y0 = int((DISPLAY_HEIGHT - PICTURE_HEIGHT) / 2)
        Display.show_image(img, x=x0, y=y0)

except KeyboardInterrupt as e:
    print("User stop", e)
except BaseException as e:
    print("Exception", e)
finally:
    if isinstance(sensor, Sensor):
        sensor.stop()
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()

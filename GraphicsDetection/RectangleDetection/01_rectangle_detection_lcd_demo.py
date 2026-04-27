# Rectangle Detection LCD demo for Yahboom K230 / CanMV
# Аналог официального примера: камера -> find_rects() -> вывод на LCD.

import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

PICTURE_WIDTH = 400
PICTURE_HEIGHT = 240

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
RECT_THRESHOLD = 8000

sensor = None
clock = time.clock()

try:
    sensor = Sensor()
    sensor.reset()

    sensor.set_framesize(width=PICTURE_WIDTH, height=PICTURE_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

    MediaManager.init()
    sensor.run()

    while True:
        os.exitpoint()
        clock.tick()

        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        rect_count = 0
        print("[Rectangle Detection Start]")

        for r in img.find_rects(threshold=RECT_THRESHOLD):
            rect_count += 1

            # Rectangle border
            img.draw_rectangle(r.rect(), color=(40, 167, 225), thickness=2)

            # Rectangle corners
            for p in r.corners():
                img.draw_circle(p[0], p[1], 8, color=(78, 90, 34), thickness=2)

            # Number near rectangle
            x0, y0, w, h = r.rect()
            img.draw_string(x0, max(0, y0 - 14), "RECT %d" % rect_count, color=(255, 255, 255), scale=1)

            print("RECT", rect_count, r)

        print("[===========================]")
        print("FPS:", clock.fps())

        img.draw_string(2, 2, "RECT:%d FPS:%.1f" % (rect_count, clock.fps()), color=(255, 255, 255), scale=1)

        # Center camera frame on LCD
        x = int((DISPLAY_WIDTH - PICTURE_WIDTH) / 2)
        y = int((DISPLAY_HEIGHT - PICTURE_HEIGHT) / 2)
        Display.show_image(img, x=x, y=y)

except KeyboardInterrupt as e:
    print("User Stop:", e)
except BaseException as e:
    print("Exception:", e)
finally:
    if isinstance(sensor, Sensor):
        sensor.stop()
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()

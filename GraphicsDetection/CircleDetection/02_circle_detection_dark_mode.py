# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Обнаружение кругов на тёмном фоне (белые круги на чёрном).
# Важно: круги ищем на копии изображения, а рисуем и выводим на LCD оригинальный кадр.
# Это предотвращает чёрный экран после binary().
# ============================================

import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

PICTURE_WIDTH = 400
PICTURE_HEIGHT = 240
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
CIRCLE_THRESHOLD = 3000

sensor = None
clock = time.clock()

try:
    sensor = Sensor(id=2)
    sensor.reset()
    sensor.set_framesize(width=PICTURE_WIDTH, height=PICTURE_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()
    sensor.run()

    x_offset = int((DISPLAY_WIDTH - PICTURE_WIDTH) / 2)
    y_offset = int((DISPLAY_HEIGHT - PICTURE_HEIGHT) / 2)

    while True:
        os.exitpoint()
        clock.tick()

        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        # Analyze copy only. Do not show this binary image on LCD.
        find_img = img.copy()
        find_img.binary([(200, 255)])
        circles = find_img.find_circles(threshold=CIRCLE_THRESHOLD)

        print("[Dark Mode Circle Detection]")
        print("count:", len(circles))

        for i, c in enumerate(circles):
            x, y, r = c.circle()
            img.draw_circle(c.circle(), color=(40, 167, 225), thickness=3)
            img.draw_cross(x, y, color=(255, 0, 0), size=6, thickness=2)
            img.draw_string(max(0, x - r), max(0, y - r - 14), "C%d R%d" % (i + 1, r), color=(255, 255, 255), scale=1)
            print("Circle", i + 1, c)

        print("FPS:", clock.fps())
        print("[===========================]")

        img.draw_string(2, 2, "C:%d FPS:%.1f" % (len(circles), clock.fps()), color=(255, 255, 255), scale=1)
        Display.show_image(img, x=x_offset, y=y_offset)

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

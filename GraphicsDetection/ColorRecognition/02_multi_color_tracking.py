# ============================================================
# 02. Multi Color Recognition (несколько цветов)
#
# Что делает:
# - ищет сразу несколько цветов
# - выделяет каждый своим цветом
# ============================================================

import time
from media.sensor import *
from media.display import *
from media.media import *

THRESHOLDS = [
    (0, 66, 7, 127, 3, 127),
    (42, 100, -128, -17, 6, 66),
    (43, 99, -43, -4, -56, -7),
]

sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=640, height=480)
sensor.set_pixformat(Sensor.RGB565)

Display.init(Display.ST7701, to_ide=True)
MediaManager.init()

sensor.run()
clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()

    for threshold in THRESHOLDS:
        blobs = img.find_blobs([threshold])
        for blob in blobs:
            img.draw_rectangle(blob[0:4], color=(255,0,0), thickness=3)

    Display.show_image(img)
    print("FPS:", clock.fps())

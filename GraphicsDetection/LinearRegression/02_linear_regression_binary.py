# ============================================================
# 02. Linear Regression с бинаризацией
#
# Что добавлено:
# - бинаризация изображения перед регрессией
# - повышает стабильность
# ============================================================

import time
from media.sensor import *
from media.display import *
from media.media import *

THRESHOLD = (0, 100)

sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=640, height=480)
sensor.set_pixformat(Sensor.GRAYSCALE)

Display.init(Display.ST7701, to_ide=True)
MediaManager.init()

sensor.run()
clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()

    # бинаризация
    img.binary([THRESHOLD])

    # регрессия
    line = img.get_regression([(255,255)])

    if line:
        img.draw_line(line.line(), color=127, thickness=4)

    Display.show_image(img)
    print("FPS:", clock.fps())

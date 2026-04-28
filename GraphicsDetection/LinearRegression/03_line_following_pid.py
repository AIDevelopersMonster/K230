# ============================================================
# 03. Простой line following (основа автопилота)
#
# Идея:
# - находим линию
# - считаем центр линии
# - сравниваем с центром экрана
# - получаем ошибку (error)
#
# Это основа для управления роботом
# ============================================================

import time
from media.sensor import *
from media.display import *
from media.media import *

THRESHOLD = (0, 100)
IMG_WIDTH = 640

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

    line = img.get_regression([THRESHOLD])

    if line:
        img.draw_line(line.line(), color=127, thickness=4)

        # центр линии
        x_center = (line.x1() + line.x2()) / 2

        # ошибка (центр экрана = 320)
        error = x_center - (IMG_WIDTH / 2)

        img.draw_string(5, 5, "err: %.1f" % error, color=255)
        print("ERROR:", error)

    Display.show_image(img)

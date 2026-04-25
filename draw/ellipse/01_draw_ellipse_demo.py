# ============================================
# K230 Draw Ellipse Demo
# Based on official PDF example
# ============================================

import time, os, math
import image
from random import randint
from media.display import *
from media.media import *

WIDTH = 640
HEIGHT = 480

img = image.Image(WIDTH, HEIGHT, image.ARGB8888)
img.clear()
img.draw_rectangle(0, 0, WIDTH, HEIGHT, color=(255,255,255), fill=True)

Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
MediaManager.init()

try:
    # Draw random ellipses
    for i in range(10):
        x = randint(0, WIDTH)
        y = randint(0, HEIGHT)
        rx = randint(10, 200)
        ry = randint(10, 150)
        rot = randint(0, 360)
        color = (randint(128,255), randint(128,255), randint(128,255))

        img.draw_ellipse(x, y, rx, ry, rot, color=color, thickness=2)

    Display.show_image(img)

    while True:
        time.sleep(2)

except Exception as e:
    print(e)

finally:
    Display.deinit()
    MediaManager.deinit()

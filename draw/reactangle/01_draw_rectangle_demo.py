# ============================================
# K230 Draw Rectangle Demo
# Based on official PDF example
# ============================================

import time, os
import image
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
    # Main rectangle
    img.draw_rectangle(120, 160, 400, 160, color=(0,191,255), thickness=2)

    # Side rectangles
    img.draw_rectangle(120, 160, 50, 50, color=(135,206,235), fill=True)
    img.draw_rectangle(120, 270, 50, 50, color=(0,191,255), fill=True)

    img.draw_rectangle(470, 160, 50, 50, color=(0,191,255), fill=True)
    img.draw_rectangle(470, 270, 50, 50, color=(135,206,235), fill=True)

    # Center blocks
    img.draw_rectangle(220, 200, 200, 80, color=(0,191,255), thickness=2)
    img.draw_rectangle(240, 220, 160, 40, color=(135,206,235), fill=True)

    Display.show_image(img)

    while True:
        time.sleep(2)

except Exception as e:
    print(e)

finally:
    Display.deinit()
    MediaManager.deinit()

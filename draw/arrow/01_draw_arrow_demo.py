# ============================================
# K230 Draw Arrow Demo
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
    # Main arrow
    img.draw_arrow(320, 200, 400, 200, color=(0,191,255), thickness=5)

    # Additional arrows
    img.draw_arrow(300, 180, 380, 180, color=(135,206,235), thickness=3)
    img.draw_arrow(340, 220, 420, 220, color=(135,206,235), thickness=3)

    # Diagonal arrows
    img.draw_arrow(250, 150, 350, 250, color=(0,191,255), thickness=3)
    img.draw_arrow(350, 150, 450, 250, color=(0,191,255), thickness=3)

    Display.show_image(img)

    while True:
        time.sleep(2)

except Exception as e:
    print(e)

finally:
    Display.deinit()
    MediaManager.deinit()

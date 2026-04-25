# ============================================
# K230 Draw Crosshair Demo
# Based on official PDF example
# ============================================

import time, os, math
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
    # Center cross
    img.draw_cross(320, 240, color=(0,191,255), size=40, thickness=3)

    # Inner circle crosses
    for i in range(8):
        angle = i * (360 / 8)
        x = int(320 + 50 * math.cos(math.radians(angle)))
        y = int(240 + 50 * math.sin(math.radians(angle)))
        img.draw_cross(x, y, color=(135,206,235), size=15, thickness=2)

    # Outer crosses
    for i in range(12):
        angle = i * (360 / 12)
        x = int(320 + 80 * math.cos(math.radians(angle)))
        y = int(240 + 80 * math.sin(math.radians(angle)))
        img.draw_cross(x, y, color=(173,216,230), size=10, thickness=1)

    Display.show_image(img)

    while True:
        time.sleep(2)

except Exception as e:
    print(e)

finally:
    Display.deinit()
    MediaManager.deinit()

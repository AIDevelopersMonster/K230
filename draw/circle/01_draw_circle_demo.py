# ============================================
# K230 Draw Circle Example
# Author: AIDevelopersMonster
#
# Description:
# Demonstrates draw_circle() based on official PDF example.
# Draws a wheel-like structure using circles.
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
    # Outer circles
    img.draw_circle(320, 240, 150, color=(50,50,50), thickness=8)
    img.draw_circle(320, 240, 130, color=(80,80,80), thickness=5)

    # Center hub
    img.draw_circle(320, 240, 40, color=(100,100,100), fill=True)
    img.draw_circle(320, 240, 40, color=(50,50,50), thickness=3)
    img.draw_circle(320, 240, 15, color=(30,30,30), fill=True)

    # Spokes
    for i in range(8):
        angle = i * (360 / 8)
        x_outer = int(320 + 130 * math.cos(math.radians(angle)))
        y_outer = int(240 + 130 * math.sin(math.radians(angle)))
        img.draw_circle(x_outer, y_outer, 10, color=(70,70,70), fill=True)

    Display.show_image(img)

    while True:
        time.sleep(2)

except Exception as e:
    print("Error:", e)

finally:
    Display.deinit()
    MediaManager.deinit()

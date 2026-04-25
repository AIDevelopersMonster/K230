# ============================================
# K230 Draw Keypoints Demo
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
img.draw_rectangle(0,0,WIDTH,HEIGHT,color=(255,255,255),fill=True)

Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
MediaManager.init()

try:
    # simulate keypoints (manual points for demo)
    for i in range(50,600,60):
        img.draw_cross(i,240,color=(255,0,0),size=10)

    Display.show_image(img)

    while True:
        time.sleep(2)

except Exception as e:
    print(e)

finally:
    Display.deinit()
    MediaManager.deinit()

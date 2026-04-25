# ============================================
# K230 Draw Text Demo
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
    # English text
    img.draw_string_advanced(200, 180, 30, "Hello World!", color=(0,191,255))

    # Chinese text
    img.draw_string_advanced(200, 240, 30, "你好，世界！", color=(0,255,127))

    Display.show_image(img)

    while True:
        time.sleep(2)

except Exception as e:
    print(e)

finally:
    Display.deinit()
    MediaManager.deinit()

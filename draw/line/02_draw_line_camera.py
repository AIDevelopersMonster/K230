# ============================================
# K230 Draw Line + Camera Example
# Author: AIDevelopersMonster
#
# Description:
# Demonstrates how to draw lines on a live camera stream.
#
# Combines:
# - Camera (Sensor)
# - draw_line()
# - Display
# ============================================

import uos as os
import time
from media.sensor import *
from media.display import *
from media.media import *

WIDTH = 640
HEIGHT = 480

sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_1)
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
MediaManager.init()

sensor.run()

while True:
    os.exitpoint()

    img = sensor.snapshot(chn=CAM_CHN_ID_1)

    # Draw crosshair lines (center)
    img.draw_line(0, HEIGHT//2, WIDTH, HEIGHT//2, color=(255,0,0), thickness=2)
    img.draw_line(WIDTH//2, 0, WIDTH//2, HEIGHT, color=(0,255,0), thickness=2)

    # Draw frame border
    img.draw_line(0, 0, WIDTH, 0, color=(0,0,255))
    img.draw_line(WIDTH, 0, WIDTH, HEIGHT, color=(0,0,255))
    img.draw_line(WIDTH, HEIGHT, 0, HEIGHT, color=(0,0,255))
    img.draw_line(0, HEIGHT, 0, 0, color=(0,0,255))

    img.draw_string(10, 10, "Draw Line + Camera", color=(255,255,0))

    Display.show_image(img)

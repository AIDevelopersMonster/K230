# ============================================
# K230 Draw Crosshair + Camera
# ============================================

import uos as os
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

    # Center crosshair
    img.draw_cross(WIDTH//2, HEIGHT//2, color=(255,0,0), size=30, thickness=2)

    # Additional crosshair points
    img.draw_cross(100,100, color=(0,255,0), size=15)
    img.draw_cross(500,300, color=(0,255,0), size=15)

    img.draw_string(10,10,"Draw Crosshair", color=(255,255,0))

    Display.show_image(img)

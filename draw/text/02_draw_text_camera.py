# ============================================
# K230 Draw Text + Camera
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

    img.draw_string(10, 10, "K230 Camera", color=(255,255,0), scale=2)
    img.draw_string(10, 40, "Draw Text", color=(0,255,0), scale=2)

    Display.show_image(img)

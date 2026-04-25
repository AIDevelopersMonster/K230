# ============================================
# K230 Draw Rectangle + Camera
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

    # Draw rectangles overlay
    img.draw_rectangle(100, 100, 200, 150, color=(255,0,0), thickness=2)
    img.draw_rectangle(150, 150, 100, 80, color=(0,255,0), fill=True)

    img.draw_string(10,10,"Draw Rectangle", color=(255,255,0))

    Display.show_image(img)

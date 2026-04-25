# ============================================
# K230 Draw Ellipse + Camera
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

    # Draw ellipse overlay
    img.draw_ellipse(WIDTH//2, HEIGHT//2, 120, 60, 0, color=(255,0,0), thickness=2)
    img.draw_ellipse(WIDTH//2, HEIGHT//2, 60, 30, 0, color=(0,255,0), thickness=2)

    img.draw_string(10,10,"Draw Ellipse", color=(255,255,0))

    Display.show_image(img)

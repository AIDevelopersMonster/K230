# ============================================
# K230 Draw Keypoints + Camera
# ============================================

import uos as os
import time
from media.sensor import *
from media.display import *
from media.media import *

WIDTH = 640
HEIGHT = 480

sensor = Sensor(width=1280, height=960)
sensor.reset()

sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_1)
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_0)
sensor.set_pixformat(Sensor.GRAYSCALE, chn=CAM_CHN_ID_0)

Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
MediaManager.init()

sensor.run()

roi = (220,140,200,200)

while True:
    os.exitpoint()

    img = sensor.snapshot(chn=CAM_CHN_ID_1)
    img_g = sensor.snapshot(chn=CAM_CHN_ID_0)

    img.draw_rectangle(roi, color=(173,216,230), thickness=2)

    keypoints = img_g.find_keypoints(threshold=30, scale_factor=1.2, max_keypoints=30, roi=roi)

    if keypoints:
        img.draw_keypoints(keypoints, color=(255,0,0), size=8, thickness=2, fill=True)

    img.draw_string(10,10,"Keypoints", color=(255,255,0))

    Display.show_image(img)

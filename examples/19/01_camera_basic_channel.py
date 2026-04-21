import time, os
from media.sensor import *
from media.display import *
from media.media import *

sensor = Sensor()
sensor.reset()

# channel 1 config (recommended)
sensor.set_framesize(width=640, height=480, chn=CAM_CHN_ID_1)
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

Display.init(Display.ST7701, width=640, height=480, to_ide=True)
MediaManager.init()

sensor.run()

while True:
    os.exitpoint()
    img = sensor.snapshot(chn=CAM_CHN_ID_1)
    Display.show_image(img)

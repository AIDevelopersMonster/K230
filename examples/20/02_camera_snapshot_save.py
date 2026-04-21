# ============================================
# K230 Example
# Camera snapshot and save
# ============================================

import uos as os
import time
from media.sensor import *
from media.display import *
from media.media import *

save_path = "/data/snapshot/"
i = 1

sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=640, height=480, chn=CAM_CHN_ID_1)
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

Display.init(Display.ST7701, width=640, height=480, to_ide=True)
MediaManager.init()

sensor.run()

while True:
    os.exitpoint()
    img = sensor.snapshot(chn=CAM_CHN_ID_1)
    Display.show_image(img)

    # save every 100 frames
    if i % 100 == 0:
        path = save_path + str(i) + ".jpg"
        img.save(path)
        print("Saved:", path)

    i += 1
    time.sleep_ms(10)

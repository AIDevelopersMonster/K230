# ============================================
# K230 Example
# Camera horizontal mirror
# ============================================

import uos as os
import time
from media.sensor import *
from media.display import *
from media.media import *


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=640, height=480, chn=CAM_CHN_ID_1)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

    # enable horizontal mirror
    sensor.set_hmirror(True)

    return sensor


def main():
    sensor = None
    try:
        sensor = init_sensor()
        Display.init(Display.ST7701, width=640, height=480, to_ide=True)
        MediaManager.init()
        sensor.run()

        while True:
            os.exitpoint()
            img = sensor.snapshot(chn=CAM_CHN_ID_1)
            Display.show_image(img)

    finally:
        if isinstance(sensor, Sensor):
            sensor.stop()
        Display.deinit()
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
        time.sleep_ms(100)
        MediaManager.deinit()


if __name__ == "__main__":
    main()

# Circle Detection for dark background (white circles on black)

import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

PICTURE_WIDTH = 400
PICTURE_HEIGHT = 240
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

CIRCLE_THRESHOLD = 3000
sensor = None
clock = time.clock()

try:
    sensor = Sensor(id=2)
    sensor.reset()
    sensor.set_framesize(width=PICTURE_WIDTH, height=PICTURE_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()
    sensor.run()

    x_offset = int((DISPLAY_WIDTH - PICTURE_WIDTH) / 2)
    y_offset = int((DISPLAY_HEIGHT - PICTURE_HEIGHT) / 2)

    while True:
        os.exitpoint()
        clock.tick()

        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        # optional: increase contrast for dark mode
        img.binary([(200, 255)])

        circles = img.find_circles(threshold=CIRCLE_THRESHOLD)

        print("[Dark Mode Circle Detection]")

        for i, c in enumerate(circles):
            img.draw_circle(c.circle(), color=(255, 255, 255), thickness=2)
            x, y, r = c.circle()
            img.draw_cross(x, y, color=(255, 0, 0), size=6)
            print("Circle", i + 1, c)

        print("FPS:", clock.fps())

        img.draw_string(2, 2, "C:%d FPS:%.1f" % (len(circles), clock.fps()), color=(255,255,255), scale=1)
        Display.show_image(img, x=x_offset, y=y_offset)

except KeyboardInterrupt as e:
    print("User Stop:", e)
except BaseException as e:
    print("Exception:", e)
finally:
    if isinstance(sensor, Sensor):
        sensor.stop()
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()

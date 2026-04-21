import time, os, gc, image
from media.sensor import *
from media.display import *
from media.media import *

WIDTH = 640
HEIGHT = 480

sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=WIDTH, height=HEIGHT)
sensor.set_pixformat(Sensor.RGB565)

Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
MediaManager.init()

sensor.run()

fps = time.clock()

while True:
    fps.tick()
    os.exitpoint()

    img = sensor.snapshot()

    # overlay text
    img.draw_string_advanced(10, 10, 24, "Camera Live", color=(255,255,0))

    Display.show_image(img)

    gc.collect()
    time.sleep_ms(5)

    print("FPS:", fps.fps())

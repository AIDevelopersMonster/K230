import time, os, gc
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
    Display.show_image(img)
    gc.collect()
    time.sleep_ms(5)
    print("FPS:", fps.fps())

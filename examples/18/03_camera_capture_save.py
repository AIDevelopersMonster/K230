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

count = 0

while True:
    os.exitpoint()

    img = sensor.snapshot()
    Display.show_image(img)

    # каждые 50 кадров сохраняем
    count += 1
    if count % 50 == 0:
        filename = "/sdcard/capture_{}.jpg".format(count)
        img.save(filename)
        print("Saved:", filename)

    gc.collect()
    time.sleep_ms(5)

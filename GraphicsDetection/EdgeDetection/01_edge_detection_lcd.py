# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Демонстрация обнаружения границ объектов на K230.
# Камера захватывает изображение, find_edges() выделяет контуры,
# результат выводится на LCD и FPS печатается в терминал.
#
# Важно: find_edges() работает с grayscale изображением.
# ============================================

import time, os, sys, gc
from media.sensor import *
from media.display import *
from media.media import *
import image

PICTURE_WIDTH = 640
PICTURE_HEIGHT = 480
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

EDGE_TYPE = image.EDGE_CANNY
EDGE_THRESHOLD = (50, 80)

sensor = None
clock = time.clock()

try:
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=PICTURE_WIDTH, height=PICTURE_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.GRAYSCALE, chn=CAM_CHN_ID_0)

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()
    sensor.run()

    x_offset = int((DISPLAY_WIDTH - PICTURE_WIDTH) / 2)
    y_offset = int((DISPLAY_HEIGHT - PICTURE_HEIGHT) / 2)

    while True:
        os.exitpoint()
        clock.tick()

        img = sensor.snapshot(chn=CAM_CHN_ID_0)
        img.find_edges(EDGE_TYPE, threshold=EDGE_THRESHOLD)

        print("[Edge Detection]")
        print("FPS:", clock.fps())
        print("threshold:", EDGE_THRESHOLD)
        print("[===========================]")

        Display.show_image(img, x=x_offset, y=y_offset)
        gc.collect()

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

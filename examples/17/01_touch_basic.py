# ============================================
# K230 Example
# Базовый пример Touch Display
# ============================================

from media.display import *
from media.media import *
from media.touch import *
import image, time

Display.init(Display.ST7701, width=640, height=480, osd_num=1, to_ide=True)
MediaManager.init()
Touch.init()

img = image.Image(640, 480, image.RGB565)

while True:
    img.clear()

    # читаем координаты касания
    point = Touch.read()

    if point:
        x, y = point[0], point[1]
        print("Touch:", x, y)
        img.draw_circle(x, y, 10, color=(255, 0, 0), thickness=2)

    Display.show_image(img)
    time.sleep(0.05)

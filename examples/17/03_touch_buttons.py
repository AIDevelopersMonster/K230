# ============================================
# K230 Example
# Кнопки через touch
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

    # рисуем кнопку
    img.draw_rectangle(200, 180, 240, 120, color=(0,255,0), thickness=2)
    img.draw_string_advanced(240, 230, 24, "BUTTON", color=(255,255,255))

    point = Touch.read()

    if point:
        x, y = point[0], point[1]

        # проверка попадания в кнопку
        if 200 < x < 440 and 180 < y < 300:
            print("Button pressed")
            img.draw_string_advanced(220, 320, 24, "CLICK!", color=(255,0,0))

    Display.show_image(img)
    time.sleep(0.05)

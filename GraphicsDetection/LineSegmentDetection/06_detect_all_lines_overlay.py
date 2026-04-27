# ============================================================
# Пример: классификация линий (горизонтальные / вертикальные / наклонные)
#
# Что делает скрипт:
# - открывает картинку mixed_lines.png
# - находит все линии
# - делит их на 3 типа:
#     горизонтальные (зелёные)
#     вертикальные (красные)
#     наклонные (синие)
# - показывает статистику на экране
#
# Как пользоваться:
# 1. Скопируйте папку img на SD-карту
# 2. Проверьте IMAGE_PATH
# 3. Запустите скрипт
#
# Если не работает:
# - проверьте путь к файлу
# - убедитесь что картинка существует
# ============================================================

import time, math, gc
import image
from media.display import *
from media.media import *

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/mixed_lines.png"
ANGLE_TOLERANCE_DEG = 12


def angle(line):
    """Вычисление угла линии"""
    x1,y1,x2,y2 = line[:4]
    a = math.degrees(math.atan2(y2-y1, x2-x1))
    return a+180 if a<0 else a


def is_h(l): return angle(l)<=ANGLE_TOLERANCE_DEG or angle(l)>=180-ANGLE_TOLERANCE_DEG

def is_v(l): return abs(angle(l)-90)<=ANGLE_TOLERANCE_DEG

Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
MediaManager.init()

try:
    img = image.Image(IMAGE_PATH)
    lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)

    h=v=o=0
    for ln in lines:
        c = ln.line()

        if is_h(c):
            img.draw_line(c, color=(0,255,0), thickness=3); h+=1
        elif is_v(c):
            img.draw_line(c, color=(255,0,0), thickness=3); v+=1
        else:
            img.draw_line(c, color=(0,128,255), thickness=3); o+=1

    img.draw_string(5,5,f"H:{h} V:{v} O:{o}", color=(255,255,0), scale=2)
    Display.show_image(img)

    print("Горизонтальные, вертикальные, наклонные:",h,v,o)

    while True:
        time.sleep_ms(100)

finally:
    gc.collect()

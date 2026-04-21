# ============================================
# K230 Example
# Базовый пример Touch Display
# Исправленная версия для Yahboom K230 / CanMV
# ============================================

import time
import os
import image

from media.display import *
from media.media import *
from machine import TOUCH

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Инициализация touch-контроллера
# Для Yahboom K230 используется machine.TOUCH(0)
tp = TOUCH(0)


def main():
    print("touch basic demo")

    # Фоновое изображение
    bg = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    bg.clear()
    bg.draw_rectangle(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, color=(255, 255, 255), fill=True)
    bg.draw_string_advanced(20, 20, 28, "Touch screen demo", color=(0, 0, 0))
    bg.draw_string_advanced(20, 60, 20, "Tap the screen to see coordinates", color=(0, 0, 255))

    # OSD-слой для маркера касания
    overlay = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    overlay.clear()

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()

    try:
        while True:
            os.exitpoint()

            # Обновляем фоновый слой
            Display.show_image(bg)

            # Чистим overlay, чтобы показывать только текущее касание
            overlay.clear()

            points = tp.read(1)
            if len(points):
                pt = points[0]
                print("Touch: x={}, y={}, event={}".format(pt.x, pt.y, pt.event))
                overlay.draw_circle(pt.x, pt.y, 18, color=(255, 0, 0), thickness=4)
                overlay.draw_string_advanced(20, 100, 22, "x={}, y={}".format(pt.x, pt.y), color=(0, 0, 0))
                Display.show_image(overlay, layer=Display.LAYER_OSD2, alpha=180)

            time.sleep(0.05)

    except KeyboardInterrupt as e:
        print("user stop:", e)
    except BaseException as e:
        print("Exception", e)

    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    main()

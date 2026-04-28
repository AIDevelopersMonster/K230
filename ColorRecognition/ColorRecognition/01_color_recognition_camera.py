# ============================================================
# 01. Color Recognition: базовое распознавание цвета с камеры
#
# Что делает:
# - получает изображение с камеры K230;
# - ищет цветовые области через img.find_blobs();
# - рисует прямоугольник вокруг найденного цвета;
# - ставит крестик в центре объекта;
# - показывает FPS.
#
# Как пользоваться:
# 1. Откройте файл в CanMV IDE.
# 2. Подключите K230 к компьютеру.
# 3. Выберите цвет через COLOR_INDEX.
# 4. Наведите камеру на объект нужного цвета.
#
# COLOR_INDEX:
# 0 - красный
# 1 - зелёный
# 2 - синий
# 3 - цвет логотипа YAHBOOM / голубой
#
# Если цвет определяется плохо:
# - улучшите освещение;
# - уберите блики;
# - настройте LAB-порог в CanMV Threshold Editor;
# - уменьшите или увеличьте значения THRESHOLDS.
# ============================================================

import time, os, sys, gc
from media.sensor import *
from media.display import *
from media.media import *
import image

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# LAB thresholds: (L Min, L Max, A Min, A Max, B Min, B Max)
THRESHOLDS = [
    (0, 66, 7, 127, 3, 127),          # red
    (42, 100, -128, -17, 6, 66),      # green
    (43, 99, -43, -4, -56, -7),       # blue
    (37, 100, -128, 127, -128, -27),  # YAHBOOM cyan/blue
]

COLOR_NAMES = ["RED", "GREEN", "BLUE", "YAHBOOM"]
COLOR_INDEX = 0


def get_closest_rgb(lab_threshold):
    l_center = (lab_threshold[0] + lab_threshold[1]) // 2
    a_center = (lab_threshold[2] + lab_threshold[3]) // 2
    b_center = (lab_threshold[4] + lab_threshold[5]) // 2
    return image.lab_to_rgb((l_center, a_center, b_center))


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def main():
    sensor = None
    try:
        sensor = init_sensor()
        Display.init(Display.ST7701, to_ide=True)
        MediaManager.init()
        sensor.run()
        clock = time.clock()

        threshold = THRESHOLDS[COLOR_INDEX]
        draw_color = get_closest_rgb(threshold)

        while True:
            clock.tick()
            img = sensor.snapshot()

            blobs = img.find_blobs([threshold], pixels_threshold=50, area_threshold=50, merge=True)
            for blob in blobs:
                img.draw_rectangle(blob[0:4], color=draw_color, thickness=4)
                img.draw_cross(blob[5], blob[6], color=draw_color, thickness=2)
                img.draw_string(blob[0], max(0, blob[1] - 20), COLOR_NAMES[COLOR_INDEX], color=draw_color, scale=2)

            fps = clock.fps()
            img.draw_string_advanced(0, 0, 30, "FPS: %.2f" % fps, color=(255, 255, 255))
            Display.show_image(img)
            print("FPS:", fps, "blobs:", len(blobs))

    except KeyboardInterrupt as e:
        print("Пользователь остановил скрипт:", e)
    except Exception as e:
        print("Ошибка:", e)
    finally:
        if sensor:
            sensor.stop()
        Display.deinit()
        MediaManager.deinit()
        gc.collect()


if __name__ == "__main__":
    main()

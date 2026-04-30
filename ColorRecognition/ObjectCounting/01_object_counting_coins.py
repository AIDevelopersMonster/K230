# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Object Counting / Подсчет объектов по цвету
#
# Что делает:
# - получает изображение с камеры K230;
# - ищет объекты одного цвета через img.find_blobs();
# - рисует рамку и крест в центре каждого объекта;
# - показывает FPS и количество объектов на экране;
# - подходит для демонстрации с картинкой монет из Yahboom Tools.
# ============================================

import time
import gc
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# LAB threshold format:
# (L_min, L_max, A_min, A_max, B_min, B_max)
# Значения ниже подходят для золотых монет из генератора Yahboom.
# Если камера считает плохо, настройте порог под свое освещение.
TRACK_THRESHOLD = (0, 100, -7, 127, 10, 83)

FONT_SIZE = 25
TEXT_COLOR = (233, 233, 233)
BOX_COLOR = (255, 255, 255)
CROSS_COLOR = (255, 255, 255)

# Фильтры помогают убрать шум и мелкие случайные пятна.
PIXELS_THRESHOLD = 50
AREA_THRESHOLD = 50
MERGE_BLOBS = True


def init_camera():
    """Initialize and configure camera."""
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    """Initialize display and media manager."""
    Display.init(Display.ST7701, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, to_ide=True)
    MediaManager.init()


def find_objects(img, threshold):
    """Find same-color objects and draw marks on the image."""
    blobs = img.find_blobs(
        [threshold],
        pixels_threshold=PIXELS_THRESHOLD,
        area_threshold=AREA_THRESHOLD,
        merge=MERGE_BLOBS,
    )

    for blob in blobs:
        img.draw_rectangle(blob[0:4], color=BOX_COLOR, thickness=2)
        img.draw_cross(blob[5], blob[6], color=CROSS_COLOR, thickness=2)

    return blobs


def draw_info(img, fps, count):
    """Draw FPS and detected object count."""
    info_text = "FPS: %.3f    Num: %d" % (fps, count)
    img.draw_string_advanced(0, 0, FONT_SIZE, info_text, color=TEXT_COLOR)


def main():
    sensor = None
    try:
        sensor = init_camera()
        init_display()
        sensor.run()

        clock = time.clock()

        while True:
            clock.tick()
            img = sensor.snapshot()

            blobs = find_objects(img, TRACK_THRESHOLD)
            draw_info(img, clock.fps(), len(blobs))

            Display.show_image(img)
            print("FPS: %.3f, objects: %d" % (clock.fps(), len(blobs)))

    except KeyboardInterrupt:
        print("Program terminated by user")
    except Exception as e:
        print("Error occurred:", e)
    finally:
        if sensor:
            sensor.stop()
            sensor.deinit()
        Display.deinit()
        MediaManager.deinit()
        gc.collect()


if __name__ == "__main__":
    main()

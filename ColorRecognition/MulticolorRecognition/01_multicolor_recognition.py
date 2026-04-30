# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Multi-color Recognition / Многоцветное распознавание
#
# Что делает:
# - получает изображение с камеры K230;
# - одновременно ищет красный, зеленый и синий цвета;
# - рисует рамку вокруг найденной цветовой области;
# - подписывает цвет: RED, GREEN, BLUE;
# - показывает FPS и количество найденных цветовых областей.
# ============================================

import time
import gc
from media.sensor import *
from media.display import *
from media.media import *

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# LAB color thresholds:
# (L Min, L Max, A Min, A Max, B Min, B Max)
COLOR_THRESHOLDS = [
    (0, 66, 7, 127, 3, 127),          # RED / красный
    (42, 100, -128, -17, 6, 66),      # GREEN / зеленый
    (43, 99, -43, -4, -56, -7),       # BLUE / синий
]

DRAW_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

COLOR_LABELS = ["RED", "GREEN", "BLUE"]

# Increase these values if there is noise.
# Decrease them if small objects are not detected.
PIXELS_THRESHOLD = 50
AREA_THRESHOLD = 500
MERGE_BLOBS = True

TEXT_COLOR = (255, 255, 255)


def init_sensor():
    """Initialize camera sensor."""
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    """Initialize LCD and IDE display output."""
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def process_color(img, color_index):
    """Detect one color and draw all found blobs.

    Returns the number of found blobs for this color.
    """
    threshold = COLOR_THRESHOLDS[color_index]
    draw_color = DRAW_COLORS[color_index]
    label = COLOR_LABELS[color_index]

    blobs = img.find_blobs(
        [threshold],
        pixels_threshold=PIXELS_THRESHOLD,
        area_threshold=AREA_THRESHOLD,
        merge=MERGE_BLOBS,
    )

    for blob in blobs:
        x = blob[0]
        y = blob[1]
        w = blob[2]
        h = blob[3]
        cx = blob[5]
        cy = blob[6]

        img.draw_rectangle((x, y, w, h), thickness=4, color=draw_color)
        img.draw_cross(cx, cy, thickness=2, color=draw_color)
        img.draw_string_advanced(x, max(0, y - 35), 30, label, color=draw_color)

    return len(blobs)


def draw_info(img, fps, counts):
    """Draw FPS and per-color counters."""
    total = counts[0] + counts[1] + counts[2]
    img.draw_string_advanced(0, 0, 24, "FPS: %.2f  TOTAL: %d" % (fps, total), color=TEXT_COLOR)
    img.draw_string_advanced(0, 28, 20, "R:%d  G:%d  B:%d" % (counts[0], counts[1], counts[2]), color=TEXT_COLOR)


def main():
    sensor = None
    try:
        sensor = init_sensor()
        init_display()
        sensor.run()
        clock = time.clock()

        while True:
            clock.tick()
            img = sensor.snapshot()

            counts = [0, 0, 0]
            for i in range(len(COLOR_THRESHOLDS)):
                counts[i] = process_color(img, i)

            fps = clock.fps()
            draw_info(img, fps, counts)
            Display.show_image(img)
            print("FPS: %.2f, RED: %d, GREEN: %d, BLUE: %d" % (fps, counts[0], counts[1], counts[2]))

    except KeyboardInterrupt as e:
        print("User interrupted:", e)
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

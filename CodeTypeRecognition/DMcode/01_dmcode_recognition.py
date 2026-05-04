# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# DM Code Recognition / Распознавание Data Matrix
#
# Что делает:
# - получает изображение с камеры K230;
# - ищет Data Matrix / DM codes через img.find_datamatrices();
# - рисует красную рамку вокруг найденного кода;
# - показывает payload, rotation и FPS;
# - печатает результат в консоль CanMV IDE.
# ============================================

import time
import math
import os
import gc
from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = 640
DETECT_HEIGHT = 480
TEXT_COLOR = (255, 0, 0)
BOX_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)

# None = поиск по всему кадру.
# Для ускорения можно указать ROI: (x, y, w, h), например (160, 80, 320, 320)
DMCODE_ROI = None


def degrees(rad):
    """Convert radians to degrees."""
    return (180.0 * rad) / math.pi


def init_sensor():
    """Initialize camera sensor."""
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    # sensor.set_pixformat(Sensor.GRAYSCALE)
    return sensor


def init_display():
    """Initialize display and media manager."""
    Display.init(Display.ST7701, width=DETECT_WIDTH, height=DETECT_HEIGHT, to_ide=True)
    MediaManager.init()


def find_dm_codes(img):
    """Find Data Matrix codes in whole frame or selected ROI."""
    if DMCODE_ROI:
        img.draw_rectangle(DMCODE_ROI, color=(120, 120, 120), thickness=1)
        return img.find_datamatrices(roi=DMCODE_ROI)
    return img.find_datamatrices()


def draw_dm_info(img, matrix):
    """Draw Data Matrix rectangle, payload and rotation."""
    payload = matrix.payload()
    rotation = degrees(matrix.rotation())
    x, y, w, h = matrix.rect()
    text_y = y - 25 if y - 25 > 0 else y

    img.draw_rectangle(matrix.rect(), color=BOX_COLOR, thickness=4)
    img.draw_cross(x + w // 2, y + h // 2, color=(0, 255, 0), thickness=2)
    img.draw_string_advanced(x, text_y, 20, "%s [%.2f] deg" % (payload, rotation), color=TEXT_COLOR)
    img.draw_string_advanced(0, 0, 20, "DM: " + payload, color=WHITE)

    print('payload "%s", rotation %.3f degrees, rect=%s' % (payload, rotation, str(matrix.rect())))


def draw_fps(img, fps, count):
    img.draw_string_advanced(0, DETECT_HEIGHT - 35, 24, "FPS: %.2f  DM: %d" % (fps, count), color=WHITE)


def should_exit():
    try:
        return os.exitpoint()
    except Exception:
        return False


def main():
    sensor = None
    try:
        sensor = init_sensor()
        init_display()
        sensor.run()
        clock = time.clock()

        while True:
            clock.tick()
            if should_exit():
                break

            img = sensor.snapshot()
            matrices = find_dm_codes(img)

            for matrix in matrices:
                draw_dm_info(img, matrix)
                break

            draw_fps(img, clock.fps(), len(matrices))
            Display.show_image(img)
            gc.collect()

    except KeyboardInterrupt:
        print("User stopped")
    except Exception as e:
        print("Error occurred:", e)
    finally:
        if sensor:
            sensor.stop()
            sensor.deinit()
        Display.deinit()
        try:
            os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
            time.sleep_ms(100)
        except Exception:
            pass
        MediaManager.deinit()
        gc.collect()


if __name__ == "__main__":
    main()

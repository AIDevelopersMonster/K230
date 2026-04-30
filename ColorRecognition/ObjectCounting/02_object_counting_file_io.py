# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Object Counting + File Read/Write
# Подсчет объектов + чтение и запись файлов
#
# Что делает:
# - читает LAB-порог из текстового файла;
# - если файла нет, создает его со значением по умолчанию;
# - считает объекты указанного цвета;
# - записывает последний результат в файл;
# - показывает, как безопасно работать с файлами на K230.
# ============================================

import time
import os
import gc
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Файлы создаются в текущей рабочей папке устройства/IDE.
THRESHOLD_FILE = "object_threshold.txt"
RESULT_FILE = "object_count_result.txt"

DEFAULT_THRESHOLD = (0, 100, -7, 127, 10, 83)
FONT_SIZE = 25
TEXT_COLOR = (233, 233, 233)
BOX_COLOR = (255, 255, 255)

PIXELS_THRESHOLD = 50
AREA_THRESHOLD = 50
MERGE_BLOBS = True


def file_exists(path):
    """Return True if file exists."""
    try:
        os.stat(path)
        return True
    except OSError:
        return False


def threshold_to_text(threshold):
    """Convert tuple threshold to comma-separated text."""
    return ",".join([str(value) for value in threshold])


def text_to_threshold(text):
    """Parse threshold text: L_min,L_max,A_min,A_max,B_min,B_max."""
    parts = text.strip().replace(" ", "").split(",")
    if len(parts) != 6:
        raise ValueError("Threshold must contain 6 numbers")
    return tuple([int(value) for value in parts])


def write_text_file(path, text):
    """Write text to file. Mode 'w' replaces old content."""
    with open(path, "w") as f:
        f.write(text)


def read_text_file(path):
    """Read whole text file."""
    with open(path, "r") as f:
        return f.read()


def load_or_create_threshold():
    """Read threshold from file or create file with default threshold."""
    if not file_exists(THRESHOLD_FILE):
        write_text_file(THRESHOLD_FILE, threshold_to_text(DEFAULT_THRESHOLD))
        print("Created", THRESHOLD_FILE, "with default threshold")
        return DEFAULT_THRESHOLD

    try:
        text = read_text_file(THRESHOLD_FILE)
        threshold = text_to_threshold(text)
        print("Loaded threshold:", threshold)
        return threshold
    except Exception as e:
        print("Cannot read threshold file, using default:", e)
        return DEFAULT_THRESHOLD


def save_count_result(count, fps):
    """Write the latest recognition result to text file."""
    text = "objects=%d\nfps=%.3f\ntime_ms=%d\n" % (count, fps, time.ticks_ms())
    write_text_file(RESULT_FILE, text)


def init_camera():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, to_ide=True)
    MediaManager.init()


def process_frame(img, threshold):
    blobs = img.find_blobs(
        [threshold],
        pixels_threshold=PIXELS_THRESHOLD,
        area_threshold=AREA_THRESHOLD,
        merge=MERGE_BLOBS,
    )

    for blob in blobs:
        img.draw_rectangle(blob[0:4], color=BOX_COLOR, thickness=2)
        img.draw_cross(blob[5], blob[6], color=BOX_COLOR, thickness=2)

    return blobs


def draw_info(img, fps, count):
    img.draw_string_advanced(0, 0, FONT_SIZE, "FPS: %.3f    Num: %d" % (fps, count), color=TEXT_COLOR)
    img.draw_string_advanced(0, 35, 18, "threshold: " + THRESHOLD_FILE, color=TEXT_COLOR)


def main():
    sensor = None
    threshold = load_or_create_threshold()
    last_save = time.ticks_ms()

    try:
        sensor = init_camera()
        init_display()
        sensor.run()
        clock = time.clock()

        while True:
            clock.tick()
            img = sensor.snapshot()
            blobs = process_frame(img, threshold)
            fps = clock.fps()
            count = len(blobs)

            draw_info(img, fps, count)
            Display.show_image(img)

            # Записываем результат не каждый кадр, а примерно раз в секунду,
            # чтобы не делать слишком много операций записи.
            if time.ticks_diff(time.ticks_ms(), last_save) > 1000:
                save_count_result(count, fps)
                last_save = time.ticks_ms()

            print("objects:", count, "fps:", fps)

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

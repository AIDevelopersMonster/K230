# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Multi-color Recognition + File Read/Write
# Многоцветное распознавание + чтение и запись файлов
#
# Что делает:
# - читает LAB-пороги цветов из текстового файла;
# - если файл доступен для записи, создает файл с порогами по умолчанию;
# - если файловая система недоступна, продолжает работу с порогами по умолчанию;
# - распознает RED, GREEN, BLUE;
# - записывает последний результат распознавания в текстовый файл.
# ============================================

import time
import os
import gc
from media.sensor import *
from media.display import *
from media.media import *

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
THRESHOLDS_FILENAME = "multicolor_thresholds.txt"
RESULT_FILENAME = "multicolor_result.txt"

DEFAULT_COLOR_THRESHOLDS = [
    (0, 66, 7, 127, 3, 127),          # RED
    (42, 100, -128, -17, 6, 66),      # GREEN
    (43, 99, -43, -4, -56, -7),       # BLUE
]

DRAW_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
COLOR_LABELS = ["RED", "GREEN", "BLUE"]

PIXELS_THRESHOLD = 50
AREA_THRESHOLD = 500
MERGE_BLOBS = True
TEXT_COLOR = (255, 255, 255)


def join_path(directory, filename):
    if directory == "/":
        return "/" + filename
    return directory + "/" + filename


def file_exists(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False


def write_text_file(path, text):
    try:
        with open(path, "w") as f:
            f.write(text)
        return True
    except OSError as e:
        print("File write failed:", path, e)
        return False


def read_text_file(path):
    with open(path, "r") as f:
        return f.read()


def find_writable_directory():
    for directory in FILE_DIR_CANDIDATES:
        try:
            os.stat(directory)
        except OSError:
            continue

        test_path = join_path(directory, "k230_write_test.tmp")
        try:
            with open(test_path, "w") as f:
                f.write("test")
            try:
                os.remove(test_path)
            except OSError:
                pass
            print("Writable directory:", directory)
            return directory
        except OSError as e:
            print("Directory is not writable:", directory, e)

    print("No writable directory found. File demo will run in read-only mode.")
    return None


def thresholds_to_text(labels, thresholds):
    lines = []
    for i in range(len(thresholds)):
        values = ",".join([str(v) for v in thresholds[i]])
        lines.append(labels[i] + ":" + values)
    return "\n".join(lines) + "\n"


def text_to_thresholds(text):
    thresholds = []
    labels = []

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            raise ValueError("Line must be LABEL:v1,v2,v3,v4,v5,v6")

        label, values_text = line.split(":", 1)
        parts = values_text.replace(" ", "").split(",")
        if len(parts) != 6:
            raise ValueError("Threshold must contain 6 numbers")

        labels.append(label.strip().upper())
        thresholds.append(tuple([int(v) for v in parts]))

    if len(thresholds) < 1:
        raise ValueError("No thresholds found in file")

    return labels, thresholds


def load_or_create_thresholds(file_dir):
    if file_dir is None:
        print("Using default thresholds, file system is not writable")
        return COLOR_LABELS, DEFAULT_COLOR_THRESHOLDS, None, None

    thresholds_path = join_path(file_dir, THRESHOLDS_FILENAME)
    result_path = join_path(file_dir, RESULT_FILENAME)

    if not file_exists(thresholds_path):
        ok = write_text_file(thresholds_path, thresholds_to_text(COLOR_LABELS, DEFAULT_COLOR_THRESHOLDS))
        if ok:
            print("Created", thresholds_path)
        else:
            print("Cannot create thresholds file, using defaults")
        return COLOR_LABELS, DEFAULT_COLOR_THRESHOLDS, thresholds_path, result_path

    try:
        text = read_text_file(thresholds_path)
        labels, thresholds = text_to_thresholds(text)
        print("Loaded thresholds from", thresholds_path)
        return labels, thresholds, thresholds_path, result_path
    except Exception as e:
        print("Cannot read thresholds file, using defaults:", e)
        return COLOR_LABELS, DEFAULT_COLOR_THRESHOLDS, thresholds_path, result_path


def save_result(result_path, labels, counts, fps):
    if result_path is None:
        return

    total = 0
    lines = ["fps=%.3f" % fps, "time_ms=%d" % time.ticks_ms()]
    for i in range(len(counts)):
        total += counts[i]
        lines.append(labels[i] + "=" + str(counts[i]))
    lines.append("total=" + str(total))

    write_text_file(result_path, "\n".join(lines) + "\n")


def get_draw_color(index):
    if index < len(DRAW_COLORS):
        return DRAW_COLORS[index]
    return (255, 255, 255)


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def process_color(img, label, threshold, color_index):
    draw_color = get_draw_color(color_index)
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


def draw_info(img, fps, labels, counts, thresholds_path):
    total = 0
    for count in counts:
        total += count
    img.draw_string_advanced(0, 0, 22, "FPS: %.2f  TOTAL: %d" % (fps, total), color=TEXT_COLOR)

    text = ""
    for i in range(len(counts)):
        if i > 0:
            text += "  "
        text += labels[i][0] + ":" + str(counts[i])
    img.draw_string_advanced(0, 26, 18, text, color=TEXT_COLOR)

    if thresholds_path:
        img.draw_string_advanced(0, 50, 16, "file: " + thresholds_path, color=TEXT_COLOR)
    else:
        img.draw_string_advanced(0, 50, 16, "file write: disabled", color=TEXT_COLOR)


def main():
    sensor = None
    file_dir = find_writable_directory()
    labels, thresholds, thresholds_path, result_path = load_or_create_thresholds(file_dir)
    last_save = time.ticks_ms()

    try:
        sensor = init_sensor()
        init_display()
        sensor.run()
        clock = time.clock()

        while True:
            clock.tick()
            img = sensor.snapshot()

            counts = []
            for i in range(len(thresholds)):
                counts.append(process_color(img, labels[i], thresholds[i], i))

            fps = clock.fps()
            draw_info(img, fps, labels, counts, thresholds_path)
            Display.show_image(img)

            if time.ticks_diff(time.ticks_ms(), last_save) > 1000:
                save_result(result_path, labels, counts, fps)
                last_save = time.ticks_ms()

            print("FPS: %.2f, counts:" % fps, counts)

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

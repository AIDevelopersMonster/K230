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
# - если файл доступен для записи, создает его со значением по умолчанию;
# - если файловая система недоступна, продолжает работу с порогом по умолчанию;
# - считает объекты указанного цвета;
# - записывает последний результат в файл, если запись доступна;
# - показывает, как безопасно работать с файлами на K230/CanMV.
# ============================================

import time
import os
import gc
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# На K230 при запуске из IDE относительный путь может быть недоступен для записи
# и open("file.txt", "w") может дать OSError: [Errno 22] EINVAL.
# Поэтому сначала пробуем реальные точки монтирования, а если они недоступны,
# работаем без записи файлов.
FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
THRESHOLD_FILENAME = "object_threshold.txt"
RESULT_FILENAME = "object_count_result.txt"

DEFAULT_THRESHOLD = (0, 100, -7, 127, 10, 83)
FONT_SIZE = 25
TEXT_COLOR = (233, 233, 233)
BOX_COLOR = (255, 255, 255)

PIXELS_THRESHOLD = 50
AREA_THRESHOLD = 50
MERGE_BLOBS = True


def join_path(directory, filename):
    """Join directory and filename without depending on os.path."""
    if directory == "/":
        return "/" + filename
    return directory + "/" + filename


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
    """Write text to file. Returns True on success, False on error."""
    try:
        with open(path, "w") as f:
            f.write(text)
        return True
    except OSError as e:
        print("File write failed:", path, e)
        return False


def read_text_file(path):
    """Read whole text file."""
    with open(path, "r") as f:
        return f.read()


def find_writable_directory():
    """Find a writable directory for demo files.

    The test file is created and removed. If no directory is writable,
    return None and the demo will continue without file output.
    """
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


def load_or_create_threshold(file_dir):
    """Read threshold from file or create file with default threshold."""
    if file_dir is None:
        print("Using default threshold, file system is not writable")
        return DEFAULT_THRESHOLD, None, None

    threshold_path = join_path(file_dir, THRESHOLD_FILENAME)
    result_path = join_path(file_dir, RESULT_FILENAME)

    if not file_exists(threshold_path):
        ok = write_text_file(threshold_path, threshold_to_text(DEFAULT_THRESHOLD))
        if ok:
            print("Created", threshold_path, "with default threshold")
        else:
            print("Cannot create threshold file, using default threshold")
        return DEFAULT_THRESHOLD, threshold_path, result_path

    try:
        text = read_text_file(threshold_path)
        threshold = text_to_threshold(text)
        print("Loaded threshold:", threshold)
        return threshold, threshold_path, result_path
    except Exception as e:
        print("Cannot read threshold file, using default:", e)
        return DEFAULT_THRESHOLD, threshold_path, result_path


def save_count_result(result_path, count, fps):
    """Write the latest recognition result to text file if path is available."""
    if result_path is None:
        return
    text = "objects=%d\nfps=%.3f\ntime_ms=%d\n" % (count, fps, time.ticks_ms())
    write_text_file(result_path, text)


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


def draw_info(img, fps, count, threshold_path):
    img.draw_string_advanced(0, 0, FONT_SIZE, "FPS: %.3f    Num: %d" % (fps, count), color=TEXT_COLOR)
    if threshold_path:
        img.draw_string_advanced(0, 35, 18, "file: " + threshold_path, color=TEXT_COLOR)
    else:
        img.draw_string_advanced(0, 35, 18, "file write: disabled", color=TEXT_COLOR)


def main():
    sensor = None
    file_dir = find_writable_directory()
    threshold, threshold_path, result_path = load_or_create_threshold(file_dir)
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

            draw_info(img, fps, count, threshold_path)
            Display.show_image(img)

            # Записываем результат не каждый кадр, а примерно раз в секунду,
            # чтобы не делать слишком много операций записи.
            if time.ticks_diff(time.ticks_ms(), last_save) > 1000:
                save_count_result(result_path, count, fps)
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

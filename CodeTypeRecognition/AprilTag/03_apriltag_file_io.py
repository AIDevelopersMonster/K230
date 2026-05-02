# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# AprilTag Recognition + File Read/Write
# Распознавание AprilTag + чтение и запись файлов
#
# Что делает:
# - читает настройки ROI и семейств тегов из файла;
# - если файл доступен для записи, создает его со значениями по умолчанию;
# - если файловая система недоступна, продолжает работу со значениями по умолчанию;
# - распознает AprilTag через img.find_apriltags();
# - записывает последний распознанный тег в текстовый файл.
# ============================================

import time
import math
import os
import gc
import image
from media.sensor import *
from media.display import *
from media.media import *

SENSOR_WIDTH = 400
SENSOR_HEIGHT = 240
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
DISPLAY_X = 120
DISPLAY_Y = 120
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (255, 0, 0)
CENTER_COLOR = (0, 255, 0)

FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
CONFIG_FILENAME = "apriltag_config.txt"
RESULT_FILENAME = "apriltag_result.txt"

FAMILY_BITS = {
    "TAG16H5": image.TAG16H5,
    "TAG25H7": image.TAG25H7,
    "TAG25H9": image.TAG25H9,
    "TAG36H10": image.TAG36H10,
    "TAG36H11": image.TAG36H11,
    "ARTOOLKIT": image.ARTOOLKIT,
}

DEFAULT_CONFIG = {
    "USE_ROI": 0,
    "ROI": (40, 20, 320, 200),
    "FAMILIES": "TAG36H11",
}

last_tag_key = ""
last_save_ms = 0
SAVE_INTERVAL_MS = 500


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


def roi_to_text(roi):
    return ",".join([str(v) for v in roi])


def text_to_roi(text):
    parts = text.replace(" ", "").split(",")
    if len(parts) != 4:
        raise ValueError("ROI must contain 4 numbers: x,y,w,h")
    return tuple([int(v) for v in parts])


def config_to_text(config):
    lines = []
    lines.append("# K230 AprilTag Recognition config")
    lines.append("# USE_ROI=0 means scan the whole frame")
    lines.append("# USE_ROI=1 means scan only ROI")
    lines.append("# FAMILIES example: TAG36H11 or TAG16H5,TAG25H7,TAG36H11")
    lines.append("USE_ROI=" + str(config["USE_ROI"]))
    lines.append("ROI=" + roi_to_text(config["ROI"]))
    lines.append("FAMILIES=" + str(config["FAMILIES"]))
    return "\n".join(lines) + "\n"


def parse_config(text):
    config = dict(DEFAULT_CONFIG)
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().upper()
        value = value.strip()
        if key == "USE_ROI":
            config["USE_ROI"] = int(value)
        elif key == "ROI":
            config["ROI"] = text_to_roi(value)
        elif key == "FAMILIES":
            config["FAMILIES"] = value.upper()
    return config


def load_or_create_config(file_dir):
    if file_dir is None:
        print("Using default config, file system is not writable")
        return dict(DEFAULT_CONFIG), None, None

    config_path = join_path(file_dir, CONFIG_FILENAME)
    result_path = join_path(file_dir, RESULT_FILENAME)

    if not file_exists(config_path):
        ok = write_text_file(config_path, config_to_text(DEFAULT_CONFIG))
        if ok:
            print("Created", config_path)
        else:
            print("Cannot create config file, using defaults")
        return dict(DEFAULT_CONFIG), config_path, result_path

    try:
        text = read_text_file(config_path)
        config = parse_config(text)
        print("Loaded config from", config_path)
        return config, config_path, result_path
    except Exception as e:
        print("Cannot read config file, using defaults:", e)
        return dict(DEFAULT_CONFIG), config_path, result_path


def families_from_text(text):
    mask = 0
    for raw_name in text.split(","):
        name = raw_name.strip().upper()
        if name in FAMILY_BITS:
            mask |= FAMILY_BITS[name]
    if mask == 0:
        mask = image.TAG36H11
    return mask


def family_name(tag):
    for name, value in FAMILY_BITS.items():
        if tag.family() == value:
            return name
    return "UNKNOWN"


def degrees(rad):
    return (180.0 * rad) / math.pi


def save_tag_result(result_path, tag, fps):
    global last_tag_key, last_save_ms
    if result_path is None:
        return

    family = family_name(tag)
    tag_id = tag.id()
    tag_key = "%s:%d" % (family, tag_id)
    now = time.ticks_ms()
    if tag_key == last_tag_key and time.ticks_diff(now, last_save_ms) < SAVE_INTERVAL_MS:
        return

    x, y, w, h = tag.rect()
    lines = [
        "time_ms=%d" % now,
        "fps=%.3f" % fps,
        "family=" + family,
        "id=" + str(tag_id),
        "rotation_deg=%.3f" % degrees(tag.rotation()),
        "x=" + str(x),
        "y=" + str(y),
        "w=" + str(w),
        "h=" + str(h),
        "cx=" + str(tag.cx()),
        "cy=" + str(tag.cy()),
        "decision_margin=" + str(tag.decision_margin()),
        "hamming=" + str(tag.hamming()),
    ]
    if write_text_file(result_path, "\n".join(lines) + "\n"):
        last_tag_key = tag_key
        last_save_ms = now


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=SENSOR_WIDTH, height=SENSOR_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def find_tags(img, config, families_mask):
    if config["USE_ROI"]:
        roi = config["ROI"]
        img.draw_rectangle(roi, color=(120, 120, 120), thickness=1)
        return img.find_apriltags(roi=roi, families=families_mask)
    return img.find_apriltags(families=families_mask)


def draw_tag(img, tag, fps, result_path):
    family = family_name(tag)
    rot = degrees(tag.rotation())
    img.draw_rectangle(tag.rect(), color=BOX_COLOR, thickness=4)
    img.draw_cross(tag.cx(), tag.cy(), color=CENTER_COLOR, thickness=2)
    img.draw_string_advanced(0, 0, 22, "%s ID:%d" % (family, tag.id()), color=TEXT_COLOR)
    img.draw_string_advanced(0, 26, 18, "rot: %.2f deg" % rot, color=TEXT_COLOR)
    save_tag_result(result_path, tag, fps)
    print("Tag Family %s, Tag ID %d, rotation %.3f degrees" % (family, tag.id(), rot))


def draw_info(img, fps, count, config_path):
    img.draw_string_advanced(0, SENSOR_HEIGHT - 26, 18, "FPS: %.2f  Tags: %d" % (fps, count), color=TEXT_COLOR)
    if config_path:
        img.draw_string_advanced(0, SENSOR_HEIGHT - 48, 14, "file: " + config_path, color=TEXT_COLOR)
    else:
        img.draw_string_advanced(0, SENSOR_HEIGHT - 48, 14, "file write: disabled", color=TEXT_COLOR)


def main():
    sensor = None
    file_dir = find_writable_directory()
    config, config_path, result_path = load_or_create_config(file_dir)
    families_mask = families_from_text(config["FAMILIES"])

    try:
        sensor = init_sensor()
        init_display()
        sensor.run()
        clock = time.clock()

        while True:
            clock.tick()
            img = sensor.snapshot()
            tags = find_tags(img, config, families_mask)
            fps = clock.fps()

            for tag in tags:
                draw_tag(img, tag, fps, result_path)
                break

            draw_info(img, fps, len(tags), config_path)
            Display.show_image(img, x=DISPLAY_X, y=DISPLAY_Y)
            gc.collect()

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

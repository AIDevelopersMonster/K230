# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# QR Code Recognition + File Read/Write
# Распознавание QR-кодов + чтение и запись файлов
#
# Что делает:
# - читает настройки ROI из файла;
# - если файл доступен для записи, создает его со значениями по умолчанию;
# - если файловая система недоступна, продолжает работу со значениями по умолчанию;
# - распознает QR-коды через img.find_qrcodes();
# - записывает последний распознанный QR-код в текстовый файл.
# ============================================

import time
import os
import gc
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (200, 0, 0)
CENTER_COLOR = (0, 255, 0)

FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
CONFIG_FILENAME = "qrcode_config.txt"
RESULT_FILENAME = "qrcode_result.txt"

DEFAULT_CONFIG = {
    "USE_ROI": 0,
    "ROI": (120, 60, 400, 360),
}

last_payload = ""
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
    lines.append("# K230 QR Code Recognition config")
    lines.append("# USE_ROI=0 means scan the whole frame")
    lines.append("# USE_ROI=1 means scan only ROI")
    lines.append("USE_ROI=" + str(config["USE_ROI"]))
    lines.append("ROI=" + roi_to_text(config["ROI"]))
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


def save_qrcode_result(result_path, qr, fps):
    global last_payload, last_save_ms
    if result_path is None:
        return

    payload = qr.payload()
    now = time.ticks_ms()
    if payload == last_payload and time.ticks_diff(now, last_save_ms) < SAVE_INTERVAL_MS:
        return

    x, y, w, h = qr.rect()
    lines = [
        "time_ms=%d" % now,
        "fps=%.3f" % fps,
        "payload=" + payload,
        "x=" + str(x),
        "y=" + str(y),
        "w=" + str(w),
        "h=" + str(h),
        "version=" + str(qr.version()),
        "ecc_level=" + str(qr.ecc_level()),
        "data_type=" + str(qr.data_type()),
    ]
    if write_text_file(result_path, "\n".join(lines) + "\n"):
        last_payload = payload
        last_save_ms = now


def init_camera():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def find_qrcodes(img, config):
    if config["USE_ROI"]:
        roi = config["ROI"]
        img.draw_rectangle(roi, color=(120, 120, 120), thickness=1)
        return img.find_qrcodes(roi=roi)
    return img.find_qrcodes()


def draw_qrcode(img, qr, fps, result_path):
    payload = qr.payload()
    x, y, w, h = qr.rect()
    img.draw_rectangle(qr.rect(), thickness=3, color=BOX_COLOR)
    img.draw_cross(x + w // 2, y + h // 2, color=CENTER_COLOR, thickness=2)
    img.draw_string_advanced(0, 0, 26, "QR: " + payload, color=TEXT_COLOR)
    save_qrcode_result(result_path, qr, fps)
    print('QR Payload "%s"' % payload)


def draw_info(img, fps, count, config_path):
    img.draw_string_advanced(0, DISPLAY_HEIGHT - 35, 24, "FPS: %.2f  QR: %d" % (fps, count), color=TEXT_COLOR)
    if config_path:
        img.draw_string_advanced(0, DISPLAY_HEIGHT - 60, 16, "file: " + config_path, color=TEXT_COLOR)
    else:
        img.draw_string_advanced(0, DISPLAY_HEIGHT - 60, 16, "file write: disabled", color=TEXT_COLOR)


def main():
    sensor = None
    file_dir = find_writable_directory()
    config, config_path, result_path = load_or_create_config(file_dir)

    try:
        sensor = init_camera()
        init_display()
        sensor.run()
        clock = time.clock()
        while True:
            clock.tick()
            img = sensor.snapshot()
            qr_codes = find_qrcodes(img, config)
            fps = clock.fps()
            for qr in qr_codes:
                draw_qrcode(img, qr, fps, result_path)
                break
            draw_info(img, fps, len(qr_codes), config_path)
            Display.show_image(img)
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

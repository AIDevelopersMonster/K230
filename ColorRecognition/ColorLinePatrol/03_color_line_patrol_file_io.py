# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Color Line Patrol + File Read/Write
# Цветное движение по линии + чтение и запись файлов
#
# Что делает:
# - читает настройки линии и PID из файла;
# - если файл доступен для записи, создает его со значениями по умолчанию;
# - если файловая система недоступна, продолжает работу со значениями по умолчанию;
# - ищет линию в нижней половине кадра;
# - записывает последний результат в текстовый файл.
# ============================================

import time
import os
import gc
import image
from media.sensor import *
from media.display import *
from media.media import *

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
SCREEN_CENTER = DISPLAY_WIDTH // 2

FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
CONFIG_FILENAME = "line_patrol_config.txt"
RESULT_FILENAME = "line_patrol_result.txt"

DEFAULT_CONFIG = {
    "COLOR": "GREEN",
    "THRESHOLD": (40, 86, -44, -20, -24, 25),
    "KP": 1.0,
    "KI": 0.1,
    "KD": 0.2,
    "BASE_SPEED": 300,
}

KNOWN_THRESHOLDS = {
    "BLACK": (21, 33, -15, 9, -9, 6),
    "GREEN": (40, 86, -44, -20, -24, 25),
}

ROI = (0, DISPLAY_HEIGHT // 2, DISPLAY_WIDTH, DISPLAY_HEIGHT // 2)
PIXELS_THRESHOLD = 80
AREA_THRESHOLD = 80
MERGE_BLOBS = True
TEXT_COLOR = (255, 255, 255)
CENTER_LINE_COLOR = (0, 255, 0)
CURRENT_LINE_COLOR = (255, 0, 0)
INTEGRAL_LIMIT = 100

prev_error = 0
integral = 0


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


def threshold_to_text(threshold):
    return ",".join([str(v) for v in threshold])


def text_to_threshold(text):
    parts = text.replace(" ", "").split(",")
    if len(parts) != 6:
        raise ValueError("THRESHOLD must contain 6 numbers")
    return tuple([int(v) for v in parts])


def config_to_text(config):
    lines = []
    lines.append("# K230 Color Line Patrol config")
    lines.append("# COLOR can be BLACK or GREEN")
    lines.append("COLOR=" + str(config["COLOR"]))
    lines.append("THRESHOLD=" + threshold_to_text(config["THRESHOLD"]))
    lines.append("KP=" + str(config["KP"]))
    lines.append("KI=" + str(config["KI"]))
    lines.append("KD=" + str(config["KD"]))
    lines.append("BASE_SPEED=" + str(config["BASE_SPEED"]))
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

        if key == "COLOR":
            color = value.upper()
            config["COLOR"] = color
            if color in KNOWN_THRESHOLDS:
                config["THRESHOLD"] = KNOWN_THRESHOLDS[color]
        elif key == "THRESHOLD":
            config["THRESHOLD"] = text_to_threshold(value)
        elif key == "KP":
            config["KP"] = float(value)
        elif key == "KI":
            config["KI"] = float(value)
        elif key == "KD":
            config["KD"] = float(value)
        elif key == "BASE_SPEED":
            config["BASE_SPEED"] = int(float(value))

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


def get_closest_rgb(lab_threshold):
    l_center = (lab_threshold[0] + lab_threshold[1]) // 2
    a_center = (lab_threshold[2] + lab_threshold[3]) // 2
    b_center = (lab_threshold[4] + lab_threshold[5]) // 2
    return image.lab_to_rgb((l_center, a_center, b_center))


def limit_value(value, min_value, max_value):
    if value > max_value:
        return max_value
    if value < min_value:
        return min_value
    return value


def calculate_pid(config, target, current):
    global prev_error, integral

    kp = config["KP"]
    ki = config["KI"]
    kd = config["KD"]
    base_speed = config["BASE_SPEED"]

    error = target - current
    integral += error
    integral = limit_value(integral, -INTEGRAL_LIMIT, INTEGRAL_LIMIT)
    derivative = error - prev_error
    output = kp * error + ki * integral + kd * derivative

    left_speed = int(base_speed - output)
    right_speed = int(base_speed + output)
    prev_error = error
    return error, left_speed, right_speed


def save_result(result_path, config, fps, error, left_speed, right_speed, found):
    if result_path is None:
        return

    lines = [
        "time_ms=%d" % time.ticks_ms(),
        "fps=%.3f" % fps,
        "found=" + str(found),
        "color=" + str(config["COLOR"]),
        "error=" + str(error),
        "left_speed=" + str(left_speed),
        "right_speed=" + str(right_speed),
    ]
    write_text_file(result_path, "\n".join(lines) + "\n")


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def find_largest_blob(blobs):
    if not blobs:
        return None
    return max(blobs, key=lambda b: b[4])


def process_line(img, config, draw_color):
    threshold = config["THRESHOLD"]
    blobs = img.find_blobs(
        [threshold],
        roi=ROI,
        pixels_threshold=PIXELS_THRESHOLD,
        area_threshold=AREA_THRESHOLD,
        merge=MERGE_BLOBS,
    )

    largest_blob = find_largest_blob(blobs)
    img.draw_rectangle(ROI, color=(120, 120, 120), thickness=1)
    img.draw_line(SCREEN_CENTER, 0, SCREEN_CENTER, DISPLAY_HEIGHT, color=CENTER_LINE_COLOR, thickness=1)

    if largest_blob is None:
        return False, 0, 0, 0

    x = largest_blob[0]
    y = largest_blob[1]
    w = largest_blob[2]
    h = largest_blob[3]
    current_x = x + w // 2
    current_y = y + h // 2

    error, left_speed, right_speed = calculate_pid(config, SCREEN_CENTER, current_x)

    img.draw_rectangle((x, y, w, h), color=draw_color, thickness=4)
    img.draw_cross(current_x, current_y, color=draw_color, thickness=2)
    img.draw_line(current_x, y, current_x, y + h, color=CURRENT_LINE_COLOR, thickness=2)
    img.draw_string_advanced(x, max(0, y - 30), 24, str(config["COLOR"]), color=draw_color)

    return True, error, left_speed, right_speed


def draw_info(img, fps, config, found, error, left_speed, right_speed, config_path):
    status = "FOUND" if found else "NO LINE"
    img.draw_string_advanced(0, 0, 22, "FPS: %.2f  %s" % (fps, status), color=TEXT_COLOR)
    img.draw_string_advanced(0, 26, 18, "err:%d  L:%d  R:%d" % (error, left_speed, right_speed), color=TEXT_COLOR)
    if config_path:
        img.draw_string_advanced(0, 50, 16, "file: " + config_path, color=TEXT_COLOR)
    else:
        img.draw_string_advanced(0, 50, 16, "file write: disabled", color=TEXT_COLOR)


def main():
    sensor = None
    file_dir = find_writable_directory()
    config, config_path, result_path = load_or_create_config(file_dir)
    draw_color = get_closest_rgb(config["THRESHOLD"])
    last_save = time.ticks_ms()

    try:
        sensor = init_sensor()
        init_display()
        sensor.run()
        clock = time.clock()

        while True:
            clock.tick()
            img = sensor.snapshot()
            found, error, left_speed, right_speed = process_line(img, config, draw_color)
            fps = clock.fps()

            draw_info(img, fps, config, found, error, left_speed, right_speed, config_path)
            Display.show_image(img)

            if time.ticks_diff(time.ticks_ms(), last_save) > 1000:
                save_result(result_path, config, fps, error, left_speed, right_speed, found)
                last_save = time.ticks_ms()

            print("FPS: %.2f, found: %s, error: %d" % (fps, str(found), error))

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

# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Color Line Patrol + UART PID
# Цветное движение по линии + UART + PID
#
# Что делает:
# - ищет линию в нижней половине кадра;
# - выбирает самый большой найденный цветовой блок;
# - вычисляет ошибку: центр экрана минус центр линии;
# - PID-регулятор рассчитывает скорости левого и правого мотора;
# - отправляет команду по UART в формате: $left,right#
# ============================================

import time
import gc
import image
from media.sensor import *
from media.display import *
from media.media import *

USE_UART = True
try:
    from ybUtils.YbUart import YbUart
except Exception as import_error:
    print("YbUart library not found:", import_error)
    USE_UART = False

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
SCREEN_CENTER = DISPLAY_WIDTH // 2

THRESHOLDS = [
    (21, 33, -15, 9, -9, 6),       # BLACK LINE
    (40, 86, -44, -20, -24, 25),   # GREEN LINE
]

COLOR_LABELS = ["BLACK", "GREEN"]
COLOR_INDEX = 1

ROI = (0, DISPLAY_HEIGHT // 2, DISPLAY_WIDTH, DISPLAY_HEIGHT // 2)
PIXELS_THRESHOLD = 80
AREA_THRESHOLD = 80
MERGE_BLOBS = True

# PID parameters. Tune for your robot and surface.
KP = 1.0
KI = 0.1
KD = 0.2
BASE_SPEED = 300
MAX_SPEED = 600
MIN_SPEED = -600
INTEGRAL_LIMIT = 100

TEXT_COLOR = (255, 255, 255)
CENTER_LINE_COLOR = (0, 255, 0)
CURRENT_LINE_COLOR = (255, 0, 0)

prev_error = 0
integral = 0
uart = None


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


def init_uart():
    global uart, USE_UART
    if not USE_UART:
        return
    try:
        uart = YbUart(9600)
        print("UART initialized at 9600 baud")
    except Exception as e:
        print("UART init failed:", e)
        USE_UART = False


def send_motor_command(left_speed, right_speed):
    if not USE_UART or uart is None:
        return
    command = "$%d,%d#" % (int(left_speed), int(right_speed))
    try:
        uart.send(command)
        print("UART:", command)
    except Exception as e:
        print("UART send failed:", e)


def calculate_pid(target, current):
    global prev_error, integral

    error = target - current
    integral += error
    integral = limit_value(integral, -INTEGRAL_LIMIT, INTEGRAL_LIMIT)
    derivative = error - prev_error

    output = KP * error + KI * integral + KD * derivative

    left_speed = BASE_SPEED - output
    right_speed = BASE_SPEED + output

    left_speed = limit_value(left_speed, MIN_SPEED, MAX_SPEED)
    right_speed = limit_value(right_speed, MIN_SPEED, MAX_SPEED)

    prev_error = error
    return int(left_speed), int(right_speed), int(error), output


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


def process_line(img, threshold, draw_color):
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
        send_motor_command(0, 0)
        return None, 0, 0, 0

    x = largest_blob[0]
    y = largest_blob[1]
    w = largest_blob[2]
    h = largest_blob[3]
    current_x = x + w // 2
    current_y = y + h // 2

    left_speed, right_speed, error, output = calculate_pid(SCREEN_CENTER, current_x)
    send_motor_command(left_speed, right_speed)

    img.draw_rectangle((x, y, w, h), color=draw_color, thickness=4)
    img.draw_cross(current_x, current_y, color=draw_color, thickness=2)
    img.draw_line(current_x, y, current_x, y + h, color=CURRENT_LINE_COLOR, thickness=2)
    img.draw_string_advanced(x, max(0, y - 30), 24, COLOR_LABELS[COLOR_INDEX], color=draw_color)

    return largest_blob, error, left_speed, right_speed


def draw_info(img, fps, blob, error, left_speed, right_speed):
    status = "FOUND" if blob else "NO LINE"
    img.draw_string_advanced(0, 0, 22, "FPS: %.2f  %s" % (fps, status), color=TEXT_COLOR)
    img.draw_string_advanced(0, 26, 18, "err:%d  L:%d  R:%d  UART:%s" % (error, left_speed, right_speed, str(USE_UART)), color=TEXT_COLOR)


def main():
    sensor = None
    try:
        init_uart()
        sensor = init_sensor()
        init_display()
        sensor.run()
        clock = time.clock()

        threshold = THRESHOLDS[COLOR_INDEX]
        draw_color = get_closest_rgb(threshold)

        while True:
            clock.tick()
            img = sensor.snapshot()
            blob, error, left_speed, right_speed = process_line(img, threshold, draw_color)
            fps = clock.fps()

            draw_info(img, fps, blob, error, left_speed, right_speed)
            Display.show_image(img)
            print("FPS: %.2f, error: %d, L: %d, R: %d" % (fps, error, left_speed, right_speed))

    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Error occurred:", e)
    finally:
        send_motor_command(0, 0)
        if sensor:
            sensor.stop()
            sensor.deinit()
        Display.deinit()
        MediaManager.deinit()
        gc.collect()


if __name__ == "__main__":
    main()

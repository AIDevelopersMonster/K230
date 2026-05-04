# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# DM Code Recognition + UART
# Распознавание Data Matrix + отправка данных по UART
#
# Что делает:
# - ищет Data Matrix / DM codes через img.find_datamatrices();
# - рисует рамку и показывает payload/rotation на экране;
# - отправляет координаты, payload и rotation через Yahboom protocol;
# - если UART-библиотек нет, продолжает работать без отправки.
# ============================================

import time
import math
import os
import gc
from media.sensor import *
from media.display import *
from media.media import *

USE_UART = True
try:
    from libs.YbProtocol import YbProtocol
    from ybUtils.YbUart import YbUart
except Exception as import_error:
    print("UART/protocol libraries not found:", import_error)
    USE_UART = False

DETECT_WIDTH = 640
DETECT_HEIGHT = 480
TEXT_COLOR = (255, 0, 0)
BOX_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)
DMCODE_ROI = None

uart = None
pto = None
last_payload = ""
last_send_ms = 0
SEND_INTERVAL_MS = 500


def degrees(rad):
    return (180.0 * rad) / math.pi


def init_uart():
    global uart, pto, USE_UART
    if not USE_UART:
        return
    try:
        uart = YbUart(baudrate=115200)
        pto = YbProtocol()
        print("UART initialized at 115200 baud")
    except Exception as e:
        print("UART init failed:", e)
        USE_UART = False


def send_dmcode_data(matrix):
    global last_payload, last_send_ms
    if not USE_UART or uart is None or pto is None:
        return

    payload = matrix.payload()
    now = time.ticks_ms()
    if payload == last_payload and time.ticks_diff(now, last_send_ms) < SEND_INTERVAL_MS:
        return

    x, y, w, h = matrix.rect()
    rotation = degrees(matrix.rotation())
    try:
        pto_data = pto.get_dmcode_data(x, y, w, h, payload, rotation)
        uart.send(pto_data)
        print("UART:", pto_data)
        last_payload = payload
        last_send_ms = now
    except Exception as e:
        print("UART send failed:", e)


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=DETECT_WIDTH, height=DETECT_HEIGHT, to_ide=True)
    MediaManager.init()


def find_dm_codes(img):
    if DMCODE_ROI:
        img.draw_rectangle(DMCODE_ROI, color=(120, 120, 120), thickness=1)
        return img.find_datamatrices(roi=DMCODE_ROI)
    return img.find_datamatrices()


def process_dmcode(img, matrix):
    payload = matrix.payload()
    rotation = degrees(matrix.rotation())
    x, y, w, h = matrix.rect()
    text_y = y - 25 if y - 25 > 0 else y

    img.draw_rectangle(matrix.rect(), color=BOX_COLOR, thickness=4)
    img.draw_cross(x + w // 2, y + h // 2, color=(0, 255, 0), thickness=2)
    img.draw_string_advanced(x, text_y, 20, "%s [%.2f] deg" % (payload, rotation), color=TEXT_COLOR)
    img.draw_string_advanced(0, 0, 20, "DM: " + payload, color=WHITE)
    img.draw_string_advanced(0, 24, 18, "UART: " + str(USE_UART), color=WHITE)

    print('payload "%s", rotation %.3f degrees' % (payload, rotation))
    send_dmcode_data(matrix)


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
        init_uart()
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
                process_dmcode(img, matrix)
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

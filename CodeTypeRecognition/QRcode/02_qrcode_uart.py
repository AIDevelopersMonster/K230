# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# QR Code Recognition + UART
# Распознавание QR-кодов + отправка данных по UART
#
# Что делает:
# - ищет QR-коды через img.find_qrcodes();
# - рисует рамку и показывает payload на экране;
# - отправляет координаты и payload через Yahboom protocol;
# - если UART-библиотек нет, продолжает работать без отправки.
# ============================================

import time
import gc
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager

USE_UART = True
try:
    from libs.YbProtocol import YbProtocol
    from ybUtils.YbUart import YbUart
except Exception as import_error:
    print("UART/protocol libraries not found:", import_error)
    USE_UART = False

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (200, 0, 0)
CENTER_COLOR = (0, 255, 0)
QRCODE_ROI = None

uart = None
pto = None
last_payload = ""
last_send_ms = 0
SEND_INTERVAL_MS = 500


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


def send_qrcode_data(rect, payload):
    global last_payload, last_send_ms
    if not USE_UART or uart is None or pto is None:
        return
    now = time.ticks_ms()
    if payload == last_payload and time.ticks_diff(now, last_send_ms) < SEND_INTERVAL_MS:
        return
    x, y, w, h = rect
    try:
        pto_data = pto.get_qrcode_data(x, y, w, h, payload)
        uart.send(pto_data)
        print("UART:", pto_data)
        last_payload = payload
        last_send_ms = now
    except Exception as e:
        print("UART send failed:", e)


def init_camera():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def find_qrcodes(img):
    if QRCODE_ROI:
        img.draw_rectangle(QRCODE_ROI, color=(120, 120, 120), thickness=1)
        return img.find_qrcodes(roi=QRCODE_ROI)
    return img.find_qrcodes()


def process_qrcode(img, qr):
    payload = qr.payload()
    rect = qr.rect()
    x, y, w, h = rect
    img.draw_rectangle(rect, thickness=3, color=BOX_COLOR)
    img.draw_cross(x + w // 2, y + h // 2, color=CENTER_COLOR, thickness=2)
    img.draw_string_advanced(0, 0, 26, "QR: " + payload, color=TEXT_COLOR)
    img.draw_string_advanced(0, 30, 20, "UART: " + str(USE_UART), color=TEXT_COLOR)
    print('QR Payload "%s"' % payload)
    send_qrcode_data(rect, payload)


def draw_fps(img, fps, count):
    img.draw_string_advanced(0, DISPLAY_HEIGHT - 35, 24, "FPS: %.2f  QR: %d" % (fps, count), color=TEXT_COLOR)


def main():
    sensor = None
    try:
        init_uart()
        sensor = init_camera()
        init_display()
        sensor.run()
        clock = time.clock()
        while True:
            clock.tick()
            img = sensor.snapshot()
            qr_codes = find_qrcodes(img)
            for qr in qr_codes:
                process_qrcode(img, qr)
                break
            draw_fps(img, clock.fps(), len(qr_codes))
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

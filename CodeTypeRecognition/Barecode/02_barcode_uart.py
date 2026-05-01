# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Barcode Recognition + UART
# Распознавание штрих-кодов + отправка данных по UART
#
# Что делает:
# - ищет 1D штрих-коды через img.find_barcodes();
# - рисует рамку и показывает payload на экране;
# - отправляет координаты и payload через Yahboom protocol;
# - если UART-библиотек нет, продолжает работать без отправки.
# ============================================

import time
import gc
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager
import image

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
BOX_COLOR = (46, 47, 48)
BARCODE_ROI = None

BARCODE_TYPES = {
    image.EAN2: "EAN2",
    image.EAN5: "EAN5",
    image.EAN8: "EAN8",
    image.UPCE: "UPCE",
    image.ISBN10: "ISBN10",
    image.UPCA: "UPCA",
    image.EAN13: "EAN13",
    image.ISBN13: "ISBN13",
    image.I25: "I25",
    image.DATABAR: "DATABAR",
    image.DATABAR_EXP: "DATABAR_EXP",
    image.CODABAR: "CODABAR",
    image.CODE39: "CODE39",
    image.PDF417: "PDF417",
    image.CODE93: "CODE93",
    image.CODE128: "CODE128",
}

uart = None
pto = None
last_payload = ""
last_send_ms = 0
SEND_INTERVAL_MS = 500


def barcode_name(code):
    return BARCODE_TYPES.get(code.type(), "UNKNOWN")


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


def send_barcode_data(rect, payload):
    """Send barcode data with rate limiting."""
    global last_payload, last_send_ms

    if not USE_UART or uart is None or pto is None:
        return

    now = time.ticks_ms()
    if payload == last_payload and time.ticks_diff(now, last_send_ms) < SEND_INTERVAL_MS:
        return

    x, y, w, h = rect
    try:
        pto_data = pto.get_barcode_data(x, y, w, h, payload)
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


def find_codes(img):
    if BARCODE_ROI:
        img.draw_rectangle(BARCODE_ROI, color=(120, 120, 120), thickness=1)
        return img.find_barcodes(roi=BARCODE_ROI)
    return img.find_barcodes()


def process_code(img, code):
    code_type = barcode_name(code)
    payload = code.payload()
    rect = code.rect()
    x, y, w, h = rect

    img.draw_rectangle(rect, thickness=6, color=BOX_COLOR)
    img.draw_cross(x + w // 2, y + h // 2, color=(255, 0, 0), thickness=2)
    img.draw_string_advanced(10, 10, 28, "Type: " + code_type, color=TEXT_COLOR)
    img.draw_string_advanced(10, 42, 28, "Data: " + payload, color=TEXT_COLOR)
    img.draw_string_advanced(10, 74, 20, "UART: " + str(USE_UART), color=TEXT_COLOR)

    print('Barcode %s, Payload "%s"' % (code_type, payload))
    send_barcode_data(rect, payload)


def draw_fps(img, fps, count):
    img.draw_string_advanced(10, DISPLAY_HEIGHT - 35, 24, "FPS: %.2f  Codes: %d" % (fps, count), color=TEXT_COLOR)


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
            codes = find_codes(img)

            for code in codes:
                process_code(img, code)
                break

            draw_fps(img, clock.fps(), len(codes))
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

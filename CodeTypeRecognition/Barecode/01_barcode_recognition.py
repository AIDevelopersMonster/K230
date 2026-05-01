# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Barcode Recognition / Распознавание штрих-кодов
#
# Что делает:
# - получает изображение с камеры K230;
# - ищет 1D штрих-коды через img.find_barcodes();
# - рисует рамку вокруг найденного штрих-кода;
# - показывает тип кода, payload и FPS;
# - печатает результат в консоль CanMV IDE.
# ============================================

import time
import gc
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager
import image

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (46, 47, 48)

# Для ускорения можно ограничить область поиска.
# None = поиск по всему кадру.
# Рекомендуемый ROI для горизонтального штрих-кода: (0, 200, 640, 80)
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


def barcode_name(code):
    """Return barcode type name."""
    return BARCODE_TYPES.get(code.type(), "UNKNOWN")


def init_camera():
    """Initialize camera settings."""
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    """Initialize LCD and IDE output."""
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def find_codes(img):
    """Find barcodes in image or selected ROI."""
    if BARCODE_ROI:
        img.draw_rectangle(BARCODE_ROI, color=(120, 120, 120), thickness=1)
        return img.find_barcodes(roi=BARCODE_ROI)
    return img.find_barcodes()


def draw_code_info(img, code):
    """Draw rectangle and decoded text for one barcode."""
    code_type = barcode_name(code)
    payload = code.payload()
    x, y, w, h = code.rect()

    img.draw_rectangle(code.rect(), thickness=6, color=BOX_COLOR)
    img.draw_string_advanced(10, 10, 28, "Type: " + code_type, color=TEXT_COLOR)
    img.draw_string_advanced(10, 42, 28, "Data: " + payload, color=TEXT_COLOR)
    img.draw_cross(x + w // 2, y + h // 2, color=(255, 0, 0), thickness=2)

    print('Barcode %s, Payload "%s", rect=%s' % (code_type, payload, str(code.rect())))


def draw_fps(img, fps, count):
    """Draw FPS and number of detected barcodes."""
    img.draw_string_advanced(10, DISPLAY_HEIGHT - 35, 24, "FPS: %.2f  Codes: %d" % (fps, count), color=TEXT_COLOR)


def main():
    sensor = None
    try:
        sensor = init_camera()
        init_display()
        sensor.run()
        clock = time.clock()

        while True:
            clock.tick()
            img = sensor.snapshot()

            codes = find_codes(img)
            for code in codes:
                draw_code_info(img, code)
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

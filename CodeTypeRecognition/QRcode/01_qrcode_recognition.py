# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# QR Code Recognition / Распознавание QR-кодов
#
# Что делает:
# - получает изображение с камеры K230;
# - ищет QR-коды через img.find_qrcodes();
# - рисует рамку вокруг найденного QR-кода;
# - показывает payload, FPS и количество найденных QR-кодов;
# - печатает результат в консоль CanMV IDE.
# ============================================

import time
import gc
from media.sensor import Sensor
from media.display import Display
from media.media import MediaManager

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (200, 0, 0)
CENTER_COLOR = (0, 255, 0)

# None = поиск по всему кадру.
# Для ускорения можно указать ROI: (x, y, w, h), например (120, 60, 400, 360)
QRCODE_ROI = None


def init_camera():
    """Initialize camera sensor."""
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    """Initialize display and media manager."""
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def find_qrcodes(img):
    """Find QR codes in whole frame or selected ROI."""
    if QRCODE_ROI:
        img.draw_rectangle(QRCODE_ROI, color=(120, 120, 120), thickness=1)
        return img.find_qrcodes(roi=QRCODE_ROI)
    return img.find_qrcodes()


def draw_qrcode_info(img, qr):
    """Draw QR code rectangle, center, and payload."""
    payload = qr.payload()
    x, y, w, h = qr.rect()

    img.draw_rectangle(qr.rect(), thickness=3, color=BOX_COLOR)
    img.draw_cross(x + w // 2, y + h // 2, color=CENTER_COLOR, thickness=2)
    img.draw_string_advanced(0, 0, 26, "QR: " + payload, color=TEXT_COLOR)

    print('QR Payload "%s", rect=%s' % (payload, str(qr.rect())))


def draw_fps(img, fps, count):
    """Draw FPS and QR count."""
    img.draw_string_advanced(0, DISPLAY_HEIGHT - 35, 24, "FPS: %.2f  QR: %d" % (fps, count), color=TEXT_COLOR)


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

            qr_codes = find_qrcodes(img)
            for qr in qr_codes:
                draw_qrcode_info(img, qr)
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

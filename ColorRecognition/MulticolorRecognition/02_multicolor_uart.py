# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Multi-color Recognition + UART
# Многоцветное распознавание + отправка данных по UART
#
# Что делает:
# - одновременно ищет красный, зеленый и синий объекты;
# - рисует рамки и подписи на экране;
# - отправляет координаты найденных объектов через протокол Yahboom;
# - показывает FPS.
# ============================================

import time
import gc
from media.sensor import *
from media.display import *
from media.media import *

# UART/protocol libraries are included in the Yahboom K230 environment.
# If you run the script on a firmware without these libraries, set USE_UART = False.
USE_UART = True

try:
    from libs.YbProtocol import YbProtocol
    from ybUtils.YbUart import YbUart
except Exception as import_error:
    print("UART libraries not found:", import_error)
    USE_UART = False

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

COLOR_THRESHOLDS = [
    (0, 66, 7, 127, 3, 127),          # RED
    (42, 100, -128, -17, 6, 66),      # GREEN
    (43, 99, -43, -4, -56, -7),       # BLUE
]

DRAW_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
COLOR_LABELS = ["RED", "GREEN", "BLUE"]

PIXELS_THRESHOLD = 50
AREA_THRESHOLD = 500
MERGE_BLOBS = True

TEXT_COLOR = (255, 255, 255)
uart = None
pto = None


def init_uart():
    """Initialize Yahboom UART protocol if available."""
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


def send_color_data(x, y, w, h, label):
    """Send detected object data over UART if UART is enabled."""
    if not USE_UART or uart is None or pto is None:
        return
    try:
        pto_data = pto.get_multi_color_data(x, y, w, h, label)
        uart.send(pto_data)
        print("UART:", pto_data)
    except Exception as e:
        print("UART send failed:", e)


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def process_color(img, color_index):
    threshold = COLOR_THRESHOLDS[color_index]
    draw_color = DRAW_COLORS[color_index]
    label = COLOR_LABELS[color_index]

    blobs = img.find_blobs(
        [threshold],
        pixels_threshold=PIXELS_THRESHOLD,
        area_threshold=AREA_THRESHOLD,
        merge=MERGE_BLOBS,
    )

    for blob in blobs:
        x = blob[0]
        y = blob[1]
        w = blob[2]
        h = blob[3]
        cx = blob[5]
        cy = blob[6]

        img.draw_rectangle((x, y, w, h), thickness=4, color=draw_color)
        img.draw_cross(cx, cy, thickness=2, color=draw_color)
        img.draw_string_advanced(x, max(0, y - 35), 30, label, color=draw_color)
        send_color_data(x, y, w, h, label)

    return len(blobs)


def draw_info(img, fps, counts):
    total = counts[0] + counts[1] + counts[2]
    img.draw_string_advanced(0, 0, 24, "FPS: %.2f  TOTAL: %d" % (fps, total), color=TEXT_COLOR)
    img.draw_string_advanced(0, 28, 20, "R:%d  G:%d  B:%d  UART:%s" % (counts[0], counts[1], counts[2], str(USE_UART)), color=TEXT_COLOR)


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
            img = sensor.snapshot()

            counts = [0, 0, 0]
            for i in range(len(COLOR_THRESHOLDS)):
                counts[i] = process_color(img, i)

            fps = clock.fps()
            draw_info(img, fps, counts)
            Display.show_image(img)
            print("FPS: %.2f, counts:" % fps, counts)

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

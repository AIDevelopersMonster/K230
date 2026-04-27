# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Скрипт обнаружения кругов с выводом на LCD-экран.
# Камера захватывает изображение, алгоритм find_circles() находит
# круги на изображении, результаты отображаются на экране
# с подсветкой окружности, центра и нумерацией найденных объектов.
#
# Сцена:
# Белые контуры кругов на чёрном фоне.
#
# Используется:
# - Sensor (камера)
# - Display (LCD экран ST7701)
# - MediaManager (управление медиа)
#
# ============================================

import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

PICTURE_WIDTH = 400
PICTURE_HEIGHT = 240

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# ВАЖНО:
# find_circles чувствительнее find_rects().
# Поэтому ограничиваем радиус и делаем threshold выше.
CIRCLE_THRESHOLD = 4200

R_MIN = 18
R_MAX = 75
R_STEP = 3

sensor = None
clock = time.clock()

try:
    # Как в рабочем rectangle demo
    sensor = Sensor()
    sensor.reset()

    sensor.set_framesize(width=PICTURE_WIDTH, height=PICTURE_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

    MediaManager.init()
    sensor.run()

    while True:
        os.exitpoint()
        clock.tick()

        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        circle_count = 0
        print("[Circle Detection Start]")

        circles = img.find_circles(
            threshold=CIRCLE_THRESHOLD,
            x_margin=20,
            y_margin=20,
            r_margin=20,
            r_min=R_MIN,
            r_max=R_MAX,
            r_step=R_STEP
        )

        for c in circles:
            x0, y0, r = c.circle()

            # Отсекаем круги у краёв кадра
            if x0 - r < 5:
                continue
            if y0 - r < 5:
                continue
            if x0 + r > PICTURE_WIDTH - 5:
                continue
            if y0 + r > PICTURE_HEIGHT - 5:
                continue

            circle_count += 1

            img.draw_circle(c.circle(), color=(40, 167, 225), thickness=3)
            img.draw_cross(x0, y0, color=(255, 0, 0), size=8, thickness=2)

            img.draw_string(
                max(0, x0 - r),
                max(0, y0 - r - 14),
                "CIRCLE %d" % circle_count,
                color=(255, 255, 255),
                scale=1
            )

            print("CIRCLE", circle_count, "x:", x0, "y:", y0, "r:", r)

        print("[===========================]")
        print("FPS:", clock.fps())

        img.draw_string(
            2,
            2,
            "CIRCLE:%d FPS:%.1f" % (circle_count, clock.fps()),
            color=(255, 255, 255),
            scale=1
        )

        x = int((DISPLAY_WIDTH - PICTURE_WIDTH) / 2)
        y = int((DISPLAY_HEIGHT - PICTURE_HEIGHT) / 2)
        Display.show_image(img, x=x, y=y)

except KeyboardInterrupt as e:
    print("User Stop:", e)

except BaseException as e:
    print("Exception:", e)

finally:
    if isinstance(sensor, Sensor):
        sensor.stop()

    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()

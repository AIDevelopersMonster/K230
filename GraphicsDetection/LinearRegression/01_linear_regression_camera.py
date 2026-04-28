# ============================================================
# 01. Linear Regression: базовый пример с камерой
#
# Назначение:
# - найти чёрную линию на белом фоне;
# - построить одну регрессионную линию через get_regression();
# - показать направление движения для line following / line patrol.
#
# Как тестировать:
# 1. Нарисуйте или откройте на экране белое поле с чёрной полосой.
# 2. Наведите камеру K230 на эту линию.
# 3. На экране появится линия регрессии.
#
# Важно:
# - THRESHOLD = (0, 100) означает: ищем тёмные пиксели.
# - line.magnitude() показывает насколько хорошо найденная область похожа на линию.
# ============================================================

import time, os, sys, gc
from media.sensor import *
from media.display import *
from media.media import *

THRESHOLD = (0, 100)
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
SENSOR_WIDTH = 640
SENSOR_HEIGHT = 480


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=SENSOR_WIDTH, height=SENSOR_HEIGHT)
    sensor.set_pixformat(Sensor.GRAYSCALE)
    return sensor


def init_display():
    Display.init(Display.ST7701, to_ide=True)
    MediaManager.init()


def main():
    sensor = None
    try:
        sensor = init_sensor()
        init_display()
        sensor.run()
        clock = time.clock()

        x_offset = round((DISPLAY_WIDTH - SENSOR_WIDTH) / 2)
        y_offset = round((DISPLAY_HEIGHT - SENSOR_HEIGHT) / 2)

        while True:
            clock.tick()
            img = sensor.snapshot()

            line = img.get_regression([THRESHOLD])
            if line:
                img.draw_line(line.line(), color=127, thickness=4)
                img.draw_string(5, 5, "mag: %.2f" % line.magnitude(), color=255, scale=2)
                print("line:", line, "mag:", line.magnitude())
            else:
                img.draw_string(5, 5, "line: N/A", color=255, scale=2)

            Display.show_image(img, x=x_offset, y=y_offset)
            print("FPS:", clock.fps())

    except KeyboardInterrupt as e:
        print("Пользователь остановил скрипт:", e)
    except Exception as e:
        print("Ошибка:", e)
    finally:
        if sensor:
            sensor.stop()
        Display.deinit()
        MediaManager.deinit()
        gc.collect()


if __name__ == "__main__":
    main()

# ============================================
# K230 Draw Keypoints + Camera
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Рабочий пример поиска и отображения ключевых точек с камеры.
# Используются два канала камеры:
# - CAM_CHN_ID_1: RGB565 изображение для вывода на дисплей
# - CAM_CHN_ID_0: GRAYSCALE изображение для find_keypoints()
#
# Важно:
# find_keypoints() работает с grayscale-изображением.
# ROI уменьшает нагрузку и повышает стабильность/FPS.
# ============================================

import uos as os
import time
from media.sensor import *
from media.display import *
from media.media import *

WIDTH = 640
HEIGHT = 480


def init_sensor():
    """Инициализация камеры K230 без Sensor(width=..., height=...)."""
    sensor = Sensor()
    sensor.reset()

    # Цветной канал для отображения.
    sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_1)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

    # Grayscale канал для анализа keypoints.
    sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.GRAYSCALE, chn=CAM_CHN_ID_0)

    return sensor


def main():
    sensor = None
    roi = (220, 140, 200, 200)

    try:
        sensor = init_sensor()

        Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
        MediaManager.init()
        sensor.run()

        while True:
            os.exitpoint()

            img = sensor.snapshot(chn=CAM_CHN_ID_1)
            img_g = sensor.snapshot(chn=CAM_CHN_ID_0)

            img.draw_rectangle(roi, color=(173, 216, 230), fill=False, thickness=3)

            keypoints = img_g.find_keypoints(
                threshold=30,
                scale_factor=1.2,
                max_keypoints=30,
                roi=roi
            )

            if keypoints:
                print(keypoints)
                img.draw_keypoints(
                    keypoints,
                    color=(255, 0, 0),
                    size=8,
                    thickness=4,
                    fill=True
                )

            img.draw_string(10, 10, "Keypoints", color=(255, 255, 0), scale=2)
            Display.show_image(img)

    except KeyboardInterrupt:
        print("User interrupted the program")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if isinstance(sensor, Sensor):
            sensor.stop()

        Display.deinit()
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
        time.sleep_ms(100)
        MediaManager.deinit()


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    main()

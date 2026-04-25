# ============================================
# K230 Draw Keypoints Demo
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Демонстрация реального поиска и отрисовки ключевых точек без камеры.
# Сначала создаём тестовое изображение с линиями и прямоугольником,
# затем переводим его в grayscale и ищем keypoints через find_keypoints().
# Найденные точки рисуем поверх исходного изображения через draw_keypoints().
#
# Используется:
# - image.Image
# - find_keypoints()
# - draw_keypoints()
# - Display
# - MediaManager
# ============================================

import time
import os
import image
from media.display import *
from media.media import *

WIDTH = 640
HEIGHT = 480


def main():
    # Создаём изображение с белым фоном.
    img = image.Image(WIDTH, HEIGHT, image.ARGB8888)
    img.clear()
    img.draw_rectangle(0, 0, WIDTH, HEIGHT, color=(255, 255, 255), fill=True)

    Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
    MediaManager.init()

    try:
        # Рисуем контрастную геометрию, чтобы алгоритму было что находить:
        # углы, пересечения, границы и резкие изменения яркости.
        img.draw_rectangle(190, 130, 260, 190, color=(0, 0, 0), thickness=3)
        img.draw_rectangle(240, 180, 160, 90, color=(0, 191, 255), thickness=3)
        img.draw_line(190, 130, 450, 320, color=(0, 0, 0), thickness=2)
        img.draw_line(450, 130, 190, 320, color=(0, 0, 0), thickness=2)
        img.draw_string(20, 20, "find_keypoints + draw_keypoints", color=(0, 0, 0), scale=2)

        # find_keypoints работает с grayscale-изображением.
        img_g = img.to_grayscale()

        keypoints = img_g.find_keypoints(
            threshold=30,
            scale_factor=1.3,
            max_keypoints=30
        )

        if keypoints:
            img.draw_keypoints(
                keypoints,
                color=(255, 0, 0),
                size=8,
                thickness=2,
                fill=True
            )
            print("Keypoints found:", keypoints)
        else:
            img.draw_string(20, 50, "No keypoints found", color=(255, 0, 0), scale=2)

        Display.show_image(img)

        while True:
            os.exitpoint()
            time.sleep_ms(100)

    except KeyboardInterrupt as e:
        print("User stop:", e)
    except Exception as e:
        print("Exception:", e)
    finally:
        Display.deinit()
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
        time.sleep_ms(100)
        MediaManager.deinit()


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    main()

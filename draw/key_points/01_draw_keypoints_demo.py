# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                         
#
# Описание:
# Демонстрация рисования ключевых точек (keypoints) на дисплее.
# Скрипт создаёт изображение и рисует на нём красные крестики,
# имитируя ключевые точки для детектирования объектов.
#
# Используется:
# - YbRGB (дисплей) / MediaManager
#
# ============================================

import time, os
import image

from media.display import *
from media.media import *

# Устанавливаем разрешение дисплея
WIDTH = 640
HEIGHT = 480

# Создаём объект изображения с нужным разрешением и форматом цвета ARGB8888
img = image.Image(WIDTH, HEIGHT, image.ARGB8888)
# Очищаем изображение (делаем его пустым)
img.clear()
# Рисуем белый прямоугольник на весь экран (фон)
img.draw_rectangle(0, 0, WIDTH, HEIGHT, color=(255, 255, 255), fill=True)

# Инициализируем дисплей ST7701 с нашим разрешением
# to_ide=True позволяет видеть изображение в IDE
Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
# Инициализируем медиаменеджер для работы с медиа-ресурсами
MediaManager.init()

try:
    # Имитируем ключевые точки - рисуем красные крестики в ряд
    # Цикл проходит от 50 до 600 пикселей по горизонтали с шагом 60
    # Все точки находятся на высоте 240 (центр экрана по вертикали)
    for i in range(50, 600, 60):
        # draw_cross рисует крестик в указанных координатах
        # цвет (255, 0, 0) = красный, размер = 10 пикселей
        img.draw_cross(i, 240, color=(255, 0, 0), size=10)

    # Отображаем готовое изображение на дисплее
    Display.show_image(img)

    # Бесконечный цикл для удержания изображения на экране
    while True:
        time.sleep(2)

except Exception as e:
    # Выводим ошибку, если что-то пошло не так
    print(e)

finally:
    # Освобождаем ресурсы при завершении программы
    Display.deinit()
    MediaManager.deinit()

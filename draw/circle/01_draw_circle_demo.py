# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                   
#
# Описание:
# Демонстрация рисования кругов с помощью функции draw_circle().
# Скрипт создаёт изображение с "механическим колесом": 
# внешние кольца, центральный узел и 8 спиц с декоративными элементами.
#
# Используется:
# - image.Image / Display / MediaManager / math
#
# ============================================

import time, os, math
import image
from media.display import *
from media.media import *

# Устанавливаем разрешение дисплея (ширина x высота)
WIDTH = 640
HEIGHT = 480

# Создаём пустое изображение с прозрачным каналом (ARGB8888)
img = image.Image(WIDTH, HEIGHT, image.ARGB8888)
# Очищаем изображение (заполняем чёрным)
img.clear()
# Рисуем белый фон на всём экране
img.draw_rectangle(0, 0, WIDTH, HEIGHT, color=(255,255,255), fill=True)

# Инициализируем дисплей (ST7701 — контроллер экрана)
Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
# Инициализируем медиа-менеджер для работы с изображениями
MediaManager.init()

try:
    # === Внешние кольца колеса ===
    # Большое серое кольцо радиусом 150 пикселей, толщина линии 8
    img.draw_circle(320, 240, 150, color=(50,50,50), thickness=8)
    # Кольцо поменьше радиусом 130 пикселей, толщина линии 5
    img.draw_circle(320, 240, 130, color=(80,80,80), thickness=5)

    # === Центральный узел (ступица) ===
    # Залитый серый круг радиусом 40
    img.draw_circle(320, 240, 40, color=(100,100,100), fill=True)
    # Тонкая обводка вокруг ступицы
    img.draw_circle(320, 240, 40, color=(50,50,50), thickness=3)
    # Маленький тёмный круг в самом центре радиусом 15
    img.draw_circle(320, 240, 15, color=(30,30,30), fill=True)

    # === Спицы с декоративными кружками ===
    # Рисуем 8 маленьких кружков по кругу (как болты на колесе)
    for i in range(8):
        # Вычисляем угол для каждого элемента (360 градусов / 8 = 45°)
        angle = i * (360 / 8)
        # Вычисляем координаты центра маленького круга на окружности радиусом 130
        # math.cos и math.sin работают с радианами, поэтому переводим градусы в радианы
        x_outer = int(320 + 130 * math.cos(math.radians(angle)))
        y_outer = int(240 + 130 * math.sin(math.radians(angle)))
        # Рисуем заполненный кружок в вычисленной позиции
        img.draw_circle(x_outer, y_outer, 10, color=(70,70,70), fill=True)

    # Показываем готовое изображение на дисплее
    Display.show_image(img)

    # Бесконечный цикл — держим изображение на экране
    while True:
        time.sleep(2)

except Exception as e:
    # Выводим ошибку, если что-то пошло не так
    print("Error:", e)

finally:
    # Освобождаем ресурсы: отключаем дисплей и медиа-менеджер
    Display.deinit()
    MediaManager.deinit()

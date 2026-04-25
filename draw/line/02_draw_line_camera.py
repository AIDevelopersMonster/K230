# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230                  
#
# Описание:
# Пример рисования линий на живом потоке с камеры.
# Показывает, как рисовать линии поверх изображения с камеры в реальном времени.
#
# Используется:
# - Sensor / Display / MediaManager
#
# ============================================

import uos as os
import time
from media.sensor import *
from media.display import *
from media.media import *

# Размеры изображения (ширина и высота в пикселях)
WIDTH = 640
HEIGHT = 480

# Создаём объект сенсора (камеры)
sensor = Sensor()
# Сбрасываем настройки сенсора к значениям по умолчанию
sensor.reset()
# Устанавливаем размер кадра: ширина, высота и канал камеры
sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_1)
# Устанавливаем формат пикселей RGB565 для канала камеры
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

# Инициализируем дисплей (ST7701 - контроллер экрана)
# width и height - размеры экрана, to_ide=True позволяет видеть вывод в IDE
Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
# Инициализируем медиа-менеджер для работы с мультимедиа
MediaManager.init()

# Запускаем сенсор (камеру) для захвата кадров
sensor.run()

# Основной бесконечный цикл программы
while True:
    # Проверяем точку выхода (для корректной остановки программы)
    os.exitpoint()

    # Получаем текущий кадр с камеры
    # chn=CAM_CHN_ID_1 указывает, с какого канала камеры брать изображение
    img = sensor.snapshot(chn=CAM_CHN_ID_1)

    # Рисуем горизонтальную линию по центру экрана (красного цвета)
    # Координаты: от (0, HEIGHT//2) до (WIDTH, HEIGHT//2)
    # thickness=2 задаёт толщину линии 2 пикселя
    img.draw_line(0, HEIGHT//2, WIDTH, HEIGHT//2, color=(255,0,0), thickness=2)
    
    # Рисуем вертикальную линию по центру экрана (зелёного цвета)
    # Координаты: от (WIDTH//2, 0) до (WIDTH//2, HEIGHT)
    img.draw_line(WIDTH//2, 0, WIDTH//2, HEIGHT, color=(0,255,0), thickness=2)

    # Рисуем рамку по периметру изображения (синего цвета)
    # Верхняя линия: от левого верхнего угла до правого верхнего
    img.draw_line(0, 0, WIDTH, 0, color=(0,0,255))
    # Правая линия: от правого верхнего угла до правого нижнего
    img.draw_line(WIDTH, 0, WIDTH, HEIGHT, color=(0,0,255))
    # Нижняя линия: от правого нижнего угла до левого нижнего
    img.draw_line(WIDTH, HEIGHT, 0, HEIGHT, color=(0,0,255))
    # Левая линия: от левого нижнего угла до левого верхнего
    img.draw_line(0, HEIGHT, 0, 0, color=(0,0,255))

    # Добавляем текстовую подпись в левый верхний угол (жёлтого цвета)
    img.draw_string(10, 10, "Draw Line + Camera", color=(255,255,0))

    # Выводим изображение с нарисованными линиями на дисплей
    Display.show_image(img)

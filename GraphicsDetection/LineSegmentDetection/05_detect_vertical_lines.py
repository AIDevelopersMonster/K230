# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                              
#
# Описание:
# Пример поиска ТОЛЬКО вертикальных линий на изображении.
# Скрипт открывает картинку vertical_lines.png, находит все линии,
# фильтрует их по углу и оставляет только вертикальные.
# Вертикальные линии рисуются красным цветом.
#
# Используется:
# - YbUart / YbRGB / YbBuzzer / YbKey
#
# ============================================

import time, math, gc
import image
from media.display import *
from media.media import *

# Размер дисплея для вывода изображения
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Путь к файлу с изображением на SD-карте
IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/vertical_lines.png"

# Допуск угла в градусах для определения вертикальной линии
# Линии с углом близким к 90 градусам (в пределах ANGLE_TOLERANCE_DEG)
# считаются вертикальными
ANGLE_TOLERANCE_DEG = 12


def line_angle_deg(line_tuple):
    """
    Вычисление угла линии в градусах (диапазон 0..180).
    
    Параметры:
        line_tuple - кортеж координат (x1, y1, x2, y2)
    
    Возвращает:
        Угол линии в градусах
    """
    x1, y1, x2, y2 = line_tuple[:4]
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle < 0:
        angle += 180
    return angle


def is_vertical(line_tuple):
    """
    Проверка: является ли линия вертикальной.
    
    Параметры:
        line_tuple - кортеж координат линии
    
    Возвращает:
        True если линия вертикальная, иначе False
    """
    # Вертикальная линия имеет угол близкий к 90 градусам
    return abs(line_angle_deg(line_tuple) - 90) <= ANGLE_TOLERANCE_DEG


# Инициализация дисплея (ST7701 - контроллер экрана K230)
Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
# Инициализация медиаменеджера для работы с файлами
MediaManager.init()

try:
    # Загружаем изображение из файла
    img = image.Image(IMAGE_PATH)
    
    # Поиск линий на изображении
    # merge_distance=15 - объединять сегменты ближе 15 пикселей
    # max_theta_diff=10 - объединять сегменты с разницей углов до 10 градусов
    lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)

    # Счётчик найденных вертикальных линий
    count = 0
    for ln in lines:
        coords = ln.line()
        # Проверяем, является ли линия вертикальной
        if is_vertical(coords):
            # Рисуем линию красным цветом (255, 0, 0) толщиной 4 пикселя
            img.draw_line(coords, color=(255, 0, 0), thickness=4)
            count += 1

    # Выводим количество найденных линий на экран жёлтым цветом
    img.draw_string(5, 5, "Vertical: %d" % count, color=(255, 255, 0), scale=2)
    # Показываем изображение на дисплее
    Display.show_image(img)

    # Печатаем результат в консоль
    print("Vertical lines:", count)

    # Бесконечный цикл для удержания изображения на экране
    while True:
        time.sleep_ms(100)

finally:
    # Освобождение памяти при завершении работы
    gc.collect()

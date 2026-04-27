# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                              
#
# Описание:
# Пример классификации линий на три типа: горизонтальные, вертикальные и наклонные.
# Скрипт открывает картинку mixed_lines.png, находит все линии и раскрашивает их:
# - зелёный = горизонтальные линии
# - красный = вертикальные линии
# - синий = наклонные линии
# Также выводится статистика по количеству линий каждого типа.
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
IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/mixed_lines.png"

# Допуск угла в градусах для определения горизонтальных и вертикальных линий
ANGLE_TOLERANCE_DEG = 12


def angle(line):
    """
    Вычисление угла линии в градусах (диапазон 0..180).
    
    Параметры:
        line - кортеж координат (x1, y1, x2, y2)
    
    Возвращает:
        Угол линии в градусах от 0 до 180
    """
    x1, y1, x2, y2 = line[:4]
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    # Преобразуем отрицательные углы в диапазон 0..180
    return a + 180 if a < 0 else a


def is_h(l):
    """
    Проверка: является ли линия горизонтальной.
    
    Параметры:
        l - кортеж координат линии
    
    Возвращает:
        True если линия горизонтальная, иначе False
    """
    # Горизонтальная линия имеет угол близкий к 0 или 180 градусам
    return angle(l) <= ANGLE_TOLERANCE_DEG or angle(l) >= 180 - ANGLE_TOLERANCE_DEG


def is_v(l):
    """
    Проверка: является ли линия вертикальной.
    
    Параметры:
        l - кортеж координат линии
    
    Возвращает:
        True если линия вертикальная, иначе False
    """
    # Вертикальная линия имеет угол близкий к 90 градусам
    return abs(angle(l) - 90) <= ANGLE_TOLERANCE_DEG


# Инициализация дисплея (ST7701 - контроллер экрана K230)
Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
# Инициализация медиаменеджера для работы с файлами
MediaManager.init()

try:
    # Загружаем изображение из файла
    img = image.Image(IMAGE_PATH)
    
    # Поиск всех линий на изображении
    # merge_distance=15 - объединять сегменты ближе 15 пикселей
    # max_theta_diff=10 - объединять сегменты с разницей углов до 10 градусов
    lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)

    # Счётчики для каждого типа линий:
    # h - горизонтальные, v - вертикальные, o - остальные (наклонные)
    h = v = o = 0
    for ln in lines:
        c = ln.line()

        # Классифицируем линию по углу и рисуем соответствующим цветом
        if is_h(c):
            # Горизонтальная линия - зелёный цвет (0, 255, 0)
            img.draw_line(c, color=(0, 255, 0), thickness=3)
            h += 1
        elif is_v(c):
            # Вертикальная линия - красный цвет (255, 0, 0)
            img.draw_line(c, color=(255, 0, 0), thickness=3)
            v += 1
        else:
            # Наклонная линия - синий цвет (0, 128, 255)
            img.draw_line(c, color=(0, 128, 255), thickness=3)
            o += 1

    # Выводим статистику на экран жёлтым цветом
    img.draw_string(5, 5, f"H:{h} V:{v} O:{o}", color=(255, 255, 0), scale=2)
    # Показываем изображение на дисплее
    Display.show_image(img)

    # Печатаем результат в консоль
    print("Горизонтальные, вертикальные, наклонные:", h, v, o)

    # Бесконечный цикл для удержания изображения на экране
    while True:
        time.sleep_ms(100)

finally:
    # Освобождение памяти при завершении работы
    gc.collect()

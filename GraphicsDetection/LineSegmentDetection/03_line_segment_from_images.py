# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                              
#
# Описание:
# Универсальный пример распознавания отрезков линий по картинке.
# Скрипт загружает изображение с SD-карты, находит линии и классифицирует их:
# - горизонтальные (зелёный цвет)
# - вертикальные (красный цвет)
# - наклонные (синий цвет)
# Можно выбрать режим: все линии, только горизонтальные или только вертикальные.
#
# Используется:
# - YbUart / YbRGB / YbBuzzer / YbKey
#
# ============================================

import os, gc, math, time
import image
from media.display import *
from media.media import *

# Размер экрана K230, на который выводим картинку.
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Режим распознавания:
# "all"        - показывать все найденные линии
# "horizontal" - показывать только горизонтальные линии
# "vertical"   - показывать только вертикальные линии
DETECT_MODE = "all"

# Путь к тестовой картинке на SD-карте.
# Можно заменить на:
# /sdcard/Graphics detection/Line segment detection/img/horizontal_lines.png
# /sdcard/Graphics detection/Line segment detection/img/vertical_lines.png
# /sdcard/Graphics detection/Line segment detection/img/vertical_horizontal_lines.png
# /sdcard/Graphics detection/Line segment detection/img/mixed_lines.png
IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/vertical_horizontal_lines.png"

# Настройки поиска линий.
# MERGE_DISTANCE отвечает за объединение близких отрезков.
# MAX_THETA_DIFF отвечает за объединение отрезков с похожим углом.
MERGE_DISTANCE = 15
MAX_THETA_DIFF = 10

# Допуск угла для определения горизонтальных и вертикальных линий.
# Чем больше значение, тем мягче фильтр.
ANGLE_TOLERANCE_DEG = 12


def line_angle_deg(line_tuple):
    """
    Вычисляет угол линии в градусах в диапазоне 0..180.
    
    Параметры:
        line_tuple - кортеж координат (x1, y1, x2, y2)
    
    Возвращает:
        Угол в градусах от 0 до 180
    """
    x1, y1, x2, y2 = line_tuple[:4]
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle < 0:
        angle += 180
    return angle


def is_horizontal(line_tuple, tolerance=ANGLE_TOLERANCE_DEG):
    """
    Проверяет, является ли линия горизонтальной.
    
    Параметры:
        line_tuple - кортеж координат линии
        tolerance - допуск угла в градусах
    
    Возвращает:
        True если линия горизонтальная, иначе False
    """
    angle = line_angle_deg(line_tuple)
    # Горизонтальная линия имеет угол близкий к 0 или 180 градусам
    return angle <= tolerance or angle >= 180 - tolerance


def is_vertical(line_tuple, tolerance=ANGLE_TOLERANCE_DEG):
    """
    Проверяет, является ли линия вертикальной.
    
    Параметры:
        line_tuple - кортеж координат линии
        tolerance - допуск угла в градусах
    
    Возвращает:
        True если линия вертикальная, иначе False
    """
    angle = line_angle_deg(line_tuple)
    # Вертикальная линия имеет угол близкий к 90 градусам
    return abs(angle - 90) <= tolerance


def need_draw(line_tuple):
    """
    Решает, нужно ли рисовать линию в выбранном режиме.
    
    Параметры:
        line_tuple - кортеж координат линии
    
    Возвращает:
        True если линию нужно рисовать, иначе False
    """
    if DETECT_MODE == "horizontal":
        return is_horizontal(line_tuple)
    if DETECT_MODE == "vertical":
        return is_vertical(line_tuple)
    return True


def main():
    # Инициализация дисплея и медиаменеджера.
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()

    try:
        # Загружаем картинку с SD-карты.
        img = image.Image(IMAGE_PATH)

        # Ищем линии на изображении.
        lines = img.find_line_segments(merge_distance=MERGE_DISTANCE,
                                       max_theta_diff=MAX_THETA_DIFF)

        # Рисуем только те линии, которые подходят под выбранный режим.
        found = 0
        for ln in lines:
            coords = ln.line()
            if not need_draw(coords):
                continue

            # Выбираем цвет по типу линии.
            if is_horizontal(coords):
                color = (0, 255, 0)      # зелёный = горизонтальная
            elif is_vertical(coords):
                color = (255, 0, 0)      # красный = вертикальная
            else:
                color = (0, 128, 255)    # синий = наклонная

            img.draw_line(coords, color=color, thickness=3)
            found += 1

        # Пишем режим и количество найденных линий на экране.
        img.draw_string(5, 5, "mode: %s" % DETECT_MODE, color=(255, 255, 0), scale=2)
        img.draw_string(5, 28, "found: %d" % found, color=(255, 255, 0), scale=2)
        Display.show_image(img)

        print("Mode:", DETECT_MODE)
        print("Found:", found)

        # Оставляем изображение на экране.
        while True:
            time.sleep_ms(100)

    finally:
        gc.collect()


if __name__ == "__main__":
    main()

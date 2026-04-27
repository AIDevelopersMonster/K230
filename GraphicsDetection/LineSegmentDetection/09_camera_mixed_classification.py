# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                              
#
# Описание:
# Классификация линий в реальном времени с камеры на три типа:
# - горизонтальные (зелёный цвет)
# - вертикальные (красный цвет)
# - наклонные (синий цвет)
# Скрипт захватывает кадр с камеры, находит все линии и раскрашивает
# их в зависимости от угла наклона. Также выводится статистика.
#
# Использование:
# 1. Откройте mixed_lines.png на экране компьютера, планшета или телефона.
# 2. Наведите камеру K230 на эту картинку.
# 3. Увидите линии разных цветов в зависимости от их ориентации.
#
# Используется:
# - YbUart / YbRGB / YbBuzzer / YbKey
#
# ============================================

import time, math, gc, os
import image
from media.sensor import *
from media.display import *
from media.media import *
from libs.PipeLine import PipeLine

# Разрешение кадра с камеры для обработки (меньше = быстрее работа)
PICTURE_WIDTH = 160
PICTURE_HEIGHT = 120

# Разрешение дисплея для вывода результата
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Допуск угла в градусах для определения горизонтальных и вертикальных линий
ANGLE_TOLERANCE_DEG = 12


def scale_line(l):
    """
    Масштабирует координаты линии из разрешения камеры в разрешение дисплея.
    
    Параметры:
        l - кортеж координат (x1, y1, x2, y2)
    
    Возвращает:
        Кортеж (x1, y1, x2, y2) с масштабированными координатами
    """
    x1, y1, x2, y2 = l[:4]
    return (round(x1 * DISPLAY_WIDTH / PICTURE_WIDTH),
            round(y1 * DISPLAY_HEIGHT / PICTURE_HEIGHT),
            round(x2 * DISPLAY_WIDTH / PICTURE_WIDTH),
            round(y2 * DISPLAY_HEIGHT / PICTURE_HEIGHT))


def angle(l):
    """
    Вычисление угла линии в градусах (диапазон 0..180).
    
    Параметры:
        l - кортеж координат (x1, y1, x2, y2)
    
    Возвращает:
        Угол линии в градусах
    """
    x1, y1, x2, y2 = l[:4]
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


def main():
    # Создаём конвейер обработки изображений
    # rgb888p_size - размер выходного кадра для дисплея
    # display_size - физический размер дисплея
    # display_mode="LCD" - вывод на встроенный дисплей
    pl = PipeLine(rgb888p_size=[640, 360], display_size=[DISPLAY_WIDTH, DISPLAY_HEIGHT], display_mode="LCD")
    # Создаём канал 1 с уменьшенным разрешением для быстрой обработки
    pl.create(ch1_frame_size=[PICTURE_WIDTH, PICTURE_HEIGHT])

    try:
        # Основной цикл обработки кадров
        while True:
            # Проверка точки выхода (для корректной остановки скрипта)
            os.exitpoint()
            
            # Получаем кадр с камеры (канал 1)
            frame = pl.sensor.snapshot(chn=CAM_CHN_ID_1)
            
            # Ищем отрезки линий на изображении
            # merge_distance=15 - объединять сегменты ближе 15 пикселей
            # max_theta_diff=10 - объединять сегменты с разницей углов до 10 градусов
            lines = frame.find_line_segments(merge_distance=15, max_theta_diff=10)

            # Создаём прозрачный ARGB-слой для рисования результатов
            overlay = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
            overlay.clear()  # Очищаем слой

            # Счётчики для каждого типа линий:
            # h - горизонтальные, v - вертикальные, o - остальные (наклонные)
            h = v = o = 0
            for ln in lines:
                c = ln.line()
                # Классифицируем линию по углу и рисуем соответствующим цветом
                if is_h(c):
                    # Горизонтальная линия - зелёный цвет (0, 255, 0)
                    overlay.draw_line(scale_line(c), color=(0, 255, 0), thickness=5)
                    h += 1
                elif is_v(c):
                    # Вертикальная линия - красный цвет (255, 0, 0)
                    overlay.draw_line(scale_line(c), color=(255, 0, 0), thickness=5)
                    v += 1
                else:
                    # Наклонная линия - синий цвет (0, 128, 255)
                    overlay.draw_line(scale_line(c), color=(0, 128, 255), thickness=5)
                    o += 1

            # Выводим статистику на экран жёлтым цветом
            overlay.draw_string(5, 5, f"H:{h} V:{v} O:{o}", color=(255, 255, 0), scale=2)
            # Показываем слой поверх основного изображения
            Display.show_image(overlay, 0, 0, Display.LAYER_OSD3)
            
            # Небольшая задержка для стабильности
            time.sleep_us(1)

    finally:
        # Освобождаем ресурсы при завершении работы
        try:
            pl.destroy()
        except Exception:
            pass
        gc.collect()  # Принудительный сборщик мусора


if __name__ == "__main__":
    main()

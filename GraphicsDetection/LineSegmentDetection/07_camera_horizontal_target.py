# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                              
#
# Описание:
# Поиск ТОЛЬКО горизонтальных линий в реальном времени с камеры.
# Скрипт захватывает кадр с камеры, находит линии и фильтрует их,
# оставляя только горизонтальные. Горизонтальные линии рисуются
# зелёным цветом поверх изображения на дисплее LCD.
#
# Использование:
# 1. Откройте картинку img/horizontal_lines.png на экране компьютера,
#    планшета или телефона.
# 2. Наведите камеру K230 на эту картинку.
# 3. Скрипт ищет линии именно с КАМЕРЫ, а не читает PNG с SD-карты.
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

# Допуск угла в градусах для определения горизонтальной линии
# Линии с углом близким к 0 или 180 градусам считаются горизонтальными
ANGLE_TOLERANCE_DEG = 12


def scale_line(line_tuple):
    """
    Масштабирует координаты линии из разрешения камеры в разрешение дисплея.
    
    Параметры:
        line_tuple - кортеж координат (x1, y1, x2, y2)
    
    Возвращает:
        Кортеж (x1, y1, x2, y2) с масштабированными координатами
    """
    x1, y1, x2, y2 = line_tuple[:4]
    return (round(x1 * DISPLAY_WIDTH / PICTURE_WIDTH),
            round(y1 * DISPLAY_HEIGHT / PICTURE_HEIGHT),
            round(x2 * DISPLAY_WIDTH / PICTURE_WIDTH),
            round(y2 * DISPLAY_HEIGHT / PICTURE_HEIGHT))


def line_angle_deg(line_tuple):
    """
    Вычисление угла линии в градусах (диапазон 0..180).
    
    Параметры:
        line_tuple - кортеж координат (x1, y1, x2, y2)
    
    Возвращает:
        Угол линии в градусах
    """
    x1, y1, x2, y2 = line_tuple[:4]
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    # Преобразуем отрицательные углы в диапазон 0..180
    return a + 180 if a < 0 else a


def is_horizontal(line_tuple):
    """
    Проверка: является ли линия горизонтальной.
    
    Параметры:
        line_tuple - кортеж координат линии
    
    Возвращает:
        True если линия горизонтальная, иначе False
    """
    a = line_angle_deg(line_tuple)
    # Горизонтальная линия имеет угол близкий к 0 или 180 градусам
    return a <= ANGLE_TOLERANCE_DEG or a >= 180 - ANGLE_TOLERANCE_DEG


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

            # Счётчик найденных горизонтальных линий
            count = 0
            for ln in lines:
                raw = ln.line()
                # Проверяем, является ли линия горизонтальной
                if is_horizontal(raw):
                    # Масштабируем координаты и рисуем линию зелёным цветом
                    overlay.draw_line(scale_line(raw), color=(0, 255, 0), thickness=6)
                    count += 1

            # Выводим количество найденных горизонтальных линий
            overlay.draw_string(5, 5, "CAM horizontal: %d" % count, color=(255, 255, 0), scale=2)
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

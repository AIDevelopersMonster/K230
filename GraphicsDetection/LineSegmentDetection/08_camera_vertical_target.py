# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                              
#
# Описание:
# Поиск ТОЛЬКО вертикальных линий в реальном времени с камеры.
# Скрипт захватывает кадр с камеры, находит линии и фильтрует их,
# оставляя только вертикальные. Вертикальные линии рисуются
# красным цветом поверх изображения на дисплее LCD.
#
# Использование:
# 1. Откройте картинку img/vertical_lines.png на экране компьютера,
#    планшета или телефона.
# 2. Наведите камеру K230 на эту картинку.
# 3. Увидите красные линии (вертикальные) поверх изображения.
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

# Допуск угла в градусах для определения вертикальной линии
# Линии с углом близким к 90 градусам считаются вертикальными
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


def is_vertical(l):
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

            # Счётчик найденных вертикальных линий
            count = 0
            for ln in lines:
                # Проверяем, является ли линия вертикальной
                if is_vertical(ln.line()):
                    # Масштабируем координаты и рисуем линию красным цветом
                    overlay.draw_line(scale_line(ln.line()), color=(255, 0, 0), thickness=6)
                    count += 1

            # Выводим количество найденных вертикальных линий
            overlay.draw_string(5, 5, f"CAM vertical: {count}", color=(255, 255, 0), scale=2)
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

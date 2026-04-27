# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                              
#
# Описание:
# Обнаружение отрезков линий в реальном времени с камеры.
# Скрипт захватывает изображение с камеры, находит прямые линии
# и рисует их поверх изображения на дисплее LCD.
#
# Используется:
# - YbUart / YbRGB / YbBuzzer / YbKey
#
# ============================================

import time, os, sys, gc
from media.sensor import *
from media.display import *
from media.media import *
from libs.PipeLine import PipeLine, ScopedTiming
import image

# Разрешение изображения с камеры для обработки (меньше = быстрее)
PICTURE_WIDTH = 160
PICTURE_HEIGHT = 120

# Разрешение дисплея для вывода результата
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480


def scale_line(line_tuple, src_w=PICTURE_WIDTH, src_h=PICTURE_HEIGHT,
               dst_w=DISPLAY_WIDTH, dst_h=DISPLAY_HEIGHT):
    """
    Масштабирует координаты линии из разрешения обработки в разрешение дисплея.
    
    Параметры:
        line_tuple - кортеж (x1, y1, x2, y2) координат линии
        src_w, src_h - ширина и высота исходного изображения
        dst_w, dst_h - ширина и высота целевого дисплея
    
    Возвращает:
        Кортеж (x1, y1, x2, y2) с масштабированными координатами
    """
    x1, y1, x2, y2 = line_tuple[:4]
    return (
        round(x1 * dst_w / src_w),
        round(y1 * dst_h / src_h),
        round(x2 * dst_w / src_w),
        round(y2 * dst_h / src_h),
    )


def main():
    # Режим отображения: LCD - вывод на встроенный дисплей
    display_mode = "LCD"

    # Создаём конвейер обработки изображений:
    # - rgb888p_size - размер выходного кадра для дисплея
    # - display_size - физический размер дисплея
    # - ch1_frame_size - размер кадра канала 1 для детекции линий
    pl = PipeLine(rgb888p_size=[640, 360], display_size=[DISPLAY_WIDTH, DISPLAY_HEIGHT],
                  display_mode=display_mode)
    pl.create(ch1_frame_size=[PICTURE_WIDTH, PICTURE_HEIGHT])

    try:
        # Основной цикл обработки кадров
        while True:
            # Проверка точки выхода (для корректной остановки скрипта)
            os.exitpoint()

            # 1) Получаем кадр с камеры (канал 1)
            # snapshot() захватывает текущее изображение с камеры
            src = pl.sensor.snapshot(chn=CAM_CHN_ID_1)

            # 2) Ищем отрезки линий на изображении
            # merge_distance - максимальное расстояние в пикселях для объединения близких сегментов
            # max_theta_diff - максимальная разница углов в градусах для объединения сегментов
            lines = src.find_line_segments(merge_distance=15, max_theta_diff=10)

            # 3) Создаём прозрачный ARGB-слой для рисования результатов
            overlay = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
            overlay.clear()  # Очищаем слой

            # Рисуем каждую найденную линию
            for n, ln in enumerate(lines):
                # Получаем масштабированные координаты линии
                x1, y1, x2, y2 = scale_line(ln.line())
                
                # Рисуем линию красным цветом толщиной 6 пикселей
                overlay.draw_line((x1, y1, x2, y2), color=(255, 0, 0), thickness=6)
                
                # Рисуем зелёный крестик в начале линии
                overlay.draw_cross(x1, y1, color=(0, 255, 0), size=8, thickness=2)
                
                # Рисуем красный крестик в конце линии
                overlay.draw_cross(x2, y2, color=(0, 0, 255), size=8, thickness=2)
                
                # Рисуем номер линии жёлтым цветом рядом с началом
                overlay.draw_string(x1, max(0, y1 - 18), str(n), color=(255, 255, 0), scale=1)

            # Выводим общее количество найденных линий в левом верхнем углу
            overlay.draw_string(5, 5, "Line segments: %d" % len(lines), color=(255, 255, 255), scale=2)
            
            # Показываем слой поверх основного изображения
            Display.show_image(overlay, 0, 0, Display.LAYER_OSD3)
            
            # Небольшая задержка для стабильности
            time.sleep_us(1)

    except KeyboardInterrupt:
        # Обработка прерывания пользователем (Ctrl+C)
        print("Stopped by user")
    finally:
        # Освобождаем ресурсы при завершении работы
        try:
            pl.destroy()
        except Exception:
            pass
        gc.collect()  # Принудительный сборщик мусора


if __name__ == "__main__":
    main()

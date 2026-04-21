# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230              
#
# Описание:
# Базовый пример работы с сенсорным экраном (Touch Display).
# Скрипт отображает координаты касания и рисует круг в точке прикосновения.
# Идеально подходит для первого знакомства с touch-интерфейсом.
#
# Используется:
# - machine.TOUCH - для чтения координат касания
# - media.display - для вывода изображения на экран
# - image - для создания и отрисовки графики
#
# ============================================

import time
import os
import image

from media.display import *
from media.media import *
from machine import TOUCH

# Размеры экрана в пикселях
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Инициализация touch-контроллера
# Для Yahboom K230 используется machine.TOUCH(0)
# tp - объект для работы с сенсорным экраном
tp = TOUCH(0)


def main():
    """
    Основная функция программы.
    Запускает бесконечный цикл, который:
    1. Отображает фоновое изображение с инструкцией
    2. Проверяет наличие касания экрана
    3. Рисует круг и выводит координаты в точке касания
    """
    print("touch basic demo")

    # Создаём фоновое изображение (буфер) размером с экран
    # Формат ARGB8888 обеспечивает высокое качество цветов
    bg = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # Очищаем фон белым цветом
    bg.clear()
    # Рисуем белый прямоугольник на весь экран (фон)
    bg.draw_rectangle(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, color=(255, 255, 255), fill=True)
    # Добавляем заголовок чёрным цветом
    bg.draw_string_advanced(20, 20, 28, "Touch screen demo", color=(0, 0, 0))
    # Добавляем инструкцию синим цветом
    bg.draw_string_advanced(20, 60, 20, "Tap the screen to see coordinates", color=(0, 0, 255))

    # Создаём дополнительный слой (overlay) для отображения маркера касания
    # Этот слой будет накладываться поверх фона
    overlay = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    overlay.clear()

    # Инициализируем дисплей с контроллером ST7701
    # width и height должны соответствовать физическим размерам экрана
    # to_ide=True позволяет отображать изображение в CanMV IDE
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    # Инициализируем медиа-менеджер для работы с изображениями
    MediaManager.init()

    try:
        # Бесконечный цикл - основа работы с сенсорным экраном
        while True:
            # Проверяем флаг выхода (для корректной остановки через IDE)
            os.exitpoint()

            # Обновляем фоновый слой на экране
            Display.show_image(bg)

            # Очищаем overlay перед каждым кадром, чтобы не было следов
            overlay.clear()

            # Читаем данные с touch-контроллера
            # read(1) запрашивает данные о 1 точке касания
            points = tp.read(1)
            
            # Если есть точки касания (список не пустой)
            if len(points):
                # Берём первую точку касания
                pt = points[0]
                # Выводим координаты и тип события в консоль для отладки
                print("Touch: x={}, y={}, event={}".format(pt.x, pt.y, pt.event))
                
                # Рисуем красный круг радиусом 18 пикселей в точке касания
                # thickness=4 задаёт толщину линии круга
                overlay.draw_circle(pt.x, pt.y, 18, color=(255, 0, 0), thickness=4)
                
                # Выводим координаты текстом под кругом
                overlay.draw_string_advanced(20, 100, 22, "x={}, y={}".format(pt.x, pt.y), color=(0, 0, 0))
                
                # Показываем overlay слой поверх основного изображения
                # layer=Display.LAYER_OSD2 - слой поверх основного
                # alpha=180 - полупрозрачность (0-255, где 255 полностью непрозрачный)
                Display.show_image(overlay, layer=Display.LAYER_OSD2, alpha=180)

            # Небольшая задержка для снижения нагрузки на процессор
            # 0.05 секунды = 50 миллисекунд
            time.sleep(0.05)

    except KeyboardInterrupt as e:
        # Обработка прерывания пользователем (Ctrl+C)
        print("user stop:", e)
    except BaseException as e:
        # Обработка любых других исключений
        print("Exception", e)

    # Корректное завершение работы: освобождаем ресурсы
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()


if __name__ == "__main__":
    # Настраиваем точку выхода для корректной работы с IDE
    os.exitpoint(os.EXITPOINT_ENABLE)
    main()

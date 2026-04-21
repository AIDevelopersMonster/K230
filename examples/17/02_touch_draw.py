# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230              
#
# Описание:
# Пример рисования пальцем на сенсорном экране.
# Скрипт позволяет рисовать линии, перемещая палец по экрану (как в Paint).
# Линии сохраняются на холсте и не стираются до перезапуска программы.
#
# Используется:
# - machine.TOUCH - для чтения координат касания и типа события
# - media.display - для вывода изображения на экран
# - image - для создания холста и отрисовки линий
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
# tp - объект для работы с сенсорным экраном
tp = TOUCH(0)


def main():
    """
    Основная функция программы рисования.
    Работает в бесконечном цикле:
    1. Отображает белый фон и холст с нарисованными линиями
    2. Считывает координаты касания
    3. Рисует линию между предыдущей и текущей точкой касания
    """
    print("touch draw demo")

    # Создаём фоновое изображение (буфер) размером с экран
    # Формат ARGB8888 обеспечивает высокое качество цветов
    bg = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # Очищаем фон белым цветом
    bg.clear()
    # Рисуем белый прямоугольник на весь экран (фон)
    bg.draw_rectangle(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, color=(255, 255, 255), fill=True)

    # Создаём отдельный слой (холст) для рисования линий
    # Все нарисованные линии сохраняются на этом слое
    canvas = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    canvas.clear()

    # Инициализируем дисплей с контроллером ST7701
    # width и height должны соответствовать физическим размерам экрана
    # to_ide=True позволяет отображать изображение в CanMV IDE
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    # Инициализируем медиа-менеджер для работы с изображениями
    MediaManager.init()

    # Переменные для хранения предыдущих координат касания
    # Нужны для рисования непрерывных линий
    last_x = None
    last_y = None

    try:
        # Бесконечный цикл - основа работы с сенсорным экраном
        while True:
            # Проверяем флаг выхода (для корректной остановки через IDE)
            os.exitpoint()

            # Показываем фоновое изображение (белый холст)
            Display.show_image(bg)

            # Читаем данные с touch-контроллера
            # read(1) запрашивает данные о 1 точке касания
            points = tp.read(1)
            
            # Если есть точки касания (список не пустой)
            if len(points):
                # Берём первую точку касания
                pt = points[0]

                # Проверяем тип события:
                # EVENT_DOWN (0) - начало касания (палец коснулся экрана)
                # EVENT_MOVE (1) - движение пальца по экрану
                # EVENT_UP (2) - конец касания (палец убран с экрана)
                # pt.event == 0 или EVENT_DOWN или EVENT_MOVE - рисуем линию
                if pt.event == 0 or pt.event == TOUCH.EVENT_DOWN or pt.event == TOUCH.EVENT_MOVE:
                    # Если есть предыдущая точка и это не событие EVENT_UP (2)
                    # Рисуем линию от предыдущей точки к текущей
                    if last_x is not None and last_y is not None and pt.event != 2:
                        # draw_line рисует линию между двумя точками
                        # color=(0,0,0) - чёрный цвет
                        # thickness=5 - толщина линии 5 пикселей
                        canvas.draw_line(last_x, last_y, pt.x, pt.y, color=(0, 0, 0), thickness=5)

                    # Сохраняем текущие координаты как предыдущие для следующего шага
                    last_x = pt.x
                    last_y = pt.y

            # Показываем холст с нарисованными линиями поверх фона
            # layer=Display.LAYER_OSD2 - слой поверх основного
            # alpha=255 - полностью непрозрачный (линии видны чётко)
            Display.show_image(canvas, layer=Display.LAYER_OSD2, alpha=255)

            # Небольшая задержка для снижения нагрузки на процессор
            # 0.02 секунды = 20 миллисекунд (быстрее чем в basic примере для плавности)
            time.sleep(0.02)

    except KeyboardInterrupt:
        # Обработка прерывания пользователем (Ctrl+C)
        pass

    # Корректное завершение работы: освобождаем ресурсы
    Display.deinit()
    MediaManager.deinit()


if __name__ == "__main__":
    # Настраиваем точку выхода для корректной работы с IDE
    os.exitpoint(os.EXITPOINT_ENABLE)
    main()

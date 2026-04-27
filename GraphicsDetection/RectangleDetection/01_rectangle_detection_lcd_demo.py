# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                               
#
# Описание:
# Скрипт обнаружения прямоугольников с выводом на LCD-экран.
# Камера захватывает изображение, алгоритм find_rects() находит
# прямоугольники на изображении, результаты отображаются на экране
# с подсветкой границ, углов и нумерацией найденных объектов.
#
# Используется:
# - Sensor (камера)
# - Display (LCD экран ST7701)
# - MediaManager (управление медиа)
#
# ============================================

# Импорт необходимых библиотек
import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

# Настройки разрешения камеры (ширина и высота захватываемого изображения)
PICTURE_WIDTH = 400
PICTURE_HEIGHT = 240

# Настройки разрешения LCD экрана
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Пороговое значение для обнаружения прямоугольников
# Чем выше значение, тем более контрастные прямоугольники будут найдены
RECT_THRESHOLD = 8000

# Переменная для хранения объекта сенсора
sensor = None
# Объект для измерения FPS (кадров в секунду)
clock = time.clock()

try:
    # Инициализация камеры (сенсора)
    sensor = Sensor()
    sensor.reset()

    # Установка разрешения и формата пикселей для камеры
    # RGB565 - формат цвета с 16 битами на пиксель
    sensor.set_framesize(width=PICTURE_WIDTH, height=PICTURE_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    # Инициализация LCD дисплея (драйвер ST7701)
    # to_ide=True позволяет работать через IDE
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

    # Инициализация менеджера медиа (необходимо для работы с камерой и дисплеем)
    MediaManager.init()
    # Запуск камеры
    sensor.run()

    # Основной цикл программы
    while True:
        # Проверка точки выхода (для корректной остановки через IDE)
        os.exitpoint()
        # Обновление таймера для расчёта FPS
        clock.tick()

        # Получение текущего кадра с камеры
        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        # Счётчик найденных прямоугольников
        rect_count = 0
        print("[Rectangle Detection Start]")

        # Поиск прямоугольников на изображении
        # threshold - минимальная площадь для обнаружения
        for r in img.find_rects(threshold=RECT_THRESHOLD):
            rect_count += 1

            # Рисуем границу прямоугольника голубым цветом (40, 167, 225)
            # thickness=2 - толщина линии в пикселях
            img.draw_rectangle(r.rect(), color=(40, 167, 225), thickness=2)

            # Рисуем круги в углах каждого прямоугольника
            # r.corners() возвращает координаты четырёх углов
            for p in r.corners():
                img.draw_circle(p[0], p[1], 8, color=(78, 90, 34), thickness=2)

            # Получаем координаты и размеры прямоугольника
            x0, y0, w, h = r.rect()
            # Рисуем номер прямоугольника над ним белым цветом
            img.draw_string(x0, max(0, y0 - 14), "RECT %d" % rect_count, color=(255, 255, 255), scale=1)

            # Вывод информации о прямоугольнике в консоль
            print("RECT", rect_count, r)

        print("[===========================]")
        print("FPS:", clock.fps())

        # Отображаем текущую статистику прямо на изображении
        img.draw_string(2, 2, "RECT:%d FPS:%.1f" % (rect_count, clock.fps()), color=(255, 255, 255), scale=1)

        # Вычисляем координаты для центрирования изображения камеры на LCD экране
        x = int((DISPLAY_WIDTH - PICTURE_WIDTH) / 2)
        y = int((DISPLAY_HEIGHT - PICTURE_HEIGHT) / 2)
        # Показываем изображение на экране со смещением для центрирования
        Display.show_image(img, x=x, y=y)

except KeyboardInterrupt as e:
    # Обработка прерывания пользователем (Ctrl+C)
    print("User Stop:", e)
except BaseException as e:
    # Обработка других исключений
    print("Exception:", e)
finally:
    # Блок finally выполняется всегда при завершении программы
    # Остановка сенсора
    if isinstance(sensor, Sensor):
        sensor.stop()
    # Деинициализация дисплея
    Display.deinit()
    # Включение режима сна для точки выхода
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # Деинициализация менеджера медиа
    MediaManager.deinit()

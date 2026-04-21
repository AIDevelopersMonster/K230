# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230               
#
# Описание:
# Базовый вывод изображения с камеры на экран
# Получает кадры с камеры и отображает их на дисплее
#
# Используется:
# - Sensor (камера)
# - Display (экран)
# - MediaManager (управление медиа)
#
# ============================================

import time, os, gc
from media.sensor import *
from media.display import *
from media.media import *

# Настраиваем разрешение изображения
WIDTH = 640
HEIGHT = 480

# Создаём объект сенсора (камеры)
sensor = Sensor()
# Сбрасываем настройки сенсора к значениям по умолчанию
sensor.reset()
# Устанавливаем размер кадра (разрешение)
sensor.set_framesize(width=WIDTH, height=HEIGHT)
# Устанавливаем формат пикселей - RGB565 (16 бит на пиксель)
sensor.set_pixformat(Sensor.RGB565)

# Инициализируем дисплей типа ST7701 с нашим разрешением
# to_ide=True позволяет передавать изображение в IDE для отладки
Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
# Инициализируем менеджер медиа для работы с потоками данных
MediaManager.init()

# Запускаем сенсор - камера начинает захват изображения
sensor.run()

# Создаём объект для измерения FPS (кадров в секунду)
fps = time.clock()

# Основной цикл программы
while True:
    # Обновляем счётчик времени для расчёта FPS
    fps.tick()
    # Проверяем наличие сигнала выхода (для корректного завершения)
    os.exitpoint()
    # Делаем снимок с камеры - получаем текущий кадр
    img = sensor.snapshot()
    # Отображаем полученное изображение на экране
    Display.show_image(img)
    # Запускаем сборщик мусора для освобождения памяти
    gc.collect()
    # Небольшая задержка для стабильности работы
    time.sleep_ms(5)
    # Выводим текущее значение FPS в консоль
    print("FPS:", fps.fps())

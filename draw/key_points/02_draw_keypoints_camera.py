# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                         
#
# Описание:
# Демонстрация детектирования и рисования ключевых точек (keypoints)
# с использованием видеопотока с камеры. Скрипт захватывает изображение
# с камеры, находит ключевые точки в указанной области (ROI) и рисует
# их на дисплее в реальном времени.
#
# Используется:
# - Sensor (камера) / YbRGB (дисплей) / MediaManager
#
# ============================================

import uos as os
import time
from media.sensor import *
from media.display import *
from media.media import *

# Устанавливаем разрешение для дисплея и камеры
WIDTH = 640
HEIGHT = 480

# Создаём объект сенсора (камеры) с максимальным разрешением 1280x960
sensor = Sensor(width=1280, height=960)
# Сбрасываем настройки сенсора к значениям по умолчанию
sensor.reset()

# Настраиваем поток CAM_CHN_ID_1 (цветное изображение)
# Устанавливаем размер кадра и формат пикселей RGB565 (цветной)
sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_1)
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

# Настраиваем поток CAM_CHN_ID_0 (чёрно-белое изображение для детектирования)
# Устанавливаем размер кадра и формат GRAYSCALE (оттенки серого)
sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_0)
sensor.set_pixformat(Sensor.GRAYSCALE, chn=CAM_CHN_ID_0)

# Инициализируем дисплей ST7701 с нашим разрешением
# to_ide=True позволяет видеть изображение в IDE
Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
# Инициализируем медиаменеджер для работы с медиа-ресурсами
MediaManager.init()

# Запускаем сенсор (начинаем захват изображения)
sensor.run()

# Определяем область интереса (ROI - Region of Interest)
# Формат: (x, y, ширина, высота)
# Ключевые точки будут искаться только в этой области экрана
roi = (220, 140, 200, 200)

# Основной бесконечный цикл программы
while True:
    # Проверяем точку выхода (позволяет корректно завершить программу)
    os.exitpoint()

    # Получаем кадр с камеры (цветное изображение для отображения)
    img = sensor.snapshot(chn=CAM_CHN_ID_1)
    # Получаем кадр с камеры (чёрно-белое изображение для детектирования)
    img_g = sensor.snapshot(chn=CAM_CHN_ID_0)

    # Рисуем прямоугольную рамку вокруг области интереса (ROI)
    # цвет (173, 216, 230) = светло-голубой, толщина линии = 2 пикселя
    img.draw_rectangle(roi, color=(173, 216, 230), thickness=2)

    # Ищем ключевые точки в чёрно-белом изображении в области ROI
    # threshold=30 - порог чувствительности детектора
    # scale_factor=1.2 - масштаб для поиска точек разного размера
    # max_keypoints=30 - максимальное количество найденных точек
    keypoints = img_g.find_keypoints(threshold=30, scale_factor=1.2, max_keypoints=30, roi=roi)

    # Если ключевые точки найдены
    if keypoints:
        # Рисуем найденные ключевые точки на цветном изображении
        # color=(255, 0, 0) - красный цвет точек
        # size=8 - размер каждой точки
        # thickness=2 - толщина линий
        # fill=True - закрашивать точки внутри
        img.draw_keypoints(keypoints, color=(255, 0, 0), size=8, thickness=2, fill=True)

    # Рисуем текстовую подпись в левом верхнем углу
    # цвет (255, 255, 0) = жёлтый
    img.draw_string(10, 10, "Keypoints", color=(255, 255, 0))

    # Отображаем итоговое изображение с графикой на дисплее
    Display.show_image(img)

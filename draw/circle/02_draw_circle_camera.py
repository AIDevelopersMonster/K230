# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                   
#
# Описание:
# Рисование кругов поверх видеопотока с камеры.
# Скрипт захватывает изображение с камеры и рисует два цветных круга
# в центре экрана, а также текстовую подпись.
#
# Используется:
# - Sensor / Display / MediaManager / image
#
# ============================================

import uos as os
from media.sensor import *
from media.display import *
from media.media import *

# Устанавливаем разрешение дисплея и камеры (ширина x высота)
WIDTH = 640
HEIGHT = 480

# Создаём объект сенсора камеры
sensor = Sensor()
# Сбрасываем настройки сенсора к значениям по умолчанию
sensor.reset()
# Устанавливаем размер кадра (разрешение) для канала камеры 1
sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_1)
# Устанавливаем формат пикселей RGB565 для канала камеры 1
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

# Инициализируем дисплей (ST7701 — контроллер экрана)
Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)
# Инициализируем медиа-менеджер для работы с изображениями
MediaManager.init()

# Запускаем захват изображения с сенсора
sensor.run()

# Основной бесконечный цикл программы
while True:
    # Проверяем точку выхода (для корректного завершения через IDE)
    os.exitpoint()

    # Делаем снимок с камеры (получаем текущий кадр)
    img = sensor.snapshot(chn=CAM_CHN_ID_1)

    # === Рисуем круги на изображении ===
    # Красный круг радиусом 100 пикселей в центре экрана
    # color=(255,0,0) — красный цвет в формате RGB
    # thickness=2 — толщина линии 2 пикселя
    img.draw_circle(WIDTH//2, HEIGHT//2, 100, color=(255,0,0), thickness=2)
    
    # Зелёный круг радиусом 50 пикселей в центре экрана
    # color=(0,255,0) — зелёный цвет в формате RGB
    img.draw_circle(WIDTH//2, HEIGHT//2, 50, color=(0,255,0), thickness=2)

    # Добавляем текстовую подпись в левый верхний угол
    # color=(255,255,0) — жёлтый цвет (красный + зелёный)
    img.draw_string(10, 10, "Draw Circle + Camera", color=(255,255,0))

    # Отображаем модифицированное изображение на дисплее
    Display.show_image(img)

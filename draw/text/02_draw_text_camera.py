# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                        
#
# Описание:
# Демонстрация отрисовки текста поверх изображения с камеры.
# Скрипт захватывает кадр с камеры и добавляет текстовые надписи.
#
# Используется:
# - YbUart / YbRGB / YbBuzzer / YbKey
#
# ============================================

# Импортируем необходимые модули
import uos as os
from media.sensor import *
from media.display import *
from media.media import *

# Настраиваем разрешение экрана (ширина и высота в пикселях)
WIDTH = 640
HEIGHT = 480

# Создаём объект сенсора (камеры)
sensor = Sensor()

# Сбрасываем настройки сенсора к значениям по умолчанию
sensor.reset()

# Устанавливаем размер кадра (разрешение изображения)
# chn=CAM_CHN_ID_1 — используем первый канал камеры
sensor.set_framesize(width=WIDTH, height=HEIGHT, chn=CAM_CHN_ID_1)

# Устанавливаем формат пикселей RGB565 для первого канала
# RGB565 — 16-битный формат цвета (меньше памяти, чем ARGB8888)
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)

# Инициализируем дисплей
# Display.ST7701 — тип контроллера дисплея
# to_ide=True — позволяет отображать изображение в IDE
Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)

# Инициализируем медиа-менеджер для работы с изображениями и видео
MediaManager.init()

# Запускаем сенсор (камеру)
sensor.run()

# Основной цикл программы
while True:
    # Проверяем точку выхода (для корректного завершения программы)
    os.exitpoint()
    
    # Делаем снимок с камеры (получаем текущий кадр)
    img = sensor.snapshot(chn=CAM_CHN_ID_1)

    # Рисуем текст на изображении
    # Параметры: x, y, текст, цвет (R, G, B), scale — масштаб шрифта
    img.draw_string(10, 10, "K230 Camera", color=(255, 255, 0), scale=2)
    img.draw_string(10, 40, "Draw Text", color=(0, 255, 0), scale=2)

    # Показываем изображение на дисплее
    Display.show_image(img)

# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230                        
#
# Описание:
# Демонстрация отрисовки текста на экране с использованием
# метода draw_string_advanced(). Скрипт создаёт белый фон,
# затем рисует текст на английском и китайском языках.
#
# Используется:
# - YbUart / YbRGB / YbBuzzer / YbKey
#
# ============================================

# Импортируем необходимые модули
import time, os
import image
from media.display import *
from media.media import *

# Настраиваем разрешение экрана (ширина и высота в пикселях)
WIDTH = 640
HEIGHT = 480

# Создаём изображение с указанным разрешением и форматом ARGB8888
# ARGB8888 — формат цвета с альфа-каналом (прозрачностью)
img = image.Image(WIDTH, HEIGHT, image.ARGB8888)

# Очищаем изображение (заполняем чёрным цветом)
img.clear()

# Рисуем белый прямоугольник на всём экране (фон)
# Параметры: x, y, ширина, высота, цвет (R, G, B), fill=True — заливка
img.draw_rectangle(0, 0, WIDTH, HEIGHT, color=(255, 255, 255), fill=True)

# Инициализируем дисплей
# Display.ST7701 — тип контроллера дисплея
# to_ide=True — позволяет отображать изображение в IDE
Display.init(Display.ST7701, width=WIDTH, height=HEIGHT, to_ide=True)

# Инициализируем медиа-менеджер для работы с изображениями и видео
MediaManager.init()

try:
    # Отрисовка английского текста
    # Параметры: x, y, размер шрифта, текст, цвет (R, G, B)
    img.draw_string_advanced(200, 180, 30, "Hello World!", color=(0, 191, 255))

    # Отрисовка китайского текста
    # draw_string_advanced поддерживает Unicode символы
    img.draw_string_advanced(200, 240, 30, "你好，世界！", color=(0, 255, 127))

    # Показываем изображение на дисплее
    Display.show_image(img)

    # Бесконечный цикл для удержания изображения на экране
    while True:
        time.sleep(2)

except Exception as e:
    # Выводим ошибку, если она возникнет
    print(e)

finally:
    # Освобождаем ресурсы при завершении программы
    Display.deinit()
    MediaManager.deinit()

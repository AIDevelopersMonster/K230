'''
Пример 3. Переключение цветов RGB LED кнопкой (YbKey + YbRGB)

Описание:
При каждом нажатии кнопки меняется цвет RGB светодиода.
Используются библиотеки:
- YbKey — для кнопки
- YbRGB — для управления RGB LED

Важно:
Кнопка работает через GPIO61 и подтянута вверх,
поэтому при нажатии возвращает 0 (is_pressed() == True)
'''

from ybUtils.YbKey import YbKey
from ybUtils.YbRGB import YbRGB
import time

# --- Инициализация ---
key = YbKey()
rgb = YbRGB()

print("Кнопка переключает цвета RGB LED")

# --- Список цветов ---
colors = [
    (255, 0, 0),    # красный
    (0, 255, 0),    # зелёный
    (0, 0, 255),    # синий
    (255, 255, 0),  # жёлтый
    (0, 255, 255),  # голубой
    (255, 0, 255),  # фиолетовый
    (0, 0, 0)       # выключено
]

color_index = 0

# начальный цвет
rgb.show_rgb(colors[color_index])

while True:
    if key.is_pressed():
        # антидребезг
        time.sleep_ms(20)

        if key.is_pressed():
            # следующий цвет
            color_index = (color_index + 1) % len(colors)
            rgb.show_rgb(colors[color_index])

            print("Текущий цвет:", colors[color_index])

            # ждём отпускания кнопки
            while key.is_pressed():
                pass

    time.sleep_ms(50)

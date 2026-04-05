# Пример 3. Перебор цветов (color cycle)
#
# Светодиод последовательно переключается между цветами.

from ybUtils.YbRGB import YbRGB
import time

rgb = YbRGB()

colors = [
    (255, 0, 0),   # Красный
    (0, 255, 0),   # Зелёный
    (0, 0, 255),   # Синий
    (255, 255, 0), # Жёлтый
    (255, 0, 255), # Пурпурный
    (0, 255, 255), # Голубой
]

while True:
    for color in colors:
        rgb.show_rgb(color)
        time.sleep(1)

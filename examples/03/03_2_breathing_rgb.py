# Пример 2. Эффект «дыхания» RGB-светодиода
#
# В этом примере используется плавное изменение яркости
# с помощью синусоидальной функции (math.sin).

from ybUtils.YbRGB import YbRGB
import time
import math

rgb = YbRGB()

# Функция эффекта дыхания
def breath_effect(r, g, b, duration=2):
    steps = 100

    # Увеличение яркости
    for i in range(steps):
        brightness = math.sin(i / steps * math.pi)
        rgb.show_rgb((int(r * brightness), int(g * brightness), int(b * brightness)))
        time.sleep(duration / (2 * steps))

    # Уменьшение яркости
    for i in range(steps, -1, -1):
        brightness = math.sin(i / steps * math.pi)
        rgb.show_rgb((int(r * brightness), int(g * brightness), int(b * brightness)))
        time.sleep(duration / (2 * steps))

# Основной цикл
while True:
    breath_effect(0, 0, 255)  # Синий цвет

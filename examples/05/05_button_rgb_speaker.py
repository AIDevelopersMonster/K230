'''
Пример 5. Кнопка + RGB LED + динамик (YbKey + YbRGB + YbBuzzer)

Описание:
Кнопка переключает режимы:
0 — красный + звук
1 — зелёный без звука
2 — синий без звука
'''

from ybUtils.YbKey import YbKey
from ybUtils.YbRGB import YbRGB
from ybUtils.YbBuzzer import YbBuzzer
import time

# --- Инициализация ---
key = YbKey()
rgb = YbRGB()
buzzer = YbBuzzer()

mode = 0

print("Комбинированный пример: кнопка управляет RGB и звуком")

while True:
    if key.is_pressed():
        # антидребезг
        time.sleep_ms(20)

        if key.is_pressed():
            mode = (mode + 1) % 3
            print("Режим:", mode)

            # ждём отпускания кнопки
            while key.is_pressed():
                pass

    # --- Режимы ---
    if mode == 0:
        # красный + звук
        rgb.show_rgb((255, 0, 0))
        buzzer.on(1000, 50, 0.2)

    elif mode == 1:
        # зелёный без звука
        rgb.show_rgb((0, 255, 0))
        buzzer.off()

    elif mode == 2:
        # синий без звука
        rgb.show_rgb((0, 0, 255))
        buzzer.off()

    time.sleep_ms(100)

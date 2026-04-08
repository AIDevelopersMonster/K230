# Пример 5. Кнопка + RGB LED + динамик

from ybUtils.YbKey import YbKey
from machine import Pin, PWM
import time

key = YbKey()

r = Pin(10, Pin.OUT)
g = Pin(11, Pin.OUT)
b = Pin(12, Pin.OUT)

buzzer = PWM(Pin(8))
mode = 0

print("Комбинированный пример")

while True:
    if key.is_pressed():
        mode = (mode + 1) % 3
        time.sleep_ms(300)

    if mode == 0:
        r.value(1); g.value(0); b.value(0)
        buzzer.freq(1000)
        buzzer.duty(50)
    elif mode == 1:
        r.value(0); g.value(1); b.value(0)
        buzzer.duty(0)
    elif mode == 2:
        r.value(0); g.value(0); b.value(1)
        buzzer.duty(0)

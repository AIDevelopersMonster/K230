# Пример 2. Управление светодиодом с помощью кнопки

from ybUtils.YbKey import YbKey
from machine import Pin
import time

key = YbKey()

# Указываем пин светодиода (можно изменить под свою плату)
led = Pin(10, Pin.OUT)

print("Кнопка управляет светодиодом")

while True:
    if key.is_pressed():
        led.value(1)  # включить LED
    else:
        led.value(0)  # выключить LED

    time.sleep_ms(50)

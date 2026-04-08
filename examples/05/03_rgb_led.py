# Пример 3. Управление RGB светодиодом

from machine import Pin
import time

r = Pin(10, Pin.OUT)
g = Pin(11, Pin.OUT)
b = Pin(12, Pin.OUT)

print("Демонстрация RGB LED")

while True:
    # Красный
    r.value(1); g.value(0); b.value(0)
    time.sleep(1)

    # Зелёный
    r.value(0); g.value(1); b.value(0)
    time.sleep(1)

    # Синий
    r.value(0); g.value(0); b.value(1)
    time.sleep(1)

# Пример 5. Полная система (кнопка + UART + WDT)

from machine import WDT
from ybUtils.YbKey import YbKey
from ybUtils.YbUart import YbUart
import time

wdt = WDT(1, 3)
key = YbKey()
uart = YbUart(115200)

while True:
    if key.is_pressed():
        print("Feed by button")
        wdt.feed()

    data = uart.read()
    if data:
        print("Feed by UART")
        wdt.feed()

    time.sleep(0.1)

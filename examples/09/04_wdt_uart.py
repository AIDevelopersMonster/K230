# Пример 4. UART кормит WDT

from machine import WDT
from ybUtils.YbUart import YbUart
import time

wdt = WDT(1, 3)
uart = YbUart(115200)

while True:
    data = uart.read()
    if data:
        print("Feed via UART")
        wdt.feed()
    time.sleep(0.1)

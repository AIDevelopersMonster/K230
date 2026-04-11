# Пример 1. Базовый WDT

from machine import WDT
import time

wdt = WDT(1, 3)

while True:
    print("Feed watchdog")
    wdt.feed()
    time.sleep(1)

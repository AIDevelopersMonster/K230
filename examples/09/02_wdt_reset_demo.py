# Пример 2. Демонстрация перезагрузки (НЕ кормим WDT)

from machine import WDT
import time

wdt = WDT(1, 3)

print("Сейчас система перезагрузится через 3 секунды...")

while True:
    time.sleep(1)

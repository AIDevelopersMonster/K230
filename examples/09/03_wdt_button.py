# Пример 3. Кнопка кормит WDT

from machine import WDT
from ybUtils.YbKey import YbKey
import time

wdt = WDT(1, 3)
key = YbKey()

while True:
    if key.is_pressed():
        print("Feed by button")
        wdt.feed()
    time.sleep(0.2)

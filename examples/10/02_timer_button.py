# Пример 2. Timer + кнопка

from machine import Timer
from ybUtils.YbKey import YbKey

key = YbKey()


def cb(t):
    if key.is_pressed():
        print("Button pressed (timer)")


timer = Timer(-1)
timer.init(freq=5, mode=Timer.PERIODIC, callback=cb)

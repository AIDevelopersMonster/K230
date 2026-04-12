# Пример 5. Timer + звук

from machine import Timer
from ybUtils.YbBuzzer import YbBuzzer

buzzer = YbBuzzer()


def cb(t):
    buzzer.beep()


timer = Timer(-1)
timer.init(freq=2, mode=Timer.PERIODIC, callback=cb)

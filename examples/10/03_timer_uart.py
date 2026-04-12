# Пример 3. Timer + UART

from machine import Timer
from ybUtils.YbUart import YbUart

uart = YbUart(115200)


def cb(t):
    data = uart.read()
    if data:
        print("UART (timer):", data.decode())


timer = Timer(-1)
timer.init(freq=10, mode=Timer.PERIODIC, callback=cb)

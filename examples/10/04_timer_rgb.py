# Пример 4. Timer + RGB

from machine import Timer
from ybUtils.YbRGB import YbRGB

rgb = YbRGB()
colors = [(255,0,0),(0,255,0),(0,0,255)]
i = 0


def cb(t):
    global i
    rgb.show_rgb(colors[i])
    i = (i+1)%3


timer = Timer(-1)
timer.init(freq=1, mode=Timer.PERIODIC, callback=cb)

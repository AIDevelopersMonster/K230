# Пример 3. FFT + RGB

from machine import FFT
from ybUtils.YbRGB import YbRGB
from ulab import numpy as np
import math

rgb = YbRGB()
N = 64
PI = 3.1415926

while True:
    data = []
    for i in range(N):
        val = 50 * math.cos(2 * PI * i / N)
        data.append(int(val))

    arr = np.array(data, dtype=np.uint16)
    fft = FFT(arr, N, 0x555)
    res = fft.run()
    ampl = fft.amplitude(res)

    peak = max(ampl)

    if peak > 1000:
        rgb.show_rgb((255,0,0))
    else:
        rgb.show_rgb((0,0,255))

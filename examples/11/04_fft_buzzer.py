# Пример 4. FFT + звук

from machine import FFT
from ybUtils.YbBuzzer import YbBuzzer
from ulab import numpy as np
import math

buzzer = YbBuzzer()
N = 64
PI = 3.1415926

while True:
    data = []
    for i in range(N):
        val = 100 * math.cos(5 * 2 * PI * i / N)
        data.append(int(val))

    arr = np.array(data, dtype=np.uint16)
    fft = FFT(arr, N, 0x555)
    res = fft.run()
    ampl = fft.amplitude(res)

    if max(ampl) > 2000:
        buzzer.beep()

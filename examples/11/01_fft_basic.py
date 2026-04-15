# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230
# ============================================

# Пример 1. Базовый FFT

from machine import FFT
import math
from ulab import numpy as np

PI = 3.1415926

# Генерация сигнала
data = []
N = 64

for i in range(N):
    val = 10 * math.cos(2 * PI * i / N) + 30 * math.cos(3 * 2 * PI * i / N)
    data.append(int(val))

# FFT
arr = np.array(data, dtype=np.uint16)
fft = FFT(arr, N, 0x555)
res = fft.run()
ampl = fft.amplitude(res)

print("Amplitude:", ampl)

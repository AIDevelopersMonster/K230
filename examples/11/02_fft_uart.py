# Пример 2. FFT + UART

from machine import FFT
from ybUtils.YbUart import YbUart
from ulab import numpy as np

uart = YbUart(115200)

while True:
    data = uart.read()
    if data:
        try:
            nums = [int(x) for x in data.decode().split(',')]
            arr = np.array(nums, dtype=np.uint16)
            fft = FFT(arr, len(nums), 0x555)
            res = fft.run()
            ampl = fft.amplitude(res)
            print("FFT:", ampl)
        except Exception as e:
            print("Error:", e)

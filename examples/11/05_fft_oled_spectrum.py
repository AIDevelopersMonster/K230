# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230
# ============================================

# Пример 5. Спектроанализатор на OLED
#
# Что делает программа:
# - генерирует тестовый сигнал из нескольких косинусов
# - выполняет FFT
# - получает амплитудный спектр
# - рисует простую спектрограмму на OLED 128x32
#
# Примечание:
# Это демонстрационный пример без микрофона.
# Вместо реального входного сигнала используется синтетический тестовый сигнал.

from machine import FFT, I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
from ulab import numpy as np
import math
import time

PI = 3.1415926535
N = 64
BAR_COUNT = 16
SAMPLING_RATE = 38400

# -------------------------------
# Инициализация OLED (I2C1)
# -------------------------------
fpioa = FPIOA()
i2c = I2C(1)
fpioa.set_function(34, FPIOA.IIC1_SCL, oe=1, ie=1, pu=1, st=1, ds=15)
fpioa.set_function(35, FPIOA.IIC1_SDA, oe=1, ie=1, pu=1, st=1, ds=15)
oled = SSD1306_I2C(128, 32, i2c)


def draw_line(y):
    for x in range(128):
        oled.pixel(x, y, 1)


def generate_signal(phase_shift=0):
    """Генерация тестового сигнала из нескольких частот."""
    data = []
    for i in range(N):
        s1 = 40 * math.cos(2 * PI * i / N + phase_shift)
        s2 = 80 * math.cos(2 * 2 * PI * i / N)
        s3 = 140 * math.cos(5 * 2 * PI * i / N)
        s4 = 30 * math.cos(9 * 2 * PI * i / N)
        data.append(int(s1 + s2 + s3 + s4))
    return data


def get_amplitudes(data):
    """Выполняет FFT и возвращает амплитудный спектр."""
    arr = np.array(data, dtype=np.uint16)
    fft = FFT(arr, N, 0x555)
    result = fft.run()
    ampl = fft.amplitude(result)
    return ampl


def draw_spectrum(ampl):
    """Рисует 16 столбиков спектра на OLED."""
    oled.fill(0)
    oled.text("FFT OLED", 0, 0)
    draw_line(9)

    # Берём только первую половину спектра, она информативна для реального сигнала
    useful = ampl[:N // 2]

    # Группируем частоты в 16 столбиков
    step = max(1, len(useful) // BAR_COUNT)
    bars = []
    for i in range(BAR_COUNT):
        start = i * step
        end = start + step
        chunk = useful[start:end]
        if len(chunk) == 0:
            bars.append(0)
        else:
            bars.append(max(chunk))

    peak = max(bars) if max(bars) > 0 else 1

    # Высота рабочей области: от y=10 до y=31
    for i, value in enumerate(bars):
        height = int((value / peak) * 20)
        x0 = i * 8
        for x in range(x0, x0 + 6):
            for y in range(31, 31 - height, -1):
                if 0 <= x < 128 and 0 <= y < 32:
                    oled.pixel(x, y, 1)

    oled.show()


phase = 0.0

while True:
    signal = generate_signal(phase)
    amplitude = get_amplitudes(signal)
    draw_spectrum(amplitude)
    phase += 0.2
    time.sleep_ms(150)

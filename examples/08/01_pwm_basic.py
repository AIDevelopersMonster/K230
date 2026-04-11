# Пример 1. Базовый PWM сигнал

from machine import PWM, FPIOA
import time

fpioa = FPIOA()

# Настройка PWM0 на IO42
fpioa.set_function(42, fpioa.PWM0)

# Частота 1000 Гц, скважность 50%
pwm0 = PWM(0, 1000, 50, enable=True)

while True:
    time.sleep(1)

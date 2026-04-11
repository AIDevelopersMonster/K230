# Пример 2. Плавное изменение яркости (PWM)

from machine import PWM, FPIOA
import time

fpioa = FPIOA()
fpioa.set_function(42, fpioa.PWM0)

pwm = PWM(0, 1000, 0, enable=True)

while True:
    for duty in range(0, 100, 5):
        pwm.duty(duty)
        time.sleep_ms(50)
    for duty in range(100, 0, -5):
        pwm.duty(duty)
        time.sleep_ms(50)

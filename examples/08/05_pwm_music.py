# Пример 5. PWM как музыка (простая)

from machine import PWM, FPIOA
import time

fpioa = FPIOA()
fpioa.set_function(42, fpioa.PWM0)

pwm = PWM(42,freq=1000,duty=50)

notes = [500, 800, 1000, 1200]

while True:
    for note in notes:
        pwm.freq(note)
        time.sleep(0.3)

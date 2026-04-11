# Пример 3. Кнопка управляет PWM

from machine import PWM, FPIOA
from ybUtils.YbKey import YbKey
import time

fpioa = FPIOA()
fpioa.set_function(42, fpioa.PWM0)

pwm = PWM(0, 1000, 10, enable=True)
key = YbKey()

duty = 10

while True:
    if key.is_pressed():
        duty += 10
        if duty > 100:
            duty = 0
        pwm.duty(duty)
        print("Duty:", duty)
        time.sleep_ms(300)
    time.sleep_ms(50)

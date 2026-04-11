# Пример 4. Управление PWM через UART

from machine import PWM, FPIOA
from ybUtils.YbUart import YbUart
import time

fpioa = FPIOA()
fpioa.set_function(42, fpioa.PWM0)

pwm = PWM(42,freq=1000,duty=50)
uart = YbUart(baudrate=115200)

while True:
    data = uart.read()
    if data:
        try:
            duty = int(data.decode().strip())
            pwm.duty(duty)
            print("Duty set:", duty)
        except:
            print("Error")
    time.sleep_ms(50)

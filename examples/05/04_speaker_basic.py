# Пример 4. Работа с динамиком (buzzer)

from machine import PWM, Pin
import time

buzzer = PWM(Pin(8))

print("Воспроизведение звука")

buzzer.freq(1000)
buzzer.duty(50)

time.sleep(1)

buzzer.duty(0)

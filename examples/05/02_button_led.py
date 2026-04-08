# Пример 2. Управление светодиодом с помощью кнопки

from ybUtils.YbKey import YbKey
from machine import Pin
from ybUtils.YbRGB import YbRGB
import time

key = YbKey()

# Указываем пин светодиода (можно изменить под свою плату)
rgb = YbRGB()

print("Кнопка управляет светодиодом")

while True:
    if key.is_pressed():
        rgb.show_rgb((82, 139, 255)) # включить LED
        
        
    else:
        rgb.show_rgb((0, 0, 0))  # выключить LED
       

    time.sleep_ms(50)

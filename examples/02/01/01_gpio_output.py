# Пример: использование FPIOA для GPIO
#
# Здесь мы назначим пин как обычный GPIO и будем мигать светодиодом

from machine import FPIOA, Pin
import time

fpioa = FPIOA()

# Назначаем физический пин 33 как GPIO33
# Это значит, что теперь он работает как обычный цифровой вывод
fpioa.set_function(33, FPIOA.GPIO33)

# Создаём объект GPIO
led = Pin(33, Pin.OUT)

print("Мигаем светодиодом...")

while True:
    led.value(1)  # включить
    time.sleep(0.5)
    led.value(0)  # выключить
    time.sleep(0.5)

# Важно:
# Если светодиод не мигает — проверь, что именно этот пин выведен на плате
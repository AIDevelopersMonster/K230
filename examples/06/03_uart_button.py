# Пример 3. Отправка состояния кнопки через UART

from ybUtils.YbUart import YbUart
from ybUtils.YbKey import YbKey
import time

uart = YbUart(baudrate=115200)
key = YbKey()

while True:
    if key.is_pressed():
        uart.send("BUTTON: PRESSED\n")
        print("Кнопка нажата")
        time.sleep_ms(300)
    time.sleep_ms(50)

# Пример 1. Базовая работа с UART на K230
#
# Отправляет сообщение и выводит всё, что приходит

from ybUtils.YbUart import YbUart
import time

uart = YbUart(baudrate=115200)

uart.send("Hello K230 UART\n")

while True:
    data = uart.read()
    if data:
        print(data.decode())
    time.sleep_ms(50)

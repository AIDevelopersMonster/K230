# Пример 2. UART Эхо (повторяет полученные данные)

from ybUtils.YbUart import YbUart
import time

uart = YbUart(baudrate=115200)

print("UART Echo запущен")

while True:
    data = uart.read()
    if data:
        text = data.decode()
        print("Получено:", text)
        uart.send("Echo: " + text)
    time.sleep_ms(50)

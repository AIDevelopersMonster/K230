# Пример 4. Управление RGB через UART

from ybUtils.YbUart import YbUart
from ybUtils.YbRGB import YbRGB
import time

uart = YbUart(baudrate=115200)
rgb = YbRGB()

print("Отправь: red / green / blue / off")

while True:
    data = uart.read()
    if data:
        cmd = data.decode().strip().lower()

        if cmd == "red":
            rgb.show_rgb((255,0,0))
        elif cmd == "green":
            rgb.show_rgb((0,255,0))
        elif cmd == "blue":
            rgb.show_rgb((0,0,255))
        elif cmd == "off":
            rgb.show_rgb((0,0,0))

        print("CMD:", cmd)

    time.sleep_ms(50)

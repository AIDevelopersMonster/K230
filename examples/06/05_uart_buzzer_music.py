# Пример 5. Управление буззером через UART

from ybUtils.YbUart import YbUart
from ybUtils.YbBuzzer import YbBuzzer
import time

uart = YbUart(baudrate=115200)
buzzer = YbBuzzer()

print("Команды: beep / alarm")

while True:
    data = uart.read()
    if data:
        cmd = data.decode().strip().lower()

        if cmd == "beep":
            buzzer.beep()
        elif cmd == "alarm":
            for _ in range(3):
                buzzer.on(1000, 50, 0.1)
                time.sleep(0.1)

        print("CMD:", cmd)

    time.sleep_ms(50)

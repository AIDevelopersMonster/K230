# Пример 4. UART команды → OLED + RGB + Буззер

from machine import I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
from ybUtils.YbUart import YbUart
from ybUtils.YbRGB import YbRGB
from ybUtils.YbBuzzer import YbBuzzer
import time

fpioa = FPIOA()
i2c = I2C(1)

fpioa.set_function(34, FPIOA.IIC1_SCL)
fpioa.set_function(35, FPIOA.IIC1_SDA)

oled = SSD1306_I2C(128, 32, i2c)
uart = YbUart(baudrate=115200)
rgb = YbRGB()
buzzer = YbBuzzer()

while True:
    data = uart.read()
    if data:
        cmd = data.decode().strip().lower()

        oled.fill(0)
        oled.text(cmd[:16], 0, 10)

        if cmd == 'red':
            rgb.show_rgb((255,0,0))
        elif cmd == 'green':
            rgb.show_rgb((0,255,0))
        elif cmd == 'blue':
            rgb.show_rgb((0,0,255))
        elif cmd == 'beep':
            buzzer.beep()

        oled.show()

    time.sleep_ms(50)

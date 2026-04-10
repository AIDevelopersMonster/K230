# Пример 3. UART → OLED (I2C)

from machine import I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
from ybUtils.YbUart import YbUart
import time

fpioa = FPIOA()
i2c = I2C(1)

fpioa.set_function(34, FPIOA.IIC1_SCL)
fpioa.set_function(35, FPIOA.IIC1_SDA)

oled = SSD1306_I2C(128, 32, i2c)
uart = YbUart(baudrate=115200)

while True:
    data = uart.read()
    if data:
        text = data.decode().strip()
        oled.fill(0)
        oled.text(text[:16], 0, 10)
        oled.show()
    time.sleep_ms(50)

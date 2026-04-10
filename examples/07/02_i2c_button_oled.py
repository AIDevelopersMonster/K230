# Пример 2. Кнопка → OLED (I2C)

from machine import I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
from ybUtils.YbKey import YbKey
import time

fpioa = FPIOA()
i2c = I2C(1)

fpioa.set_function(34, FPIOA.IIC1_SCL)
fpioa.set_function(35, FPIOA.IIC1_SDA)

oled = SSD1306_I2C(128, 32, i2c)
key = YbKey()

while True:
    oled.fill(0)
    if key.is_pressed():
        oled.text('Button: ON', 0, 10)
    else:
        oled.text('Button: OFF', 0, 10)
    oled.show()
    time.sleep_ms(100)

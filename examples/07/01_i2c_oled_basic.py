# Пример 1. Базовая работа с OLED по I2C

from machine import I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
import time

fpioa = FPIOA()
i2c = I2C(1)

# Настройка пинов (из документации)
fpioa.set_function(34, FPIOA.IIC1_SCL)
fpioa.set_function(35, FPIOA.IIC1_SDA)

oled = SSD1306_I2C(128, 32, i2c)

oled.fill(0)
oled.text('Hello K230', 0, 10)
oled.show()

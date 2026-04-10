# I2C (IIC) примеры для K230

В этой папке показана работа с I2C (IIC) на K230.

## Основы

I2C использует 2 линии:
- SCL (clock)
- SDA (data)

## Подключение OLED

- VCC → 5V
- GND → GND
- SCL → GPIO34
- SDA → GPIO35

## Примеры

| Файл | Описание |
|------|----------|
| 01_i2c_oled_basic.py | Вывод текста |
| 02_i2c_button_oled.py | Кнопка → OLED |
| 03_i2c_uart_oled.py | UART → OLED |
| 04_i2c_full_control.py | Полное управление |

## Особенности

- Используется I2C(1)
- SSD1306 дисплей 128x32

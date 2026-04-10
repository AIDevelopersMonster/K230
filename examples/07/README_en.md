# I2C (IIC) Examples for K230

This folder demonstrates I2C communication on K230.

## Basics

I2C uses 2 lines:
- SCL (clock)
- SDA (data)

## OLED Wiring

- VCC → 5V
- GND → GND
- SCL → GPIO34
- SDA → GPIO35

## Examples

| File | Description |
|------|-------------|
| 01_i2c_oled_basic.py | Display text |
| 02_i2c_button_oled.py | Button → OLED |
| 03_i2c_uart_oled.py | UART → OLED |
| 04_i2c_full_control.py | Full control |

## Notes

- Uses I2C(1)
- SSD1306 128x32 display

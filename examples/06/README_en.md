# UART Examples for K230

This folder demonstrates UART communication on K230.

## Basics

UART is a serial communication protocol.

Wiring:
- TX → RX
- RX → TX
- GND → GND

Baudrate: 115200

## Examples

| File | Description |
|------|-------------|
| 01_uart_basic.py | Basic send/receive |
| 02_uart_echo.py | Echo example |
| 03_uart_button.py | Send button state |
| 04_uart_rgb_control.py | Control RGB via UART |
| 05_uart_buzzer_music.py | Control buzzer |

## Commands

RGB:
- red
- green
- blue
- off

Buzzer:
- beep
- alarm

# WDT Examples for K230

Watchdog Timer resets system if not fed.

## Basics

- WDT(id, timeout)
- wdt.feed()

## Examples

| File | Description |
|------|-------------|
| 01_wdt_basic.py | Basic WDT |
| 02_wdt_reset_demo.py | Reset demo |
| 03_wdt_button.py | Button feed |
| 04_wdt_uart.py | UART feed |
| 05_wdt_full_system.py | Full system |

## Note

System resets if watchdog is not fed.

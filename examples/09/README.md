# WDT (Watchdog) примеры для K230

WDT — это таймер, который перезапускает систему если его не "кормить".

## Основы

- WDT(id, timeout)
- wdt.feed()

## Примеры

| Файл | Описание |
|------|----------|
| 01_wdt_basic.py | Базовый WDT |
| 02_wdt_reset_demo.py | Перезагрузка |
| 03_wdt_button.py | Кнопка → WDT |
| 04_wdt_uart.py | UART → WDT |
| 05_wdt_full_system.py | Полная система |

## Важно

Если не вызвать wdt.feed() — система перезагрузится.

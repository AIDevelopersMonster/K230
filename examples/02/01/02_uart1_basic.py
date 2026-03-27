# Пример: настройка UART через FPIOA
#
# Используем стандартные пины:
# GPIO9 -> TX
# GPIO10 -> RX

from machine import FPIOA, UART

fpioa = FPIOA()

# Назначаем функции
fpioa.set_function(9, FPIOA.UART1_TXD, ie=0, oe=1)
fpioa.set_function(10, FPIOA.UART1_RXD, ie=1, oe=0)

# Инициализируем UART
uart = UART(UART.UART1, 115200)

print("UART готов. Отправляем сообщение...")

uart.write("Hello from K230!\n")

# Подсказка:
# Подключись через USB-UART адаптер и смотри вывод в терминале
# Пример 6. WDT + OLED UI для K230
#
# Что делает программа:
# - запускает watchdog
# - показывает состояние системы на OLED
# - показывает статус кнопки
# - показывает наличие UART-активности
# - при получении данных по UART кормит watchdog
# - при нажатии кнопки тоже кормит watchdog
# - если долго нет активности, watchdog перезапустит систему

from machine import WDT, I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
from ybUtils.YbKey import YbKey
from ybUtils.YbUart import YbUart
import time

# -------------------------------
# Настройки
# -------------------------------
WDT_ID = 1
WDT_TIMEOUT = 3          # секунды
UART_TIMEOUT = 2         # если дольше нет UART, считаем канал неактивным

# -------------------------------
# Инициализация OLED (I2C1)
# -------------------------------
fpioa = FPIOA()
i2c = I2C(1)
fpioa.set_function(34, FPIOA.IIC1_SCL, oe=1, ie=1, pu=1, st=1, ds=15)
fpioa.set_function(35, FPIOA.IIC1_SDA, oe=1, ie=1, pu=1, st=1, ds=15)
oled = SSD1306_I2C(128, 32, i2c)

# -------------------------------
# Инициализация устройств
# -------------------------------
wdt = WDT(WDT_ID, WDT_TIMEOUT)
key = YbKey()
uart = YbUart(baudrate=115200)

# -------------------------------
# Состояние системы
# -------------------------------
last_uart_time = time.time()
last_uart_text = "none"
feed_count = 0
last_source = "boot"


def draw_line(y):
    # На некоторых версиях SSD1306 нет hline(),
    # поэтому рисуем линию вручную через pixel().
    for x in range(128):
        oled.pixel(x, y, 1)


def draw_ui(button_state, uart_ok, seconds_left):
    oled.fill(0)

    # Заголовок
    oled.text("WDT OLED UI", 0, 0)
    draw_line(9)

    # Строка 1
    oled.text("BTN:" + button_state, 0, 12)
    oled.text("UART:" + uart_ok, 64, 12)

    # Строка 2
    oled.text("Feed:" + str(feed_count), 0, 22)
    oled.text("T:" + str(seconds_left), 80, 22)

    oled.show()


print("WDT + OLED UI started")
print("UART heartbeat timeout:", UART_TIMEOUT, "sec")
print("WDT timeout:", WDT_TIMEOUT, "sec")

while True:
    now = time.time()

    # -------------------------------
    # Читаем кнопку
    # -------------------------------
    if key.is_pressed():
        button_state = "ON"
        wdt.feed()
        feed_count += 1
        last_source = "button"
        print("Feed by button")
        time.sleep_ms(250)
    else:
        button_state = "OFF"

    # -------------------------------
    # Читаем UART
    # -------------------------------
    data = uart.read()
    if data:
        try:
            last_uart_text = data.decode().strip()
        except:
            last_uart_text = "decode err"

        last_uart_time = now
        wdt.feed()
        feed_count += 1
        last_source = "uart"
        print("Feed by UART:", last_uart_text)

    # -------------------------------
    # Определяем статус UART
    # -------------------------------
    uart_age = now - last_uart_time
    uart_ok = "OK" if uart_age < UART_TIMEOUT else "WAIT"

    # Сколько примерно осталось до потенциального сброса
    seconds_left = int(max(0, WDT_TIMEOUT - uart_age))

    # -------------------------------
    # Если UART недавно был активен,
    # дополнительно поддерживаем систему живой
    # -------------------------------
    if uart_age < UART_TIMEOUT:
        wdt.feed()
        feed_count += 1
        last_source = "auto"

    # Обновляем OLED
    draw_ui(button_state, uart_ok, seconds_left)

    time.sleep(0.1)

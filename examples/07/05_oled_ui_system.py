# OLED UI система для K230
#
# Что умеет:
# - отображает несколько экранов на OLED 128x32
# - переключает экраны по кнопке
# - показывает UART сообщения
# - управляет RGB и буззером по UART командам
#
# UART команды:
# red, green, blue, off, beep

from machine import I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
from ybUtils.YbKey import YbKey
from ybUtils.YbUart import YbUart
from ybUtils.YbRGB import YbRGB
from ybUtils.YbBuzzer import YbBuzzer
import time

# ---------- Инициализация ----------
fpioa = FPIOA()
# Настройка I2C1 для OLED
fpioa.set_function(34, FPIOA.IIC1_SCL, oe=1, ie=1, pu=1, st=1, ds=15)
fpioa.set_function(35, FPIOA.IIC1_SDA, oe=1, ie=1, pu=1, st=1, ds=15)


i2c = I2C(1)


oled = SSD1306_I2C(128, 32, i2c)
key = YbKey()
uart = YbUart(baudrate=115200)
rgb = YbRGB()
buzzer = YbBuzzer()

# ---------- Состояние системы ----------
screen = 0
screen_count = 4
last_uart = "No data"
last_color = "off"
last_button = "OFF"

# ---------- Вспомогательные функции ----------
def draw_header(title):
    oled.fill(0)
    oled.text(title, 0, 0)



def draw_main():
    draw_header("OLED UI")
    oled.text("Btn: next screen", 0, 12)
    oled.text("UART active", 0, 22)
    oled.show()


def draw_button():
    draw_header("BUTTON")
    oled.text("State:", 0, 12)
    oled.text(last_button, 50, 12)
    oled.text("Press=next UI", 0, 22)
    oled.show()


def draw_uart():
    draw_header("UART")
    oled.text("Last:", 0, 12)
    oled.text(last_uart[:16], 0, 22)
    oled.show()


def draw_control():
    draw_header("CONTROL")
    oled.text("RGB: " + last_color, 0, 12)
    oled.text("Cmd: red blue", 0, 22)
    oled.show()


def render_screen():
    if screen == 0:
        draw_main()
    elif screen == 1:
        draw_button()
    elif screen == 2:
        draw_uart()
    elif screen == 3:
        draw_control()


# ---------- Стартовый экран ----------
render_screen()

# ---------- Главный цикл ----------
while True:
    # Кнопка переключает экран
    if key.is_pressed():
        last_button = "ON"
        screen = (screen + 1) % screen_count
        buzzer.on(1800, 40, 0.05)
        render_screen()
        time.sleep_ms(250)
    else:
        last_button = "OFF"

    # Чтение UART команд
    data = uart.read()
    if data:
        try:
            cmd = data.decode().strip().lower()
        except:
            cmd = "decode err"

        last_uart = cmd

        if cmd == "red":
            rgb.show_rgb((255, 0, 0))
            last_color = "red"
        elif cmd == "green":
            rgb.show_rgb((0, 255, 0))
            last_color = "green"
        elif cmd == "blue":
            rgb.show_rgb((0, 0, 255))
            last_color = "blue"
        elif cmd == "off":
            rgb.show_rgb((0, 0, 0))
            last_color = "off"
        elif cmd == "beep":
            buzzer.beep()

        render_screen()

    # Если открыт экран кнопки, обновляем состояние постоянно
    if screen == 1:
        render_screen()

    time.sleep_ms(30)

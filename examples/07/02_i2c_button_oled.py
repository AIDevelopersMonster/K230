# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230  
#
# Описание:
# Пример работы с кнопкой и OLED дисплеем через I2C.
# Отображает состояние кнопки (нажата/не нажата) на экране.
#
# Используется:
# - YbUart / YbRGB / YbBuzzer / YbKey
#
# ============================================

# Пример 2. Кнопка → OLED (I2C)

# Импортируем необходимые модули:
# machine - базовые функции для работы с железом (I2C, FPIOA)
# ybUtils.ssd1306 - драйвер для OLED дисплея SSD1306
# ybUtils.YbKey - класс для работы с кнопкой платы
# time - функции для работы со временем (задержки)
from machine import I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
from ybUtils.YbKey import YbKey
import time

# Создаём объект для настройки пинов (FPIOA - Flexible Programmable Input/Output Array)
fpioa = FPIOA()

# Создаём объект I2C с номером шины 1
i2c = I2C(1)

# Настраиваем пины для работы I2C:
# Пин 34 назначаем как SCL (тактовый сигнал)
# Пин 35 назначаем как SDA (линия данных)
fpioa.set_function(34, FPIOA.IIC1_SCL)
fpioa.set_function(35, FPIOA.IIC1_SDA)

# Создаём объект OLED дисплея:
# 128 - ширина экрана в пикселях
# 32 - высота экрана в пикселях
# i2c - шина I2C для связи с дисплеем
oled = SSD1306_I2C(128, 32, i2c)

# Создаём объект для работы с кнопкой
key = YbKey()

# Бесконечный цикл для постоянного опроса состояния кнопки
while True:
    # Очищаем экран перед каждым обновлением
    oled.fill(0)
    
    # Проверяем, нажата ли кнопка
    if key.is_pressed():
        # Если кнопка нажата - выводим "Button: ON"
        oled.text('Button: ON', 0, 10)
    else:
        # Если кнопка не нажата - выводим "Button: OFF"
        oled.text('Button: OFF', 0, 10)
    
    # Обновляем дисплей, чтобы показать изменения
    oled.show()
    
    # Делаем паузу 100 миллисекунд, чтобы не перегружать процессор
    time.sleep_ms(100)

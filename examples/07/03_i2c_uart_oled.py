# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230  
#
# Описание:
# Пример приёма данных через UART и отображения на OLED дисплее.
# Получает текст по последовательному порту и показывает его на экране.
#
# Используется:
# - YbUart / YbRGB / YbBuzzer / YbKey
#
# ============================================

# Пример 3. UART → OLED (I2C)

# Импортируем необходимые модули:
# machine - базовые функции для работы с железом (I2C, FPIOA)
# ybUtils.ssd1306 - драйвер для OLED дисплея SSD1306
# ybUtils.YbUart - класс для работы с UART (последовательный порт)
# time - функции для работы со временем (задержки)
from machine import I2C, FPIOA
from ybUtils.ssd1306 import SSD1306_I2C
from ybUtils.YbUart import YbUart
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

# Создаём объект для работы с UART:
# baudrate=115200 - скорость передачи данных (бит в секунду)
uart = YbUart(baudrate=115200)

# Бесконечный цикл для постоянного опроса UART
while True:
    # Читаем данные из UART порта
    data = uart.read()
    
    # Если данные получены (не пустые)
    if data:
        # Декодируем байты в строку и убираем лишние пробелы
        text = data.decode().strip()
        
        # Очищаем экран перед выводом нового текста
        oled.fill(0)
        
        # Выводим текст на экран (максимум 16 символов)
        # [:16] - берём только первые 16 символов, чтобы текст поместился
        oled.text(text[:16], 0, 10)
        
        # Обновляем дисплей
        oled.show()
    
    # Делаем паузу 50 миллисекунд перед следующей проверкой
    time.sleep_ms(50)

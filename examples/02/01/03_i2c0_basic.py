# Пример: настройка I2C через FPIOA
#
# Используем:
# GPIO32 -> SCL
# GPIO33 -> SDA

from machine import FPIOA, I2C

fpioa = FPIOA()

# Назначаем функции
fpioa.set_function(32, FPIOA.IIC0_SCL)
fpioa.set_function(33, FPIOA.IIC0_SDA)

# Инициализируем I2C
i2c = I2C(0, freq=100000)

print("Сканируем I2C устройства...")

devices = i2c.scan()
print("Найдено устройств:", devices)

# Подключи любой I2C датчик и посмотри, определяется ли он
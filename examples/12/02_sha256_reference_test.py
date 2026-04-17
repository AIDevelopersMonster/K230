# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230        
#
# Описание:
# Проверка работы SHA-256 с эталонными значениями.
# Показывает:
# 1) как использовать update() для поэтапного вычисления хеша;
# 2) как сравнивать результат с известными эталонными значениями;
# 3) что SHA-256 работает корректно на разных размерах данных.
#
# Используется:
# - hashlib
# - binascii (или ubinascii для MicroPython)
#
# ============================================

import hashlib

try:
    import binascii
except ImportError:
    import ubinascii as binascii


def to_hex(data):
    """
    Преобразует байты в hex-строку.
    
    Почему это нужно? 
    На некоторых прошивках K230 метод hexdigest() может отсутствовать,
    поэтому мы используем binascii.hexlify() для получения hex-представления.
    
    :param data: байты (bytes)
    :return: строка с hex-представлением
    """
    value = binascii.hexlify(data)
    # Если hexlify вернул bytes, декодируем в строку
    if isinstance(value, bytes):
        return value.decode()
    return value


print("=== K230 SHA-256 reference test ===")

# Тест 1: создаём массив из 65 нулевых байтов
# Мы передаём его дважды через update(), чтобы проверить работу по частям
a = bytes([0] * 65)
b = hashlib.sha256()
b.update(a)  # первая порция данных
b.update(a)  # вторая порция данных
c = b.digest()  # получаем итоговый хеш (32 байта)

print("test #1 digest =", c)
# Для сравнения показываем тот же хеш в hex-формате
print("test #1 hex    =", to_hex(hashlib.sha256(a + a).digest()))

# Ожидаемое значение хеша для 130 нулевых байтов (65 + 65)
expected1 = b"\xe5Z\\'sj\x87a\xc8\xe9j\xce\xc0r\x10#%\xe0\x8c\xb2\xd0\xdb\xb4\xd4p,\xfe8\xf8\xab\x07\t"
if c != expected1:
    raise Exception("error #1! {}".format(c))

# Тест 2: работаем с большим массивом данных (1024 байта)
# Проверяем, что SHA-256 корректно обрабатывает большие объёмы
a = bytes([0] * 1024)
b = hashlib.sha256(a)  # можно передать данные сразу при создании объекта
c = b.digest()

print("test #2 digest =", c)
print("test #2 hex    =", to_hex(c))

# Ожидаемое значение хеша для 1024 нулевых байтов
expected2 = b'_p\xbf\x18\xa0\x86\x00p\x16\xe9H\xb0J\xed;\x82\x10:6\xbe\xa4\x17U\xb6\xcd\xdf\xaf\x10\xac\xe3\xc6\xef'
if c != expected2:
    raise Exception("error #2! {}".format(c))

# Если все тесты пройдены, выводим PASS
print("PASS")

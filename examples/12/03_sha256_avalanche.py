# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Демонстрация эффекта лавины SHA-256.
# Меняем в сообщении один символ и смотрим,
# насколько сильно меняется итоговый хеш.
#
# Используется:
# - hashlib
# ============================================

import hashlib

try:
    import binascii
except ImportError:
    import ubinascii as binascii


def to_hex(data):
    """Перевод bytes в hex-строку без hexdigest()."""
    value = binascii.hexlify(data)
    if isinstance(value, bytes):
        return value.decode()
    return value


def count_bits_in_byte(value):
    """Подсчёт количества единичных бит в одном байте."""
    count = 0
    while value:
        count += value & 1
        value >>= 1
    return count


def count_diff_bits(d1, d2):
    """Сколько бит отличаются между двумя digest по 32 байта."""
    diff = 0
    for i in range(len(d1)):
        diff += count_bits_in_byte(d1[i] ^ d2[i])
    return diff


m1 = b"K230 Vision Module"
m2 = b"K230 Vision ModulE"  # изменили только один символ

d1 = hashlib.sha256(m1).digest()
d2 = hashlib.sha256(m2).digest()

diff_bits = count_diff_bits(d1, d2)

print("message #1:", m1)
print("hash #1   :", to_hex(d1))
print()
print("message #2:", m2)
print("hash #2   :", to_hex(d2))
print()
print("Different bits:", diff_bits, "from 256")

if d1 == d2:
    raise Exception("Avalanche demo failed: hashes should differ")

print("PASS")

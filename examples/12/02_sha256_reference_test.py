# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Адаптация рабочего примера SHA-256 для K230.
# Показывает два способа использования:
# 1) создать пустой объект и подавать данные через update();
# 2) передать данные прямо в конструктор sha256(data).
#
# Используется:
# - hashlib
# ============================================

import hashlib

print("=== K230 SHA-256 reference test ===")

# --------------------------------------------
# Test 1: 65 нулевых байт, поданных два раза.
# Это эквивалентно хешированию 130 нулевых байт.
# --------------------------------------------
a = bytes([0] * 65)
b = hashlib.sha256()
b.update(a)
b.update(a)
c = b.digest()
print("test #1 digest    =", c)
print("test #1 hexdigest =", hashlib.sha256(a + a).hexdigest())

expected1 = b"\xe5Z\\'sj\x87a\xc8\xe9j\xce\xc0r\x10#%\xe0\x8c\xb2\xd0\xdb\xb4\xd4p,\xfe8\xf8\xab\x07\t"
if c != expected1:
    raise Exception("error #1! {}".format(c))

# --------------------------------------------
# Test 2: 1024 нулевых байта, переданных сразу.
# --------------------------------------------
a = bytes([0] * 1024)
b = hashlib.sha256(a)
c = b.digest()
print("test #2 digest    =", c)
print("test #2 hexdigest =", b.hexdigest())

expected2 = b'_p\xbf\x18\xa0\x86\x00p\x16\xe9H\xb0J\xed;\x82\x10:6\xbe\xa4\x17U\xb6\xcd\xdf\xaf\x10\xac\xe3\xc6\xef'
if c != expected2:
    raise Exception("error #2! {}".format(c))

print("PASS")

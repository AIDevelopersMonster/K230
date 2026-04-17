# ============================================
# K230 Example
# Описание:
# Проверка ошибок AES:
# 1) неверная длина ключа
# 2) неверная длина данных
# ============================================

import ucryptolib

# Test 1: invalid key length
try:
    ucryptolib.aes(b'short_key', ucryptolib.MODE_ECB)
    raise Exception('Invalid key NOT detected')
except ValueError:
    print('Invalid key length: PASS')

# Test 2: invalid data length (не кратно 16 байтам)
try:
    key = b'1234567890abcdef'
    cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)
    cipher.encrypt(b'short')
    raise Exception('Invalid data length NOT detected')
except ValueError:
    print('Invalid data length: PASS')

print('PASS')

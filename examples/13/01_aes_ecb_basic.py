# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Базовый пример AES-128 в режиме ECB для K230.
# Показывает:
# 1) создание AES-объекта;
# 2) шифрование 16-байтного блока;
# 3) расшифровку и проверку результата.
#
# Используется:
# - ucryptolib
# ============================================

import ucryptolib

try:
    import binascii
except ImportError:
    import ubinascii as binascii


def to_hex(data):
    value = binascii.hexlify(data)
    if isinstance(value, bytes):
        return value.decode()
    return value


key = b'1234567890abcdef'          # 16 bytes -> AES-128
plaintext = b'This is 16 bytes'    # exactly 16 bytes

cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)
encrypted = cipher.encrypt(plaintext)

cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)
decrypted = cipher.decrypt(encrypted)

print('key       =', key)
print('plaintext =', plaintext)
print('encrypted =', encrypted)
print('encrypted(hex) =', to_hex(encrypted))
print('decrypted =', decrypted)

assert decrypted == plaintext, 'AES-128 ECB failed'
print('PASS')

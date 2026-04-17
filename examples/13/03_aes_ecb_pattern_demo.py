# ============================================
# K230 Example
# Демонстрация слабости ECB режима
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

key = b'1234567890abcdef'

# два одинаковых блока
block = b'AAAAAAAAAAAAAAAA'
data = block + block

cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)
encrypted = cipher.encrypt(data)

block1 = encrypted[:16]
block2 = encrypted[16:32]

print('block1 =', to_hex(block1))
print('block2 =', to_hex(block2))
print('blocks equal:', block1 == block2)

print('ECB weakness demo: identical plaintext blocks -> identical ciphertext')

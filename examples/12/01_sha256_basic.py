# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Базовый пример SHA-256 для K230.
# Показывает:
# 1) как посчитать хеш строки;
# 2) разницу между digest() и hex-представлением;
# 3) что один и тот же вход всегда даёт один и тот же выход.
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
    """Перевод bytes в hex-строку без использования hexdigest()."""
    value = binascii.hexlify(data)
    if isinstance(value, bytes):
        return value.decode()
    return value


def show_hash(title, data):
    """Печать SHA-256 в бинарном и hex формате."""
    h_bin = hashlib.sha256(data).digest()
    h_hex = to_hex(h_bin)

    print("=" * 50)
    print(title)
    print("data      =", data)
    print("bytes len =", len(data))
    print("digest    =", h_bin)
    print("hex       =", h_hex)
    print("hex len   =", len(h_hex), "symbols")
    print("digest len=", len(h_bin), "bytes")


message = b"K230 SHA-256 demo"
same_message = b"K230 SHA-256 demo"
other_message = b"K230 SHA-256 demo!"

show_hash("Example 1: basic SHA-256", message)
show_hash("Example 2: same input -> same hash", same_message)
show_hash("Example 3: another message", other_message)

h1 = to_hex(hashlib.sha256(message).digest())
h2 = to_hex(hashlib.sha256(same_message).digest())
h3 = to_hex(hashlib.sha256(other_message).digest())

print("=" * 50)
print("Determinism check:")
print("hash(message) == hash(same_message):", h1 == h2)
print("hash(message) == hash(other_message):", h1 == h3)

if h1 != h2:
    raise Exception("Determinism check failed")

if h1 == h3:
    raise Exception("Different messages should not match in this demo")

print("PASS")

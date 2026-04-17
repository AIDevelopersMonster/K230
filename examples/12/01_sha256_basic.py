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
# 2) разницу между digest() и hexdigest();
# 3) что один и тот же вход всегда даёт один и тот же выход.
#
# Используется:
# - uhashlib
# ============================================

import uhashlib


def show_hash(title, data):
    """Печать SHA-256 в бинарном и hex формате."""
    h_hex = uhashlib.sha256(data).hexdigest()
    h_bin = uhashlib.sha256(data).digest()

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

h1 = uhashlib.sha256(message).hexdigest()
h2 = uhashlib.sha256(same_message).hexdigest()
h3 = uhashlib.sha256(other_message).hexdigest()

print("=" * 50)
print("Determinism check:")
print("hash(message) == hash(same_message):", h1 == h2)
print("hash(message) == hash(other_message):", h1 == h3)

if h1 != h2:
    raise Exception("Determinism check failed")

if h1 == h3:
    raise Exception("Different messages should not match in this demo")

print("PASS")

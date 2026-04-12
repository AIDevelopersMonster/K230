# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub https://github.com/AIDevelopersMonster/K230
# ============================================

# Пример 1. Базовый Timer (one-shot + periodic)

from machine import Timer
import time

# Однократный callback
def once_cb(t):
    print("One-shot timer triggered")

# Периодический callback
def periodic_cb(t):
    print("Periodic timer triggered")

# Создаём виртуальный таймер
timer = Timer(-1)

# One-shot (100 мс)
timer.init(period=100, mode=Timer.ONE_SHOT, callback=once_cb)
time.sleep(0.2)

# Periodic (1 Гц)
timer.init(freq=1, mode=Timer.PERIODIC, callback=periodic_cb)
time.sleep(3)

timer.deinit()
print("Timer stopped")

# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Базовый пример многопоточности для K230.
# Показывает, как запустить два потока через _thread,
# чтобы они по очереди печатали сообщения в терминал.
#
# Используется:
# - _thread
# - time
# ============================================

import _thread
import time


def worker(name):
    """Функция, выполняемая в каждом потоке."""
    while True:
        print("This is thread {}".format(name))
        # Важно: даём планировщику шанс переключить поток
        time.sleep(1)


# Запускаем первый поток
_thread.start_new_thread(worker, ("THREAD_1",))

# Небольшая задержка, чтобы первый поток успел стартовать
# как в учебном примере
if hasattr(time, "sleep_ms"):
    time.sleep_ms(500)
else:
    time.sleep(0.5)

# Запускаем второй поток
_thread.start_new_thread(worker, ("THREAD_2",))

# Главный поток ничего не делает, только поддерживает программу живой
while True:
    if hasattr(time, "sleep_ms"):
        time.sleep_ms(1)
    else:
        time.sleep(0.001)

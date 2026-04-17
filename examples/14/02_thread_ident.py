# ============================================
# K230 Example
# Описание:
# Демонстрация идентификаторов потоков и
# параллельного выполнения.
# ============================================

import _thread
import time


def worker():
    thread_id = _thread.get_ident()
    counter = 0

    while True:
        print("Thread ID: {} | counter: {}".format(thread_id, counter))
        counter += 1

        # важно для переключения потоков
        if hasattr(time, "sleep_ms"):
            time.sleep_ms(500)
        else:
            time.sleep(0.5)


# запуск двух потоков
_thread.start_new_thread(worker, ())
_thread.start_new_thread(worker, ())

# основной цикл
while True:
    if hasattr(time, "sleep_ms"):
        time.sleep_ms(1)
    else:
        time.sleep(0.001)

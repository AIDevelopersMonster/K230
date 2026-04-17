# ============================================
# K230 Example
# Описание:
# Демонстрация синхронизации потоков через lock.
# Два потока увеличивают общий счётчик.
# ============================================

import _thread
import time

# общий ресурс
shared_counter = 0
lock = _thread.allocate_lock()


def worker(name):
    global shared_counter

    for i in range(5):
        lock.acquire()

        temp = shared_counter
        temp += 1
        shared_counter = temp

        print("{} incremented counter to {}".format(name, shared_counter))

        lock.release()

        # даём другим потокам шанс
        if hasattr(time, "sleep_ms"):
            time.sleep_ms(200)
        else:
            time.sleep(0.2)


# запуск потоков
_thread.start_new_thread(worker, ("THREAD_1",))
_thread.start_new_thread(worker, ("THREAD_2",))

# ждём завершения
while True:
    if hasattr(time, "sleep_ms"):
        time.sleep_ms(1)
    else:
        time.sleep(0.001)

# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Описание:
# Демонстрация синхронизации потоков через lock.
# Два потока увеличивают общий счётчик.
# Показывает, как избежать проблем при доступе к общим данным.
#
# Используется:
# - _thread
# - time
# ============================================

import _thread
import time

# Общий ресурс - переменная, которую используют оба потока
shared_counter = 0

# Создаём lock (замок) для синхронизации доступа к общему ресурсу
lock = _thread.allocate_lock()


def worker(name):
    """
    Функция, выполняемая в каждом потоке.
    Увеличивает общий счётчик на 1 пять раз.
    
    Аргументы:
        name - имя потока (строка)
    """
    global shared_counter  # Говорим, что используем глобальную переменную

    # Выполняем 5 итераций
    for i in range(5):
        # Захватываем lock перед доступом к общему ресурсу
        # Другие потоки ждут, пока lock не будет освобождён
        lock.acquire()

        # Критическая секция - код, который должен выполняться только одним потоком
        temp = shared_counter
        temp += 1
        shared_counter = temp

        print("{} incremented counter to {}".format(name, shared_counter))

        # Освобождаем lock, чтобы другой поток мог работать
        lock.release()

        # Даём другим потокам шанс выполниться
        # Небольшая задержка между операциями
        if hasattr(time, "sleep_ms"):
            time.sleep_ms(200)  # 200 мс = 0.2 секунды
        else:
            time.sleep(0.2)


# Запускаем первый поток с именем THREAD_1
_thread.start_new_thread(worker, ("THREAD_1",))

# Запускаем второй поток с именем THREAD_2
_thread.start_new_thread(worker, ("THREAD_2",))

# Основной поток ждёт завершения работы
# В реальном проекте здесь была бы логика ожидания завершения потоков
while True:
    # Короткая задержка, чтобы не занимать процессор полностью
    if hasattr(time, "sleep_ms"):
        time.sleep_ms(1)
    else:
        time.sleep(0.001)

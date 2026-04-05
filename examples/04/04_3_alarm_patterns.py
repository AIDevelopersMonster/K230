# Пример 3. Набор тревожных сигналов для буззера на YAHBOOM K230
#
# В этом примере собраны несколько полезных шаблонов сигналов:
# 1) короткая тревога
# 2) двойной сигнал подтверждения
# 3) сирена с изменением частоты
# 4) сигнал ошибки
#
# Этот пример удобно использовать как основу для своих проектов:
# охранная система, уведомления, ошибки, подтверждение действий.

from ybUtils.YbBuzzer import YbBuzzer
import time

# Создаём объект управления буззером
buzzer = YbBuzzer()


def short_alarm(repeat=3):
    """Короткая тревога: несколько одинаковых коротких сигналов."""
    for _ in range(repeat):
        buzzer.on(1200, 60, 0.15)
        time.sleep(0.10)
    buzzer.off()


def confirm_signal():
    """Двойной короткий сигнал подтверждения."""
    buzzer.on(1800, 50, 0.08)
    time.sleep(0.08)
    buzzer.on(2200, 50, 0.08)
    buzzer.off()


def error_signal():
    """Сигнал ошибки: два низких звука."""
    for _ in range(2):
        buzzer.on(700, 55, 0.25)
        time.sleep(0.12)
    buzzer.off()


def siren(cycles=3):
    """Сирена: плавное повышение и понижение частоты."""
    for _ in range(cycles):
        # Повышаем частоту
        for freq in range(800, 2001, 100):
            buzzer.on(freq, 50, 0.03)
            time.sleep(0.01)

        # Понижаем частоту
        for freq in range(2000, 799, -100):
            buzzer.on(freq, 50, 0.03)
            time.sleep(0.01)

    buzzer.off()


if __name__ == "__main__":
    # Демонстрация всех шаблонов по очереди
    print("1. Короткая тревога")
    short_alarm()
    time.sleep(1)

    print("2. Сигнал подтверждения")
    confirm_signal()
    time.sleep(1)

    print("3. Сигнал ошибки")
    error_signal()
    time.sleep(1)

    print("4. Сирена")
    siren()
    buzzer.off()

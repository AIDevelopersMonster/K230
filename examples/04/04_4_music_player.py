# Пример 4. Проигрыватель мелодий для буззера на YAHBOOM K230
#
# Этот пример показывает, как оформить универсальный музыкальный проигрыватель
# для пассивного буззера на K230.
#
# Возможности:
# 1) словарь нот с частотами
# 2) паузы между нотами
# 3) воспроизведение разных мелодий
# 4) удобная структура для добавления своих песен

from ybUtils.YbBuzzer import YbBuzzer
import time

# Создаём объект управления буззером
buzzer = YbBuzzer()

# Словарь нот (частоты в Гц)
NOTES = {
    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523,
    "D5": 587,
    "E5": 659,
    "F5": 698,
    "G5": 784,
    "A5": 880,
    "B5": 988,
    "P": 0,  # Пауза
}

# Длительности
WHOLE = 1.0
HALF = 0.5
QUARTER = 0.25
EIGHTH = 0.125


def play_note(note, duration, volume=50, gap=0.05):
    """Проигрывает одну ноту или паузу."""
    freq = NOTES.get(note, 0)

    if freq == 0:
        # Если это пауза, просто ждём
        time.sleep(duration)
    else:
        buzzer.on(freq, volume, duration)

    # Короткая пауза между нотами для читаемости мелодии
    time.sleep(gap)


def play_melody(melody, volume=50):
    """Проигрывает список нот в формате: [("C5", 0.25), ...]"""
    for note, duration in melody:
        play_note(note, duration, volume)
    buzzer.off()


# Мелодия 1. Twinkle Twinkle Little Star
TWINKLE = [
    ("C5", QUARTER), ("C5", QUARTER), ("G5", QUARTER), ("G5", QUARTER),
    ("A5", QUARTER), ("A5", QUARTER), ("G5", HALF),
    ("F5", QUARTER), ("F5", QUARTER), ("E5", QUARTER), ("E5", QUARTER),
    ("D5", QUARTER), ("D5", QUARTER), ("C5", HALF),
]

# Мелодия 2. Простая восходящая гамма
SCALE_UP = [
    ("C4", EIGHTH), ("D4", EIGHTH), ("E4", EIGHTH), ("F4", EIGHTH),
    ("G4", EIGHTH), ("A4", EIGHTH), ("B4", EIGHTH), ("C5", QUARTER),
]

# Мелодия 3. Сигнал запуска
STARTUP_TONE = [
    ("C5", EIGHTH), ("E5", EIGHTH), ("G5", EIGHTH), ("C5", QUARTER),
]


if __name__ == "__main__":
    print("Проигрываем сигнал запуска...")
    play_melody(STARTUP_TONE, volume=55)
    time.sleep(1)

    print("Проигрываем гамму...")
    play_melody(SCALE_UP, volume=50)
    time.sleep(1)

    print("Проигрываем Twinkle Twinkle Little Star...")
    play_melody(TWINKLE, volume=50)

    # По завершении выключаем буззер
    buzzer.off()

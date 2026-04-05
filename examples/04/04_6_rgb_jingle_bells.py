# Пример 6. RGB + музыка Jingle Bells на YAHBOOM K230
#
# В этом примере встроенный RGB-светодиод и пассивный буззер
# работают синхронно: каждой ноте соответствует цвет.
#
# Что демонстрирует пример:
# 1) проигрывание простой версии мелодии Jingle Bells
# 2) световую индикацию для каждой ноты
# 3) использование пауз между фразами
#
# Подходит для праздничных проектов, демонстраций и обучения.

from ybUtils.YbBuzzer import YbBuzzer
from ybUtils.YbRGB import YbRGB
import time

buzzer = YbBuzzer()
rgb = YbRGB()

# Ноты и их частоты (Гц)
NOTES = {
    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523,
    "P": 0,  # Пауза
}

# Цвета для нот
NOTE_COLORS = {
    "C4": (255, 0, 0),
    "D4": (255, 127, 0),
    "E4": (255, 255, 0),
    "F4": (0, 255, 0),
    "G4": (0, 255, 255),
    "A4": (0, 0, 255),
    "B4": (139, 0, 255),
    "C5": (255, 0, 255),
    "P": (0, 0, 0),
}

# Длительности
Q = 0.25  # четверть
H = 0.50  # половина
E = 0.125 # восьмая


def play_note_with_rgb(note, duration, volume=50, gap=0.05):
    """Проигрывает ноту и включает соответствующий цвет RGB."""
    freq = NOTES.get(note, 0)
    color = NOTE_COLORS.get(note, (255, 255, 255))

    if freq == 0:
        buzzer.off()
        rgb.show_rgb((0, 0, 0))
        time.sleep(duration)
    else:
        rgb.show_rgb(color)
        buzzer.on(freq, volume, duration)

    # После каждой ноты кратко гасим светодиод
    rgb.show_rgb((0, 0, 0))
    time.sleep(gap)


def play_melody(melody, volume=50):
    """Проигрывает мелодию со световой индикацией."""
    for note, duration in melody:
        play_note_with_rgb(note, duration, volume)

    buzzer.off()
    rgb.show_rgb((0, 0, 0))


# Упрощённая версия Jingle Bells
JINGLE_BELLS = [
    ("E4", Q), ("E4", Q), ("E4", H),
    ("E4", Q), ("E4", Q), ("E4", H),
    ("E4", Q), ("G4", Q), ("C4", Q), ("D4", Q), ("E4", 0.75),
    ("P", Q),

    ("F4", Q), ("F4", Q), ("F4", Q), ("F4", Q),
    ("F4", Q), ("E4", Q), ("E4", Q), ("E4", Q), ("E4", Q),
    ("D4", Q), ("D4", Q), ("E4", Q), ("D4", H), ("G4", H),
]


if __name__ == "__main__":
    print("Запуск RGB + Jingle Bells...")
    play_melody(JINGLE_BELLS, volume=50)

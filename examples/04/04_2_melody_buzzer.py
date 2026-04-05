# Пример 2. Воспроизведение мелодии на буззере
#
# Буззер на K230 является пассивным, поэтому можно задавать
# частоту сигнала и получать разные ноты.

from ybUtils.YbBuzzer import YbBuzzer
import time

buzzer = YbBuzzer()

# Частоты нот (Гц)
C5 = 523
D5 = 587
E5 = 659
F5 = 698
G5 = 784
A5 = 880
B5 = 988

BEAT = 0.3

# Простая мелодия (Twinkle Twinkle)
def play_melody():
    notes = [
        (C5, BEAT), (C5, BEAT), (G5, BEAT), (G5, BEAT),
        (A5, BEAT), (A5, BEAT), (G5, BEAT * 2),
        (F5, BEAT), (F5, BEAT), (E5, BEAT), (E5, BEAT),
        (D5, BEAT), (D5, BEAT), (C5, BEAT * 2),
    ]

    for freq, duration in notes:
        buzzer.on(freq, 50, duration)
        time.sleep(0.1)

    buzzer.off()

play_melody()

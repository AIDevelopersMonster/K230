'''
Пример 4. Управление динамиком (buzzer) с помощью кнопки

Описание:
При нажатии кнопки воспроизводится звуковой сигнал.
Используются библиотеки:
- YbKey — кнопка
- YbBuzzer — динамик
'''

from ybUtils.YbKey import YbKey
from ybUtils.YbBuzzer import YbBuzzer
import time

# --- Инициализация ---
key = YbKey()
buzzer = YbBuzzer()

print("Нажмите кнопку — будет звук")

while True:
    if key.is_pressed():
        # антидребезг
        time.sleep_ms(20)

        if key.is_pressed():
            print("Кнопка нажата → звук")

            # короткий сигнал
            buzzer.beep()

            # ждём отпускания кнопки
            while key.is_pressed():
                pass

    time.sleep_ms(50)

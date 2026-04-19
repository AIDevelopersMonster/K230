# ============================================
# K230 Example
# Создание изображения в памяти и вывод
# ============================================

from media.display import *
from media.media import *
import image
import time

Display.init(Display.ST7701, width=640, height=480, osd_num=1, to_ide=True)
MediaManager.init()

# Создаём пустое изображение
img = image.Image(640, 480, image.RGB888)

# Рисуем простой графический элемент
img.draw_string(50, 200, "Hello K230", color=(255, 255, 0), scale=3)

Display.show_image(img)

print('Generated image displayed')

while True:
    time.sleep(1)

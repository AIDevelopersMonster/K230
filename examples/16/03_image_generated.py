# ============================================
# K230 Example
# Создание изображения в памяти и вывод
# Исправленная версия: используется framebuffer,
# чтобы картинка полностью отображалась и в IDE, и на дисплее.
# ============================================

from media.display import *
from media.media import *
import image
import time

Display.init(Display.ST7701, width=640, height=480, osd_num=1, to_ide=True)
MediaManager.init()

# Создаём изображение сразу с копированием в framebuffer
img = image.Image(640, 480, image.RGB888, copy_to_fb=True)

# Фон и текст
img.clear()
img.draw_string(40, 200, "Hello K230", color=(255, 255, 0), scale=3)
img.draw_string(40, 260, "Generated in RAM", color=(0, 255, 255), scale=2)

Display.show_image(img)

print('Generated image displayed')

while True:
    time.sleep(1)

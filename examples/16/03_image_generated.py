from media.display import *
from media.media import *
import image
import time

Display.init(Display.ST7701, width=640, height=480, osd_num=1, to_ide=True)
MediaManager.init()

# Загружаем картинку
img = image.Image('/sdcard/resources/wp.png', copy_to_fb=True)

# Конвертируем в RGB888, как рекомендует документация для PNG
img = img.to_rgb888()

# Пишем текст поверх картинки
img.draw_string_advanced(30, 30, 28, "Hello K230", color=(255, 255, 0))
img.draw_string_advanced(30, 70, 20, "wp.png demo", color=(0, 255, 255))

# Показываем
Display.show_image(img)

print("Image with text displayed")

while True:
    time.sleep(1)

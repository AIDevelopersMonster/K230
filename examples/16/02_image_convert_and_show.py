# ============================================
# K230 Example
# Демонстрация преобразования формата изображения
# ============================================

from media.display import *
from media.media import *
import image
import time

Display.init(Display.ST7701, width=640, height=480, osd_num=1, to_ide=True)
MediaManager.init()

# Загружаем изображение
img = image.Image('/sdcard/resources/wp.png')

# Демонстрация разных форматов
img_rgb = img.to_rgb888()

print('Converted to RGB888')

Display.show_image(img_rgb)

while True:
    time.sleep(1)

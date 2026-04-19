# ============================================
# K230 Example
# Базовое отображение картинки из файла
# ============================================

from media.display import *
from media.media import *
import image
import time

# Инициализация дисплея
Display.init(Display.ST7701, width=640, height=480, osd_num=1, to_ide=True)
MediaManager.init()

# Загрузка картинки с SD-карты
img = image.Image('/sdcard/resources/wp.png', copy_to_fb=True)

# Для корректного отображения PNG конвертируем в RGB888
img = img.to_rgb888()

# Показываем картинку на экране
Display.show_image(img)

print('Image displayed: /sdcard/resources/wp.png')

while True:
    time.sleep(1)

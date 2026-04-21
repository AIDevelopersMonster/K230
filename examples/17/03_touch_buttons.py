# ============================================
# K230 Example
# Кнопка через touch (исправленная версия)
# ============================================

import time, os
import image

from media.display import *
from media.media import *
from machine import TOUCH

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

tp = TOUCH(0)


def main():
    print("touch button demo")

    bg = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    bg.clear()
    bg.draw_rectangle(0,0,DISPLAY_WIDTH,DISPLAY_HEIGHT,color=(255,255,255),fill=True)

    overlay = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()

    try:
        while True:
            os.exitpoint()

            bg.draw_rectangle(200,180,240,120,color=(0,255,0),thickness=3)
            bg.draw_string_advanced(250,230,24,"BUTTON",color=(0,0,0))

            Display.show_image(bg)

            overlay.clear()

            points = tp.read(1)
            if len(points):
                pt = points[0]

                if 200 < pt.x < 440 and 180 < pt.y < 300:
                    print("Button pressed")
                    overlay.draw_string_advanced(220,320,28,"CLICK!",color=(255,0,0))

            Display.show_image(overlay, layer=Display.LAYER_OSD2, alpha=200)

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass

    Display.deinit()
    MediaManager.deinit()


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    main()

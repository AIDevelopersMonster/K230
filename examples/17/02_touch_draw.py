# ============================================
# K230 Example
# Рисование пальцем (исправленная версия)
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
    print("touch draw demo")

    # фон
    bg = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    bg.clear()
    bg.draw_rectangle(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, color=(255,255,255), fill=True)

    # слой рисования
    canvas = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    canvas.clear()

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()

    last_x = None
    last_y = None

    try:
        while True:
            os.exitpoint()

            Display.show_image(bg)

            points = tp.read(1)
            if len(points):
                pt = points[0]

                if pt.event == 0 or pt.event == TOUCH.EVENT_DOWN or pt.event == TOUCH.EVENT_MOVE:
                    if last_x is not None and last_y is not None and pt.event != 2:
                        canvas.draw_line(last_x, last_y, pt.x, pt.y, color=(0,0,0), thickness=5)

                    last_x = pt.x
                    last_y = pt.y

            Display.show_image(canvas, layer=Display.LAYER_OSD2, alpha=255)

            time.sleep(0.02)

    except KeyboardInterrupt:
        pass

    Display.deinit()
    MediaManager.deinit()


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    main()

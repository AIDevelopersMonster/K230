# ============================================
# K230 Draw Line Example
# Author: AIDevelopersMonster
# Board: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Description:
# Static image example for img.draw_line().
# Draws a simple line-based Yahboom-style logo on a white background.
#
# API:
# img.draw_line(x0, y0, x1, y1, color=(R, G, B), thickness=N)
# x0, y0 - start point
# x1, y1 - end point
# color - RGB line color
# thickness - line width in pixels
# ============================================

import time
import os
import image
from media.display import *
from media.media import *

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480


def draw_yahboom_lines(img, start_x, start_y, color, thickness):
    """Draw the word 'Yahboom' using only straight lines."""
    # Y
    img.draw_line(start_x, start_y, start_x + 20, start_y + 20, color=color, thickness=thickness)
    img.draw_line(start_x + 40, start_y, start_x + 20, start_y + 20, color=color, thickness=thickness)
    img.draw_line(start_x + 20, start_y + 20, start_x + 20, start_y + 45, color=color, thickness=thickness)

    # a
    x = start_x + 55
    img.draw_line(x, start_y + 20, x + 25, start_y + 20, color=color, thickness=thickness)
    img.draw_line(x + 25, start_y + 20, x + 25, start_y + 45, color=color, thickness=thickness)
    img.draw_line(x + 25, start_y + 45, x, start_y + 45, color=color, thickness=thickness)
    img.draw_line(x, start_y + 45, x, start_y + 30, color=color, thickness=thickness)
    img.draw_line(x, start_y + 30, x + 25, start_y + 30, color=color, thickness=thickness)

    # h
    x = start_x + 95
    img.draw_line(x, start_y, x, start_y + 45, color=color, thickness=thickness)
    img.draw_line(x, start_y + 25, x + 25, start_y + 25, color=color, thickness=thickness)
    img.draw_line(x + 25, start_y + 25, x + 25, start_y + 45, color=color, thickness=thickness)

    # b
    x = start_x + 135
    img.draw_line(x, start_y, x, start_y + 45, color=color, thickness=thickness)
    img.draw_line(x, start_y + 20, x + 25, start_y + 20, color=color, thickness=thickness)
    img.draw_line(x + 25, start_y + 20, x + 25, start_y + 45, color=color, thickness=thickness)
    img.draw_line(x + 25, start_y + 45, x, start_y + 45, color=color, thickness=thickness)

    # o
    for x in (start_x + 175, start_x + 215):
        img.draw_line(x, start_y + 20, x + 25, start_y + 20, color=color, thickness=thickness)
        img.draw_line(x + 25, start_y + 20, x + 25, start_y + 45, color=color, thickness=thickness)
        img.draw_line(x + 25, start_y + 45, x, start_y + 45, color=color, thickness=thickness)
        img.draw_line(x, start_y + 45, x, start_y + 20, color=color, thickness=thickness)

    # m
    x = start_x + 255
    img.draw_line(x, start_y + 20, x, start_y + 45, color=color, thickness=thickness)
    img.draw_line(x, start_y + 20, x + 12, start_y + 32, color=color, thickness=thickness)
    img.draw_line(x + 12, start_y + 32, x + 24, start_y + 20, color=color, thickness=thickness)
    img.draw_line(x + 24, start_y + 20, x + 24, start_y + 45, color=color, thickness=thickness)


def main():
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    img.clear()
    img.draw_rectangle(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, color=(255, 255, 255), fill=True)

    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()

    try:
        color = (0, 191, 255)
        thickness = 4
        draw_yahboom_lines(img, 170, 210, color, thickness)
        img.draw_string(10, 10, "draw_line(x0,y0,x1,y1,color,thickness)", color=(0, 0, 0))
        Display.show_image(img)

        while True:
            os.exitpoint()
            time.sleep_ms(100)

    except KeyboardInterrupt as e:
        print("User stop:", e)
    except Exception as e:
        print("Exception:", e)
    finally:
        Display.deinit()
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
        time.sleep_ms(100)
        MediaManager.deinit()


if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    main()

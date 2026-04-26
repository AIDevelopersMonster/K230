# Line segment detection from test images on Yahboom K230 / CanMV
# Put images into: Graphics detection/Line segment detection/img/
# The demo detects all / horizontal / vertical line segments.

import os, gc, math, time
import image
from media.display import *
from media.media import *

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Change this mode when you want to solve a different task:
# "all"        - show every detected line segment
# "horizontal" - show only horizontal lines
# "vertical"   - show only vertical lines
DETECT_MODE = "all"

# Test image path on the board. Copy the img folder next to this script.
IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/horizontal_vertical_lines.png"

# Detection settings.
MERGE_DISTANCE = 15
MAX_THETA_DIFF = 10
ANGLE_TOLERANCE_DEG = 12


def line_angle_deg(line_tuple):
    """Return line angle in degrees in range 0..180."""
    x1, y1, x2, y2 = line_tuple[:4]
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle < 0:
        angle += 180
    return angle


def is_horizontal(line_tuple, tolerance=ANGLE_TOLERANCE_DEG):
    angle = line_angle_deg(line_tuple)
    return angle <= tolerance or angle >= 180 - tolerance


def is_vertical(line_tuple, tolerance=ANGLE_TOLERANCE_DEG):
    angle = line_angle_deg(line_tuple)
    return abs(angle - 90) <= tolerance


def need_draw(line_tuple):
    if DETECT_MODE == "horizontal":
        return is_horizontal(line_tuple)
    if DETECT_MODE == "vertical":
        return is_vertical(line_tuple)
    return True


def main():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()

    try:
        img = image.Image(IMAGE_PATH)
        lines = img.find_line_segments(merge_distance=MERGE_DISTANCE,
                                       max_theta_diff=MAX_THETA_DIFF)

        found = 0
        for ln in lines:
            coords = ln.line()
            if not need_draw(coords):
                continue

            if is_horizontal(coords):
                color = (0, 255, 0)      # green = horizontal
            elif is_vertical(coords):
                color = (255, 0, 0)      # red = vertical
            else:
                color = (0, 128, 255)    # blue = other angle

            img.draw_line(coords, color=color, thickness=3)
            found += 1

        img.draw_string(5, 5, "mode: %s" % DETECT_MODE, color=(255, 255, 0), scale=2)
        img.draw_string(5, 28, "found: %d" % found, color=(255, 255, 0), scale=2)
        Display.show_image(img)

        print("Mode:", DETECT_MODE)
        print("Found:", found)

        while True:
            time.sleep_ms(100)

    finally:
        gc.collect()


if __name__ == "__main__":
    main()

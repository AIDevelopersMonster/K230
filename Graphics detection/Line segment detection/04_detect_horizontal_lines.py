# Detect only horizontal line segments from img/horizontal_lines.png
# Copy the img folder to the same path on the K230 SD card.

import time, math, gc
import image
from media.display import *
from media.media import *

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/horizontal_lines.png"
ANGLE_TOLERANCE_DEG = 12


def line_angle_deg(line_tuple):
    x1, y1, x2, y2 = line_tuple[:4]
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle < 0:
        angle += 180
    return angle


def is_horizontal(line_tuple):
    angle = line_angle_deg(line_tuple)
    return angle <= ANGLE_TOLERANCE_DEG or angle >= 180 - ANGLE_TOLERANCE_DEG


Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
MediaManager.init()

try:
    img = image.Image(IMAGE_PATH)
    lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)

    count = 0
    for ln in lines:
        coords = ln.line()
        if is_horizontal(coords):
            img.draw_line(coords, color=(0, 255, 0), thickness=4)
            count += 1

    img.draw_string(5, 5, "Horizontal: %d" % count, color=(255, 255, 0), scale=2)
    Display.show_image(img)
    print("Horizontal lines:", count)

    while True:
        time.sleep_ms(100)
finally:
    gc.collect()

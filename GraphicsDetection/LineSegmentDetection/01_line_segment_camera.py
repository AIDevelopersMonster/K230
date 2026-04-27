# Line segment detection on Yahboom K230 / CanMV
# Beginner-friendly real-time demo: detects straight line segments and draws them on the LCD.

import time, os, sys, gc
from media.sensor import *
from media.display import *
from media.media import *
from libs.PipeLine import PipeLine, ScopedTiming
import image

PICTURE_WIDTH = 160
PICTURE_HEIGHT = 120
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480


def scale_line(line_tuple, src_w=PICTURE_WIDTH, src_h=PICTURE_HEIGHT,
               dst_w=DISPLAY_WIDTH, dst_h=DISPLAY_HEIGHT):
    """Scale (x1, y1, x2, y2) from processing resolution to display resolution."""
    x1, y1, x2, y2 = line_tuple[:4]
    return (
        round(x1 * dst_w / src_w),
        round(y1 * dst_h / src_h),
        round(x2 * dst_w / src_w),
        round(y2 * dst_h / src_h),
    )


def main():
    display_mode = "LCD"

    # Pipeline uses a low-resolution camera channel for detection and a 640x480 OSD layer for drawing.
    pl = PipeLine(rgb888p_size=[640, 360], display_size=[DISPLAY_WIDTH, DISPLAY_HEIGHT],
                  display_mode=display_mode)
    pl.create(ch1_frame_size=[PICTURE_WIDTH, PICTURE_HEIGHT])

    try:
        while True:
            os.exitpoint()

            # 1) Read a small image from camera channel 1.
            src = pl.sensor.snapshot(chn=CAM_CHN_ID_1)

            # 2) Detect line segments.
            # merge_distance: maximum gap in pixels for merging close segments.
            # max_theta_diff: maximum angle difference in degrees for merging segments.
            lines = src.find_line_segments(merge_distance=15, max_theta_diff=10)

            # 3) Draw result on transparent ARGB layer.
            overlay = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
            overlay.clear()

            for n, ln in enumerate(lines):
                x1, y1, x2, y2 = scale_line(ln.line())
                overlay.draw_line((x1, y1, x2, y2), color=(255, 0, 0), thickness=6)
                overlay.draw_cross(x1, y1, color=(0, 255, 0), size=8, thickness=2)
                overlay.draw_cross(x2, y2, color=(0, 0, 255), size=8, thickness=2)
                overlay.draw_string(x1, max(0, y1 - 18), str(n), color=(255, 255, 0), scale=1)

            overlay.draw_string(5, 5, "Line segments: %d" % len(lines), color=(255, 255, 255), scale=2)
            Display.show_image(overlay, 0, 0, Display.LAYER_OSD3)
            time.sleep_us(1)

    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        try:
            pl.destroy()
        except Exception:
            pass
        gc.collect()


if __name__ == "__main__":
    main()

# ============================================================
# Камера: поиск ТОЛЬКО горизонтальных линий
#
# Правильный сценарий демонстрации:
# 1. Откройте картинку img/horizontal_lines.png на экране компьютера,
#    планшета или телефона.
# 2. Наведите камеру K230 на эту картинку.
# 3. Скрипт ищет линии именно с КАМЕРЫ, а не читает PNG с SD-карты.
#
# Что делает скрипт:
# - получает кадр с камеры;
# - ищет отрезки линий через find_line_segments();
# - оставляет только горизонтальные;
# - рисует их зелёным цветом на OSD-слое.
#
# Если линии не находятся:
# - увеличьте яркость экрана с картинкой;
# - уберите блики;
# - держите камеру ровнее;
# - увеличьте ANGLE_TOLERANCE_DEG;
# - попробуйте приблизить/отдалить камеру.
# ============================================================

import time, math, gc
import image
from media.sensor import *
from media.display import *
from media.media import *
from libs.PipeLine import PipeLine

PICTURE_WIDTH = 160
PICTURE_HEIGHT = 120
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
ANGLE_TOLERANCE_DEG = 12


def scale_line(line_tuple):
    x1, y1, x2, y2 = line_tuple[:4]
    return (round(x1 * DISPLAY_WIDTH / PICTURE_WIDTH),
            round(y1 * DISPLAY_HEIGHT / PICTURE_HEIGHT),
            round(x2 * DISPLAY_WIDTH / PICTURE_WIDTH),
            round(y2 * DISPLAY_HEIGHT / PICTURE_HEIGHT))


def line_angle_deg(line_tuple):
    x1, y1, x2, y2 = line_tuple[:4]
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return a + 180 if a < 0 else a


def is_horizontal(line_tuple):
    a = line_angle_deg(line_tuple)
    return a <= ANGLE_TOLERANCE_DEG or a >= 180 - ANGLE_TOLERANCE_DEG


def main():
    pl = PipeLine(rgb888p_size=[640, 360], display_size=[DISPLAY_WIDTH, DISPLAY_HEIGHT], display_mode="LCD")
    pl.create(ch1_frame_size=[PICTURE_WIDTH, PICTURE_HEIGHT])

    try:
        while True:
            os.exitpoint()
            frame = pl.sensor.snapshot(chn=CAM_CHN_ID_1)
            lines = frame.find_line_segments(merge_distance=15, max_theta_diff=10)

            overlay = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
            overlay.clear()

            count = 0
            for ln in lines:
                raw = ln.line()
                if is_horizontal(raw):
                    overlay.draw_line(scale_line(raw), color=(0, 255, 0), thickness=6)
                    count += 1

            overlay.draw_string(5, 5, "CAM horizontal: %d" % count, color=(255, 255, 0), scale=2)
            Display.show_image(overlay, 0, 0, Display.LAYER_OSD3)
            time.sleep_us(1)

    finally:
        try:
            pl.destroy()
        except Exception:
            pass
        gc.collect()


if __name__ == "__main__":
    main()

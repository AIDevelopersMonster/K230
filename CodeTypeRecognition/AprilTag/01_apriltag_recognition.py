# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# AprilTag Recognition / Распознавание AprilTag
#
# Что делает:
# - получает изображение с камеры K230;
# - ищет AprilTag через img.find_apriltags();
# - поддерживает несколько семейств тегов;
# - рисует рамку, центр и подпись с family/id/rotation;
# - печатает результат в консоль CanMV IDE.
# ============================================

import time
import math
import gc
import image
from media.sensor import *
from media.display import *
from media.media import *

SENSOR_WIDTH = 400
SENSOR_HEIGHT = 240
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
DISPLAY_X = 120
DISPLAY_Y = 120
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (255, 0, 0)
CENTER_COLOR = (0, 255, 0)

# AprilTag supports several tag families. More enabled families = lower FPS.
tag_families = 0
tag_families |= image.TAG16H5
tag_families |= image.TAG25H7
tag_families |= image.TAG25H9
tag_families |= image.TAG36H10
tag_families |= image.TAG36H11
tag_families |= image.ARTOOLKIT

# None = scan whole frame. Example ROI: (40, 20, 320, 200)
APRILTAG_ROI = None


def family_name(tag):
    family_dict = {
        image.TAG16H5: "TAG16H5",
        image.TAG25H7: "TAG25H7",
        image.TAG25H9: "TAG25H9",
        image.TAG36H10: "TAG36H10",
        image.TAG36H11: "TAG36H11",
        image.ARTOOLKIT: "ARTOOLKIT",
    }
    return family_dict.get(tag.family(), "UNKNOWN")


def degrees(rad):
    return (180.0 * rad) / math.pi


def init_sensor():
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=SENSOR_WIDTH, height=SENSOR_HEIGHT)
    sensor.set_pixformat(Sensor.RGB565)
    return sensor


def init_display():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()


def find_tags(img):
    if APRILTAG_ROI:
        img.draw_rectangle(APRILTAG_ROI, color=(120, 120, 120), thickness=1)
        return img.find_apriltags(roi=APRILTAG_ROI, families=tag_families)
    return img.find_apriltags(families=tag_families)


def draw_tag_info(img, tag):
    family = family_name(tag)
    tag_id = tag.id()
    rot = degrees(tag.rotation())

    img.draw_rectangle(tag.rect(), color=BOX_COLOR, thickness=4)
    img.draw_cross(tag.cx(), tag.cy(), color=CENTER_COLOR, thickness=2)
    img.draw_string_advanced(0, 0, 22, "%s ID:%d" % (family, tag_id), color=TEXT_COLOR)
    img.draw_string_advanced(0, 26, 18, "rot: %.2f deg" % rot, color=TEXT_COLOR)

    print("Tag Family %s, Tag ID %d, rotation %.3f degrees" % (family, tag_id, rot))


def draw_fps(img, fps, count):
    img.draw_string_advanced(0, SENSOR_HEIGHT - 26, 18, "FPS: %.2f  Tags: %d" % (fps, count), color=TEXT_COLOR)


def main():
    sensor = None
    try:
        sensor = init_sensor()
        init_display()
        sensor.run()
        clock = time.clock()

        while True:
            clock.tick()
            img = sensor.snapshot()
            tags = find_tags(img)

            for tag in tags:
                draw_tag_info(img, tag)
                break

            draw_fps(img, clock.fps(), len(tags))
            Display.show_image(img, x=DISPLAY_X, y=DISPLAY_Y)
            gc.collect()

    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Error occurred:", e)
    finally:
        if sensor:
            sensor.stop()
            sensor.deinit()
        Display.deinit()
        MediaManager.deinit()
        gc.collect()


if __name__ == "__main__":
    main()

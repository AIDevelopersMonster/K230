# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / FaceOrientationDetection
# 02_face_orientation_file_io.py
#
# Face orientation detection with file read/write.
# It creates and reads a config file, writes the latest Euler angles to TXT,
# and appends a CSV history log.
#
# Copy face_pose_common.py to the same folder on the TF card:
# /sdcard/FaceRecognition/FaceOrientationDetection/face_pose_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
import os
import time
import gc

try:
    import sys
    sys.path.append("/sdcard/FaceRecognition/FaceOrientationDetection")
except Exception:
    pass

from face_pose_common import create_pose_app

APP_DIR = "/sdcard/FaceRecognition/FaceOrientationDetection"
CONFIG_PATH = APP_DIR + "/face_orientation_config.txt"
LAST_RESULT_PATH = APP_DIR + "/face_orientation_last_result.txt"
LOG_PATH = APP_DIR + "/face_orientation_log.csv"

DEFAULT_CONFIG = """# K230 face orientation detection config\nFACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel\nFACE_POSE_KMODEL_PATH=/sdcard/kmodel/face_pose.kmodel\nANCHORS_PATH=/sdcard/utils/prior_data_320.bin\nCONFIDENCE_THRESHOLD=0.50\nNMS_THRESHOLD=0.20\nWRITE_INTERVAL_MS=1000\nDRAW_ANGLES=1\n"""

fp = None


def split_path(path):
    return [item for item in path.split("/") if item]


def ensure_dir(path):
    current = "/" if path.startswith("/") else ""
    for part in split_path(path):
        if current == "/":
            current = "/" + part
        elif current:
            current = current + "/" + part
        else:
            current = part
        try:
            os.stat(current)
        except Exception:
            os.mkdir(current)


def file_exists(path):
    try:
        os.stat(path)
        return True
    except Exception:
        return False


def write_text(path, text, mode="w"):
    folder = path.rsplit("/", 1)[0]
    if folder:
        ensure_dir(folder)
    with open(path, mode) as f:
        f.write(text)


def read_text(path, default=""):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return default


def ensure_config():
    ensure_dir(APP_DIR)
    if not file_exists(CONFIG_PATH):
        write_text(CONFIG_PATH, DEFAULT_CONFIG, "w")


def read_config():
    ensure_config()
    text = read_text(CONFIG_PATH, "")
    cfg = {}
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        cfg[key.strip().upper()] = value.strip()
    return cfg


def parse_int(value, default_value):
    try:
        return int(value)
    except Exception:
        return default_value


def ticks_ms_safe():
    try:
        return time.ticks_ms()
    except Exception:
        return int(time.time() * 1000)


def ticks_diff_safe(now, before):
    try:
        return time.ticks_diff(now, before)
    except Exception:
        return now - before


def csv_safe(value):
    return str(value).replace("\r", " ").replace("\n", " ").replace(",", ";")


def append_csv(path, header, row):
    need_header = not file_exists(path)
    with open(path, "a") as f:
        if need_header:
            f.write(",".join(header) + "\n")
        f.write(",".join([csv_safe(v) for v in row]) + "\n")


def write_pose_files(det_boxes, pose_res, fps):
    now = ticks_ms_safe()
    face_count = len(det_boxes) if det_boxes else 0
    pitch, yaw, roll = 0.0, 0.0, 0.0
    if pose_res:
        euler = pose_res[0][1]
        pitch, yaw, roll = euler[0], euler[1], euler[2]

    text = "time_ms=%d\n" % now
    text += "fps=%.3f\n" % fps
    text += "face_count=%d\n" % face_count
    text += "pitch=%.3f\n" % pitch
    text += "yaw=%.3f\n" % yaw
    text += "roll=%.3f\n" % roll
    write_text(LAST_RESULT_PATH, text, "w")

    append_csv(LOG_PATH,
               ["time_ms", "fps", "face_count", "pitch", "yaw", "roll"],
               [now, "%.3f" % fps, face_count, "%.3f" % pitch, "%.3f" % yaw, "%.3f" % roll])


def exce_demo(pl):
    global fp
    cfg = read_config()
    write_interval_ms = parse_int(cfg.get("WRITE_INTERVAL_MS", "1000"), 1000)
    draw_angles = cfg.get("DRAW_ANGLES", "1") == "1"
    last_write = 0
    try:
        fp = create_pose_app(pl, cfg)
        while True:
            with ScopedTiming("total", 1):
                start = ticks_ms_safe()
                img = pl.get_frame()
                det_boxes, pose_res = fp.run(img)
                fp.draw_result(pl, det_boxes, pose_res, draw_angles=draw_angles)
                pl.show_image()
                elapsed = ticks_diff_safe(ticks_ms_safe(), start)
                fps = 1000.0 / elapsed if elapsed > 0 else 0
                now = ticks_ms_safe()
                if ticks_diff_safe(now, last_write) >= write_interval_ms:
                    write_pose_files(det_boxes, pose_res, fps)
                    last_write = now
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face orientation file I/O demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    global fp
    if fp:
        fp.deinit()
        fp = None
    gc.collect()


if __name__ == "__main__":
    pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
    try:
        pl.create()
        exce_demo(pl)
    finally:
        exit_demo()
        try:
            pl.destroy()
        except Exception:
            pass

# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / KeyPointRecognition
# 02_face_landmark_file_io.py
#
# Facial key point recognition with file read/write.
# This example imports keypoint_common.py and adds:
# - config file reading;
# - latest result TXT writing;
# - CSV log appending.
#
# Copy keypoint_common.py to the same folder on the TF card:
# /sdcard/FaceRecognition/KeyPointRecognition/keypoint_common.py
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
import os
import time
import gc

try:
    import sys
    sys.path.append("/sdcard/FaceRecognition/KeyPointRecognition")
except Exception:
    pass

from keypoint_common import FaceLandMark, load_anchors

APP_DIR = "/sdcard/FaceRecognition/KeyPointRecognition"
CONFIG_PATH = APP_DIR + "/keypoint_config.txt"
LAST_RESULT_PATH = APP_DIR + "/keypoint_last_result.txt"
LOG_PATH = APP_DIR + "/keypoint_log.csv"

DEFAULT_CONFIG = """# K230 facial key point recognition config\nFACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel\nFACE_LANDMARK_KMODEL_PATH=/sdcard/kmodel/face_landmark.kmodel\nANCHORS_PATH=/sdcard/utils/prior_data_320.bin\nCONFIDENCE_THRESHOLD=0.50\nNMS_THRESHOLD=0.20\nWRITE_INTERVAL_MS=1000\n"""

FACE_DET_INPUT_SIZE = [320, 320]
FACE_LANDMARK_INPUT_SIZE = [192, 192]

flm = None


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


def parse_float(value, default_value):
    try:
        return float(value)
    except Exception:
        return default_value


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


def write_landmark_files(det_boxes, landmark_res, fps):
    now = ticks_ms_safe()
    face_count = len(det_boxes) if det_boxes else 0
    keypoint_count = 0
    first_x = 0
    first_y = 0

    if landmark_res:
        pred = landmark_res[0]
        keypoint_count = len(pred) // 2
        if len(pred) >= 2:
            first_x = int(pred[0])
            first_y = int(pred[1])

    text = "time_ms=%d\n" % now
    text += "fps=%.3f\n" % fps
    text += "face_count=%d\n" % face_count
    text += "keypoint_count=%d\n" % keypoint_count
    text += "first_keypoint_x=%d\n" % first_x
    text += "first_keypoint_y=%d\n" % first_y
    write_text(LAST_RESULT_PATH, text, "w")

    append_csv(
        LOG_PATH,
        ["time_ms", "fps", "face_count", "keypoint_count", "first_keypoint_x", "first_keypoint_y"],
        [now, "%.3f" % fps, face_count, keypoint_count, first_x, first_y]
    )


def create_app(pl, cfg):
    det_model = cfg.get("FACE_DET_KMODEL_PATH", "/sdcard/kmodel/face_detection_320.kmodel")
    landmark_model = cfg.get("FACE_LANDMARK_KMODEL_PATH", "/sdcard/kmodel/face_landmark.kmodel")
    anchors_path = cfg.get("ANCHORS_PATH", "/sdcard/utils/prior_data_320.bin")
    confidence = parse_float(cfg.get("CONFIDENCE_THRESHOLD", "0.50"), 0.50)
    nms = parse_float(cfg.get("NMS_THRESHOLD", "0.20"), 0.20)
    anchors = load_anchors(anchors_path)
    return FaceLandMark(
        det_model,
        landmark_model,
        det_input_size=FACE_DET_INPUT_SIZE,
        landmark_input_size=FACE_LANDMARK_INPUT_SIZE,
        anchors=anchors,
        confidence_threshold=confidence,
        nms_threshold=nms,
        rgb888p_size=pl.rgb888p_size,
        display_size=pl.display_size,
        debug_mode=0
    )


def exce_demo(pl):
    global flm
    cfg = read_config()
    write_interval_ms = parse_int(cfg.get("WRITE_INTERVAL_MS", "1000"), 1000)
    last_write = 0
    try:
        flm = create_app(pl, cfg)
        while True:
            with ScopedTiming("total", 0):
                start = ticks_ms_safe()
                img = pl.get_frame()
                det_boxes, landmark_res = flm.run(img)
                flm.draw_result(pl, det_boxes, landmark_res)
                pl.show_image()
                elapsed = ticks_diff_safe(ticks_ms_safe(), start)
                fps = 1000.0 / elapsed if elapsed > 0 else 0
                now = ticks_ms_safe()
                if ticks_diff_safe(now, last_write) >= write_interval_ms:
                    write_landmark_files(det_boxes, landmark_res, fps)
                    last_write = now
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face landmark file I/O demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    global flm
    if flm:
        flm.deinit()
        flm = None
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

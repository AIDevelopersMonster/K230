# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / FaceDetectition
# 03_face_detection_file_io.py
#
# Face detection demo with file reading and writing.
# It creates and reads a config file, then writes the latest face result
# and appends a CSV log.
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from media.media import *
from time import *
import nncase_runtime as nn
import ulab.numpy as np
import aidemo
import time
import gc
import os

APP_DIR = "/sdcard/FaceRecognition/FaceDetectition"
CONFIG_PATH = APP_DIR + "/face_detection_config.txt"
LAST_RESULT_PATH = APP_DIR + "/face_detection_last_result.txt"
LOG_PATH = APP_DIR + "/face_detection_log.csv"

DEFAULT_KMODEL_PATH = "/sdcard/kmodel/face_detection_320.kmodel"
DEFAULT_ANCHORS_PATH = "/sdcard/utils/prior_data_320.bin"
MODEL_INPUT_SIZE = [320, 320]
ANCHOR_LEN = 4200
DET_DIM = 4

DEFAULT_CONFIG = """# K230 Face Detection config\nKMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel\nANCHORS_PATH=/sdcard/utils/prior_data_320.bin\nCONFIDENCE_THRESHOLD=0.50\nNMS_THRESHOLD=0.20\nWRITE_INTERVAL_MS=1000\n"""

face_det = None


def align_up(value, align):
    return (value + align - 1) // align * align


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
            try:
                os.mkdir(current)
            except Exception as e:
                print("Cannot create folder", current, e)
                return False
    return True


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
    return CONFIG_PATH


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
    text = str(value)
    text = text.replace("\r", " ").replace("\n", " ").replace(",", ";")
    return text


def append_csv(path, header, row):
    need_header = not file_exists(path)
    with open(path, "a") as f:
        if need_header:
            f.write(",".join(header) + "\n")
        f.write(",".join([csv_safe(v) for v in row]) + "\n")


def write_detection_files(dets, fps):
    ensure_dir(APP_DIR)
    now = ticks_ms_safe()
    count = len(dets) if dets else 0
    if dets:
        x, y, w, h = map(lambda v: int(round(v, 0)), dets[0][:4])
    else:
        x, y, w, h = 0, 0, 0, 0

    text = "time_ms=%d\n" % now
    text += "fps=%.3f\n" % fps
    text += "face_count=%d\n" % count
    text += "x=%d\n" % x
    text += "y=%d\n" % y
    text += "w=%d\n" % w
    text += "h=%d\n" % h
    write_text(LAST_RESULT_PATH, text, "w")

    append_csv(LOG_PATH,
               ["time_ms", "fps", "face_count", "x", "y", "w", "h"],
               [now, "%.3f" % fps, count, x, y, w, h])


def load_anchors(path):
    anchors = np.fromfile(path, dtype=np.float)
    return anchors.reshape((ANCHOR_LEN, DET_DIM))


class FaceDetectionApp(AIBase):
    def __init__(self, kmodel_path, model_input_size, anchors,
                 confidence_threshold=0.5, nms_threshold=0.2,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.kmodel_path = kmodel_path
        self.model_input_size = model_input_size
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.anchors = anchors
        self.rgb888p_size = [align_up(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [align_up(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode
        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT, nn.ai2d_format.NCHW_FMT, np.uint8, np.uint8)

    def get_padding_param(self):
        dst_w = self.model_input_size[0]
        dst_h = self.model_input_size[1]
        ratio_w = dst_w / self.rgb888p_size[0]
        ratio_h = dst_h / self.rgb888p_size[1]
        ratio = min(ratio_w, ratio_h)
        new_w = int(ratio * self.rgb888p_size[0])
        new_h = int(ratio * self.rgb888p_size[1])
        dw = (dst_w - new_w) / 2
        dh = (dst_h - new_h) / 2
        return (int(round(0)), int(round(dh * 2 + 0.1)), int(round(0)), int(round(dw * 2 - 0.1)))

    def config_preprocess(self, input_image_size=None):
        ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
        top, bottom, left, right = self.get_padding_param()
        self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])
        self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
        self.ai2d.build([1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                        [1, 3, self.model_input_size[1], self.model_input_size[0]])

    def postprocess(self, results):
        post_ret = aidemo.face_det_post_process(
            self.confidence_threshold, self.nms_threshold, self.model_input_size[1],
            self.anchors, self.rgb888p_size, results)
        return post_ret[0] if post_ret else post_ret

    def draw_result(self, pl, dets):
        if dets:
            pl.osd_img.clear()
            for det in dets:
                x, y, w, h = map(lambda v: int(round(v, 0)), det[:4])
                x = x * self.display_size[0] // self.rgb888p_size[0]
                y = y * self.display_size[1] // self.rgb888p_size[1]
                w = w * self.display_size[0] // self.rgb888p_size[0]
                h = h * self.display_size[1] // self.rgb888p_size[1]
                pl.osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)
        else:
            pl.osd_img.clear()


def create_app(pl, cfg):
    kmodel_path = cfg.get("KMODEL_PATH", DEFAULT_KMODEL_PATH)
    anchors_path = cfg.get("ANCHORS_PATH", DEFAULT_ANCHORS_PATH)
    confidence = parse_float(cfg.get("CONFIDENCE_THRESHOLD", "0.50"), 0.50)
    nms = parse_float(cfg.get("NMS_THRESHOLD", "0.20"), 0.20)
    anchors = load_anchors(anchors_path)
    app = FaceDetectionApp(kmodel_path, MODEL_INPUT_SIZE, anchors, confidence, nms,
                           rgb888p_size=pl.rgb888p_size,
                           display_size=pl.display_size,
                           debug_mode=0)
    app.config_preprocess()
    return app


def exce_demo(pl):
    global face_det
    cfg = read_config()
    write_interval_ms = parse_int(cfg.get("WRITE_INTERVAL_MS", "1000"), 1000)
    last_write = 0
    try:
        face_det = create_app(pl, cfg)
        while True:
            with ScopedTiming("total", 0):
                start = ticks_ms_safe()
                img = pl.get_frame()
                res = face_det.run(img)
                face_det.draw_result(pl, res)
                pl.show_image()
                elapsed = ticks_diff_safe(ticks_ms_safe(), start)
                fps = 1000.0 / elapsed if elapsed > 0 else 0
                now = ticks_ms_safe()
                if ticks_diff_safe(now, last_write) >= write_interval_ms:
                    write_detection_files(res, fps)
                    last_write = now
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face detection file I/O demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    global face_det
    if face_det:
        try:
            face_det.deinit()
        except Exception as e:
            print("deinit error:", e)
        face_det = None
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

# ============================================
# K230 FaceRecognition / AIvision common module
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Copy this file to /sdcard/libs/face_aivision_common.py
# and import it in examples as:
# from libs.face_aivision_common import create_face_detection_app, safe_deinit
# ============================================

from libs.PipeLine import ScopedTiming
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

APP_DIR = "/sdcard/FaceRecognition/AIvision"
CONFIG_PATH = APP_DIR + "/face_config.txt"
LAST_RESULT_PATH = APP_DIR + "/face_last_result.txt"
LOG_PATH = APP_DIR + "/face_log.csv"

DEFAULT_KMODEL_PATH = "/sdcard/kmodel/face_detection_320.kmodel"
DEFAULT_ANCHORS_PATH = "/sdcard/utils/prior_data_320.bin"
DEFAULT_MODEL_INPUT_SIZE = [320, 320]
DEFAULT_ANCHOR_LEN = 4200
DEFAULT_DET_DIM = 4

DEFAULT_CONFIG_TEXT = """# K230 FaceRecognition AIvision config\n# The demo creates this file automatically if it does not exist.\n# You can edit it on the TF card and run 02_face_detection_file_io.py again.\n\nKMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel\nANCHORS_PATH=/sdcard/utils/prior_data_320.bin\nCONFIDENCE_THRESHOLD=0.50\nNMS_THRESHOLD=0.20\nDEBUG_MODE=0\nSAVE_LOG=1\nWRITE_INTERVAL_MS=1000\n"""


def align_up(value, align):
    return (value + align - 1) // align * align


def _split_path(path):
    parts = []
    for item in path.split("/"):
        if item:
            parts.append(item)
    return parts


def ensure_dir(path):
    """Create a directory recursively if it does not exist."""
    if not path or path == "/":
        return True
    current = "/" if path.startswith("/") else ""
    for part in _split_path(path):
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
    """Write text to a file. mode='w' replaces, mode='a' appends."""
    folder = path.rsplit("/", 1)[0]
    if folder:
        ensure_dir(folder)
    with open(path, mode) as f:
        f.write(text)


def read_text(path, default=""):
    """Read a text file. Return default if the file is missing."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return default


def ensure_default_config():
    ensure_dir(APP_DIR)
    if not file_exists(CONFIG_PATH):
        write_text(CONFIG_PATH, DEFAULT_CONFIG_TEXT, "w")
    return CONFIG_PATH


def read_config(path=CONFIG_PATH):
    """Read KEY=VALUE settings from a text config file."""
    ensure_default_config()
    cfg = {}
    text = read_text(path, "")
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        cfg[key.strip().upper()] = value.strip()
    return cfg


def parse_int(value, default_value=0):
    try:
        return int(value)
    except Exception:
        return default_value


def parse_float(value, default_value=0.0):
    try:
        return float(value)
    except Exception:
        return default_value


def ticks_ms_safe():
    try:
        return time.ticks_ms()
    except Exception:
        try:
            return int(time.time() * 1000)
        except Exception:
            return 0


def csv_safe(value):
    text = str(value)
    text = text.replace("\r", " ").replace("\n", " ")
    text = text.replace(",", ";")
    return text


def append_csv(path, header, row):
    """Append one CSV row. The header is written only once."""
    folder = path.rsplit("/", 1)[0]
    if folder:
        ensure_dir(folder)
    need_header = not file_exists(path)
    with open(path, "a") as f:
        if need_header:
            f.write(",".join(header) + "\n")
        f.write(",".join([csv_safe(v) for v in row]) + "\n")


def detection_count(dets):
    if dets:
        return len(dets)
    return 0


def get_best_detection(dets):
    """Return the first detection and its score if available."""
    if not dets:
        return None, 0.0
    det = dets[0]
    score = 0.0
    try:
        if len(det) > 4:
            score = float(det[4])
    except Exception:
        score = 0.0
    return det, score


def write_detection_files(dets, fps=0.0, result_path=LAST_RESULT_PATH, log_path=LOG_PATH):
    """Write the latest face result and append a CSV log row."""
    ensure_dir(APP_DIR)
    now = ticks_ms_safe()
    count = detection_count(dets)
    det, score = get_best_detection(dets)

    if det:
        x, y, w, h = map(lambda v: int(round(v, 0)), det[:4])
    else:
        x, y, w, h = 0, 0, 0, 0

    text = "time_ms=%d\n" % now
    text += "fps=%.3f\n" % fps
    text += "face_count=%d\n" % count
    text += "best_score=%.4f\n" % score
    text += "x=%d\n" % x
    text += "y=%d\n" % y
    text += "w=%d\n" % w
    text += "h=%d\n" % h
    write_text(result_path, text, "w")

    append_csv(
        log_path,
        ["time_ms", "fps", "face_count", "best_score", "x", "y", "w", "h"],
        [now, "%.3f" % fps, count, "%.4f" % score, x, y, w, h]
    )


def load_anchors(path=DEFAULT_ANCHORS_PATH, anchor_len=DEFAULT_ANCHOR_LEN, det_dim=DEFAULT_DET_DIM):
    """Load face detection anchors from /sdcard/utils/prior_data_320.bin."""
    try:
        anchors = np.fromfile(path, dtype=np.float)
    except Exception:
        anchors = np.fromfile(path, dtype=np.float32)
    return anchors.reshape((anchor_len, det_dim))


class FaceDetectionApp(AIBase):
    """Single-model face detection app based on AIBase."""

    def __init__(self, kmodel_path, model_input_size, anchors,
                 confidence_threshold=0.5, nms_threshold=0.2,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.kmodel_path = kmodel_path
        self.model_input_size = model_input_size
        self.anchors = anchors
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.rgb888p_size = [align_up(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [align_up(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode

        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(
            nn.ai2d_format.NCHW_FMT,
            nn.ai2d_format.NCHW_FMT,
            np.uint8,
            np.uint8
        )

    def config_preprocess(self, input_image_size=None):
        """Configure AI2D preprocessing: resize camera RGBP888 to model input."""
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build(
                [1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                [1, 3, self.model_input_size[1], self.model_input_size[0]]
            )

    def postprocess(self, results):
        """Convert model outputs to face rectangles using the K230 aidemo library."""
        with ScopedTiming("postprocess", self.debug_mode > 0):
            post_ret = aidemo.face_det_post_process(
                self.confidence_threshold,
                self.nms_threshold,
                self.model_input_size[1],
                self.anchors,
                self.rgb888p_size,
                results
            )
            if len(post_ret) == 0:
                return post_ret
            return post_ret[0]

    def draw_result(self, pl, dets):
        """Draw face rectangles on the PipeLine OSD layer.

        det[:4] from aidemo.face_det_post_process is x, y, w, h.
        Keep rgb888p_size and display_size equal on the 640x480 LCD demo to avoid vertical offset.
        """
        with ScopedTiming("display_draw", self.debug_mode > 0):
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


def create_face_detection_app(pl, cfg=None):
    """Create and configure FaceDetectionApp from Pipeline and optional config."""
    if cfg is None:
        cfg = {}
    kmodel_path = cfg.get("KMODEL_PATH", DEFAULT_KMODEL_PATH)
    anchors_path = cfg.get("ANCHORS_PATH", DEFAULT_ANCHORS_PATH)
    confidence_threshold = parse_float(cfg.get("CONFIDENCE_THRESHOLD", "0.50"), 0.50)
    nms_threshold = parse_float(cfg.get("NMS_THRESHOLD", "0.20"), 0.20)
    debug_mode = parse_int(cfg.get("DEBUG_MODE", "0"), 0)

    anchors = load_anchors(anchors_path)
    app = FaceDetectionApp(
        kmodel_path,
        model_input_size=DEFAULT_MODEL_INPUT_SIZE,
        anchors=anchors,
        confidence_threshold=confidence_threshold,
        nms_threshold=nms_threshold,
        rgb888p_size=pl.rgb888p_size,
        display_size=pl.display_size,
        debug_mode=debug_mode
    )
    app.config_preprocess()
    return app


def safe_deinit(app):
    if app:
        try:
            app.deinit()
        except Exception as e:
            print("deinit error:", e)
    gc.collect()

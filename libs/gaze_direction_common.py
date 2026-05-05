# ============================================
# K230 GazeDirection common module
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Copy this file to /sdcard/libs/gaze_direction_common.py
# Demos import it as:
# from libs.gaze_direction_common import create_eye_gaze_app, safe_deinit
# ============================================

from libs.PipeLine import ScopedTiming
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import aidemo
import math
import gc

FACE_DET_KMODEL_PATH = "/sdcard/kmodel/face_detection_320.kmodel"
EYE_GAZE_KMODEL_PATH = "/sdcard/kmodel/eye_gaze.kmodel"
ANCHORS_PATH = "/sdcard/utils/prior_data_320.bin"
FACE_DET_INPUT_SIZE = [320, 320]
EYE_GAZE_INPUT_SIZE = [448, 448]
CONFIDENCE_THRESHOLD = 0.50
NMS_THRESHOLD = 0.20
ANCHOR_LEN = 4200
DET_DIM = 4


def align_up(value, align):
    return (value + align - 1) // align * align


def parse_float(value, default_value=0.0):
    try:
        return float(value)
    except Exception:
        return default_value


def load_anchors(path=ANCHORS_PATH):
    anchors = np.fromfile(path, dtype=np.float)
    return anchors.reshape((ANCHOR_LEN, DET_DIM))


class FaceDetApp(AIBase):
    """Face detection app: pad -> resize -> face_det_post_process."""

    def __init__(self, kmodel_path, model_input_size, anchors,
                 confidence_threshold=0.25, nms_threshold=0.3,
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
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT,
                                 nn.ai2d_format.NCHW_FMT,
                                 np.uint8,
                                 np.uint8)

    def get_pad_param(self):
        dst_w = self.model_input_size[0]
        dst_h = self.model_input_size[1]
        ratio_w = dst_w / self.rgb888p_size[0]
        ratio_h = dst_h / self.rgb888p_size[1]
        ratio = ratio_w if ratio_w < ratio_h else ratio_h
        new_w = int(ratio * self.rgb888p_size[0])
        new_h = int(ratio * self.rgb888p_size[1])
        dw = (dst_w - new_w) / 2
        dh = (dst_h - new_h) / 2
        top = int(round(0))
        bottom = int(round(dh * 2 + 0.1))
        left = int(round(0))
        right = int(round(dw * 2 - 0.1))
        return [0, 0, 0, 0, top, bottom, left, right]

    def config_preprocess(self, input_image_size=None):
        with ScopedTiming("face det preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build([1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                            [1, 3, self.model_input_size[1], self.model_input_size[0]])

    def postprocess(self, results):
        with ScopedTiming("face det postprocess", self.debug_mode > 0):
            res = aidemo.face_det_post_process(self.confidence_threshold,
                                               self.nms_threshold,
                                               self.model_input_size[0],
                                               self.anchors,
                                               self.rgb888p_size,
                                               results)
            if len(res) == 0:
                return res
            return res[0]


class EyeGazeApp(AIBase):
    """Eye gaze estimation app: crop face -> resize -> eye_gaze_post_process."""

    def __init__(self, kmodel_path, model_input_size,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.kmodel_path = kmodel_path
        self.model_input_size = model_input_size
        self.rgb888p_size = [align_up(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [align_up(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode
        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT,
                                 nn.ai2d_format.NCHW_FMT,
                                 np.uint8,
                                 np.uint8)

    def config_preprocess(self, det, input_image_size=None):
        with ScopedTiming("eye gaze preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            x, y, w, h = map(lambda v: int(round(v, 0)), det[:4])
            self.ai2d.crop(x, y, w, h)
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build([1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                            [1, 3, self.model_input_size[1], self.model_input_size[0]])

    def postprocess(self, results):
        with ScopedTiming("eye gaze postprocess", self.debug_mode > 0):
            post_ret = aidemo.eye_gaze_post_process(results)
            return post_ret[0], post_ret[1]


class EyeGaze:
    """Main task: Face Detection -> Eye Gaze Estimation -> arrow visualization."""

    def __init__(self, face_det_kmodel, eye_gaze_kmodel,
                 det_input_size, eye_gaze_input_size, anchors,
                 confidence_threshold=0.25, nms_threshold=0.3,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        self.face_det_kmodel = face_det_kmodel
        self.eye_gaze_kmodel = eye_gaze_kmodel
        self.det_input_size = det_input_size
        self.eye_gaze_input_size = eye_gaze_input_size
        self.anchors = anchors
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.rgb888p_size = [align_up(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [align_up(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode

        self.face_det = FaceDetApp(face_det_kmodel,
                                   model_input_size=det_input_size,
                                   anchors=anchors,
                                   confidence_threshold=confidence_threshold,
                                   nms_threshold=nms_threshold,
                                   rgb888p_size=self.rgb888p_size,
                                   display_size=self.display_size,
                                   debug_mode=debug_mode)
        self.eye_gaze = EyeGazeApp(eye_gaze_kmodel,
                                   model_input_size=eye_gaze_input_size,
                                   rgb888p_size=self.rgb888p_size,
                                   display_size=self.display_size,
                                   debug_mode=debug_mode)
        self.face_det.config_preprocess()

    def run(self, input_np):
        det_boxes = self.face_det.run(input_np)
        eye_gaze_res = []
        for det_box in det_boxes:
            self.eye_gaze.config_preprocess(det_box)
            pitch, yaw = self.eye_gaze.run(input_np)
            eye_gaze_res.append((pitch, yaw))
        return det_boxes, eye_gaze_res

    def get_arrow_points(self, det, gaze_ret):
        pitch, yaw = gaze_ret
        length = self.display_size[0] / 2
        x, y, w, h = map(lambda v: int(round(v, 0)), det[:4])
        x = x * self.display_size[0] // self.rgb888p_size[0]
        y = y * self.display_size[1] // self.rgb888p_size[1]
        w = w * self.display_size[0] // self.rgb888p_size[0]
        h = h * self.display_size[1] // self.rgb888p_size[1]
        center_x = x + w / 2.0
        center_y = y + h / 2.0
        dx = -length * math.sin(pitch) * math.cos(yaw)
        dy = -length * math.sin(yaw)
        target_x = int(center_x + dx)
        target_y = int(center_y + dy)
        return int(center_x), int(center_y), target_x, target_y, pitch, yaw

    def draw_result(self, pl, dets, eye_gaze_res, send_uart=False, uart=None, pto=None):
        """Draw gaze arrows and optionally send $x0,y0,x1,y1# through UART.

        Returns a list of tuples:
        (center_x, center_y, target_x, target_y, pitch, yaw)
        """
        arrows = []
        pl.osd_img.clear()
        if dets:
            for det, gaze_ret in zip(dets, eye_gaze_res):
                cx, cy, tx, ty, pitch, yaw = self.get_arrow_points(det, gaze_ret)
                pl.osd_img.draw_arrow(cx, cy, tx, ty,
                                      color=(255, 255, 0, 0),
                                      size=30,
                                      thickness=4)
                arrows.append((cx, cy, tx, ty, pitch, yaw))
                if send_uart:
                    send_eye_gaze_uart(cx, cy, tx, ty, uart, pto)
        return arrows

    def deinit(self):
        try:
            self.face_det.deinit()
        except Exception as e:
            print("face_det deinit error:", e)
        try:
            self.eye_gaze.deinit()
        except Exception as e:
            print("eye_gaze deinit error:", e)
        gc.collect()


def create_eye_gaze_app(pl, cfg=None):
    if cfg is None:
        cfg = {}
    face_det_model = cfg.get("FACE_DET_KMODEL_PATH", FACE_DET_KMODEL_PATH)
    eye_gaze_model = cfg.get("EYE_GAZE_KMODEL_PATH", EYE_GAZE_KMODEL_PATH)
    anchors_path = cfg.get("ANCHORS_PATH", ANCHORS_PATH)
    confidence = parse_float(cfg.get("CONFIDENCE_THRESHOLD", CONFIDENCE_THRESHOLD), CONFIDENCE_THRESHOLD)
    nms = parse_float(cfg.get("NMS_THRESHOLD", NMS_THRESHOLD), NMS_THRESHOLD)
    anchors = load_anchors(anchors_path)
    return EyeGaze(face_det_model,
                   eye_gaze_model,
                   det_input_size=FACE_DET_INPUT_SIZE,
                   eye_gaze_input_size=EYE_GAZE_INPUT_SIZE,
                   anchors=anchors,
                   confidence_threshold=confidence,
                   nms_threshold=nms,
                   rgb888p_size=pl.rgb888p_size,
                   display_size=pl.display_size,
                   debug_mode=0)


def init_uart():
    """Initialize Yahboom UART protocol if available. Returns (uart, pto)."""
    try:
        from libs.YbProtocol import YbProtocol
        from ybUtils.YbUart import YbUart
        uart = YbUart(baudrate=115200)
        pto = YbProtocol()
        print("UART ready")
        return uart, pto
    except Exception as e:
        print("UART unavailable:", e)
        return None, None


def send_eye_gaze_uart(x0, y0, x1, y1, uart=None, pto=None):
    """Send gaze arrow through UART. Text fallback format: $x0,y0,x1,y1#."""
    packet_text = "$%d,%d,%d,%d#" % (x0, y0, x1, y1)
    print(packet_text)
    if uart:
        try:
            if pto:
                uart.send(pto.get_eye_gaze_data(x0, y0, x1, y1))
            else:
                uart.send(packet_text)
        except Exception as e:
            print("UART send error:", e)


def safe_deinit(app):
    if app:
        try:
            app.deinit()
        except Exception as e:
            print("deinit error:", e)
    gc.collect()

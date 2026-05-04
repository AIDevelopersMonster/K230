# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / FaceDetectition
# 02_face_detection_uart.py
#
# Face detection demo with UART output.
# The serial packet format is: $x,y,w,h#
# x, y, w, h are the face rectangle coordinates in 640x480 display space.
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

try:
    from libs.YbProtocol import YbProtocol
    from ybUtils.YbUart import YbUart
except Exception:
    YbProtocol = None
    YbUart = None

KMODEL_PATH = "/sdcard/kmodel/face_detection_320.kmodel"
ANCHORS_PATH = "/sdcard/utils/prior_data_320.bin"
MODEL_INPUT_SIZE = [320, 320]
CONFIDENCE_THRESHOLD = 0.50
NMS_THRESHOLD = 0.20
ANCHOR_LEN = 4200
DET_DIM = 4

face_det = None
uart = None
pto = None


def align_up(value, align):
    return (value + align - 1) // align * align


def load_anchors(path=ANCHORS_PATH):
    anchors = np.fromfile(path, dtype=np.float)
    return anchors.reshape((ANCHOR_LEN, DET_DIM))


def send_face_packet(x, y, w, h):
    """Send face rectangle through UART. Falls back to text packet if protocol is unavailable."""
    global uart, pto
    packet_text = "$%d,%d,%d,%d#" % (x, y, w, h)
    print(packet_text)
    if uart:
        try:
            if pto:
                uart.send(pto.get_face_detect_data(x, y, w, h))
            else:
                uart.send(packet_text)
        except Exception as e:
            print("UART send error:", e)


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
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            top, bottom, left, right = self.get_padding_param()
            self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build([1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                            [1, 3, self.model_input_size[1], self.model_input_size[0]])

    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            post_ret = aidemo.face_det_post_process(
                self.confidence_threshold, self.nms_threshold, self.model_input_size[1],
                self.anchors, self.rgb888p_size, results)
            return post_ret[0] if post_ret else post_ret

    def draw_result(self, pl, dets):
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
                    send_face_packet(x, y, w, h)
            else:
                pl.osd_img.clear()


def init_uart():
    global uart, pto
    if YbUart:
        try:
            uart = YbUart(baudrate=115200)
            pto = YbProtocol() if YbProtocol else None
            print("UART ready")
        except Exception as e:
            uart = None
            pto = None
            print("UART unavailable:", e)


def create_app(pl):
    anchors = load_anchors(ANCHORS_PATH)
    app = FaceDetectionApp(KMODEL_PATH, MODEL_INPUT_SIZE, anchors,
                           CONFIDENCE_THRESHOLD, NMS_THRESHOLD,
                           rgb888p_size=pl.rgb888p_size,
                           display_size=pl.display_size,
                           debug_mode=0)
    app.config_preprocess()
    return app


def exce_demo(pl):
    global face_det
    init_uart()
    try:
        face_det = create_app(pl)
        while True:
            with ScopedTiming("total", 0):
                img = pl.get_frame()
                res = face_det.run(img)
                face_det.draw_result(pl, res)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face detection UART demo exit:", e)
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

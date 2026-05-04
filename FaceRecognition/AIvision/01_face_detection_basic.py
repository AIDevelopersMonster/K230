# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / AIvision
# 01_face_detection_basic.py
#
# Standalone demo: this file does not import local helper modules.
# Copy only this file to the K230 and run it in CanMV IDE.
#
# What it demonstrates:
# - creates one PipeLine instance;
# - loads face_detection_320.kmodel and anchors;
# - configures AI2D preprocessing;
# - runs inference in a loop;
# - draws face rectangles on the OSD layer.
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

KMODEL_PATH = "/sdcard/kmodel/face_detection_320.kmodel"
ANCHORS_PATH = "/sdcard/utils/prior_data_320.bin"
MODEL_INPUT_SIZE = [320, 320]
CONFIDENCE_THRESHOLD = 0.50
NMS_THRESHOLD = 0.20
ANCHOR_LEN = 4200
DET_DIM = 4

face_det = None


def align_up(value, align):
    return (value + align - 1) // align * align


def load_anchors(path=ANCHORS_PATH):
    """Load anchors used by the face detection postprocess function."""
    try:
        anchors = np.fromfile(path, dtype=np.float)
    except Exception:
        anchors = np.fromfile(path, dtype=np.float32)
    return anchors.reshape((ANCHOR_LEN, DET_DIM))


class FaceDetectionApp(AIBase):
    """AIBase-based face detection app."""

    def __init__(self, kmodel_path, model_input_size, anchors,
                 confidence_threshold=0.5, nms_threshold=0.2,
                 rgb888p_size=[640, 360], display_size=[640, 480], debug_mode=0):
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
        """Configure resize preprocessing for the model."""
        with ScopedTiming("set preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build(
                [1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                [1, 3, self.model_input_size[1], self.model_input_size[0]]
            )

    def postprocess(self, results):
        """Convert model outputs to face rectangles."""
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
        """Draw face rectangles on the OSD layer."""
        with ScopedTiming("display_draw", self.debug_mode > 0):
            pl.osd_img.clear()
            if not dets:
                return
            for det in dets:
                x, y, w, h = map(lambda v: int(round(v, 0)), det[:4])
                score = 0.0
                try:
                    if len(det) > 4:
                        score = float(det[4])
                except Exception:
                    score = 0.0

                x = x * self.display_size[0] // self.rgb888p_size[0]
                y = y * self.display_size[1] // self.rgb888p_size[1]
                w = w * self.display_size[0] // self.rgb888p_size[0]
                h = h * self.display_size[1] // self.rgb888p_size[1]

                pl.osd_img.draw_rectangle(x, y, w, h, color=(255, 255, 0, 255), thickness=2)
                try:
                    pl.osd_img.draw_string_advanced(x, max(0, y - 28), 24,
                                                    "Face %.2f" % score,
                                                    color=(255, 255, 255, 255))
                except Exception:
                    pass


def create_face_detection_app(pl):
    anchors = load_anchors(ANCHORS_PATH)
    app = FaceDetectionApp(
        KMODEL_PATH,
        model_input_size=MODEL_INPUT_SIZE,
        anchors=anchors,
        confidence_threshold=CONFIDENCE_THRESHOLD,
        nms_threshold=NMS_THRESHOLD,
        rgb888p_size=pl.rgb888p_size,
        display_size=pl.display_size,
        debug_mode=0
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


def exce_demo(pl):
    """Execute the current AI routine using an existing PipeLine instance."""
    global face_det
    try:
        face_det = create_face_detection_app(pl)

        while True:
            with ScopedTiming("total", 0):
                img = pl.get_frame()
                dets = face_det.run(img)
                face_det.draw_result(pl, dets)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)

    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face detection demo exit:", e)
    finally:
        safe_deinit(face_det)
        face_det = None


def exit_demo():
    """Release the current AI routine instance."""
    global face_det
    safe_deinit(face_det)
    face_det = None


if __name__ == "__main__":
    rgb888p_size = [640, 360]
    display_size = [640, 480]
    display_mode = "lcd"

    pl = PipeLine(rgb888p_size=rgb888p_size, display_size=display_size, display_mode=display_mode)
    try:
        pl.create()
        exce_demo(pl)
    finally:
        exit_demo()
        try:
            pl.destroy()
        except Exception:
            pass

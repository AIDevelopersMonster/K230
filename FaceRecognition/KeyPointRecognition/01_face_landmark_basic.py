# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / KeyPointRecognition
# 01_face_landmark_basic.py
#
# Standalone facial key point recognition demo.
# It follows the Yahboom Face Landmark example structure:
# FaceDetApp -> FaceLandMarkApp -> FaceLandMark -> draw on OSD.
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from media.media import *
from time import *
import nncase_runtime as nn
import ulab.numpy as np
import time
import image
import aidemo
import gc

flm = None

FACE_DET_KMODEL_PATH = "/sdcard/kmodel/face_detection_320.kmodel"
FACE_LANDMARK_KMODEL_PATH = "/sdcard/kmodel/face_landmark.kmodel"
ANCHORS_PATH = "/sdcard/utils/prior_data_320.bin"
FACE_DET_INPUT_SIZE = [320, 320]
FACE_LANDMARK_INPUT_SIZE = [192, 192]
CONFIDENCE_THRESHOLD = 0.50
NMS_THRESHOLD = 0.20
ANCHOR_LEN = 4200
DET_DIM = 4


def align_up(value, align):
    return (value + align - 1) // align * align


def load_anchors(path=ANCHORS_PATH):
    anchors = np.fromfile(path, dtype=np.float)
    return anchors.reshape((ANCHOR_LEN, DET_DIM))


class FaceDetApp(AIBase):
    """Face detection application class."""

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
        self.ai2d.set_ai2d_dtype(
            nn.ai2d_format.NCHW_FMT,
            nn.ai2d_format.NCHW_FMT,
            np.uint8,
            np.uint8
        )

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
            self.ai2d.build(
                [1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                [1, 3, self.model_input_size[1], self.model_input_size[0]]
            )

    def postprocess(self, results):
        with ScopedTiming("face det postprocess", self.debug_mode > 0):
            res = aidemo.face_det_post_process(
                self.confidence_threshold,
                self.nms_threshold,
                self.model_input_size[0],
                self.anchors,
                self.rgb888p_size,
                results
            )
            if len(res) == 0:
                return res
            return res[0]


class FaceLandMarkApp(AIBase):
    """Facial landmark detection application class."""

    def __init__(self, kmodel_path, model_input_size,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.kmodel_path = kmodel_path
        self.model_input_size = model_input_size
        self.rgb888p_size = [align_up(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [align_up(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode
        self.matrix_dst = None

        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(
            nn.ai2d_format.NCHW_FMT,
            nn.ai2d_format.NCHW_FMT,
            np.uint8,
            np.uint8
        )

    def get_affine_matrix(self, bbox):
        with ScopedTiming("get affine matrix", self.debug_mode > 1):
            x1, y1, w, h = map(lambda x: int(round(x, 0)), bbox[:4])
            scale_ratio = self.model_input_size[0] / (max(w, h) * 1.5)
            cx = (x1 + w / 2) * scale_ratio
            cy = (y1 + h / 2) * scale_ratio
            half_input_len = self.model_input_size[0] / 2

            matrix_dst = np.zeros((2, 3), dtype=np.float)
            matrix_dst[0, 0] = scale_ratio
            matrix_dst[0, 1] = 0
            matrix_dst[0, 2] = half_input_len - cx
            matrix_dst[1, 0] = 0
            matrix_dst[1, 1] = scale_ratio
            matrix_dst[1, 2] = half_input_len - cy
            return matrix_dst

    def config_preprocess(self, det, input_image_size=None):
        with ScopedTiming("landmark preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            self.matrix_dst = self.get_affine_matrix(det)
            affine_matrix = [
                self.matrix_dst[0][0], self.matrix_dst[0][1], self.matrix_dst[0][2],
                self.matrix_dst[1][0], self.matrix_dst[1][1], self.matrix_dst[1][2]
            ]
            self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, affine_matrix)
            self.ai2d.build(
                [1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                [1, 3, self.model_input_size[1], self.model_input_size[0]]
            )

    def postprocess(self, results):
        with ScopedTiming("landmark postprocess", self.debug_mode > 0):
            pred = results[0]
            half_input_len = self.model_input_size[0] // 2
            pred = pred.flatten()

            for i in range(len(pred)):
                pred[i] += (pred[i] + 1) * half_input_len

            matrix_dst_inv = aidemo.invert_affine_transform(self.matrix_dst)
            matrix_dst_inv = matrix_dst_inv.flatten()

            half_out_len = len(pred) // 2
            for kp_id in range(half_out_len):
                old_x = pred[kp_id * 2]
                old_y = pred[kp_id * 2 + 1]
                new_x = old_x * matrix_dst_inv[0] + old_y * matrix_dst_inv[1] + matrix_dst_inv[2]
                new_y = old_x * matrix_dst_inv[3] + old_y * matrix_dst_inv[4] + matrix_dst_inv[5]
                pred[kp_id * 2] = new_x
                pred[kp_id * 2 + 1] = new_y
            return pred


class FaceLandMark:
    """Main facial landmark detection class."""

    def __init__(self, face_det_kmodel, face_landmark_kmodel,
                 det_input_size, landmark_input_size, anchors,
                 confidence_threshold=0.25, nms_threshold=0.3,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        self.face_det_kmodel = face_det_kmodel
        self.face_landmark_kmodel = face_landmark_kmodel
        self.det_input_size = det_input_size
        self.landmark_input_size = landmark_input_size
        self.anchors = anchors
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.rgb888p_size = [align_up(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [align_up(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode

        # 106-point landmark groups: eyebrows, eyes, pupils, nose, lips, face contour.
        self.dict_kp_seq = [
            [43, 44, 45, 47, 46, 50, 51, 49, 48],
            [97, 98, 99, 100, 101, 105, 104, 103, 102],
            [35, 36, 33, 37, 39, 42, 40, 41],
            [89, 90, 87, 91, 93, 96, 94, 95],
            [34, 88],
            [72, 73, 74, 86],
            [77, 78, 79, 80, 85, 84, 83],
            [52, 55, 56, 53, 59, 58, 61, 68, 67, 71, 63, 64],
            [65, 54, 60, 57, 69, 70, 62, 66],
            [1, 9, 10, 11, 12, 13, 14, 15, 16, 2, 3, 4, 5, 6, 7, 8, 0,
             24, 23, 22, 21, 20, 19, 18, 32, 31, 30, 29, 28, 27, 26, 25, 17]
        ]

        self.color_list_for_osd_kp = [
            (255, 0, 255, 0),
            (255, 0, 255, 0),
            (255, 255, 0, 255),
            (255, 255, 0, 255),
            (255, 255, 0, 0),
            (255, 255, 170, 0),
            (255, 255, 255, 0),
            (255, 0, 255, 255),
            (255, 255, 220, 50),
            (255, 30, 30, 255)
        ]

        self.face_det = FaceDetApp(
            self.face_det_kmodel,
            model_input_size=self.det_input_size,
            anchors=self.anchors,
            confidence_threshold=self.confidence_threshold,
            nms_threshold=self.nms_threshold,
            rgb888p_size=self.rgb888p_size,
            display_size=self.display_size,
            debug_mode=self.debug_mode
        )
        self.face_landmark = FaceLandMarkApp(
            self.face_landmark_kmodel,
            model_input_size=self.landmark_input_size,
            rgb888p_size=self.rgb888p_size,
            display_size=self.display_size,
            debug_mode=self.debug_mode
        )
        self.face_det.config_preprocess()

    def run(self, input_np):
        det_boxes = self.face_det.run(input_np)
        landmark_res = []
        for det_box in det_boxes:
            self.face_landmark.config_preprocess(det_box)
            res = self.face_landmark.run(input_np)
            landmark_res.append(res)
        return det_boxes, landmark_res

    def draw_result(self, pl, dets, landmark_res):
        pl.osd_img.clear()
        if dets:
            draw_img_np = np.zeros((self.display_size[1], self.display_size[0], 4), dtype=np.uint8)
            draw_img = image.Image(
                self.display_size[0],
                self.display_size[1],
                image.ARGB8888,
                alloc=image.ALLOC_REF,
                data=draw_img_np
            )

            for pred in landmark_res:
                for sub_part_index in range(len(self.dict_kp_seq)):
                    sub_part = self.dict_kp_seq[sub_part_index]
                    point_set = []
                    for kp_index in range(len(sub_part)):
                        real_kp_index = sub_part[kp_index]
                        x, y = pred[real_kp_index * 2], pred[real_kp_index * 2 + 1]
                        x = int(x * self.display_size[0] // self.rgb888p_size[0])
                        y = int(y * self.display_size[1] // self.rgb888p_size[1])
                        point_set.append((x, y))

                    if sub_part_index in (9, 6):
                        color = np.array(self.color_list_for_osd_kp[sub_part_index], dtype=np.uint8)
                        aidemo.polylines(draw_img_np, np.array(point_set), False, color, 5, 8, 0)
                    elif sub_part_index == 4:
                        color = self.color_list_for_osd_kp[sub_part_index]
                        for kp in point_set:
                            draw_img.draw_circle(kp[0], kp[1], 2, color, 1)
                    else:
                        color = np.array(self.color_list_for_osd_kp[sub_part_index], dtype=np.uint8)
                        aidemo.contours(draw_img_np, np.array(point_set), -1, color, 2, 8)

            pl.osd_img.copy_from(draw_img)

    def deinit(self):
        try:
            self.face_det.deinit()
        except Exception as e:
            print("face_det deinit error:", e)
        try:
            self.face_landmark.deinit()
        except Exception as e:
            print("face_landmark deinit error:", e)


def create_landmark_app(pl):
    anchors = load_anchors(ANCHORS_PATH)
    return FaceLandMark(
        FACE_DET_KMODEL_PATH,
        FACE_LANDMARK_KMODEL_PATH,
        det_input_size=FACE_DET_INPUT_SIZE,
        landmark_input_size=FACE_LANDMARK_INPUT_SIZE,
        anchors=anchors,
        confidence_threshold=CONFIDENCE_THRESHOLD,
        nms_threshold=NMS_THRESHOLD,
        rgb888p_size=pl.rgb888p_size,
        display_size=pl.display_size,
        debug_mode=0
    )


def exce_demo(pl):
    global flm
    try:
        flm = create_landmark_app(pl)
        while True:
            with ScopedTiming("total", 0):
                img = pl.get_frame()
                det_boxes, landmark_res = flm.run(img)
                flm.draw_result(pl, det_boxes, landmark_res)
                pl.show_image()
                gc.collect()
                time.sleep_us(10)
    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face landmark demo exit:", e)
    finally:
        exit_demo()


def exit_demo():
    global flm
    if flm:
        flm.deinit()
        flm = None
    gc.collect()


if __name__ == "__main__":
    rgb888p_size = [640, 480]
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

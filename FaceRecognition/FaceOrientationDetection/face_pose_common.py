# ============================================
# K230 FaceRecognition / FaceOrientationDetection common module
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Copy this file together with the demos to:
# /sdcard/FaceRecognition/FaceOrientationDetection/face_pose_common.py
# ============================================

from libs.PipeLine import ScopedTiming
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo
import gc

FACE_DET_KMODEL_PATH = "/sdcard/kmodel/face_detection_320.kmodel"
FACE_POSE_KMODEL_PATH = "/sdcard/kmodel/face_pose.kmodel"
ANCHORS_PATH = "/sdcard/utils/prior_data_320.bin"
FACE_DET_INPUT_SIZE = [320, 320]
FACE_POSE_INPUT_SIZE = [120, 120]
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


class FacePoseApp(AIBase):
    """Face orientation app. It outputs rotation matrix and Euler angles."""

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

    def get_affine_matrix(self, bbox):
        with ScopedTiming("get affine matrix", self.debug_mode > 1):
            factor = 2.7
            x1, y1, w, h = map(lambda x: int(round(x, 0)), bbox[:4])
            edge_size = self.model_input_size[1]
            trans_distance = edge_size / 2.0
            center_x = x1 + w / 2.0
            center_y = y1 + h / 2.0
            maximum_edge = factor * (h if h > w else w)
            scale = edge_size * 2.0 / maximum_edge
            cx = trans_distance - scale * center_x
            cy = trans_distance - scale * center_y
            return [scale, 0, cx, 0, scale, cy]

    def config_preprocess(self, det, input_image_size=None):
        with ScopedTiming("pose preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            matrix_dst = self.get_affine_matrix(det)
            self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, matrix_dst)
            self.ai2d.build([1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                            [1, 3, self.model_input_size[1], self.model_input_size[0]])

    def rotation_matrix_to_euler_angles(self, R):
        sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
        if sy < 1e-6:
            pitch = np.arctan2(-R[1, 2], R[1, 1]) * 180 / np.pi
            yaw = np.arctan2(-R[2, 0], sy) * 180 / np.pi
            roll = 0
        else:
            pitch = np.arctan2(R[2, 1], R[2, 2]) * 180 / np.pi
            yaw = np.arctan2(-R[2, 0], sy) * 180 / np.pi
            roll = np.arctan2(R[1, 0], R[0, 0]) * 180 / np.pi
        return [pitch, yaw, roll]

    def get_euler(self, data):
        R = data[:3, :3].copy()
        eular = self.rotation_matrix_to_euler_angles(R)
        return R, eular

    def postprocess(self, results):
        with ScopedTiming("pose postprocess", self.debug_mode > 0):
            R, eular = self.get_euler(results[0][0])
            return R, eular


class FacePose:
    """Main task: Face Detection -> Face Pose -> 3D cube visualization."""

    def __init__(self, face_det_kmodel, face_pose_kmodel,
                 det_input_size, pose_input_size, anchors,
                 confidence_threshold=0.25, nms_threshold=0.3,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        self.face_det_kmodel = face_det_kmodel
        self.face_pose_kmodel = face_pose_kmodel
        self.det_input_size = det_input_size
        self.pose_input_size = pose_input_size
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
        self.face_pose = FacePoseApp(face_pose_kmodel,
                                     model_input_size=pose_input_size,
                                     rgb888p_size=self.rgb888p_size,
                                     display_size=self.display_size,
                                     debug_mode=debug_mode)
        self.face_det.config_preprocess()

    def run(self, input_np):
        det_boxes = self.face_det.run(input_np)
        pose_res = []
        for det_box in det_boxes:
            self.face_pose.config_preprocess(det_box)
            R, eular = self.face_pose.run(input_np)
            pose_res.append((R, eular))
        return det_boxes, pose_res

    def build_projection_matrix(self, det):
        x1, y1, w, h = map(lambda x: int(round(x, 0)), det[:4])
        center_x = x1 + w / 2.0
        center_y = y1 + h / 2.0
        rear_width = 0.5 * w
        rear_height = 0.5 * h
        rear_depth = 0
        factor = np.sqrt(2.0)
        front_width = factor * rear_width
        front_height = factor * rear_height
        front_depth = factor * rear_width
        temp = [
            [-rear_width, -rear_height, rear_depth],
            [-rear_width, rear_height, rear_depth],
            [rear_width, rear_height, rear_depth],
            [rear_width, -rear_height, rear_depth],
            [-front_width, -front_height, front_depth],
            [-front_width, front_height, front_depth],
            [front_width, front_height, front_depth],
            [front_width, -front_height, front_depth]
        ]
        return np.array(temp), (center_x, center_y)

    def draw_result(self, pl, dets, pose_res, draw_angles=False):
        pl.osd_img.clear()
        if dets:
            draw_img_np = np.zeros((self.display_size[1], self.display_size[0], 4), dtype=np.uint8)
            draw_img = image.Image(self.display_size[0], self.display_size[1], image.ARGB8888,
                                   alloc=image.ALLOC_REF, data=draw_img_np)
            line_color = np.array([255, 0, 0, 255], dtype=np.uint8)
            for i, det in enumerate(dets):
                projections, center_point = self.build_projection_matrix(det)
                R, euler = pose_res[i]
                first_points = []
                second_points = []
                for pp in range(8):
                    sum_x, sum_y = 0.0, 0.0
                    for cc in range(3):
                        sum_x += projections[pp][cc] * R[cc][0]
                        sum_y += projections[pp][cc] * (-R[cc][1])
                    x = (sum_x + center_point[0]) / self.rgb888p_size[0] * self.display_size[0]
                    y = (sum_y + center_point[1]) / self.rgb888p_size[1] * self.display_size[1]
                    x = max(0, min(x, self.display_size[0]))
                    y = max(0, min(y, self.display_size[1]))
                    if pp < 4:
                        first_points.append((x, y))
                    else:
                        second_points.append((x, y))
                first_points = np.array(first_points, dtype=np.float)
                second_points = np.array(second_points, dtype=np.float)
                aidemo.polylines(draw_img_np, first_points, True, line_color, 2, 8, 0)
                aidemo.polylines(draw_img_np, second_points, True, line_color, 2, 8, 0)
                for ll in range(4):
                    x0, y0 = int(first_points[ll][0]), int(first_points[ll][1])
                    x1, y1 = int(second_points[ll][0]), int(second_points[ll][1])
                    draw_img.draw_line(x0, y0, x1, y1, color=(255, 0, 0, 255), thickness=2)
                if draw_angles:
                    x_text = int(center_point[0] * self.display_size[0] // self.rgb888p_size[0])
                    y_text = int(center_point[1] * self.display_size[1] // self.rgb888p_size[1])
                    try:
                        draw_img.draw_string_advanced(max(0, x_text - 90), max(0, y_text - 90), 20,
                                                      "P %.1f Y %.1f R %.1f" % (euler[0], euler[1], euler[2]),
                                                      color=(255, 255, 255, 255))
                    except Exception:
                        pass
            pl.osd_img.copy_from(draw_img)

    def deinit(self):
        try:
            self.face_det.deinit()
        except Exception as e:
            print("face_det deinit error:", e)
        try:
            self.face_pose.deinit()
        except Exception as e:
            print("face_pose deinit error:", e)
        gc.collect()


def create_pose_app(pl, cfg=None):
    if cfg is None:
        cfg = {}
    det_model = cfg.get("FACE_DET_KMODEL_PATH", FACE_DET_KMODEL_PATH)
    pose_model = cfg.get("FACE_POSE_KMODEL_PATH", FACE_POSE_KMODEL_PATH)
    anchors_path = cfg.get("ANCHORS_PATH", ANCHORS_PATH)
    confidence = float(cfg.get("CONFIDENCE_THRESHOLD", CONFIDENCE_THRESHOLD))
    nms = float(cfg.get("NMS_THRESHOLD", NMS_THRESHOLD))
    anchors = load_anchors(anchors_path)
    return FacePose(det_model,
                    pose_model,
                    det_input_size=FACE_DET_INPUT_SIZE,
                    pose_input_size=FACE_POSE_INPUT_SIZE,
                    anchors=anchors,
                    confidence_threshold=confidence,
                    nms_threshold=nms,
                    rgb888p_size=pl.rgb888p_size,
                    display_size=pl.display_size,
                    debug_mode=0)

# ============================================
# K230 RegisterFace common module
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# Copy this file to /sdcard/libs/register_face_common.py
# Demos import it as:
# from libs.register_face_common import ...
# ============================================

from libs.PipeLine import ScopedTiming
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from media.media import *
import nncase_runtime as nn
import ulab.numpy as np
import image
import aidemo
import os
import math
import re
import gc

FACE_DET_KMODEL_PATH = "/sdcard/kmodel/face_detection_320.kmodel"
FACE_RECOGNITION_KMODEL_PATH = "/sdcard/kmodel/face_recognition.kmodel"
ANCHORS_PATH = "/sdcard/utils/prior_data_320.bin"
DEFAULT_PHOTO_DIR = "/data/photo/register/"
DEFAULT_DATABASE_ROOT = "/data/face_database/"
DEFAULT_DATABASE_DIR = "/data/face_database/register/"
FACE_DET_INPUT_SIZE = [320, 320]
FACE_REG_INPUT_SIZE = [112, 112]
CONFIDENCE_THRESHOLD = 0.50
NMS_THRESHOLD = 0.20
FACE_RECOGNITION_THRESHOLD = 0.65
ANCHOR_LEN = 4200
DET_DIM = 4


def align_up(value, align):
    return (value + align - 1) // align * align


def parse_float(value, default_value=0.0):
    try:
        return float(value)
    except Exception:
        return default_value


def parse_int(value, default_value=0):
    try:
        return int(value)
    except Exception:
        return default_value


def split_path(path):
    return [item for item in path.split("/") if item]


def ensure_dir(directory):
    """Recursively create a directory on the K230 filesystem."""
    if not directory or directory == "/":
        return True
    directory = directory.rstrip("/")
    current = "/" if directory.startswith("/") else ""
    for part in split_path(directory):
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
                print("Created directory:", current)
            except Exception as e:
                try:
                    os.stat(current)
                except Exception:
                    print("Cannot create directory", current, e)
                    return False
    return True


def file_exists(path):
    try:
        os.stat(path)
        return True
    except Exception:
        return False


def get_directory_name(path):
    parts = path.rstrip("/").split("/")
    for part in reversed(parts):
        if part:
            return part
    return "register"


def join_path(folder, name):
    if folder.endswith("/"):
        return folder + name
    return folder + "/" + name


def is_image_file(name):
    lower = name.lower()
    return lower.endswith(".jpg") or lower.endswith(".jpeg") or lower.endswith(".png") or lower.endswith(".bmp")


def remove_extension(name):
    if "." in name:
        return name.rsplit(".", 1)[0]
    return name


def load_anchors(path=ANCHORS_PATH):
    anchors = np.fromfile(path, dtype=np.float)
    return anchors.reshape((ANCHOR_LEN, DET_DIM))


class FaceDetApp(AIBase):
    """Face detection app that returns face boxes and 5-point landmarks."""

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
        self.image_size = self.rgb888p_size
        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT,
                                 nn.ai2d_format.NCHW_FMT,
                                 np.uint8,
                                 np.uint8)

    def get_pad_param(self, image_input_size=None):
        if image_input_size is None:
            image_input_size = self.rgb888p_size
        dst_w = self.model_input_size[0]
        dst_h = self.model_input_size[1]
        ratio_w = dst_w / image_input_size[0]
        ratio_h = dst_h / image_input_size[1]
        ratio = ratio_w if ratio_w < ratio_h else ratio_h
        new_w = int(ratio * image_input_size[0])
        new_h = int(ratio * image_input_size[1])
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
            if input_image_size:
                # The registration example from Yahboom passes image size as [height, width].
                self.image_size = [input_image_size[1], input_image_size[0]]
            else:
                self.image_size = self.rgb888p_size
            self.ai2d.pad(self.get_pad_param(ai2d_input_size), 0, [104, 117, 123])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build([1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                            [1, 3, self.model_input_size[1], self.model_input_size[0]])

    def postprocess(self, results):
        with ScopedTiming("face det postprocess", self.debug_mode > 0):
            res = aidemo.face_det_post_process(self.confidence_threshold,
                                               self.nms_threshold,
                                               self.model_input_size[0],
                                               self.anchors,
                                               self.image_size,
                                               results)
            if len(res) == 0:
                return res, res
            return res[0], res[1]


class FaceRegistrationApp(AIBase):
    """Face feature extraction app. It aligns a face with 5 landmarks and outputs a feature vector."""

    def __init__(self, kmodel_path, model_input_size,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        super().__init__(kmodel_path, model_input_size, rgb888p_size, debug_mode)
        self.kmodel_path = kmodel_path
        self.model_input_size = model_input_size
        self.rgb888p_size = [align_up(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [align_up(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode
        self.umeyama_args_112 = [
            38.2946, 51.6963,
            73.5318, 51.5014,
            56.0252, 71.7366,
            41.5493, 92.3655,
            70.7299, 92.2041
        ]
        self.ai2d = Ai2d(debug_mode)
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT,
                                 nn.ai2d_format.NCHW_FMT,
                                 np.uint8,
                                 np.uint8)

    def config_preprocess(self, landm, input_image_size=None):
        with ScopedTiming("face reg preprocess config", self.debug_mode > 0):
            ai2d_input_size = input_image_size if input_image_size else self.rgb888p_size
            affine_matrix = self.get_affine_matrix(landm)
            self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, affine_matrix)
            self.ai2d.build([1, 3, ai2d_input_size[1], ai2d_input_size[0]],
                            [1, 3, self.model_input_size[1], self.model_input_size[0]])

    def postprocess(self, results):
        with ScopedTiming("face reg postprocess", self.debug_mode > 0):
            return results[0][0]

    def svd22(self, a):
        s = [0.0, 0.0]
        u = [0.0, 0.0, 0.0, 0.0]
        v = [0.0, 0.0, 0.0, 0.0]
        s[0] = (math.sqrt((a[0] - a[3]) ** 2 + (a[1] + a[2]) ** 2) +
                math.sqrt((a[0] + a[3]) ** 2 + (a[1] - a[2]) ** 2)) / 2
        s[1] = abs(s[0] - math.sqrt((a[0] - a[3]) ** 2 + (a[1] + a[2]) ** 2))
        v[2] = math.sin((math.atan2(2 * (a[0] * a[1] + a[2] * a[3]),
                                   a[0] ** 2 - a[1] ** 2 + a[2] ** 2 - a[3] ** 2)) / 2) if s[0] > s[1] else 0
        v[0] = math.sqrt(1 - v[2] ** 2)
        v[1] = -v[2]
        v[3] = v[0]
        u[0] = -(a[0] * v[0] + a[1] * v[2]) / s[0] if s[0] != 0 else 1
        u[2] = -(a[2] * v[0] + a[3] * v[2]) / s[0] if s[0] != 0 else 0
        u[1] = (a[0] * v[1] + a[1] * v[3]) / s[1] if s[1] != 0 else -u[2]
        u[3] = (a[2] * v[1] + a[3] * v[3]) / s[1] if s[1] != 0 else u[0]
        v[0] = -v[0]
        v[2] = -v[2]
        return u, s, v

    def image_umeyama_112(self, src):
        src_num = 5
        src_dim = 2
        src_mean = [0.0, 0.0]
        dst_mean = [0.0, 0.0]
        for i in range(0, src_num * 2, 2):
            src_mean[0] += src[i]
            src_mean[1] += src[i + 1]
            dst_mean[0] += self.umeyama_args_112[i]
            dst_mean[1] += self.umeyama_args_112[i + 1]
        src_mean[0] /= src_num
        src_mean[1] /= src_num
        dst_mean[0] /= src_num
        dst_mean[1] /= src_num

        src_demean = [[0.0, 0.0] for _ in range(src_num)]
        dst_demean = [[0.0, 0.0] for _ in range(src_num)]
        for i in range(src_num):
            src_demean[i][0] = src[2 * i] - src_mean[0]
            src_demean[i][1] = src[2 * i + 1] - src_mean[1]
            dst_demean[i][0] = self.umeyama_args_112[2 * i] - dst_mean[0]
            dst_demean[i][1] = self.umeyama_args_112[2 * i + 1] - dst_mean[1]

        A = [[0.0, 0.0], [0.0, 0.0]]
        for i in range(src_dim):
            for k in range(src_dim):
                for j in range(src_num):
                    A[i][k] += dst_demean[j][i] * src_demean[j][k]
                A[i][k] /= src_num

        T = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        U, S, V = self.svd22([A[0][0], A[0][1], A[1][0], A[1][1]])
        T[0][0] = U[0] * V[0] + U[1] * V[2]
        T[0][1] = U[0] * V[1] + U[1] * V[3]
        T[1][0] = U[2] * V[0] + U[3] * V[2]
        T[1][1] = U[2] * V[1] + U[3] * V[3]

        src_demean_mean = [0.0, 0.0]
        src_demean_var = [0.0, 0.0]
        for i in range(src_num):
            src_demean_mean[0] += src_demean[i][0]
            src_demean_mean[1] += src_demean[i][1]
        src_demean_mean[0] /= src_num
        src_demean_mean[1] /= src_num
        for i in range(src_num):
            src_demean_var[0] += (src_demean_mean[0] - src_demean[i][0]) ** 2
            src_demean_var[1] += (src_demean_mean[1] - src_demean[i][1]) ** 2
        src_demean_var[0] /= src_num
        src_demean_var[1] /= src_num
        scale = 1.0 / (src_demean_var[0] + src_demean_var[1]) * (S[0] + S[1])

        T[0][2] = dst_mean[0] - scale * (T[0][0] * src_mean[0] + T[0][1] * src_mean[1])
        T[1][2] = dst_mean[1] - scale * (T[1][0] * src_mean[0] + T[1][1] * src_mean[1])
        T[0][0] *= scale
        T[0][1] *= scale
        T[1][0] *= scale
        T[1][1] *= scale
        return T

    def get_affine_matrix(self, sparse_points):
        with ScopedTiming("get affine matrix", self.debug_mode > 1):
            matrix_dst = self.image_umeyama_112(sparse_points)
            return [matrix_dst[0][0], matrix_dst[0][1], matrix_dst[0][2],
                    matrix_dst[1][0], matrix_dst[1][1], matrix_dst[1][2]]


class FaceRegistration:
    """Batch registration: image files -> 128D feature .bin database."""

    def __init__(self, face_det_kmodel, face_reg_kmodel, det_input_size,
                 reg_input_size, database_dir, anchors,
                 confidence_threshold=0.25, nms_threshold=0.3,
                 rgb888p_size=[640, 480], display_size=[640, 480], debug_mode=0):
        self.face_det = FaceDetApp(face_det_kmodel,
                                   model_input_size=det_input_size,
                                   anchors=anchors,
                                   confidence_threshold=confidence_threshold,
                                   nms_threshold=nms_threshold,
                                   rgb888p_size=rgb888p_size,
                                   display_size=display_size,
                                   debug_mode=debug_mode)
        self.face_reg = FaceRegistrationApp(face_reg_kmodel,
                                            model_input_size=reg_input_size,
                                            rgb888p_size=rgb888p_size,
                                            display_size=display_size,
                                            debug_mode=debug_mode)
        self.database_dir = database_dir
        self.debug_mode = debug_mode
        ensure_dir(database_dir)

    def image2rgb888array(self, img):
        with ScopedTiming("image to rgb888 array", self.debug_mode > 0):
            img_data_rgb888 = img.to_rgb888()
            img_hwc = img_data_rgb888.to_numpy_ref()
            shape = img_hwc.shape
            img_tmp = img_hwc.reshape((shape[0] * shape[1], shape[2]))
            img_tmp_trans = img_tmp.transpose()
            img_res = img_tmp_trans.copy()
            return img_res.reshape((1, shape[2], shape[0], shape[1]))

    def register_array(self, input_np, img_file):
        self.face_det.config_preprocess(input_image_size=[input_np.shape[3], input_np.shape[2]])
        det_boxes, landms = self.face_det.run(input_np)
        try:
            if det_boxes is not None and len(det_boxes) > 0:
                if len(det_boxes) == 1:
                    db_i_name = remove_extension(img_file)
                    for landm in landms:
                        self.face_reg.config_preprocess(landm, input_image_size=[input_np.shape[3], input_np.shape[2]])
                        reg_result = self.face_reg.run(input_np)
                        out_file = join_path(self.database_dir, db_i_name + ".bin")
                        with open(out_file, "wb") as file:
                            file.write(reg_result.tobytes())
                        print("Success:", out_file)
                        return True, db_i_name, out_file
                else:
                    print("Only one person in a picture when you sign up:", img_file)
                    return False, "multi_face", ""
            else:
                print("No person detected:", img_file)
                return False, "no_face", ""
        except Exception as e:
            print("Register failed:", img_file, e)
            return False, "failed", ""
        return False, "failed", ""

    def register_image_file(self, img_path):
        img_file = img_path.split("/")[-1]
        img = image.Image(img_path)
        try:
            img.compress_for_ide()
        except Exception:
            pass
        input_np = self.image2rgb888array(img)
        return self.register_array(input_np, img_file)

    def register_folder(self, photo_dir):
        ok_count = 0
        fail_count = 0
        ensure_dir(self.database_dir)
        try:
            img_list = os.listdir(photo_dir)
        except Exception as e:
            print("Cannot open photo directory:", photo_dir, e)
            return ok_count, fail_count
        for img_file in img_list:
            if not is_image_file(img_file):
                continue
            full_img_file = join_path(photo_dir, img_file)
            print(full_img_file)
            ok, reason, out_file = self.register_image_file(full_img_file)
            if ok:
                ok_count += 1
            else:
                fail_count += 1
            gc.collect()
        print("Register finished. success=%d failed=%d" % (ok_count, fail_count))
        return ok_count, fail_count

    def deinit(self):
        try:
            self.face_det.deinit()
        except Exception as e:
            print("face_det deinit error:", e)
        try:
            self.face_reg.deinit()
        except Exception as e:
            print("face_reg deinit error:", e)
        gc.collect()


class FaceRecognition:
    """Live recognition: camera frame -> known/unknown result."""

    def __init__(self, face_det_kmodel, face_reg_kmodel, det_input_size, reg_input_size,
                 database_dir, anchors, confidence_threshold=0.25, nms_threshold=0.3,
                 face_recognition_threshold=0.65, rgb888p_size=[640, 480],
                 display_size=[640, 480], debug_mode=0):
        self.database_dir = database_dir
        self.face_recognition_threshold = face_recognition_threshold
        self.rgb888p_size = [align_up(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [align_up(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode
        self.max_register_face = 100
        self.valid_register_face = 0
        self.db_name = []
        self.db_data = []
        self.face_det = FaceDetApp(face_det_kmodel,
                                   model_input_size=det_input_size,
                                   anchors=anchors,
                                   confidence_threshold=confidence_threshold,
                                   nms_threshold=nms_threshold,
                                   rgb888p_size=self.rgb888p_size,
                                   display_size=self.display_size,
                                   debug_mode=debug_mode)
        self.face_reg = FaceRegistrationApp(face_reg_kmodel,
                                            model_input_size=reg_input_size,
                                            rgb888p_size=self.rgb888p_size,
                                            display_size=self.display_size,
                                            debug_mode=debug_mode)
        self.face_det.config_preprocess()
        self.database_init()

    def database_init(self):
        self.db_name = []
        self.db_data = []
        self.valid_register_face = 0
        try:
            db_file_list = os.listdir(self.database_dir)
        except Exception as e:
            print("No face database detected. Check path:", self.database_dir, e)
            return
        for db_file in db_file_list:
            if not db_file.endswith(".bin"):
                continue
            if self.valid_register_face >= self.max_register_face:
                break
            full_db_file = join_path(self.database_dir, db_file)
            try:
                with open(full_db_file, "rb") as f:
                    data = f.read()
                feature = np.frombuffer(data, dtype=np.float)
                self.db_data.append(feature)
                self.db_name.append(remove_extension(db_file))
                self.valid_register_face += 1
            except Exception as e:
                print("Cannot load database file:", full_db_file, e)
        print("Loaded face database:", self.valid_register_face)

    def database_reset(self):
        print("database clearing...")
        self.db_name = []
        self.db_data = []
        self.valid_register_face = 0
        print("database clear done")

    def database_search(self, feature):
        v_id = -1
        v_score_max = 0.0
        try:
            feature /= np.linalg.norm(feature)
            for i in range(self.valid_register_face):
                db_feature = self.db_data[i]
                db_feature /= np.linalg.norm(db_feature)
                v_score = np.dot(feature, db_feature) / 2 + 0.5
                if v_score > v_score_max:
                    v_score_max = v_score
                    v_id = i
        except Exception as e:
            print("database search error:", e)
            return "unknown"
        if v_id == -1:
            return "unknown"
        if v_score_max < self.face_recognition_threshold:
            return "unknown"
        return "name: %s, score: %.4f" % (self.db_name[v_id], v_score_max)

    def run(self, input_np):
        det_boxes, landms = self.face_det.run(input_np)
        recg_res = []
        if landms is not None:
            for landm in landms:
                self.face_reg.config_preprocess(landm)
                feature = self.face_reg.run(input_np)
                recg_res.append(self.database_search(feature))
        return det_boxes, recg_res

    def draw_result(self, pl, dets, recg_results, send_uart=False, uart=None, pto=None):
        records = []
        pl.osd_img.clear()
        if dets:
            for i, det in enumerate(dets):
                x1, y1, w, h = map(lambda x: int(round(x, 0)), det[:4])
                x1 = x1 * self.display_size[0] // self.rgb888p_size[0]
                y1 = y1 * self.display_size[1] // self.rgb888p_size[1]
                w = w * self.display_size[0] // self.rgb888p_size[0]
                h = h * self.display_size[1] // self.rgb888p_size[1]
                recg_text = recg_results[i] if i < len(recg_results) else "unknown"
                if recg_text == "unknown":
                    pl.osd_img.draw_rectangle(x1, y1, w, h, color=(255, 0, 0, 255), thickness=4)
                    name = "unknown"
                    score = "0"
                else:
                    pl.osd_img.draw_rectangle(x1, y1, w, h, color=(255, 0, 255, 0), thickness=4)
                    name, score = parse_recognition_text(recg_text)
                try:
                    pl.osd_img.draw_string_advanced(x1, y1, 32, recg_text, color=(255, 255, 0, 0))
                except Exception:
                    pass
                records.append((x1, y1, w, h, name, score))
                if send_uart:
                    send_face_recognition_uart(x1, y1, w, h, name, score, uart, pto)
        return records

    def deinit(self):
        try:
            self.face_det.deinit()
        except Exception as e:
            print("face_det deinit error:", e)
        try:
            self.face_reg.deinit()
        except Exception as e:
            print("face_reg deinit error:", e)
        gc.collect()


def parse_recognition_text(recg_text):
    pattern = r"name: (.*), score: (.*)"
    try:
        match = re.match(pattern, recg_text)
        if match:
            return match.group(1), match.group(2)
    except Exception:
        pass
    return recg_text, "0"


def create_registration_app(cfg=None, photo_dir=None):
    if cfg is None:
        cfg = {}
    face_det_model = cfg.get("FACE_DET_KMODEL_PATH", FACE_DET_KMODEL_PATH)
    face_reg_model = cfg.get("FACE_RECOGNITION_KMODEL_PATH", FACE_RECOGNITION_KMODEL_PATH)
    anchors_path = cfg.get("ANCHORS_PATH", ANCHORS_PATH)
    confidence = parse_float(cfg.get("CONFIDENCE_THRESHOLD", CONFIDENCE_THRESHOLD), CONFIDENCE_THRESHOLD)
    nms = parse_float(cfg.get("NMS_THRESHOLD", NMS_THRESHOLD), NMS_THRESHOLD)
    if photo_dir is None:
        photo_dir = cfg.get("PHOTO_DIR", DEFAULT_PHOTO_DIR)
    database_root = cfg.get("DATABASE_ROOT", DEFAULT_DATABASE_ROOT)
    database_dir = cfg.get("DATABASE_DIR", "")
    if not database_dir:
        database_dir = join_path(database_root, get_directory_name(photo_dir)) + "/"
    anchors = load_anchors(anchors_path)
    return FaceRegistration(face_det_model,
                            face_reg_model,
                            det_input_size=FACE_DET_INPUT_SIZE,
                            reg_input_size=FACE_REG_INPUT_SIZE,
                            database_dir=database_dir,
                            anchors=anchors,
                            confidence_threshold=confidence,
                            nms_threshold=nms)


def batch_register_faces(photo_dir=DEFAULT_PHOTO_DIR, cfg=None):
    app = create_registration_app(cfg, photo_dir)
    try:
        return app.register_folder(photo_dir)
    finally:
        app.deinit()


def create_recognition_app(pl, cfg=None):
    if cfg is None:
        cfg = {}
    face_det_model = cfg.get("FACE_DET_KMODEL_PATH", FACE_DET_KMODEL_PATH)
    face_reg_model = cfg.get("FACE_RECOGNITION_KMODEL_PATH", FACE_RECOGNITION_KMODEL_PATH)
    anchors_path = cfg.get("ANCHORS_PATH", ANCHORS_PATH)
    database_dir = cfg.get("DATABASE_DIR", DEFAULT_DATABASE_DIR)
    confidence = parse_float(cfg.get("CONFIDENCE_THRESHOLD", CONFIDENCE_THRESHOLD), CONFIDENCE_THRESHOLD)
    nms = parse_float(cfg.get("NMS_THRESHOLD", NMS_THRESHOLD), NMS_THRESHOLD)
    threshold = parse_float(cfg.get("FACE_RECOGNITION_THRESHOLD", FACE_RECOGNITION_THRESHOLD), FACE_RECOGNITION_THRESHOLD)
    anchors = load_anchors(anchors_path)
    return FaceRecognition(face_det_model,
                           face_reg_model,
                           det_input_size=FACE_DET_INPUT_SIZE,
                           reg_input_size=FACE_REG_INPUT_SIZE,
                           database_dir=database_dir,
                           anchors=anchors,
                           confidence_threshold=confidence,
                           nms_threshold=nms,
                           face_recognition_threshold=threshold,
                           rgb888p_size=pl.rgb888p_size,
                           display_size=pl.display_size)


def init_uart():
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


def send_face_recognition_uart(x, y, w, h, name, score, uart=None, pto=None):
    if name == "unknown":
        packet_text = "$%d,%d,%d,%d,unknown#" % (x, y, w, h)
    else:
        packet_text = "$%d,%d,%d,%d,%s,%s#" % (x, y, w, h, name, score)
    print(packet_text)
    if uart:
        try:
            if pto:
                uart.send(pto.get_face_recoginiton_data(x, y, w, h, name, score))
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

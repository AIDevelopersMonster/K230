# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / RegisterFace
# 01_register_faces_from_folder.py
#
# Batch face registration from image files.
# It scans PHOTO_DIR, detects exactly one face in each image,
# extracts a 128D feature vector, and writes .bin files to DATABASE_DIR.
#
# Required shared library on K230:
# /sdcard/libs/register_face_common.py
# ============================================

from libs.register_face_common import batch_register_faces
import gc

# Rename image files to person names before registration:
# /data/photo/register/peter.jpg -> peter.bin in database
PHOTO_DIR = "/data/photo/register/"

# Optional: leave DATABASE_DIR empty to create /data/face_database/<photo_folder_name>/
CONFIG = {
    "FACE_DET_KMODEL_PATH": "/sdcard/kmodel/face_detection_320.kmodel",
    "FACE_RECOGNITION_KMODEL_PATH": "/sdcard/kmodel/face_recognition.kmodel",
    "ANCHORS_PATH": "/sdcard/utils/prior_data_320.bin",
    "DATABASE_ROOT": "/data/face_database/",
    "DATABASE_DIR": "",
    "CONFIDENCE_THRESHOLD": "0.50",
    "NMS_THRESHOLD": "0.20"
}


def exce_demo(pl=None):
    print("Start face registration...")
    print("Photo directory:", PHOTO_DIR)
    ok_count, fail_count = batch_register_faces(PHOTO_DIR, CONFIG)
    print("Done. success=%d failed=%d" % (ok_count, fail_count))
    gc.collect()


def exit_demo():
    gc.collect()


if __name__ == "__main__":
    exce_demo(None)

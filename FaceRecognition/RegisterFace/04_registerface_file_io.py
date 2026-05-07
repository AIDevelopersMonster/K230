# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / RegisterFace
# 04_registerface_file_io.py
#
# File read/write example for face registration and recognition.
# It creates a config file, reads paths and thresholds, runs batch registration,
# and writes a TXT/CSV report.
#
# Required shared library on K230:
# /sdcard/libs/register_face_common.py
# ============================================

from libs.register_face_common import batch_register_faces, ensure_dir, file_exists
import os
import time
import gc

APP_DIR = "/sdcard/FaceRecognition/RegisterFace"
CONFIG_PATH = APP_DIR + "/register_face_config.txt"
LAST_RESULT_PATH = APP_DIR + "/register_face_last_result.txt"
LOG_PATH = APP_DIR + "/register_face_log.csv"

DEFAULT_CONFIG = """# K230 RegisterFace config\nFACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel\nFACE_RECOGNITION_KMODEL_PATH=/sdcard/kmodel/face_recognition.kmodel\nANCHORS_PATH=/sdcard/utils/prior_data_320.bin\nPHOTO_DIR=/data/photo/register/\nDATABASE_ROOT=/data/face_database/\nDATABASE_DIR=\nCONFIDENCE_THRESHOLD=0.50\nNMS_THRESHOLD=0.20\nFACE_RECOGNITION_THRESHOLD=0.65\n"""


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


def ticks_ms_safe():
    try:
        return time.ticks_ms()
    except Exception:
        return int(time.time() * 1000)


def csv_safe(value):
    return str(value).replace("\r", " ").replace("\n", " ").replace(",", ";")


def append_csv(path, header, row):
    need_header = not file_exists(path)
    with open(path, "a") as f:
        if need_header:
            f.write(",".join(header) + "\n")
        f.write(",".join([csv_safe(v) for v in row]) + "\n")


def write_report(photo_dir, ok_count, fail_count):
    now = ticks_ms_safe()
    text = "time_ms=%d\n" % now
    text += "photo_dir=%s\n" % photo_dir
    text += "success_count=%d\n" % ok_count
    text += "failed_count=%d\n" % fail_count
    write_text(LAST_RESULT_PATH, text, "w")
    append_csv(LOG_PATH,
               ["time_ms", "photo_dir", "success_count", "failed_count"],
               [now, photo_dir, ok_count, fail_count])


def exce_demo(pl=None):
    cfg = read_config()
    photo_dir = cfg.get("PHOTO_DIR", "/data/photo/register/")
    print("Config:", CONFIG_PATH)
    print("Photo directory:", photo_dir)
    ok_count, fail_count = batch_register_faces(photo_dir, cfg)
    write_report(photo_dir, ok_count, fail_count)
    print("Report written:", LAST_RESULT_PATH)
    print("CSV log written:", LOG_PATH)
    gc.collect()


def exit_demo():
    gc.collect()


if __name__ == "__main__":
    exce_demo(None)

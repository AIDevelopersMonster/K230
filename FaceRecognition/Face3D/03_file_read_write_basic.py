# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / Face3D
# 03_file_read_write_basic.py
#
# Simple file read/write example for beginners.
# This example does not run AI.
# ============================================

import os

APP_DIR = "/sdcard/FaceRecognition/Face3D"
TEXT_PATH = APP_DIR + "/file_demo.txt"
LOG_PATH = APP_DIR + "/file_demo_log.csv"


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
            os.mkdir(current)


def write_text_file():
    # Mode "w" creates a file or replaces old content.
    with open(TEXT_PATH, "w") as f:
        f.write("K230 Face3D file demo\n")
        f.write("open mode w replaces old content\n")


def append_files():
    # Mode "a" appends text to the end of the file.
    with open(TEXT_PATH, "a") as f:
        f.write("open mode a appends this line\n")

    # CSV is also a plain text file.
    with open(LOG_PATH, "a") as f:
        f.write("event,value\n")
        f.write("face_count,1\n")
        f.write("mesh_count,1\n")


def read_text_file():
    # Mode "r" reads an existing file.
    with open(TEXT_PATH, "r") as f:
        text = f.read()
    print("--- file content ---")
    print(text)


def main():
    ensure_dir(APP_DIR)
    write_text_file()
    append_files()
    read_text_file()
    print("Files created:")
    print(TEXT_PATH)
    print(LOG_PATH)


if __name__ == "__main__":
    main()

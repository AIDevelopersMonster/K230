# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / FaceDetectition
# 04_file_read_write_basic.py
#
# Simple file read/write example for beginners.
# This file does not use AI. It only explains open(), write(), read(), and append.
# ============================================

import os

APP_DIR = "/sdcard/FaceRecognition/FaceDetectition"
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


def write_file():
    # Mode "w" creates the file or replaces old content.
    with open(TEXT_PATH, "w") as f:
        f.write("K230 Face Detection file demo\n")
        f.write("mode=w replaces old content\n")


def append_file():
    # Mode "a" appends text to the end of the file.
    with open(TEXT_PATH, "a") as f:
        f.write("mode=a appends this new line\n")

    # CSV files are also simple text files.
    with open(LOG_PATH, "a") as f:
        f.write("event,value\n")
        f.write("face_count,1\n")


def read_file():
    # Mode "r" reads an existing file.
    with open(TEXT_PATH, "r") as f:
        text = f.read()
    print("--- file content ---")
    print(text)


def main():
    ensure_dir(APP_DIR)
    write_file()
    append_file()
    read_file()
    print("Files created:")
    print(TEXT_PATH)
    print(LOG_PATH)


if __name__ == "__main__":
    main()

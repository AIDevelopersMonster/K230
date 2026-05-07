# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / RegisterFace
# 05_file_read_write_basic.py
#
# Simple file read/write example for beginners.
# This example does not run AI.
# ============================================

import os

APP_DIR = "/sdcard/FaceRecognition/RegisterFace"
TEXT_PATH = APP_DIR + "/file_demo.txt"
LOG_PATH = APP_DIR + "/file_demo_log.csv"
BIN_PATH = APP_DIR + "/feature_demo.bin"


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
    # Mode "w" creates a text file or replaces old content.
    with open(TEXT_PATH, "w") as f:
        f.write("K230 RegisterFace file demo\n")
        f.write("open mode w replaces old content\n")


def append_files():
    # Mode "a" appends text to the end of the file.
    with open(TEXT_PATH, "a") as f:
        f.write("open mode a appends this line\n")

    # CSV is also a plain text file.
    with open(LOG_PATH, "a") as f:
        f.write("event,value\n")
        f.write("registered,1\n")
        f.write("recognized,unknown\n")


def write_binary_file():
    # Mode "wb" writes binary data. Real face features are saved this way.
    data = bytes([1, 2, 3, 4, 5, 6, 7, 8])
    with open(BIN_PATH, "wb") as f:
        f.write(data)


def read_text_file():
    # Mode "r" reads an existing text file.
    with open(TEXT_PATH, "r") as f:
        text = f.read()
    print("--- text file content ---")
    print(text)


def read_binary_file():
    # Mode "rb" reads binary data.
    with open(BIN_PATH, "rb") as f:
        data = f.read()
    print("--- binary file length ---")
    print(len(data))


def main():
    ensure_dir(APP_DIR)
    write_text_file()
    append_files()
    write_binary_file()
    read_text_file()
    read_binary_file()
    print("Files created:")
    print(TEXT_PATH)
    print(LOG_PATH)
    print(BIN_PATH)


if __name__ == "__main__":
    main()

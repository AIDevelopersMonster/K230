# ============================================
# K230 Example
# Author: AIDevelopersMonster
# Board: Yahboom K230 Vision Module
# GitHub: https://github.com/AIDevelopersMonster/K230
#
# FaceRecognition / AIvision
# 02_face_detection_file_io.py
#
# What it demonstrates:
# - reads settings from /sdcard/FaceRecognition/AIvision/face_config.txt;
# - creates the config file automatically on first run;
# - writes the latest face detection result to face_last_result.txt;
# - appends a history log to face_log.csv;
# - keeps the same AI code structure as the basic demo.
# ============================================

from libs.PipeLine import PipeLine, ScopedTiming
import time
import gc

from face_aivision_common import (
    create_face_detection_app,
    safe_deinit,
    ensure_default_config,
    read_config,
    parse_int,
    write_detection_files,
    LAST_RESULT_PATH,
    LOG_PATH,
)

face_det = None


def _ticks_ms():
    try:
        return time.ticks_ms()
    except Exception:
        return int(time.time() * 1000)


def _elapsed_ms(now, before):
    try:
        return time.ticks_diff(now, before)
    except Exception:
        return now - before


def exce_demo(pl):
    """Execute face detection and demonstrate file reading/writing."""
    global face_det
    ensure_default_config()
    cfg = read_config()
    save_log = cfg.get("SAVE_LOG", "1") == "1"
    write_interval_ms = parse_int(cfg.get("WRITE_INTERVAL_MS", "1000"), 1000)
    last_write_ms = 0

    try:
        face_det = create_face_detection_app(pl, cfg)

        while True:
            with ScopedTiming("total", 0):
                start_ms = _ticks_ms()
                img = pl.get_frame()
                dets = face_det.run(img)
                fps = 0.0

                elapsed = _elapsed_ms(_ticks_ms(), start_ms)
                if elapsed > 0:
                    fps = 1000.0 / elapsed

                face_det.draw_result(pl, dets, label="Face")
                pl.show_image()

                now = _ticks_ms()
                if save_log and _elapsed_ms(now, last_write_ms) >= write_interval_ms:
                    write_detection_files(dets, fps, LAST_RESULT_PATH, LOG_PATH)
                    last_write_ms = now

                gc.collect()
                time.sleep_us(10)

    except KeyboardInterrupt as e:
        print("User interrupted:", e)
    except Exception as e:
        print("Face detection file I/O demo exit:", e)
    finally:
        safe_deinit(face_det)
        face_det = None


def exit_demo():
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

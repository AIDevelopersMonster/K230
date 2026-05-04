# K230: FaceRecognition / AIvision

This folder contains demo examples for the **Yahboom K230 Vision Module** and K230 face detection through the AI vision pipeline.

The examples follow the structure from the PDF **AI vision processing code structure**: the camera captures a frame, `PipeLine` passes an RGBP888 image to AI, AI runs preprocessing → inference → postprocessing, and the result is drawn on the OSD layer and shown on the display.

## Files

| File | Purpose |
| --- | --- |
| `face_aivision_common.py` | Shared module: `FaceDetectionApp`, anchors loading, file read/write helpers, CSV log, result drawing. |
| `01_face_detection_basic.py` | Basic example: camera, model, inference, and face rectangles on screen. |
| `02_face_detection_file_io.py` | File I/O example: read settings from a file and write recognition results to files. |
| `03_face_detection_external_call.py` | Shows the structure for calling an AI routine from another program through `exce_demo(pl)` and `exit_demo()`. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## Required files on the TF card

Make sure the following files exist on the K230 TF card:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/utils/prior_data_320.bin
```

If your paths are different, run `02_face_detection_file_io.py` once. It creates this config file:

```text
/sdcard/FaceRecognition/AIvision/face_config.txt
```

Then edit `KMODEL_PATH` and `ANCHORS_PATH` in that file.

## Quick start

1. Copy `FaceRecognition/AIvision` to the K230 or open a `.py` file in CanMV IDE.
2. Connect the Yahboom K230 Vision Module over USB.
3. Run `01_face_detection_basic.py`.
4. Point the camera at a face.
5. A yellow rectangle should appear around the detected face.

## AI pipeline structure

Main idea:

```text
Sensor → Frame → AI → OSD → Display
```

In code:

```python
pl = PipeLine(rgb888p_size=[640, 360], display_size=[640, 480], display_mode="lcd")
pl.create()

face_det = create_face_detection_app(pl)
img = pl.get_frame()
dets = face_det.run(img)
face_det.draw_result(pl, dets)
pl.show_image()
```

### Why only one PipeLine instance is used

`PipeLine` controls the camera and the display. Therefore, one program should create only one `PipeLine` instance. AI routines should receive it as a parameter:

```python
def exce_demo(pl):
    face_det = create_face_detection_app(pl)
    ...
```

## Main parts of FaceDetectionApp

`face_aivision_common.py` contains:

```python
class FaceDetectionApp(AIBase):
```

It follows the usual AI demo structure:

1. `__init__()` — model path, model input size, anchors, thresholds.
2. `config_preprocess()` — AI2D resize from the camera frame to `320x320` model input.
3. `run()` — inherited from `AIBase`; runs preprocessing → inference → postprocessing.
4. `postprocess()` — calls `aidemo.face_det_post_process()`.
5. `draw_result()` — draws face rectangles on the OSD layer `pl.osd_img`.
6. `deinit()` — releases model resources.

## Reading files on K230

Use `open()` with mode `"r"` to read a text file:

```python
with open("/sdcard/FaceRecognition/AIvision/face_config.txt", "r") as f:
    text = f.read()
```

`02_face_detection_file_io.py` reads a configuration file like this:

```text
KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
ANCHORS_PATH=/sdcard/utils/prior_data_320.bin
CONFIDENCE_THRESHOLD=0.50
NMS_THRESHOLD=0.20
DEBUG_MODE=0
SAVE_LOG=1
WRITE_INTERVAL_MS=1000
```

Parsing a `KEY=VALUE` line:

```python
key, value = line.split("=", 1)
cfg[key.strip().upper()] = value.strip()
```

## Writing files on K230

Use mode `"w"` to write a file. It creates the file if it does not exist and replaces old content if it already exists:

```python
with open("/sdcard/FaceRecognition/AIvision/face_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Use mode `"a"` to append text to the end of a file:

```python
with open("/sdcard/FaceRecognition/AIvision/face_log.csv", "a") as f:
    f.write("time_ms,fps,face_count\n")
```

### open() modes

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. Missing file causes an error. |
| `"w"` | Write a new file. Existing content is deleted. |
| `"a"` | Append data to the end of the file. Existing content is preserved. |

## Files created by example 02

When `02_face_detection_file_io.py` runs, it creates this folder:

```text
/sdcard/FaceRecognition/AIvision
```

The folder contains:

```text
face_config.txt       # model and logging settings
face_last_result.txt  # latest result
face_log.csv          # result history
```

Example `face_last_result.txt`:

```text
time_ms=123456
fps=22.500
face_count=1
best_score=0.9210
x=180
y=90
w=120
h=120
```

Example CSV log:

```text
time_ms,fps,face_count,best_score,x,y,w,h
123456,22.500,1,0.9210,180,90,120,120
```

## Why file writing is rate-limited

Face detection runs in an infinite loop. Writing files every frame would create too many writes to the TF card. The config file includes:

```text
WRITE_INTERVAL_MS=1000
```

This means the result is written at most once per second.

## Face detection tips

1. Use good lighting.
2. Keep the face large enough in the camera frame.
3. Avoid covering the face with hands or objects.
4. If FPS is low, reduce `rgb888p_size`.
5. If false detections appear, increase `CONFIDENCE_THRESHOLD`.
6. If faces are not detected, try lowering `CONFIDENCE_THRESHOLD`, for example to `0.40`.

## Calling the routine from another file

`03_face_detection_external_call.py` demonstrates the structure where external code creates one `PipeLine`, and the AI routine uses it:

```python
pl = PipeLine(rgb888p_size=[640, 360], display_size=[640, 480], display_mode="lcd")
pl.create()
exce_demo(pl)
```

To stop and release resources:

```python
exit_demo()
```

This structure is useful when you want to combine several AI modes in one menu or GUI.

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230 Vision Module  
**Repository:** https://github.com/AIDevelopersMonster/K230

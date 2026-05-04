# K230: FaceRecognition / FaceDetectition

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on **Face Detection**.

The examples follow the PDF **Face Detection** and the K230 AI Vision structure: the camera captures a frame, `PipeLine` sends an RGBP888 image to AI, the model runs inference, `aidemo.face_det_post_process()` returns face rectangles, and the result is drawn on the OSD layer over the camera image.

> The folder name keeps the spelling from the request: `FaceDetectition`.

## Files

| File | Purpose |
| --- | --- |
| `01_face_detection_basic.py` | Basic demo: detect faces and draw yellow rectangles on screen. |
| `02_face_detection_uart.py` | Face detection plus UART output. Packet format: `$x,y,w,h#`. |
| `03_face_detection_file_io.py` | Face detection plus reading settings from a config file and writing results to TXT/CSV. |
| `04_file_read_write_basic.py` | Beginner file read/write demo without AI. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## What Face Detection demonstrates

Face Detection finds faces in a frame and returns rectangles:

```text
x, y, w, h
```

Where:

| Field | Meaning |
| --- | --- |
| `x` | top-left X coordinate of the rectangle |
| `y` | top-left Y coordinate of the rectangle |
| `w` | rectangle width |
| `h` | rectangle height |

The examples use:

```python
rgb888p_size = [640, 480]
display_size = [640, 480]
```

This is important: if the AI frame and display frame have different aspect ratios, the face rectangle may shift.

## Required files on the TF card

Make sure these files exist on the K230 TF card:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/utils/prior_data_320.bin
```

If your files are stored in different locations, use `03_face_detection_file_io.py`. It creates a config file where you can change the paths.

## Quick start

1. Open `01_face_detection_basic.py` in CanMV IDE.
2. Connect the Yahboom K230 Vision Module over USB.
3. Run the example.
4. Point the camera at a face.
5. A yellow rectangle should appear around the face.

## AI pipeline structure

Main flow:

```text
Sensor → Frame → AI → OSD → Display
```

In code:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
res = face_det.run(img)
face_det.draw_result(pl, res)
pl.show_image()
```

`PipeLine` manages the camera and display, so one program should create only one `PipeLine` object.

## Why pad is used before resize

The examples use preprocessing like the Yahboom manufacturer example:

```python
top, bottom, left, right = self.get_padding_param()
self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

`pad` keeps the original frame aspect ratio before resizing the image to the model input size `320x320`. If the code only uses `resize`, the image may be distorted and the rectangle may be drawn around only part of the face.

## Main parts of FaceDetectionApp

`FaceDetectionApp` inherits from `AIBase` and contains:

1. `__init__()` — paths, thresholds, anchors, frame size, and display size.
2. `get_padding_param()` — padding calculation.
3. `config_preprocess()` — AI2D configuration: `pad` → `resize`.
4. `postprocess()` — call to `aidemo.face_det_post_process()`.
5. `draw_result()` — draw rectangles on `pl.osd_img`.
6. `deinit()` — release model resources.

## UART example

`02_face_detection_uart.py` sends face coordinates in this format:

```text
$x,y,w,h#
```

Example:

```text
$180,90,120,120#
```

If `YbProtocol` and `YbUart` are available in the firmware, the demo uses the Yahboom protocol:

```python
pto.get_face_detect_data(x, y, w, h)
uart.send(pto_data)
```

If these libraries are not available, the demo still works on screen and prints a text packet to the console.

## Reading files on K230

Read a file with `open()` mode `"r"`:

```python
with open("/sdcard/FaceRecognition/FaceDetectition/face_detection_config.txt", "r") as f:
    text = f.read()
```

`03_face_detection_file_io.py` reads a config like this:

```text
KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
ANCHORS_PATH=/sdcard/utils/prior_data_320.bin
CONFIDENCE_THRESHOLD=0.50
NMS_THRESHOLD=0.20
WRITE_INTERVAL_MS=1000
```

Parsing a line:

```python
key, value = line.split("=", 1)
cfg[key.strip().upper()] = value.strip()
```

## Writing files on K230

Use mode `"w"` to create or fully replace a file:

```python
with open("/sdcard/FaceRecognition/FaceDetectition/face_detection_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Use mode `"a"` to append text to the end of a file:

```python
with open("/sdcard/FaceRecognition/FaceDetectition/face_detection_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,x,y,w,h\n")
```

### open() modes

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. Missing file causes an error. |
| `"w"` | Write from the beginning. Old content is deleted. |
| `"a"` | Append data to the end. Old content is preserved. |

## Files created by example 03

When `03_face_detection_file_io.py` runs, it creates this folder:

```text
/sdcard/FaceRecognition/FaceDetectition
```

The folder contains:

```text
face_detection_config.txt       # model and writing settings
face_detection_last_result.txt  # latest detection result
face_detection_log.csv          # result history
```

Example `face_detection_last_result.txt`:

```text
time_ms=123456
fps=22.500
face_count=1
x=180
y=90
w=120
h=120
```

## Why writing is rate-limited

Face Detection runs in an infinite loop. Writing to a file every frame would create too many writes to the TF card. The config includes:

```text
WRITE_INTERVAL_MS=1000
```

This means the result is written at most once per second.

## Tips

1. Use good lighting.
2. Keep the face large enough in the frame.
3. Use `rgb888p_size=[640, 480]` and `display_size=[640, 480]` for correct rectangles on LCD.
4. If a face is not detected, reduce `CONFIDENCE_THRESHOLD`, for example to `0.40`.
5. If false detections appear, increase `CONFIDENCE_THRESHOLD`, for example to `0.60`.
6. If rectangles are shifted, make sure `config_preprocess()` uses `pad` before `resize`.

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230 Vision Module  
**Repository:** https://github.com/AIDevelopersMonster/K230

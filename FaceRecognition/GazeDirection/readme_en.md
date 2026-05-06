# K230: FaceRecognition / GazeDirection

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on **Gaze direction detection**.

The examples follow the PDF **Gaze direction detection** and the manufacturer working example. The PDF says the original example is located at `Source code/07.Face/05.eye_gaze.py`: after running the example and pointing the K230 camera at a face, the direction the eyes are looking at is marked on the screen.

## Important: the shared file is in `libs`

The shared code is stored as a library:

```text
libs/gaze_direction_common.py
```

On the K230, copy this file to:

```text
/sdcard/libs/gaze_direction_common.py
```

The demos import it like this:

```python
from libs.gaze_direction_common import create_eye_gaze_app, safe_deinit
```

If `gaze_direction_common.py` is placed only next to the examples in `FaceRecognition/GazeDirection`, the import `from libs.gaze_direction_common ...` will not find it.

## Files

| File | Purpose |
| --- | --- |
| `../../libs/gaze_direction_common.py` | Shared library: `FaceDetApp`, `EyeGazeApp`, `EyeGaze`, UART helpers. |
| `01_gaze_direction_basic.py` | Basic demo: face detection, gaze estimation, and arrow drawing. |
| `02_gaze_direction_uart.py` | Gaze estimation plus UART output with arrow coordinates. |
| `03_gaze_direction_file_io.py` | Gaze estimation plus config reading and TXT/CSV result writing. |
| `04_file_read_write_basic.py` | Beginner file read/write demo without AI. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## What Gaze Direction Detection demonstrates

The algorithm has two stages:

```text
Face Detection → Eye Gaze Estimation
```

1. `FaceDetApp` detects a face and returns a rectangle `x, y, w, h`.
2. `EyeGazeApp` crops the face region and resizes it for the gaze model.
3. The `eye_gaze.kmodel` model returns `pitch` and `yaw`.
4. The code converts `pitch/yaw` into a 2D vector using trigonometry.
5. `draw_result()` draws a gaze direction arrow on the OSD layer.

## Required files on the TF card

Make sure these files exist on the K230 TF card:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/eye_gaze.kmodel
/sdcard/utils/prior_data_320.bin
```

If your paths are different, use `03_gaze_direction_file_io.py`. It creates a config file where you can change the paths.

## Quick start

1. Copy `libs/gaze_direction_common.py` from the repository to the K230:

```text
/sdcard/libs/gaze_direction_common.py
```

2. Copy the `FaceRecognition/GazeDirection` folder to the TF card or open an example in CanMV IDE.
3. Connect the Yahboom K230 Vision Module over USB.
4. Run `01_gaze_direction_basic.py`.
5. Point the camera at a face.
6. An arrow should appear on the screen showing the gaze direction.

## AI pipeline structure

Main flow:

```text
Sensor → Frame → Face Detection → Eye Gaze AI → OSD → Display
```

In code:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, eye_gaze_res = eg.run(img)
eg.draw_result(pl, det_boxes, eye_gaze_res)
pl.show_image()
```

`PipeLine` manages the camera and display, so one program should create only one `PipeLine` object.

## Why pad is used before resize

For the face detection model, preprocessing must preserve the frame aspect ratio:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

If the code only uses `resize`, the face rectangle and gaze arrow may shift.

## Why crop is used for Eye Gaze

After face detection, the gaze model needs the face region:

```python
x, y, w, h = map(lambda v: int(round(v, 0)), det[:4])
self.ai2d.crop(x, y, w, h)
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

After inference, the code calls:

```python
post_ret = aidemo.eye_gaze_post_process(results)
```

It returns `pitch` and `yaw`.

## How the gaze arrow is calculated

The arrow starts from the center of the detected face:

```python
center_x = x + w / 2.0
center_y = y + h / 2.0
```

The arrow endpoint is calculated from `pitch` and `yaw`:

```python
dx = -length * math.sin(pitch) * math.cos(yaw)
target_x = int(center_x + dx)
dy = -length * math.sin(yaw)
target_y = int(center_y + dy)
```

Then the arrow is drawn:

```python
pl.osd_img.draw_arrow(center_x, center_y, target_x, target_y)
```

## UART output

`02_gaze_direction_uart.py` sends arrow coordinates through UART in this format:

```text
$x0,y0,x1,y1#
```

Where:

| Field | Meaning |
| --- | --- |
| `x0, y0` | arrow start point |
| `x1, y1` | arrow end point |

If the Yahboom `YbProtocol` and `YbUart` libraries are available, the demo uses:

```python
pto.get_eye_gaze_data(x0, y0, x1, y1)
uart.send(pto_data)
```

If the UART libraries are not available, the demo still draws the arrow and prints the text packet to the console.

## Reading files on K230

Read a file with `open()` mode `"r"`:

```python
with open("/sdcard/FaceRecognition/GazeDirection/gaze_direction_config.txt", "r") as f:
    text = f.read()
```

`03_gaze_direction_file_io.py` reads a config like this:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
EYE_GAZE_KMODEL_PATH=/sdcard/kmodel/eye_gaze.kmodel
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
with open("/sdcard/FaceRecognition/GazeDirection/gaze_direction_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Use mode `"a"` to append text to the end of a file:

```python
with open("/sdcard/FaceRecognition/GazeDirection/gaze_direction_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,x0,y0,x1,y1,pitch,yaw\n")
```

### open() modes

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. Missing file causes an error. |
| `"w"` | Write from the beginning. Old content is deleted. |
| `"a"` | Append data to the end. Old content is preserved. |

## Files created by example 03

When `03_gaze_direction_file_io.py` runs, it creates this folder:

```text
/sdcard/FaceRecognition/GazeDirection
```

The folder contains:

```text
gaze_direction_config.txt       # model and writing settings
gaze_direction_last_result.txt  # latest result
gaze_direction_log.csv          # result history
```

Example `gaze_direction_last_result.txt`:

```text
time_ms=123456
fps=18.500
face_count=1
x0=320
y0=240
x1=120
y1=200
pitch=0.123456
yaw=-0.234567
```

## Why writing is rate-limited

Gaze Direction Detection runs in an infinite loop. Writing to a file every frame would create too many writes to the TF card. The config includes:

```text
WRITE_INTERVAL_MS=1000
```

This means the result is written at most once per second.

## Tips

1. Use good lighting.
2. Keep the face large enough in the frame.
3. Use `rgb888p_size=[640, 480]` and `display_size=[640, 480]` for correct LCD output.
4. If a face is not detected, reduce `CONFIDENCE_THRESHOLD`, for example to `0.40`.
5. If the arrow is shifted, check `pad → resize` for Face Detection and `crop → resize` for Eye Gaze.
6. Make sure the board has the fresh file `/sdcard/libs/gaze_direction_common.py`.

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230 Vision Module  
**Repository:** https://github.com/AIDevelopersMonster/K230

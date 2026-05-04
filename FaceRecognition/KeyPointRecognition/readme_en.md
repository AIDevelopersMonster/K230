# K230: FaceRecognition / KeyPointRecognition

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on **Facial key point recognition**.

The examples follow the PDF **Facial key point recognition** and the manufacturer working example. The PDF says the original example is located at `Source code/07.Face/02.face_landmark.py`: the program first performs Face Detection, then runs a landmark model for each detected face, and finally draws facial contours for eyes, eyebrows, nose, lips, and the face outline on the screen.

## Files

| File | Purpose |
| --- | --- |
| `01_face_landmark_basic.py` | Full basic facial key point recognition demo. Can be run as a standalone file. |
| `keypoint_common.py` | Shared module with `FaceDetApp`, `FaceLandMarkApp`, and `FaceLandMark`. Used by example 02. |
| `02_face_landmark_file_io.py` | Facial landmark recognition plus config reading and TXT/CSV result writing. |
| `03_file_read_write_basic.py` | Beginner file read/write demo without AI. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## What Key Point Recognition demonstrates

The algorithm has two stages:

```text
Face Detection → Face Landmark Recognition
```

1. `FaceDetApp` detects a face and returns a rectangle `x, y, w, h`.
2. `FaceLandMarkApp` crops and normalizes the face area through affine transform.
3. The `face_landmark.kmodel` model predicts facial key points.
4. Inverse affine transform converts the points back to the original image coordinates.
5. `draw_result()` draws face contours on the OSD layer.

The demo uses 106 facial key points: eyebrows, eyes, pupils, nose, lips, and face contour.

## Required files on the TF card

Make sure these files exist on the K230 TF card:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/face_landmark.kmodel
/sdcard/utils/prior_data_320.bin
```

If your files are stored in different locations, use `02_face_landmark_file_io.py`. It creates a config file where you can change the paths.

## Quick start

1. Open `01_face_landmark_basic.py` in CanMV IDE.
2. Connect the Yahboom K230 Vision Module over USB.
3. Run the example.
4. Point the camera at a face.
5. Colored lines and points should appear on the face.

For example 02, copy two files to the same folder on the TF card:

```text
/sdcard/FaceRecognition/KeyPointRecognition/keypoint_common.py
/sdcard/FaceRecognition/KeyPointRecognition/02_face_landmark_file_io.py
```

## AI pipeline structure

Main flow:

```text
Sensor → Frame → Face Detection → Landmark AI → OSD → Display
```

In code:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, landmark_res = flm.run(img)
flm.draw_result(pl, det_boxes, landmark_res)
pl.show_image()
```

`PipeLine` manages the camera and display, so one program should create only one `PipeLine` object.

## Why pad is used before resize

For the face detection model, preprocessing must keep the original frame aspect ratio:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

If the code only uses `resize`, the face rectangle and landmark points may shift.

## Why affine transform is used

The landmark model needs a normalized face region. For each detected face, the program builds an affine matrix:

```python
self.matrix_dst = self.get_affine_matrix(det)
self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, affine_matrix)
```

After inference, key point coordinates are converted back through inverse affine transform:

```python
matrix_dst_inv = aidemo.invert_affine_transform(self.matrix_dst)
```

This allows the points to be drawn in the correct positions on the original camera frame.

## Reading files on K230

Read a file with `open()` mode `"r"`:

```python
with open("/sdcard/FaceRecognition/KeyPointRecognition/keypoint_config.txt", "r") as f:
    text = f.read()
```

`02_face_landmark_file_io.py` reads a config like this:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
FACE_LANDMARK_KMODEL_PATH=/sdcard/kmodel/face_landmark.kmodel
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
with open("/sdcard/FaceRecognition/KeyPointRecognition/keypoint_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Use mode `"a"` to append text to the end of a file:

```python
with open("/sdcard/FaceRecognition/KeyPointRecognition/keypoint_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,keypoint_count\n")
```

### open() modes

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. Missing file causes an error. |
| `"w"` | Write from the beginning. Old content is deleted. |
| `"a"` | Append data to the end. Old content is preserved. |

## Files created by example 02

When `02_face_landmark_file_io.py` runs, it creates this folder:

```text
/sdcard/FaceRecognition/KeyPointRecognition
```

The folder contains:

```text
keypoint_config.txt       # model and writing settings
keypoint_last_result.txt  # latest result
keypoint_log.csv          # result history
```

Example `keypoint_last_result.txt`:

```text
time_ms=123456
fps=12.500
face_count=1
keypoint_count=106
first_keypoint_x=180
first_keypoint_y=90
```

## Why writing is rate-limited

Facial key point recognition runs in an infinite loop. Writing to a file every frame would create too many writes to the TF card. The config includes:

```text
WRITE_INTERVAL_MS=1000
```

This means the result is written at most once per second.

## Tips

1. Use good lighting.
2. Keep the face large enough in the frame.
3. Use `rgb888p_size=[640, 480]` and `display_size=[640, 480]` for correct LCD output.
4. If a face is not detected, reduce `CONFIDENCE_THRESHOLD`, for example to `0.40`.
5. If points are shifted, check `pad → resize` for Face Detection and affine transform for Landmark.
6. For `02_face_landmark_file_io.py`, make sure `keypoint_common.py` is in the same folder.

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230 Vision Module  
**Repository:** https://github.com/AIDevelopersMonster/K230

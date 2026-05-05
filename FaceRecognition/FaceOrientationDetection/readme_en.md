# K230: FaceRecognition / FaceOrientationDetection

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on **Face orientation detection**.

The examples follow the PDF **Face orientation detection** and the manufacturer working example. The PDF says the original example is located at `Source code/07.Face/03.face_pose.py`: the program first detects the face, then estimates the face pose, and draws a 3D cube on the screen to show the current face direction.

## Files

| File | Purpose |
| --- | --- |
| `face_pose_common.py` | Shared module with `FaceDetApp`, `FacePoseApp`, and `FacePose`. |
| `01_face_orientation_basic.py` | Basic demo: face detection, orientation estimation, and a 3D cube on screen. |
| `02_face_orientation_file_io.py` | Face orientation plus config reading and `pitch/yaw/roll` result writing to TXT/CSV. |
| `03_file_read_write_basic.py` | Beginner file read/write demo without AI. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## What Face Orientation Detection demonstrates

The algorithm has two stages:

```text
Face Detection → Face Pose Estimation
```

1. `FaceDetApp` detects a face and returns a rectangle `x, y, w, h`.
2. `FacePoseApp` normalizes the face area through affine transform.
3. The `face_pose.kmodel` model predicts a rotation matrix `R`.
4. `rotation_matrix_to_euler_angles()` converts the matrix into Euler angles:
   - `pitch` — head tilt up/down;
   - `yaw` — head rotation left/right;
   - `roll` — head tilt toward the shoulder.
5. `draw_result()` builds a 3D projection and draws a cube over the face.

## Required files on the TF card

Make sure these files exist on the K230 TF card:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/face_pose.kmodel
/sdcard/utils/prior_data_320.bin
```

If your files are stored in different locations, use `02_face_orientation_file_io.py`. It creates a config file where you can change the paths.

## Quick start

1. Copy the `FaceRecognition/FaceOrientationDetection` folder to the TF card.
2. Make sure `face_pose_common.py` is in the same folder as the examples:

```text
/sdcard/FaceRecognition/FaceOrientationDetection/face_pose_common.py
```

3. Open `01_face_orientation_basic.py` in CanMV IDE.
4. Connect the Yahboom K230 Vision Module over USB.
5. Run the example.
6. Point the camera at a face.
7. A red 3D cube should appear on the screen, showing the face orientation.

## AI pipeline structure

Main flow:

```text
Sensor → Frame → Face Detection → Face Pose AI → OSD → Display
```

In code:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, pose_res = fp.run(img)
fp.draw_result(pl, det_boxes, pose_res)
pl.show_image()
```

`PipeLine` manages the camera and display, so one program should create only one `PipeLine` object.

## Why pad is used before resize

For the face detection model, preprocessing must keep the original frame aspect ratio:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

If the code only uses `resize`, the face rectangle and 3D visualization may shift.

## Why affine transform is used

The face pose model needs a normalized face region. For each detected face, the program builds an affine matrix:

```python
matrix_dst = self.get_affine_matrix(det)
self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, matrix_dst)
```

After inference, the model returns a rotation matrix, and the code calculates `pitch`, `yaw`, and `roll`.

## Reading files on K230

Read a file with `open()` mode `"r"`:

```python
with open("/sdcard/FaceRecognition/FaceOrientationDetection/face_orientation_config.txt", "r") as f:
    text = f.read()
```

`02_face_orientation_file_io.py` reads a config like this:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
FACE_POSE_KMODEL_PATH=/sdcard/kmodel/face_pose.kmodel
ANCHORS_PATH=/sdcard/utils/prior_data_320.bin
CONFIDENCE_THRESHOLD=0.50
NMS_THRESHOLD=0.20
WRITE_INTERVAL_MS=1000
DRAW_ANGLES=1
```

Parsing a line:

```python
key, value = line.split("=", 1)
cfg[key.strip().upper()] = value.strip()
```

## Writing files on K230

Use mode `"w"` to create or fully replace a file:

```python
with open("/sdcard/FaceRecognition/FaceOrientationDetection/face_orientation_last_result.txt", "w") as f:
    f.write("yaw=0.0\n")
```

Use mode `"a"` to append text to the end of a file:

```python
with open("/sdcard/FaceRecognition/FaceOrientationDetection/face_orientation_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,pitch,yaw,roll\n")
```

### open() modes

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. Missing file causes an error. |
| `"w"` | Write from the beginning. Old content is deleted. |
| `"a"` | Append data to the end. Old content is preserved. |

## Files created by example 02

When `02_face_orientation_file_io.py` runs, it creates this folder:

```text
/sdcard/FaceRecognition/FaceOrientationDetection
```

The folder contains:

```text
face_orientation_config.txt       # model and writing settings
face_orientation_last_result.txt  # latest result
face_orientation_log.csv          # result history
```

Example `face_orientation_last_result.txt`:

```text
time_ms=123456
fps=20.000
face_count=1
pitch=1.234
yaw=-10.500
roll=2.100
```

## Why writing is rate-limited

Face orientation estimation runs in an infinite loop. Writing to a file every frame would create too many writes to the TF card. The config includes:

```text
WRITE_INTERVAL_MS=1000
```

This means the result is written at most once per second.

## Application scenarios

The PDF lists typical use cases: driver monitoring, attention analysis, human-computer interaction, VR/AR, security monitoring, smart retail, and photography assistance.

## Tips

1. Use good lighting.
2. Keep the face large enough in the frame.
3. Use `rgb888p_size=[640, 480]` and `display_size=[640, 480]` for correct LCD output.
4. If a face is not detected, reduce `CONFIDENCE_THRESHOLD`, for example to `0.40`.
5. If the cube is shifted, check `pad → resize` for Face Detection and `affine` for Face Pose.
6. For examples 01 and 02, make sure `face_pose_common.py` is in the same folder.

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230 Vision Module  
**Repository:** https://github.com/AIDevelopersMonster/K230

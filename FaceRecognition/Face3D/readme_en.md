# K230: FaceRecognition / Face3D

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on **Face 3D Network** — drawing a 3D face mesh.

The examples follow the PDF **Face 3D Network** and the manufacturer working example. The PDF says the original example is located at `Source code summary/07.Face/04.face_mesh.py`: after running the example and pointing the K230 camera at a face, the face on the screen is covered with a 3D network. The PDF also notes that the Face 3D Network model is relatively large, so it is normal if faces are not recognized during the first few seconds; if too many faces appear at the same time, the system may freeze.

## Important: the shared file is in `libs`

The shared code is stored as a library:

```text
libs/face3d_common.py
```

On the K230, copy this file to:

```text
/sdcard/libs/face3d_common.py
```

The demos import it like this:

```python
from libs.face3d_common import create_face_mesh_app
```

If `face3d_common.py` is placed only next to the examples in `FaceRecognition/Face3D`, the import `from libs.face3d_common ...` will not find it.

## Files

| File | Purpose |
| --- | --- |
| `../../libs/face3d_common.py` | Shared library: `FaceDetApp`, `FaceMeshApp`, `FaceMeshPostApp`, `FaceMesh`. |
| `01_face3d_basic.py` | Basic demo: face detection, 3D mesh generation, and screen output. |
| `02_face3d_file_io.py` | Face3D plus config reading and TXT/CSV result writing. |
| `03_file_read_write_basic.py` | Beginner file read/write demo without AI. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## What Face 3D Network demonstrates

The algorithm has several stages:

```text
Face Detection → Face Mesh Params → Face Mesh Postprocess → OSD → Display
```

1. `FaceDetApp` detects a face and returns a rectangle `x, y, w, h`.
2. `FaceMeshApp` calculates an ROI around the face, runs `crop → resize`, and executes `face_alignment.kmodel`.
3. Model results are denormalized with statistical parameters `param_mean` and `param_std`.
4. `FaceMeshPostApp` converts face parameters into 3D mesh vertices through `face_alignment_post.kmodel`.
5. `aidemo.face_mesh_post_process()` maps points into display coordinates.
6. `aidemo.face_draw_mesh()` draws the 3D mesh over the face.

## Required files on the TF card

Make sure these files exist on the K230 TF card:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/face_alignment.kmodel
/sdcard/kmodel/face_alignment_post.kmodel
/sdcard/utils/prior_data_320.bin
```

If your paths are different, use `02_face3d_file_io.py`. It creates a config file where you can change the paths.

## Quick start

1. Copy `libs/face3d_common.py` from the repository to the K230:

```text
/sdcard/libs/face3d_common.py
```

2. Copy the `FaceRecognition/Face3D` folder to the TF card or open an example in CanMV IDE.
3. Connect the Yahboom K230 Vision Module over USB.
4. Run `01_face3d_basic.py`.
5. Point the camera at a face.
6. After a few seconds, a 3D face mesh should appear on the face.

## Why recognition may not appear during the first seconds

The PDF explicitly notes that the model needed for Face 3D Network is relatively large. Therefore, it is normal if the face is not recognized during the first few seconds after startup.

## Why many faces may freeze the system

The PDF also notes that if too many faces appear on the screen at the same time, the system may freeze. In that case, press **RST** to restart. To avoid this, you can limit the number of processed faces in the `run()` method.

For example, process only the first detected face:

```python
for det_box in det_boxes[:1]:
    ...
```

## AI pipeline structure

The main loop in code:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, mesh_res = fm.run(img)
fm.draw_result(pl, det_boxes, mesh_res)
pl.show_image()
```

`PipeLine` manages the camera and display, so one program should create only one `PipeLine` object.

## Why pad is used before resize

For the face detection model, preprocessing must preserve the frame aspect ratio:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

If the code only uses `resize`, the face rectangle and the following 3D mesh may shift.

## Why crop is used for Face Mesh

After face detection, `FaceMeshApp` calculates an ROI around the face:

```python
roi = self.parse_roi_box_from_bbox(det)
self.ai2d.crop(int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3]))
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

The ROI is expanded and slightly moved down to include the whole face and chin.

## Reading files on K230

Read a file with `open()` mode `"r"`:

```python
with open("/sdcard/FaceRecognition/Face3D/face3d_config.txt", "r") as f:
    text = f.read()
```

`02_face3d_file_io.py` reads a config like this:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
FACE_MESH_KMODEL_PATH=/sdcard/kmodel/face_alignment.kmodel
FACE_MESH_POST_KMODEL_PATH=/sdcard/kmodel/face_alignment_post.kmodel
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
with open("/sdcard/FaceRecognition/Face3D/face3d_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Use mode `"a"` to append text to the end of a file:

```python
with open("/sdcard/FaceRecognition/Face3D/face3d_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,mesh_count\n")
```

### open() modes

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. Missing file causes an error. |
| `"w"` | Write from the beginning. Old content is deleted. |
| `"a"` | Append data to the end. Old content is preserved. |

## Files created by example 02

When `02_face3d_file_io.py` runs, it creates this folder:

```text
/sdcard/FaceRecognition/Face3D
```

The folder contains:

```text
face3d_config.txt       # model and writing settings
face3d_last_result.txt  # latest result
face3d_log.csv          # result history
```

Example `face3d_last_result.txt`:

```text
time_ms=123456
fps=8.500
face_count=1
mesh_count=1
first_mesh_len=1434
```

## Why writing is rate-limited

Face 3D Network runs in an infinite loop. Writing to a file every frame would create too many writes to the TF card. The config includes:

```text
WRITE_INTERVAL_MS=1000
```

This means the result is written at most once per second.

## Application scenarios

The PDF lists typical use cases: secure authentication, medical use, AR/VR, smart retail, sentiment analysis, video games and entertainment, telemedicine, and virtual makeup or glasses try-on.

## Tips

1. Use good lighting.
2. Keep the face large enough in the frame.
3. Use `rgb888p_size=[640, 480]` and `display_size=[640, 480]` for correct LCD output.
4. Do not show too many faces at the same time: the model is heavy and the system may freeze.
5. To improve stability, process only the first face: `det_boxes[:1]`.
6. Make sure the board has the fresh file `/sdcard/libs/face3d_common.py`.

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230 Vision Module  
**Repository:** https://github.com/AIDevelopersMonster/K230

# K230: FaceRecognition / RegisterFace

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on **Register for face recognition** — face registration and live face recognition.

The examples follow the PDF **Register for face recognition** and the manufacturer working example. The PDF explains that face recognition has two parts: first you run **Registration** to create a face database from photos, and then you run **Recognition** to recognize faces from the camera.

## Important: the shared file is in `libs`

The shared code is stored as a library:

```text
libs/register_face_common.py
```

On the K230, copy this file to:

```text
/sdcard/libs/register_face_common.py
```

The demos import it like this:

```python
from libs.register_face_common import create_recognition_app, safe_deinit
```

If `register_face_common.py` is placed only next to the examples in `FaceRecognition/RegisterFace`, the import `from libs.register_face_common ...` will not find it.

## Files

| File | Purpose |
| --- | --- |
| `../../libs/register_face_common.py` | Shared library: Face Detection, Face Registration, Face Recognition, database helpers, UART helpers. |
| `01_register_faces_from_folder.py` | Register faces from an image folder. Creates `.bin` feature files. |
| `02_face_recognition_basic.py` | Live face recognition from the camera without UART. |
| `03_face_recognition_uart.py` | Live face recognition with UART output. |
| `04_registerface_file_io.py` | Face registration plus config reading and TXT/CSV report writing. |
| `05_file_read_write_basic.py` | Beginner TXT/CSV/BIN read/write example without AI. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## What RegisterFace demonstrates

Face Recognition has two stages:

```text
Registration → Recognition
```

### 1. Registration

During registration the program:

1. Reads images from a photo folder.
2. Detects a face in each image.
3. Checks that the image contains exactly one face.
4. Uses 5 facial landmarks to align the face through affine transform.
5. Runs `face_recognition.kmodel`.
6. Gets a 128-dimensional feature vector.
7. Saves the feature vector to a `.bin` file.

The `.bin` file name is taken from the photo file name:

```text
/data/photo/register/peter.jpg
→ /data/face_database/register/peter.bin
```

### 2. Recognition

During recognition the program:

1. Loads `.bin` files from the database folder.
2. Gets a frame from the camera.
3. Detects faces.
4. Extracts a feature vector for each face.
5. Compares the feature vector with the database.
6. Draws the result on screen:
   - `unknown` — the face is not in the database;
   - `name: ..., score: ...` — the face is recognized.

## Required files on the TF card

Make sure these files exist on the K230 TF card:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/face_recognition.kmodel
/sdcard/utils/prior_data_320.bin
```

Also copy the shared library:

```text
/sdcard/libs/register_face_common.py
```

## Preparing photos

The PDF recommends taking photos with the K230 first instead of using random images directly. Camera images from K230 may differ from original images because of lighting, the camera sensor, white balance, and other environmental factors. Photos taken with the K230 are better suited for recognition on the same module.

Put photos here:

```text
/data/photo/register/
```

Rename image files to person names:

```text
peter.jpg
alex.jpg
maria.jpg
```

Each registration photo should contain **only one face**. If an image contains multiple faces, that file will be skipped.

## Quick start: registration

1. Copy `libs/register_face_common.py` to the K230:

```text
/sdcard/libs/register_face_common.py
```

2. Put photos in:

```text
/data/photo/register/
```

3. Run:

```text
FaceRecognition/RegisterFace/01_register_faces_from_folder.py
```

4. After successful registration, `.bin` database files will appear, for example:

```text
/data/face_database/register/peter.bin
/data/face_database/register/alex.bin
```

If `PHOTO_DIR` in `01_register_faces_from_folder.py` points to another folder, the database is created in:

```text
/data/face_database/<photo_folder_name>/
```

## Quick start: recognition

1. Check the database path in `02_face_recognition_basic.py`:

```python
"DATABASE_DIR": "/data/face_database/register/"
```

2. Run:

```text
FaceRecognition/RegisterFace/02_face_recognition_basic.py
```

3. Point the camera at a face.
4. If the face exists in the database, the name and score will be shown.
5. If the face is not in the database, the result will be `unknown`.

## UART output

`03_face_recognition_uart.py` sends recognition results through UART.

For an unknown face:

```text
$x,y,w,h,unknown#
```

For a recognized face:

```text
$x,y,w,h,name,score#
```

Where:

| Field | Meaning |
| --- | --- |
| `x, y, w, h` | face rectangle coordinates on a 640x480 display |
| `unknown` | face not found in the database |
| `name` | name from the database `.bin` file |
| `score` | recognition score; higher score means higher confidence |

If Yahboom `YbProtocol` and `YbUart` libraries are available, the demo uses:

```python
pto.get_face_recoginiton_data(x, y, w, h, name, score)
uart.send(pto_data)
```

If UART libraries are unavailable, the packet is printed to the console.

## AI pipeline structure

Registration flow:

```text
Image file → Face Detection → Landmarks → Affine Align → Feature Extract → .bin database
```

Recognition flow:

```text
Sensor → Frame → Face Detection → Feature Extract → Database Search → OSD → Display
```

In live mode, the main loop looks like this:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, recg_res = fr.run(img)
fr.draw_result(pl, det_boxes, recg_res)
pl.show_image()
```

`PipeLine` controls the camera and display, so one program should create only one `PipeLine` object.

## Why pad is used before resize

For the face detection model, preprocessing must preserve the frame aspect ratio:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

If the code only uses `resize`, the face and landmarks may shift, which makes registration and recognition worse.

## Why affine transform is used

For recognition, the face must be aligned to the standard 112x112 position. The code uses 5 facial landmarks and Umeyama alignment:

```python
affine_matrix = self.get_affine_matrix(landm)
self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, affine_matrix)
```

After alignment, `face_recognition.kmodel` extracts the feature vector.

## Face database structure

The face database is a folder with `.bin` files:

```text
/data/face_database/register/
```

Example:

```text
peter.bin
alex.bin
maria.bin
```

Each `.bin` file contains a binary face feature vector. The file name without extension is used as the person name.

## How database search works

For each detected face, the program:

1. Extracts a feature vector.
2. Normalizes it.
3. Compares it with every feature vector in the database using dot product.
4. Converts the score with:

```python
v_score = np.dot(feature, db_feature) / 2 + 0.5
```

5. If the score is below `FACE_RECOGNITION_THRESHOLD`, the result is `unknown`.

You can adjust the threshold in the config or example:

```text
FACE_RECOGNITION_THRESHOLD=0.65
```

## Reading files on K230

Read a text file with `open()` mode `"r"`:

```python
with open("/sdcard/FaceRecognition/RegisterFace/register_face_config.txt", "r") as f:
    text = f.read()
```

`04_registerface_file_io.py` creates this config:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
FACE_RECOGNITION_KMODEL_PATH=/sdcard/kmodel/face_recognition.kmodel
ANCHORS_PATH=/sdcard/utils/prior_data_320.bin
PHOTO_DIR=/data/photo/register/
DATABASE_ROOT=/data/face_database/
DATABASE_DIR=
CONFIDENCE_THRESHOLD=0.50
NMS_THRESHOLD=0.20
FACE_RECOGNITION_THRESHOLD=0.65
```

Parsing a line:

```python
key, value = line.split("=", 1)
cfg[key.strip().upper()] = value.strip()
```

## Writing files on K230

Use mode `"w"` to create or fully replace a text file:

```python
with open("/sdcard/FaceRecognition/RegisterFace/register_face_last_result.txt", "w") as f:
    f.write("success_count=3\n")
```

Use mode `"a"` to append text to the end of a file:

```python
with open("/sdcard/FaceRecognition/RegisterFace/register_face_log.csv", "a") as f:
    f.write("time_ms,photo_dir,success_count,failed_count\n")
```

Use binary mode `"wb"` to write a feature vector:

```python
with open("/data/face_database/register/peter.bin", "wb") as f:
    f.write(reg_result.tobytes())
```

Use binary mode `"rb"` to read a `.bin` feature file:

```python
with open("/data/face_database/register/peter.bin", "rb") as f:
    data = f.read()
```

### open() modes

| Mode | Meaning |
| --- | --- |
| `"r"` | Read a text file. Missing file causes an error. |
| `"w"` | Write a text file from the beginning. Old content is deleted. |
| `"a"` | Append text to the end. Old content is preserved. |
| `"rb"` | Read a binary file. Used for `.bin` feature files. |
| `"wb"` | Write a binary file. Used to save `.bin` feature files. |

## Files created by example 04

When `04_registerface_file_io.py` runs, it creates this folder:

```text
/sdcard/FaceRecognition/RegisterFace
```

The folder contains:

```text
register_face_config.txt       # registration settings
register_face_last_result.txt  # latest report
register_face_log.csv          # run history
```

Example `register_face_last_result.txt`:

```text
time_ms=123456
photo_dir=/data/photo/register/
success_count=3
failed_count=0
```

## ENOENT error

If you see `OSError: [Errno 2] ENOENT`, the folder or file path is wrong or the folder has not been created. The PDF explicitly shows that using the K230 `os` module to access a non-existent directory can terminate the program. The shared module uses `ensure_dir()` to create folders recursively.

## Tips

1. Take registration photos with the K230 camera when possible.
2. Use exactly one face per registration photo.
3. The photo file name becomes the person name in the database.
4. Use good lighting.
5. If many faces are shown as `unknown`, reduce `FACE_RECOGNITION_THRESHOLD`, for example to `0.60`.
6. If false matches appear, increase `FACE_RECOGNITION_THRESHOLD`, for example to `0.70`.
7. Make sure the board has the fresh file `/sdcard/libs/register_face_common.py`.

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230 Vision Module  
**Repository:** https://github.com/AIDevelopersMonster/K230

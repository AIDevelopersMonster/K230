# Line Segment Detection (K230)

## Description

This example demonstrates how to detect line segments using `find_line_segments()` on Yahboom K230 / CanMV.

The folder contains three types of examples:

1. real-time camera processing;
2. synthetic image processing in memory;
3. processing pre-prepared images from the `img` folder.

The `find_line_segments()` function uses the LSD (Line Segment Detector) algorithm and/or Hough transform. It returns a list of `image.line` objects, each containing the start and end coordinates of a segment. The parameters `merge_distance` and `max_theta_diff` control the merging of nearby lines and lines with similar angles.

---

## Folder Structure

```text
Graphics detection/Line segment detection/
├── 01_line_segment_camera.py
├── 02_line_segment_static.py
├── 03_line_segment_from_images.py
├── 04_detect_horizontal_lines.py
├── 05_detect_vertical_lines.py
├── 06_detect_all_lines_overlay.py
├── 07_camera_horizontal_target.py
├── 08_camera_vertical_target.py
├── 09_camera_mixed_classification.py
├── readme.md
├── readme_en.md
└── img/
    ├── horizontal_lines.png
    ├── vertical_lines.png
    ├── vertical_horizontal_lines.png
    └── mixed_lines.png
```

---

## Which Script Uses Which Image

| Script | Source | What it Shows |
|---|---|---|
| `01_line_segment_camera.py` | camera | Real-time detection of all lines from camera |
| `02_line_segment_static.py` | memory | Educational example: draws lines in memory and detects them |
| `03_line_segment_from_images.py` | PNG file | Universal example: can detect all, only horizontal, or only vertical lines |
| `04_detect_horizontal_lines.py` | `img/horizontal_lines.png` | Detects only horizontal lines on a static image |
| `05_detect_vertical_lines.py` | `img/vertical_lines.png` | Detects only vertical lines on a static image |
| `06_detect_all_lines_overlay.py` | `img/mixed_lines.png` | Detects all lines and colors them: horizontal, vertical, diagonal |
| `07_camera_horizontal_target.py` | camera | Real-time detection of ONLY horizontal lines |
| `08_camera_vertical_target.py` | camera | Real-time detection of ONLY vertical lines |
| `09_camera_mixed_classification.py` | camera | Real-time classification of all lines (horizontal/vertical/diagonal) |

**Colors in Examples:**

- **green** — horizontal lines;
- **red** — vertical lines;
- **blue** — diagonal lines;
- **yellow text** — number of detected lines.

---

## Where to Put Images

On your computer, images are located in the repository:

```text
Graphics detection/Line segment detection/img/
```

On the K230 board, copy them to the SD card at the same path:

```text
/sdcard/Graphics detection/Line segment detection/img/
```

If the path is different, modify the `IMAGE_PATH` variable in the required script:

```python
IMAGE_PATH = "/sdcard/your_path/img/vertical_horizontal_lines.png"
```

---

## How to Run

### Camera Examples

1. Connect the camera to K230
2. Run one of the scripts:
   - `01_line_segment_camera.py` — detect all lines
   - `07_camera_horizontal_target.py` — only horizontal lines
   - `08_camera_vertical_target.py` — only vertical lines
   - `09_camera_mixed_classification.py` — classify all types
3. Point the camera at an object with clear lines

### Image Examples

1. Copy the `img` folder to the K230 SD card
2. Open the script in CanMV IDE
3. Check the `IMAGE_PATH` variable
4. Run the script

### Static Example

Run `02_line_segment_static.py` — it requires neither camera nor SD card.

---

## Configuring the Universal Script

In `03_line_segment_from_images.py`, you can change the detection mode:

```python
DETECT_MODE = "all"        # detect all lines
DETECT_MODE = "horizontal" # detect only horizontal lines
DETECT_MODE = "vertical"   # detect only vertical lines
```

You can also change the image:

```python
IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/mixed_lines.png"
```

---

## Main API

```python
lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)
```

**Parameters:**

- `merge_distance` — maximum distance between two segments for merging (in pixels);
- `max_theta_diff` — maximum angle difference for merging segments (in degrees).

**Result:**

- list of line objects;
- line coordinates can be obtained via `line.line()` → `(x1, y1, x2, y2)`.

**Usage Example:**

```python
for line in lines:
    coords = line.line()
    img.draw_line(coords, color=(0, 255, 0), thickness=3)
```

---

## Reading and Writing Files

### Reading a Text File

```python
with open("/sdcard/data.txt", "r") as f:
    data = f.read()
print(data)
```

### Writing a Text File

```python
with open("/sdcard/result.txt", "w") as f:
    f.write("Hello K230")
```

### Example: Writing Line Coordinates

```python
with open("/sdcard/lines.csv", "w") as f:
    f.write("x1,y1,x2,y2\n")
    for line in lines:
        x1, y1, x2, y2 = line.line()
        f.write("%d,%d,%d,%d\n" % (x1, y1, x2, y2))
```

---

## If the Image Does Not Open

Check:

1. the file is actually on the SD card;
2. the filename matches `IMAGE_PATH`;
3. the `.png` extension is correct;
4. the path does not contain extra spaces;
5. the image has a valid format, preferably `PNG`, `640x480`.

---

## If Lines Are Not Detected

Try:

- making lines thicker: 3–6 pixels;
- using white lines on a black background;
- increasing `merge_distance`;
- increasing `ANGLE_TOLERANCE_DEG` for horizontal/vertical filtering;
- ensuring lines do not touch the image edge;
- providing good lighting when working with the camera;
- removing glare and reflections.

---

## Tips for Working with Camera

1. **Lighting**: ensure uniform illumination of the object
2. **Contrast**: use high-contrast objects
3. **Distance**: find the optimal distance to the object
4. **Angle**: keep the camera perpendicular to the object plane
5. **Stability**: mount the camera for stable imaging

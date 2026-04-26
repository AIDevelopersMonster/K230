# Line Segment Detection (K230)

## 📋 Description

This folder contains practical examples of detecting line segments using `find_line_segments()` on Yahboom K230.

There are two types of demos:

1. Camera-based (real-time)
2. Image-based (from prepared test images in `img` folder)

According to documentation, `find_line_segments()` uses LSD and Hough Transform, and parameters like `merge_distance` and `max_theta_diff` control merging of segments. fileciteturn0file0

---

## 📂 Folder structure

```
Graphics detection/Line segment detection/
├── 01_line_segment_camera.py
├── 02_line_segment_static.py
├── 03_line_segment_from_images.py
├── 04_detect_horizontal_lines.py
├── 05_detect_vertical_lines.py
├── 06_detect_all_lines_overlay.py
├── readme.md
├── readme_en.md
└── img/
    ├── horizontal_lines.png
    ├── vertical_lines.png
    ├── vertical_horizontal_lines.png
    └── mixed_lines.png
```

---

## 🧪 Script ↔ Image mapping

| Script | Image | Description |
|-------|------|------------|
| 01_line_segment_camera.py | camera | Real-time detection |
| 02_line_segment_static.py | none | Synthetic demo (draws lines in memory) |
| 03_line_segment_from_images.py | configurable | Universal demo (all / horizontal / vertical) |
| 04_detect_horizontal_lines.py | horizontal_lines.png | Detect horizontal lines |
| 05_detect_vertical_lines.py | vertical_lines.png | Detect vertical lines |
| 06_detect_all_lines_overlay.py | mixed_lines.png | Classify all lines (H/V/other) |

Color meaning:
- green → horizontal
- red → vertical
- blue → angled

---

## 📁 Where to put images

Copy images to SD card:

```
/sdcard/Graphics detection/Line segment detection/img/
```

Update path if needed:

```python
IMAGE_PATH = "/sdcard/.../img/mixed_lines.png"
```

---

## ▶️ How to run

### Camera demo
Run:
```
01_line_segment_camera.py
```

### Image demo
1. Copy images to SD card
2. Open script in IDE
3. Check IMAGE_PATH
4. Run

---

## ⚙️ Universal script settings

In `03_line_segment_from_images.py`:

```python
DETECT_MODE = "all"
```

Options:
```
all
horizontal
vertical
```

---

## 🧠 API

```python
lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)
```

---

## 📂 File read/write

Read:
```python
with open("/sdcard/data.txt", "r") as f:
    data = f.read()
```

Write:
```python
with open("/sdcard/data.txt", "w") as f:
    f.write("Hello")
```

---

## ❗ Troubleshooting

### Image not loading
- check SD path
- check filename
- use PNG 640x480

### Lines not detected
- increase line thickness
- use high contrast (white on black)
- tune merge_distance
- tune angle tolerance

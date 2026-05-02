# K230: AprilTag Recognition

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on AprilTag recognition. The K230 camera captures an image, detects tags with `img.find_apriltags()`, and reads the tag family, ID, bounding box, center point, and rotation angle.

AprilTag is a two-dimensional visual marker often used in robotics, navigation, augmented reality, camera calibration, and visual positioning. Unlike a QR code, an AprilTag usually encodes a numeric ID and is well suited for position and orientation detection.

## Files

| File | Purpose |
| --- | --- |
| `01_apriltag_recognition.py` | Basic demo: detect AprilTag, draw rectangle and center, show family, ID, rotation, and FPS. |
| `02_apriltag_uart.py` | AprilTag recognition plus sending coordinates, ID, and rotation through UART/Yahboom protocol. |
| `03_apriltag_file_io.py` | AprilTag recognition plus reading ROI/families from a file and writing the result to a file. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## Quick start

1. Prepare an AprilTag. You can use the Yahboom tag files or the AprilTag generator in CanMV IDE.
2. Open `01_apriltag_recognition.py` in CanMV IDE.
3. Connect the K230 board to your computer through USB.
4. Run the script.
5. Point the camera at the AprilTag and keep it clear and in focus.
6. The screen will show a red rectangle around the tag, a green cross in the center, and text with the family, ID, and rotation angle.
7. The CanMV IDE console will print a line like:

```text
Tag Family TAG36H11, Tag ID 0, rotation 2.836 degrees
```

## How AprilTag recognition works

The main function is:

```python
tags = img.find_apriltags(families=tag_families)
```

It returns a list of `image.apriltag` objects. For each detected tag, you can get:

```python
tag.rect()             # (x, y, w, h), tag bounding box
tag.id()               # numeric ID inside the family
tag.family()           # tag family
tag.cx(), tag.cy()     # tag center
tag.rotation()         # rotation angle in radians
tag.decision_margin()  # detection confidence
tag.hamming()          # accepted/corrected Hamming error
```

Drawing the rectangle and center:

```python
img.draw_rectangle(tag.rect(), color=(255, 0, 0), thickness=4)
img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0), thickness=2)
```

Converting rotation to degrees:

```python
rotation_deg = (180.0 * tag.rotation()) / math.pi
```

## AprilTag families

The examples can enable different tag families:

```python
tag_families = 0
tag_families |= image.TAG16H5
tag_families |= image.TAG25H7
tag_families |= image.TAG25H9
tag_families |= image.TAG36H10
tag_families |= image.TAG36H11
tag_families |= image.ARTOOLKIT
```

The more families are enabled at the same time, the lower the FPS may be. For most demonstrations, `TAG36H11` is a good choice.

## ROI: faster detection

By default, the example scans the whole frame:

```python
APRILTAG_ROI = None
```

To make detection faster, you can scan only a selected area:

```python
APRILTAG_ROI = (40, 20, 320, 200)
```

ROI format:

```python
(x, y, w, h)
```

If the tag is always near the center of the image, ROI can improve FPS.

## UART example

`02_apriltag_uart.py` sends data through the Yahboom protocol:

```python
pto_data = pto.get_apriltag_data(x, y, w, h, tag.id(), rotation_deg)
uart.send(pto_data)
```

UART is initialized with:

```python
uart = YbUart(baudrate=115200)
```

If your firmware does not include `libs.YbProtocol` or `ybUtils.YbUart`, the example disables UART and continues recognition on the screen.

## Reading files on K230

`03_apriltag_file_io.py` demonstrates reading settings from a text file.

File name:

```text
apriltag_config.txt
```

Example content:

```text
# K230 AprilTag Recognition config
USE_ROI=0
ROI=40,20,320,200
FAMILIES=TAG36H11
```

Reading the file:

```python
with open("/sdcard/apriltag_config.txt", "r") as f:
    text = f.read()
```

Parsing one config line:

```python
key, value = line.split("=", 1)
```

Parsing ROI:

```python
parts = value.replace(" ", "").split(",")
roi = tuple([int(v) for v in parts])
```

Parsing families:

```text
FAMILIES=TAG16H5,TAG25H7,TAG36H11
```

On CanMV/K230, a relative path may not be writable when the script is started from IDE. Therefore, the demo first searches for a writable directory:

```python
FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
```

If the file system is not writable, the demo continues with default values.

## Writing files on K230

Text writing uses `open(..., "w")`:

```python
with open("/sdcard/apriltag_result.txt", "w") as f:
    f.write("family=TAG36H11\nid=0\n")
```

Open modes:

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. |
| `"w"` | Write and replace old content. If the file does not exist, it is created. |
| `"a"` | Append text to the end of the file. |

The result file `apriltag_result.txt` is updated when a tag is recognized:

```text
time_ms=123456
fps=45.500
family=TAG36H11
id=0
rotation_deg=2.836
x=120
y=70
w=95
h=95
cx=167
cy=117
decision_margin=48.2
hamming=0
```

Why not write every frame: the same tag may be recognized many times in a row, so the example rate-limits file writes.

## Tips for good recognition

1. Use a clearly printed AprilTag with high contrast.
2. Keep the tag in focus.
3. Remove glare and strong shadows.
4. Do not make the tag too small in the frame.
5. For better FPS, enable only the needed family, for example `TAG36H11`.
6. Use ROI if the tag is always in one area of the frame.
7. If there is strong perspective distortion or poor lighting, increase tag size or improve lighting.

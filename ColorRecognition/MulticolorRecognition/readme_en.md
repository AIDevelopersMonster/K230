# K230: Multicolor Recognition

This folder contains demonstration examples for the **Yahboom K230 Vision Module**. The camera detects several colors in one frame, draws rectangles around detected regions, labels each color, and displays FPS.

This topic is based on the **Multicolor Recognition** lesson: after learning single-color recognition, the program applies several LAB color thresholds to the same camera frame. This makes it possible to detect red, green, and blue objects at the same time.

## Files

| File | Purpose |
| --- | --- |
| `01_multicolor_recognition.py` | Basic demo: detect RED, GREEN, and BLUE from the camera. |
| `02_multicolor_uart.py` | Multicolor recognition plus sending detected object data over UART with the Yahboom protocol. |
| `03_multicolor_file_io.py` | Multicolor recognition plus reading LAB thresholds from a file and writing results to a file. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## Quick start

1. Open `01_multicolor_recognition.py` in CanMV IDE.
2. Connect the K230 board to your computer.
3. Point the camera at red, green, or blue objects.
4. Run the script.
5. The screen will show rectangles, labels `RED`, `GREEN`, `BLUE`, FPS, and per-color counters.

## How multicolor recognition works

Each color has its own LAB threshold:

```python
COLOR_THRESHOLDS = [
    (0, 66, 7, 127, 3, 127),          # RED
    (42, 100, -128, -17, 6, 66),      # GREEN
    (43, 99, -43, -4, -56, -7),       # BLUE
]
```

Each threshold has this format:

```python
(L_min, L_max, A_min, A_max, B_min, B_max)
```

In the main loop, the program captures one frame and checks it against every color threshold:

```python
for i in range(len(COLOR_THRESHOLDS)):
    counts[i] = process_color(img, i)
```

Inside `process_color()`, the detection call is:

```python
blobs = img.find_blobs([threshold], pixels_threshold=50, area_threshold=500, merge=True)
```

For every detected blob, the program draws a rectangle, a center cross, and a text label.

## UART example

`02_multicolor_uart.py` shows how to send detected object coordinates over UART:

```python
pto_data = pto.get_multi_color_data(x, y, w, h, label)
uart.send(pto_data)
```

The UART baud rate is:

```python
YbUart(baudrate=115200)
```

If your firmware does not include `libs.YbProtocol` or `ybUtils.YbUart`, the example disables UART and continues camera recognition on the screen.

## Reading files on K230

`03_multicolor_file_io.py` demonstrates reading LAB thresholds from a text file.

File name:

```text
multicolor_thresholds.txt
```

Example content:

```text
RED:0,66,7,127,3,127
GREEN:42,100,-128,-17,6,66
BLUE:43,99,-43,-4,-56,-7
```

Reading the file:

```python
with open("/sdcard/multicolor_thresholds.txt", "r") as f:
    text = f.read()
```

Parsing a line:

```python
label, values_text = line.split(":", 1)
parts = values_text.replace(" ", "").split(",")
threshold = tuple([int(v) for v in parts])
```

On CanMV/K230, a relative path may be unavailable for writing when the script is started from IDE. Therefore, the demo first searches for a writable directory:

```python
FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
```

If no writable directory is available, the demo continues using default thresholds.

## Writing files on K230

Text writing uses `open(..., "w")`:

```python
with open("/sdcard/multicolor_result.txt", "w") as f:
    f.write("RED=1\nGREEN=0\nBLUE=2\n")
```

Open modes:

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. |
| `"w"` | Write and replace old content. If the file does not exist, it is created. |
| `"a"` | Append text to the end of the file. |

The result file `multicolor_result.txt` is updated about once per second:

```text
fps=62.500
time_ms=123456
RED=1
GREEN=0
BLUE=2
total=3
```

Why not write every frame: the camera runs quickly, and constant file writes are usually unnecessary. It is better to write periodically or only when data changes.

## Accuracy tuning

If recognition is not good:

1. Improve lighting.
2. Remove glare and shadows.
3. Use CanMV Threshold Editor to tune LAB thresholds.
4. Increase `pixels_threshold` and `area_threshold` if there is noise.
5. Decrease `area_threshold` if small objects are not detected.
6. Make sure the object color is different enough from the background.

## Program structure

1. Import modules.
2. Define display size and LAB thresholds.
3. Initialize the camera and display.
4. Main loop:
   - capture a frame;
   - loop through the color list;
   - find color blobs with `find_blobs()`;
   - draw rectangles, center crosses, and labels;
   - show FPS and counters;
   - display the image.
5. Handle errors and release resources.

## How to add your own color

Add a new LAB threshold, rectangle color, and label:

```python
COLOR_THRESHOLDS.append((37, 100, -128, 127, -128, -27))
DRAW_COLORS.append((0, 255, 255))
COLOR_LABELS.append("CYAN")
```

In `03_multicolor_file_io.py`, you can also add a new line to `multicolor_thresholds.txt`:

```text
CYAN:37,100,-128,127,-128,-27
```

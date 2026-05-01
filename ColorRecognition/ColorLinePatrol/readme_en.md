# K230: Color Line Patrol

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on color line patrol. The camera detects a line of a selected color in the lower part of the frame, calculates the line offset from the screen center, and, in the extended example, sends motor commands through UART.

Main idea: the line is detected as a color blob with `img.find_blobs()`. The largest detected blob is selected, its center is calculated, and the difference between the screen center and the line center becomes the control error. A PID controller can then calculate different speeds for the left and right motors.

## Files

| File | Purpose |
| --- | --- |
| `01_color_line_patrol.py` | Safe visual demo: line detection, bounding box, line center, and offset error. UART and motors are not used. |
| `02_color_line_patrol_uart_pid.py` | Line patrol demo with UART and PID, sending `$left,right#` commands. |
| `03_color_line_patrol_file_io.py` | Demo for reading settings from a file and writing results to a file. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## Quick start

1. Open `01_color_line_patrol.py` in CanMV IDE.
2. Connect the K230 board to your computer.
3. Prepare a line on a light background, for example a green or black strip.
4. Point the camera so the line appears in the lower half of the image.
5. Run the script.
6. The screen will show:
   - a gray ROI rectangle, the area where the line is searched;
   - a green vertical line, the screen center;
   - a red vertical line, the detected line center;
   - a rectangle around the detected line;
   - the `error` value.

## How line detection works

The examples use LAB thresholds:

```python
THRESHOLDS = [
    (21, 33, -15, 9, -9, 6),       # BLACK
    (40, 86, -44, -20, -24, 25),   # GREEN
]
```

Each threshold has this format:

```python
(L_min, L_max, A_min, A_max, B_min, B_max)
```

Detection is limited to the lower half of the image:

```python
ROI = (0, DISPLAY_HEIGHT // 2, DISPLAY_WIDTH, DISPLAY_HEIGHT // 2)
```

This is useful for a line-following robot because the line is usually closer to the bottom of the camera frame.

The main detection call is:

```python
blobs = img.find_blobs([threshold], roi=ROI, pixels_threshold=80, area_threshold=80, merge=True)
```

The largest region is selected:

```python
largest_blob = max(blobs, key=lambda b: b[4])
```

Then the line center is calculated:

```python
current_x = x + w // 2
error = SCREEN_CENTER - current_x
```

If `error` is close to zero, the line is near the center. If it is positive or negative, the line is shifted left or right.

## PID and UART

`02_color_line_patrol_uart_pid.py` demonstrates PID control.

PID parameters:

```python
KP = 1.0
KI = 0.1
KD = 0.2
BASE_SPEED = 300
```

Speed calculation:

```python
output = KP * error + KI * integral + KD * derivative
left_speed = BASE_SPEED - output
right_speed = BASE_SPEED + output
```

The command is sent over UART in this format:

```text
$left,right#
```

Example:

```text
$280,320#
```

If no line is detected, the stop command is sent:

```text
$0,0#
```

UART is initialized with:

```python
uart = YbUart(9600)
```

If `ybUtils.YbUart` is missing in your firmware, the example disables UART and continues showing visual debug information on the screen.

## Reading files on K230

`03_color_line_patrol_file_io.py` demonstrates reading settings from a text file.

File name:

```text
line_patrol_config.txt
```

Example content:

```text
# K230 Color Line Patrol config
COLOR=GREEN
THRESHOLD=40,86,-44,-20,-24,25
KP=1.0
KI=0.1
KD=0.2
BASE_SPEED=300
```

Reading the file:

```python
with open("/sdcard/line_patrol_config.txt", "r") as f:
    text = f.read()
```

Parsing one config line:

```python
key, value = line.split("=", 1)
```

Parsing a LAB threshold:

```python
parts = value.replace(" ", "").split(",")
threshold = tuple([int(v) for v in parts])
```

On CanMV/K230, a relative path may not be writable when the script is started from IDE. Therefore, the demo first searches for a writable directory:

```python
FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
```

If the file system is not writable, the demo continues with default values.

## Writing files on K230

Text writing uses `open(..., "w")`:

```python
with open("/sdcard/line_patrol_result.txt", "w") as f:
    f.write("error=0\n")
```

Open modes:

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. |
| `"w"` | Write and replace old content. If the file does not exist, it is created. |
| `"a"` | Append text to the end of the file. |

The result file `line_patrol_result.txt` is updated about once per second:

```text
time_ms=123456
fps=55.300
found=True
color=GREEN
error=-12
left_speed=312
right_speed=288
```

Why not write every frame: the camera runs quickly, and constant file writes are usually unnecessary. It is better to write periodically.

## Accuracy tuning

If the line is not detected well:

1. Improve lighting.
2. Remove glare and shadows.
3. Use a background with strong contrast against the line.
4. Tune the LAB threshold with CanMV Threshold Editor.
5. Increase `pixels_threshold` and `area_threshold` if there is noise.
6. Decrease `area_threshold` if a thin line is not detected.
7. Check the ROI: the line must be in the lower half of the frame.

## PID tuning

If the robot turns too sharply, decrease `KP`.

If the robot returns to the line too slowly, increase `KP`.

If there is a constant offset, carefully increase `KI`.

If movement is jerky, adjust `KD` or reduce the base speed.

Start testing with low speed values and check the commands without motors or with the robot lifted.

## How to select another line color

In `01_color_line_patrol.py` and `02_color_line_patrol_uart_pid.py`, change:

```python
COLOR_INDEX = 0  # BLACK
COLOR_INDEX = 1  # GREEN
```

In `03_color_line_patrol_file_io.py`, edit `line_patrol_config.txt`:

```text
COLOR=BLACK
```

or set your own LAB threshold:

```text
THRESHOLD=21,33,-15,9,-9,6
```

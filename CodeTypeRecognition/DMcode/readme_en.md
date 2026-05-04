# K230: DM Code / Data Matrix Recognition

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on **DM code / Data Matrix** recognition. The K230 camera captures an image, detects Data Matrix codes with `img.find_datamatrices()`, extracts the decoded `payload`, calculates the rotation angle, and displays the result on the screen.

DM code, or Data Matrix, is a two-dimensional code made of black and white cells. It is often used for industrial marking, small part traceability, and applications where the code must fit into a small area.

## Files

| File | Purpose |
| --- | --- |
| `01_dmcode_recognition.py` | Basic demo: detect Data Matrix, draw rectangle, show payload, rotation, and FPS. |
| `02_dmcode_uart.py` | Data Matrix recognition plus sending coordinates, payload, and rotation through UART/Yahboom protocol. |
| `03_dmcode_file_io.py` | Data Matrix recognition plus reading ROI from a file and writing the result to a file. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## Quick start

1. Generate a DM code / Data Matrix. You can use the Yahboom generator or any online Data Matrix generator.
2. Open `01_dmcode_recognition.py` in CanMV IDE.
3. Connect the K230 board to your computer through USB.
4. Run the script.
5. Point the camera at the DM code and keep it large, flat, and in focus.
6. The screen will show a red rectangle, payload, and rotation angle.
7. The CanMV IDE console will print a line like:

```text
payload "Hi, Yahboom", rotation 3.000 degrees
```

## How Data Matrix recognition works

The main function is:

```python
matrices = img.find_datamatrices()
```

It returns a list of detected Data Matrix objects. For each detected code, the examples use:

```python
matrix.rect()       # (x, y, w, h), code bounding box
matrix.payload()    # decoded text
matrix.rotation()   # rotation angle in radians
```

Drawing a rectangle:

```python
img.draw_rectangle(matrix.rect(), color=(255, 0, 0), thickness=4)
```

Drawing payload and rotation:

```python
rotation = (180.0 * matrix.rotation()) / math.pi
img.draw_string_advanced(x, y, 20, "%s [%.2f] deg" % (payload, rotation), color=(255, 0, 0))
```

## DM code and QR code

DM code and QR code are both two-dimensional codes, but they are often used differently:

| Feature | DM code / Data Matrix | QR code |
| --- | --- | --- |
| Appearance | Solid L-shaped border | Three large position markers |
| Size | Can be very small | Usually needs more space |
| Use cases | Industrial marking, small parts | Links, payments, marketing, general data |
| Robustness | Can still be read when partially damaged | Also supports error correction |

The PDF notes that the recognition success rate of DM codes may be lower than QR codes. If a code is not recognized, try rotating the code or the camera.

## ROI: faster detection

By default, the example scans the whole frame:

```python
DMCODE_ROI = None
```

To make detection faster, you can scan only a selected area:

```python
DMCODE_ROI = (160, 80, 320, 320)
```

ROI format:

```python
(x, y, w, h)
```

If the DM code is always near the center of the frame, ROI can improve FPS.

## UART example

`02_dmcode_uart.py` sends data through the Yahboom protocol:

```python
pto_data = pto.get_dmcode_data(x, y, w, h, payload, rotation)
uart.send(pto_data)
```

UART is initialized with:

```python
uart = YbUart(baudrate=115200)
```

If your firmware does not include `libs.YbProtocol` or `ybUtils.YbUart`, the example disables UART and continues recognition on the screen.

## Reading files on K230

`03_dmcode_file_io.py` demonstrates reading settings from a text file.

File name:

```text
dmcode_config.txt
```

Example content:

```text
# K230 Data Matrix / DM Code Recognition config
USE_ROI=0
ROI=160,80,320,320
```

Reading the file:

```python
with open("/sdcard/dmcode_config.txt", "r") as f:
    text = f.read()
```

Parsing a config line:

```python
key, value = line.split("=", 1)
```

Parsing ROI:

```python
parts = value.replace(" ", "").split(",")
roi = tuple([int(v) for v in parts])
```

On CanMV/K230, a relative path may not be writable when the script is started from IDE. Therefore, the demo first searches for a writable directory:

```python
FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
```

If the file system is not writable, the demo continues with default values.

## Writing files on K230

Text writing uses `open(..., "w")`:

```python
with open("/sdcard/dmcode_result.txt", "w") as f:
    f.write("payload=Hi, Yahboom\n")
```

Open modes:

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. |
| `"w"` | Write and replace old content. If the file does not exist, it is created. |
| `"a"` | Append text to the end of the file. |

The result file `dmcode_result.txt` is updated when a Data Matrix code is recognized:

```text
time_ms=123456
fps=28.500
payload=Hi, Yahboom
rotation_deg=3.000
x=190
y=120
w=180
h=180
```

Why not write every frame: the same DM code may be recognized many times in a row, so the example rate-limits file writes.

## Tips for good recognition

1. Keep the DM code in focus.
2. Use good contrast: black code on a white background.
3. Remove glare from the screen or paper.
4. Make the code large enough in the frame.
5. If the code is not recognized, try rotating the code or the camera.
6. Use ROI if the code always appears in one area of the frame.
7. Try `Sensor.GRAYSCALE` if RGB565 is unstable in your lighting conditions.

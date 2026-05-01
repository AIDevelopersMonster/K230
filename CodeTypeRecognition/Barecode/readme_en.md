# K230: Barcode Recognition

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on 1D barcode recognition. The K230 camera captures an image, detects barcodes with `img.find_barcodes()`, identifies the barcode type, extracts the decoded `payload`, and displays the result on the screen.

> The folder name is `Barecode` because it was requested that way. The correct English term is `Barcode`.

## Files

| File | Purpose |
| --- | --- |
| `01_barcode_recognition.py` | Basic demo: detect a barcode, draw a rectangle, show type, payload, and FPS. |
| `02_barcode_uart.py` | Barcode recognition plus sending data through UART/Yahboom protocol. |
| `03_barcode_file_io.py` | Barcode recognition plus reading ROI settings from a file and writing the result to a file. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## Quick start

1. Generate a 1D barcode. You can use the Yahboom barcode generator or any online barcode generator.
2. Open `01_barcode_recognition.py` in CanMV IDE.
3. Connect the K230 board to your computer through USB.
4. Run the script.
5. Point the camera at the barcode and make sure it is in focus.
6. The screen will show a rectangle around the barcode, the barcode type, and the decoded text.
7. The CanMV IDE console will print a line like:

```text
Barcode CODE128, Payload "What can I say"
```

## How barcode recognition works

The main function is:

```python
codes = img.find_barcodes()
```

It returns a list of `image.barcode` objects. For each detected barcode, you can get:

```python
code.rect()      # (x, y, w, h), barcode bounding box
code.payload()   # decoded text or number
code.type()      # barcode type
code.rotation()  # rotation angle
code.quality()   # quality / number of successful detections
```

Drawing a rectangle:

```python
img.draw_rectangle(code.rect(), thickness=6, color=(46, 47, 48))
```

Drawing decoded text:

```python
img.draw_string_advanced(10, 10, 28, "Data: " + payload, color=(255, 255, 255))
```

## Supported barcode types

The examples include a `BARCODE_TYPES` dictionary that converts numeric barcode types into readable names:

```python
BARCODE_TYPES = {
    image.EAN13: "EAN13",
    image.ISBN13: "ISBN13",
    image.CODE39: "CODE39",
    image.CODE93: "CODE93",
    image.CODE128: "CODE128",
}
```

The full code includes EAN2, EAN5, EAN8, UPCE, ISBN10, UPCA, EAN13, ISBN13, I25, DATABAR, CODABAR, CODE39, PDF417, CODE93, and CODE128.

## ROI: faster detection

By default, the example scans the whole frame:

```python
BARCODE_ROI = None
```

To make detection faster, you can scan only a horizontal region in the middle of the frame:

```python
BARCODE_ROI = (0, 200, 640, 80)
```

ROI format:

```python
(x, y, w, h)
```

Barcodes are linear images, so it is often enough to scan a narrow strip of 40, 80, or 160 pixels high if the barcode is inside that area.

## UART example

`02_barcode_uart.py` sends data through the Yahboom protocol:

```python
pto_data = pto.get_barcode_data(x, y, w, h, payload)
uart.send(pto_data)
```

UART is initialized with:

```python
uart = YbUart(baudrate=115200)
```

If your firmware does not include `libs.YbProtocol` or `ybUtils.YbUart`, the example disables UART and continues recognition on the screen.

## Reading files on K230

`03_barcode_file_io.py` demonstrates reading settings from a text file.

File name:

```text
barcode_config.txt
```

Example content:

```text
# K230 Barcode Recognition config
USE_ROI=0
ROI=0,200,640,80
```

Reading the file:

```python
with open("/sdcard/barcode_config.txt", "r") as f:
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
with open("/sdcard/barcode_result.txt", "w") as f:
    f.write("payload=What can I say\n")
```

Open modes:

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. |
| `"w"` | Write and replace old content. If the file does not exist, it is created. |
| `"a"` | Append text to the end of the file. |

The result file `barcode_result.txt` is updated when a barcode is recognized:

```text
time_ms=123456
fps=32.500
type=CODE128
payload=What can I say
x=102
y=180
w=420
h=90
```

Why not write every frame: the same barcode may be recognized many times in a row, so the example rate-limits file writes.

## Tips for good recognition

1. Keep the barcode in focus.
2. Remove glare from the screen or paper.
3. Make the barcode large enough in the frame.
4. Use good contrast: black bars on a white background.
5. Use ROI if the frame rate is low.
6. Do not use compressed or Bayer images with `find_barcodes()`.
7. If the barcode is not decoded, try rotating the camera or increasing barcode size.

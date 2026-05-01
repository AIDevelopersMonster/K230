# K230: QR Code Recognition

This folder contains demonstration examples for the **Yahboom K230 Vision Module** on QR code recognition. The K230 camera captures an image, detects QR codes with `img.find_qrcodes()`, extracts the decoded `payload`, and displays the result on the screen.

A QR code differs from a standard barcode because it stores data in a two-dimensional matrix. QR codes usually have a larger capacity, can store URLs, text, and other data, and support error correction levels.

## Files

| File | Purpose |
| --- | --- |
| `01_qrcode_recognition.py` | Basic demo: detect a QR code, draw a rectangle, show payload and FPS. |
| `02_qrcode_uart.py` | QR code recognition plus sending data through UART/Yahboom protocol. |
| `03_qrcode_file_io.py` | QR code recognition plus reading ROI settings from a file and writing the result to a file. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## Quick start

1. Generate a QR code. You can use the Yahboom QR Code Generator or any online QR code generator.
2. Open `01_qrcode_recognition.py` in CanMV IDE.
3. Connect the K230 board to your computer through USB.
4. Run the script.
5. Point the camera at the QR code and make sure it is large, flat, and in focus.
6. The screen will show a rectangle around the QR code and the decoded content.
7. The CanMV IDE console will print the QR code payload.

## How QR code recognition works

The main function is:

```python
qr_codes = img.find_qrcodes()
```

It returns a list of `image.qrcode` objects. For each detected QR code, you can get:

```python
qr.rect()             # (x, y, w, h), QR code bounding box
qr.payload()          # text, URL, or other decoded data
qr.version()          # QR code version
qr.ecc_level()        # error correction level
qr.mask()             # QR code mask
qr.data_type()        # data type
qr.eci()              # encoding indicator
qr.is_numeric()       # True if data is numeric
qr.is_alphanumeric()  # True if data is alphanumeric
qr.is_binary()        # True if data is binary
qr.is_kanji()         # True if data is Kanji
```

Drawing a rectangle:

```python
img.draw_rectangle(qr.rect(), thickness=3, color=(200, 0, 0))
```

Drawing the payload on the screen:

```python
img.draw_string_advanced(0, 0, 26, "QR: " + qr.payload(), color=(255, 255, 255))
```

## ROI: faster detection

By default, the example scans the whole frame:

```python
QRCODE_ROI = None
```

To make detection faster, you can scan only a selected area:

```python
QRCODE_ROI = (120, 60, 400, 360)
```

ROI format:

```python
(x, y, w, h)
```

If the QR code is always near the center of the image, ROI can improve FPS.

## UART example

`02_qrcode_uart.py` sends data through the Yahboom protocol:

```python
pto_data = pto.get_qrcode_data(x, y, w, h, payload)
uart.send(pto_data)
```

UART is initialized with:

```python
uart = YbUart(baudrate=115200)
```

If your firmware does not include `libs.YbProtocol` or `ybUtils.YbUart`, the example disables UART and continues recognition on the screen.

## Reading files on K230

`03_qrcode_file_io.py` demonstrates reading settings from a text file.

File name:

```text
qrcode_config.txt
```

Example content:

```text
# K230 QR Code Recognition config
USE_ROI=0
ROI=120,60,400,360
```

Reading the file:

```python
with open("/sdcard/qrcode_config.txt", "r") as f:
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
with open("/sdcard/qrcode_result.txt", "w") as f:
    f.write("payload=Yahboom Technology Co.,Ltd\n")
```

Open modes:

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. |
| `"w"` | Write and replace old content. If the file does not exist, it is created. |
| `"a"` | Append text to the end of the file. |

The result file `qrcode_result.txt` is updated when a QR code is recognized:

```text
time_ms=123456
fps=28.500
payload=Yahboom Technology Co.,Ltd
x=180
y=90
w=240
h=240
version=3
ecc_level=3
data_type=2
```

Why not write every frame: the same QR code may be recognized many times in a row, so the example rate-limits file writes.

## QR code error correction level

QR codes support error correction levels L, M, Q, and H. A higher level can tolerate more damage or noise, but the QR pattern becomes denser. For demonstrations, a high level such as H is useful if the QR code may be partially covered or noisy.

## Tips for good recognition

1. Keep the QR code in focus.
2. Avoid strong tilt and perspective distortion.
3. Remove glare from the screen or paper.
4. Make the QR code large enough in the frame.
5. Use good contrast: black QR code on a white background.
6. Use ROI if the frame rate is low.
7. If the QR code is not decoded, increase QR size or improve lighting.

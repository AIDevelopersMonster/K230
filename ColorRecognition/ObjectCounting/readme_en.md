# K230: Object Counting by Color

This folder contains demonstration examples for the Yahboom K230 Vision Module. The camera detects objects with a similar color, draws a rectangle around every detected object, and displays the number of objects on the screen.

The examples are based on the **Object counting** lesson. The lesson suggests using the Yahboom **Generate Random Number of Coins** tool, generating an image with coins, running the example, and pointing the camera at the generated image. The top-left corner of the screen shows FPS and the number of detected coins.

## Files

| File | Purpose |
| --- | --- |
| `01_object_counting_coins.py` | Basic object counting example using a LAB color threshold. |
| `02_object_counting_file_io.py` | Object counting plus reading the LAB threshold from a file and writing the result to a file. |
| `readme.md` | Russian instructions. |
| `readme_en.md` | English instructions. |

## Quick start

1. Open `01_object_counting_coins.py` in CanMV IDE.
2. Connect the K230 board to your computer.
3. Generate a coin image with Yahboom **Generate Random Number of Coins**.
4. Run the script and point the camera at the image.
5. The screen will show rectangles around the detected objects, FPS, and `Num`, the number of detected objects.

## How counting works

The main detection call is:

```python
blobs = img.find_blobs([threshold], pixels_threshold=50, area_threshold=50, merge=True)
```

`threshold` is a LAB color threshold in this format:

```python
(L_min, L_max, A_min, A_max, B_min, B_max)
```

The coin demo uses this threshold:

```python
TRACK_THRESHOLD = (0, 100, -7, 127, 10, 83)
```

Then the program loops over all detected blobs:

```python
for blob in blobs:
    img.draw_rectangle(blob[0:4])
    img.draw_cross(blob[5], blob[6])
```

The number of objects is the length of the `blobs` list:

```python
count = len(blobs)
```

## Reading files on K230

The second example, `02_object_counting_file_io.py`, demonstrates reading a text file that contains the color threshold.

File name:

```text
object_threshold.txt
```

The file should contain one line with 6 numbers:

```text
0,100,-7,127,10,83
```

Reading the file:

```python
with open("object_threshold.txt", "r") as f:
    text = f.read()
```

Converting text to a LAB threshold:

```python
parts = text.strip().replace(" ", "").split(",")
threshold = tuple([int(value) for value in parts])
```

If the file does not exist, the example creates it automatically with the default value.

## Writing files on K230

Text file writing is done with `open(..., "w")`:

```python
with open("object_count_result.txt", "w") as f:
    f.write("objects=24\n")
```

Open modes:

| Mode | Meaning |
| --- | --- |
| `"r"` | Read an existing file. |
| `"w"` | Write and replace old content. If the file does not exist, it is created. |
| `"a"` | Append text to the end of the file. |

In the second example, the latest result is written to `object_count_result.txt` about once per second:

```text
objects=24
fps=65.529
time_ms=123456
```

Why not write every frame: the camera can run at a high frame rate, and continuous file writes are unnecessary. It is usually better to write periodically or only when the count changes.

## Accuracy tuning

If recognition is not good:

1. Improve lighting.
2. Remove glare from the screen or object.
3. Tune the LAB threshold for your real environment.
4. Increase `pixels_threshold` and `area_threshold` if there is noise.
5. Decrease these thresholds if small objects are not detected.

## Program structure

1. Import modules.
2. Define constants: screen size, LAB threshold, text colors.
3. Initialize the camera and display.
4. Main loop:
   - capture a frame;
   - find color blobs;
   - draw rectangles and center crosses;
   - draw FPS and object count;
   - show the image.
5. Handle errors and release resources.

## Useful modifications

To count another color, replace `TRACK_THRESHOLD` or edit `object_threshold.txt`.

To keep a history of measurements, change the result file mode from `"w"` to `"a"`:

```python
with open("object_count_result.txt", "a") as f:
    f.write("objects=%d\n" % count)
```

This appends new lines to the end of the file instead of replacing old data.

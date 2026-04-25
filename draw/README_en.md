# Draw Examples for Yahboom K230

## Overview

The `draw/` folder contains educational examples demonstrating graphical drawing functions on the K230 Vision Module. These functions allow you to overlay visual elements on images such as lines, shapes, text, and keypoints.

Basic pipeline:

```text
image → draw_* → display
```

For camera-based examples:

```text
camera → snapshot → draw_* → Display.show_image()
```

---

## Folder Structure

```text
draw/
├── line/
├── circle/
├── reactangle/
├── ellipse/
├── arrow/
├── crosshair/
├── text/
└── key_points/
```

---

## Drawing Functions

### Line

```python
img.draw_line(x0, y0, x1, y1, color=(255,0,0), thickness=2)
```

Used for guides, grids, and UI lines.

---

### Circle

```python
img.draw_circle(x, y, radius, color=(0,255,0), thickness=2)
```

Used for markers and highlights.

---

### Rectangle

```python
img.draw_rectangle(x, y, w, h, color=(0,191,255), thickness=2)
```

Used for bounding boxes and ROI areas.

---

### Ellipse

```python
img.draw_ellipse(cx, cy, rx, ry, rot, color=(255,0,0))
```

Used for visual zones and UI elements.

---

### Arrow

```python
img.draw_arrow(x0, y0, x1, y1, color=(255,255,0))
```

Used to show direction or movement.

---

### Crosshair

```python
img.draw_cross(x, y, color=(255,0,0), size=20)
```

Used as a target marker or center indicator.

---

### Text

```python
img.draw_string(x, y, "Text", color=(255,255,0), scale=2)
img.draw_string_advanced(x, y, size, "Hello", color=(0,191,255))
```

Used for UI, debugging, and labels.

---

### Keypoints

```python
keypoints = img.find_keypoints(...)
img.draw_keypoints(keypoints)
```

Keypoints represent important visual features such as corners and edges.

---

## For Users

1. Run `01_*_demo.py` to see static examples.
2. Run `02_*_camera.py` to see real-time camera overlays.

---

## For Developers

Basic pattern:

```python
img = sensor.snapshot()
img.draw_*(...)
Display.show_image(img)
```

You can combine multiple functions to build UI overlays and visualization tools.

---

## File Operations

### Save image

```python
img.save("/data/result.jpg")
```

### Load image

```python
img = image.Image("/data/result.jpg")
Display.show_image(img)
```

---

## Applications

- Computer Vision overlays
- Object detection visualization
- Robotics interfaces
- Debugging and monitoring

---

## Learning Path

1. line
2. circle
3. rectangle
4. ellipse
5. arrow
6. crosshair
7. text
8. keypoints

Then move to advanced CV/AI projects.

# Draw Circle (K230)

## 📋 Description

Examples of using the `draw_circle()` function to draw circles on the Yahboom K230 board.

Based on the official K230 PDF documentation.

## 🎯 For Beginners

This example will show you:
- How to draw circles of different sizes and colors
- How to use X, Y coordinates and radius
- How to combine multiple circles to create complex shapes
- How to draw over camera video stream

## 🧠 draw_circle() API

```python
img.draw_circle(x, y, radius, color=(R,G,B), thickness=1, fill=False)
```

**Parameters:**
- `x` — X coordinate of the circle center (horizontal)
- `y` — Y coordinate of the circle center (vertical)
- `radius` — circle radius in pixels
- `color` — circle color in format (Red, Green, Blue), values from 0 to 255
- `thickness` — line thickness for the circle outline (default 1 pixel)
- `fill` — if `True`, the circle will be filled with solid color

**Color Examples:**
- `(255, 0, 0)` — red
- `(0, 255, 0)` — green
- `(0, 0, 255)` — blue
- `(255, 255, 0)` — yellow
- `(255, 255, 255)` — white
- `(0, 0, 0)` — black

## 📁 Script Examples

### 01_draw_circle_demo.py — Mechanical Wheel

**What it does:**
Draws a static image of a "mechanical wheel" using multiple circles:
- Two outer rings of different sizes
- Central hub
- 8 decorative elements around the circle (like bolts on a car wheel)

**What you'll learn:**
- How to draw circles at screen center (coordinates 320, 240 for 640x480 resolution)
- How to use `fill=True` parameter to fill a circle
- How to use math (trigonometry) to calculate positions of elements around a circle
- How to combine circles of different sizes to create complex shapes

**Run:**
```bash
python 01_draw_circle_demo.py
```

### 02_draw_circle_camera.py — Circles Over Camera

**What it does:**
Captures video stream from camera and draws over it:
- Red circle with 100 pixels radius
- Green circle with 50 pixels radius
- Text label "Draw Circle + Camera"

**What you'll learn:**
- How to initialize camera on K230
- How to capture frames from camera using `sensor.snapshot()`
- How to draw graphics over real video stream
- How to create interactive augmented reality applications

**Run:**
```bash
python 02_draw_circle_camera.py
```

## 🎥 Image Processing Pipeline

```
Camera → Frame Snapshot → Draw Circles → Display
```

## 💾 File Operations

### Save Image
```python
img.save("/data/test.jpg")
```

### Load Image from File
```python
img = image.Image("/data/test.jpg")
```

## 👤 For Users

1. Connect the K230 board to your computer
2. Upload one of the scripts to the board
3. Run the script via IDE or directly
4. Observe the result on the display

## 👨‍💻 For Developers

**Helpful Tips:**
- Coordinates (0, 0) are at the top-left corner of the screen
- Use (WIDTH//2, HEIGHT//2) for screen center
- Combine `draw_circle()` with other drawing functions:
  - `draw_line()` — lines
  - `draw_rectangle()` — rectangles
  - `draw_string()` — text
- Experiment with transparency and line thickness

**Project Ideas:**
- Camera scope/crosshair
- Dashboard indicators
- Simple games (targets, buttons)
- Data visualization (pie charts)

## 🔗 Resources

- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)
- Official K230 Documentation

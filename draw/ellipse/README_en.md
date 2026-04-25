# Draw Ellipse (K230)

## 📋 Description

Examples of using the `draw_ellipse()` function for drawing ellipses on the Yahboom K230 board.

Based on official K230 PDF documentation.

## 🎯 What You Will Learn

- How to create an image and draw ellipses on it
- How to capture images from the camera and add graphical overlays
- How to work with the K230 display and media system

## 🧠 draw_ellipse() API

```python
img.draw_ellipse(cx, cy, rx, ry, rot, color=(R,G,B), thickness=1)
```

**Parameters:**
- `cx`, `cy` - coordinates of the ellipse center (in pixels)
- `rx` - radius of the ellipse along the X-axis (horizontal size)
- `ry` - radius of the ellipse along the Y-axis (vertical size)
- `rot` - rotation angle in degrees (0-360)
- `color` - color in RGB format as a tuple (R, G, B), where each component is 0-255
- `thickness` - line thickness in pixels (default is 1)

## 📁 Examples

### 01_draw_ellipse_demo.py - Random Ellipses

**What it does:**
- Creates a white background on the screen
- Draws 10 random ellipses with different parameters:
  - Random center position
  - Random sizes (radii)
  - Random rotation angle
  - Random bright color

**Run:**
```bash
python 01_draw_ellipse_demo.py
```

### 02_draw_ellipse_camera.py - Ellipses Over Camera Image

**What it does:**
- Captures real-time images from the camera
- Draws two concentric ellipses in the center of the screen:
  - Large red ellipse (120x60 pixels)
  - Small green ellipse (60x30 pixels)
- Adds "Draw Ellipse" text label in yellow

**Run:**
```bash
python 02_draw_ellipse_camera.py
```

## 🎥 Image Processing Pipeline

```
Camera → Snapshot (frame capture) → draw_ellipse (drawing) → Display (output to screen)
```

## 💾 File Operations

### Save Image

```python
# Save current image to JPG file
img.save("/data/test.jpg")
```

### Load Image

```python
# Load image from file
img = image.Image("/data/test.jpg")
```

## 👤 For Beginners

1. **Run the example** - choose one of the scripts and run it on the K230 board
2. **Observe the result** - ellipses will appear on the display screen
3. **Experiment** - change parameters (sizes, colors, positions) and see how the result changes

## 👨‍💻 For Developers

**Helpful Tips:**
- Use `(WIDTH//2, HEIGHT//2)` to get the center of the screen
- Radii `rx` and `ry` determine the ellipse's horizontal and vertical size
- If `rx == ry`, you'll get a circle
- Rotation angle `rot` is measured in degrees counter-clockwise
- Colors are specified in RGB format: `(255,0,0)` - red, `(0,255,0)` - green, `(0,0,255)` - blue

**Color Formats:**
- `(255, 0, 0)` - Red
- `(0, 255, 0)` - Green
- `(0, 0, 255)` - Blue
- `(255, 255, 0)` - Yellow
- `(255, 255, 255)` - White
- `(0, 0, 0)` - Black

## 🔗 Resources

- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)
- Official K230 Documentation

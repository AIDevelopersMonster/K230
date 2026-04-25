# Draw Rectangle (K230)

## 📋 Description

Examples of using the `draw_rectangle()` function to draw rectangles on the Yahboom K230 board.
Based on official PDF documentation.

### What is draw_rectangle?

`draw_rectangle()` is a function for drawing rectangles on an image.
It allows you to create both outlined and filled rectangles.

## 🧠 API

### Syntax

```python
img.draw_rectangle(x, y, w, h, color=(R,G,B), thickness=1, fill=False)
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `x` | X coordinate of the top-left corner (in pixels) | `100` |
| `y` | Y coordinate of the top-left corner (in pixels) | `100` |
| `w` | Width of the rectangle (in pixels) | `200` |
| `h` | Height of the rectangle (in pixels) | `150` |
| `color` | Color in RGB format (Red, Green, Blue) | `(255,0,0)` - red |
| `thickness` | Line thickness for the outline (in pixels) | `2` |
| `fill` | Fill the rectangle with color (`True` or `False`) | `True` |

### Color Examples

- `(255, 0, 0)` — Red
- `(0, 255, 0)` — Green
- `(0, 0, 255)` — Blue
- `(255, 255, 0)` — Yellow
- `(0, 191, 255)` — Cyan
- `(135, 206, 235)` — Light Blue
- `(255, 255, 255)` — White
- `(0, 0, 0)` — Black

## 📁 Examples

### 01_draw_rectangle_demo.py
**Rectangle Drawing Demo**

This script creates an image with a white background and draws several rectangles:
- A large cyan outline
- Four small rectangles at the corners (filled)
- A central block with outline and fill

**Run:**
```bash
python 01_draw_rectangle_demo.py
```

### 02_draw_rectangle_camera.py
**Overlay Rectangles on Camera Image**

This script captures an image from the camera and draws over it:
- A red rectangle outline
- A green filled rectangle
- A text label "Draw Rectangle"

**Run:**
```bash
python 02_draw_rectangle_camera.py
```

## 🎥 Pipeline

### For camera example:

```
Camera → Snapshot → Draw Rectangles → Display
```

1. **Sensor** — camera captures the image
2. **snapshot()** — get the frame from the camera
3. **draw_rectangle()** — draw rectangles on the frame
4. **Display.show_image()** — display the image on screen

## 💾 File Operations

### Save Image

```python
# Save image to JPG file
img.save("/data/test.jpg")
```

### Load Image

```python
# Load image from file
img = image.Image("/data/test.jpg")
```

## 👤 For Users

1. Connect the K230 board to your computer
2. Open the development environment (IDE)
3. Select the desired example
4. Run the script
5. Observe the result on the screen

## 👨‍💻 For Developers

### Usage Tips:

1. **Coordinates**: The coordinate system starts from the top-left corner (0, 0)
2. **Combining Functions**: You can combine `draw_rectangle()` with other functions:
   - `draw_circle()` — drawing circles
   - `draw_line()` — drawing lines
   - `draw_string()` — adding text

3. **Performance**: When working with the camera, try to minimize the number of drawing operations in the loop

### Combination Example:

```python
# Draw a rectangle
img.draw_rectangle(50, 50, 100, 100, color=(255,0,0), thickness=2)

# Add a circle inside
img.draw_circle(100, 100, 30, color=(0,255,0), fill=True)

# Add text
img.draw_string(50, 200, "Hello!", color=(255,255,255))
```

## 🔗 Resources

- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)
- Official K230 Documentation

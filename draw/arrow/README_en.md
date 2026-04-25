# Draw Arrow (K230)

## 📋 Description

Examples of using the `draw_arrow()` function to draw arrows on the Yahboom K230 board.  
These scripts demonstrate how to draw arrows on a static image and over a camera video stream.

Based on the official K230 PDF documentation.

## 🔧 Requirements

- Board: **Yahboom K230**
- Display: **ST7701** (640x480)
- Camera (for camera example)

## 🧠 API

### Drawing an Arrow

```python
img.draw_arrow(x0, y0, x1, y1, color=(R, G, B), thickness=1)
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| `x0`, `y0` | Starting coordinates of the arrow (top-left corner = 0,0) |
| `x1`, `y1` | Ending coordinates of the arrow (where the arrow points) |
| `color` | Arrow color in RGB format, e.g., `(255, 0, 0)` for red |
| `thickness` | Line thickness in pixels (default is 1) |

### Drawing Text

```python
img.draw_string(x, y, "Text", color=(R, G, B))
```

## 📁 Examples

### 01_draw_arrow_demo.py — Static Arrows

**Description:**  
The script creates an image with a white background and draws several arrows of different colors and thicknesses.

**What it does:**
- Creates a white background
- Draws a main horizontal arrow
- Adds additional arrows above and below
- Draws diagonal arrows
- Displays the result on the screen

**How to run:**
```bash
python 01_draw_arrow_demo.py
```

### 02_draw_arrow_camera.py — Arrows Over Camera

**Description:**  
The script captures an image from the camera and draws colored arrows and text over it.

**What it does:**
- Initializes the camera
- Captures a frame
- Draws red and green arrows
- Adds "Draw Arrow" label
- Displays the result on the screen in real-time

**How to run:**
```bash
python 02_draw_arrow_camera.py
```

## 🎥 Pipeline (Data Flow)

### For camera example:
```
Camera → Snapshot (frame capture) → draw_arrow (drawing) → Display (screen)
```

### For static example:
```
Create Image → Draw Background → draw_arrow → Display (screen)
```

## 💾 File Operations

### Saving an Image
```python
img.save("/data/test.jpg")
```

### Loading an Image
```python
img = image.Image("/data/test.jpg")
```

## 👤 For Beginners

**How to run the example:**
1. Connect the K230 board to your computer
2. Open the K230 IDE
3. Copy the script into the IDE
4. Click the Run button

**What you will see:**
- In example 01: A static image with arrows on a white background
- In example 02: A live camera feed with drawn arrows

## 👨‍💻 For Developers

**Useful tips:**
- Coordinates start at the top-left corner of the screen (0, 0)
- X increases to the right, Y increases downward
- Colors are specified in RGB format (0-255 for each channel)
- You can combine `draw_arrow()` with other drawing functions

**Project ideas:**
- Robot direction visualization
- Navigation system indicators
- Angle and direction arrows
- UI elements for touch interfaces

## 📚 Additional Resources

- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)
- Official K230 Documentation
- Other drawing examples in the `draw/` folder

## ⚠️ Notes

- Make sure the display is properly connected to the board
- For camera functionality, check the camera module connection
- If errors occur, check the logs in the IDE console

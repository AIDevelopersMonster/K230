# Draw Line (K230)

## 📋 What is this

Examples of using `draw_line()` to draw lines on images and live camera streams.

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230  
**GitHub:** https://github.com/AIDevelopersMonster/K230

## 🧠 API

```python
img.draw_line(x0, y0, x1, y1, color=(R,G,B), thickness=1)
```

| Parameter | Description |
|-----------|-------------|
| x0, y0 | Start point of the line (X and Y coordinates) |
| x1, y1 | End point of the line (X and Y coordinates) |
| color | Line color in RGB format (Red, Green, Blue) |
| thickness | Line width in pixels (default: 1) |

## 📁 Examples

### 01_draw_line_logo.py
**Static Image**
- Draws the word "Yahboom" using lines on a white background
- No camera required
- Great for learning the API and understanding drawing principles
- **Uses:** `image.Image`, `Display`, `MediaManager`

### 02_draw_line_camera.py
**Live Camera Stream**
- Draws lines over live video from the camera in real-time
- Shows crosshair in the center and frame border
- Demonstrates practical application of draw_line()
- **Uses:** `Sensor`, `Display`, `MediaManager`

## 🎥 Camera Pipeline

Image processing pipeline:

```
Camera → snapshot (capture frame) → draw_line (drawing) → display (output to screen)
```

Step by step:
1. `sensor.reset()` - reset camera settings to default
2. `sensor.set_framesize()` - set frame resolution
3. `sensor.set_pixformat()` - set color format
4. `sensor.snapshot()` - capture current frame
5. `img.draw_line()` - draw lines on the frame
6. `Display.show_image()` - display result on screen

## 💾 File Read/Write

### Save Image

```python
img.save("/data/snapshot/test.jpg")
```

Example usage: save every 100th frame for later analysis.

### Load Image

```python
img = image.Image("/data/snapshot/test.jpg")
Display.show_image(img)
```

## 🚀 Quick Start

1. **Connect the camera** to the K230 board
2. **Run the example** `02_draw_line_camera.py`
3. **Observe** lines overlaid on the video stream on the screen

## 💡 For Developers

- All drawing operations are performed on the `image.Image` object
- Can be combined with other functions: `draw_string()`, `draw_rectangle()`, `draw_circle()`
- Drawing works in real-time without delays
- Coordinate system: (0,0) is the top-left corner of the screen

## 👤 For Users

- Simply run any of the examples
- Lines will appear automatically
- Easy to change color, thickness, and position of lines
- Experiment with coordinates to create your own patterns

## ⚙️ Parameter Settings

### Change Line Color
```python
# Red color
color = (255, 0, 0)
# Green color
color = (0, 255, 0)
# Blue color
color = (0, 0, 255)
# White color
color = (255, 255, 255)
```

### Change Line Thickness
```python
# Thin line
thickness = 1
# Medium line
thickness = 3
# Thick line
thickness = 5
```


# Draw Crosshair (K230)

## 📋 Description

Examples of using the `draw_cross()` function to draw crosshairs on the Yahboom K230 board.

This project demonstrates two approaches:
1. **Static image** - drawing a crosshair on a white background
2. **Real-time camera** - overlaying crosshairs on live video feed

Based on official K230 PDF documentation.

## 🔧 Requirements

- Yahboom K230 board
- ST7701 display (for screen output examples)
- Camera (for example 02)

## 🧠 API Functions

### draw_cross() - Drawing a Cross/Crosshair

```python
img.draw_cross(x, y, color=(R, G, B), size=5, thickness=1)
```

**Parameters:**
- `x` - X coordinate of cross center (horizontal position)
- `y` - Y coordinate of cross center (vertical position)
- `color` - cross color in (Red, Green, Blue) format, values from 0 to 255
- `size` - cross size in pixels (length of each of the 4 lines from center)
- `thickness` - line thickness of the cross in pixels

**Color Examples:**
- `(255, 0, 0)` - red
- `(0, 255, 0)` - green
- `(0, 0, 255)` - blue
- `(255, 255, 0)` - yellow
- `(0, 191, 255)` - cyan/light blue

## 📁 Examples

### 01_draw_crosshair_demo.py - Static Crosshair

**What it does:**
- Creates a white background
- Draws a large central cyan cross
- Adds 8 small crosses on an inner circle
- Adds 12 crosses on an outer circle
- Displays the result on screen

**Features:**
- Uses trigonometry to calculate circular positions
- Demonstrates different sizes and colors

**Run:**
```bash
python 01_draw_crosshair_demo.py
```

### 02_draw_crosshair_camera.py - Camera Overlay Crosshair

**What it does:**
- Captures images from camera in real-time
- Draws a red crosshair in the center
- Adds two green aiming points
- Displays "Draw Crosshair" text
- Shows processed image on display

**Features:**
- Real-time operation (60 FPS)
- Suitable for targeting systems
- Handles exit button press

**Run:**
```bash
python 02_draw_crosshair_camera.py
```

## 🎥 Processing Pipeline

### For camera example:
```
Camera → Frame Capture (snapshot) → Draw Crosses (draw_cross) → Display
```

### For static example:
```
Create Image → Draw Background → Draw Crosses → Display
```

## 💾 File Operations

### Save image
```python
img.save("/data/test.jpg")
```

### Load image
```python
img = image.Image("/data/test.jpg")
```

## 👤 For Beginners

1. **Learn coordinates**: Screen is 640x480, center is at point (320, 240)
2. **Experiment with colors**: Change RGB values for different colors
3. **Adjust size**: The `size` parameter controls cross size
4. **Try thicknesses**: The `thickness` parameter changes line width

## 👨‍💻 For Developers

- Use integer division `//` for center coordinates
- Combine multiple `draw_cross()` calls for complex crosshairs
- Don't forget to free resources in `finally` block
- Check exit point via `os.exitpoint()` in loops

## 🛠️ Modules

- `media.sensor` - camera operations
- `media.display` - display output
- `media.media` - media manager
- `image` - image processing

## 📞 Support

GitHub: https://github.com/AIDevelopersMonster/K230

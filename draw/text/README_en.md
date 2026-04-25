# Draw Text (K230)

## 📋 Description

This folder contains examples of text rendering on the Yahboom K230 board.
The scripts demonstrate the use of `draw_string()` and `draw_string_advanced()` methods
for displaying text on the screen or overlaying it on camera images.

All code comments are written in Russian to help beginners understand
how each element of the script works.

## 🚀 Quick Start

1. Connect the K230 board to your computer
2. Open any example in the IDE
3. Run the script and observe the result on the screen

## 🧠 API Methods

### draw_string()
Basic method for text rendering.

```python
img.draw_string(x, y, text, color=(R, G, B), scale=1)
```

**Parameters:**
- `x`, `y` — coordinates of the top-left corner of the text
- `text` — string to display
- `color` — text color in format (Red, Green, Blue), values from 0 to 255
- `scale` — font scale (1 = base size)

### draw_string_advanced()
Advanced method with Unicode support (Russian, Chinese, etc.).

```python
img.draw_string_advanced(x, y, size, text, color=(R, G, B))
```

**Parameters:**
- `x`, `y` — coordinates of the top-left corner of the text
- `size` — font size in pixels
- `text` — string to display (supports Unicode)
- `color` — text color in format (Red, Green, Blue)

## 📁 Examples

### 01_draw_text_demo.py
**What it does:** Creates a white background and displays text in English and Chinese.

**Features:**
- Uses `draw_string_advanced()` for Unicode support
- Static image (no camera)
- Demonstrates text color manipulation

### 02_draw_text_camera.py
**What it does:** Captures images from the camera and adds text overlays.

**Features:**
- Uses `draw_string()` for fast rendering
- Real-time camera operation
- Shows how to overlay text on video stream

## 🎥 Pipeline

```
Camera → Snapshot → Draw Text → Display
```

## 💾 File Operations

### Save Image
```python
img.save("/data/test.jpg")
```

### Load Image
```python
img = image.Image("/data/test.jpg")
```

## ⚙️ Resolution Settings

The examples use a resolution of 640x480 pixels:
```python
WIDTH = 640
HEIGHT = 480
```

You can change these values to match your display.

## 🔧 Used Modules

- `media.sensor` — camera operations
- `media.display` — display control
- `media.media` — media manager
- `image` — image processing

## 👤 For Beginners

1. **Study 01_draw_text_demo.py** — simple example with a static image
2. **Try changing text and colors** — experiment with parameters
3. **Move to 02_draw_text_camera.py** — real-time camera operation

## 👨‍💻 For Developers

- Use `draw_string()` for simple labels (Latin characters, numbers)
- Use `draw_string_advanced()` for multilingual text
- Don't forget to release resources in the `finally` block
- Check exit point via `os.exitpoint()` in loops

## 📝 Project Structure

```
draw/text/
├── 01_draw_text_demo.py      # Text drawing demo
├── 02_draw_text_camera.py    # Text over camera
├── README.md                 # Russian version
└── README_en.md              # This file (English version)
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Text not displaying | Check Display and MediaManager initialization |
| Wrong colors | Ensure color format (R, G, B) is correct |
| Camera not working | Check sensor connection and initialization |

## 📞 Contacts

Author: AIDevelopersMonster  
GitHub: https://github.com/AIDevelopersMonster/K230

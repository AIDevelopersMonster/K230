# Draw Keypoints (K230)

## 📋 Description

Examples of using `draw_keypoints()` and `find_keypoints()` functions for detecting and displaying keypoints on the Yahboom K230 board.

Based on the official K230 PDF documentation.

## 🎯 For Beginners

This example will show you:
- What keypoints are and how to use them
- How to detect keypoints in camera images
- How to draw detected keypoints on the display
- How to define a Region of Interest (ROI) for point detection
- How to combine camera video stream with graphics

## 🧠 API Functions

### find_keypoints()

Detecting keypoints in an image:

```python
keypoints = img.find_keypoints(threshold=30, scale_factor=1.2, max_keypoints=30, roi=None)
```

**Parameters:**
- `threshold` — detector sensitivity threshold (lower value = more points detected)
- `scale_factor` — scale for detecting points of different sizes (typically 1.1-1.3)
- `max_keypoints` — maximum number of detected points
- `roi` — Region of Interest, format: (x, y, width, height)

**Returns:** keypoints object or None if no points found

### draw_keypoints()

Drawing detected keypoints:

```python
img.draw_keypoints(keypoints, color=(R,G,B), size=8, thickness=2, fill=True)
```

**Parameters:**
- `keypoints` — object with detected keypoints (result from find_keypoints)
- `color` — point color in format (Red, Green, Blue), values from 0 to 255
- `size` — size of each keypoint in pixels
- `thickness` — line thickness for outlines
- `fill` — if `True`, points will be filled with solid color

### draw_cross()

Drawing a cross at specified coordinates:

```python
img.draw_cross(x, y, color=(R,G,B), size=10)
```

**Parameters:**
- `x` — X-axis coordinate of cross center (horizontal)
- `y` — Y-axis coordinate of cross center (vertical)
- `color` — cross color in format (Red, Green, Blue)
- `size` — cross size in pixels

**Color Examples:**
- `(255, 0, 0)` — red
- `(0, 255, 0)` — green
- `(0, 0, 255)` — blue
- `(255, 255, 0)` — yellow
- `(255, 255, 255)` — white
- `(0, 0, 0)` — black

## 📁 Script Examples

### 01_draw_keypoints_demo.py — Keypoints Demo

**What it does:**
Creates a static image with a white background and draws a row of red crosses on it, simulating keypoints for object detection.

**What you'll learn:**
- Creating images with specified resolution and color format
- Drawing simple shapes (rectangles, crosses)
- Using loops to draw multiple identical elements
- Initializing the display and showing images on it

**Run:**
```bash
python 01_draw_keypoints_demo.py
```

### 02_draw_keypoints_camera.py — Keypoints with Camera

**What it does:**
Captures real-time video stream from the camera and:
- Displays color image from the camera
- Detects keypoints in the specified Region of Interest (ROI) on grayscale image
- Draws detected keypoints in red over the video stream
- Highlights the search area with a light blue rectangle

**What you'll learn:**
- Initializing the K230 camera with two streams (color and grayscale)
- Capturing frames from camera using `sensor.snapshot()`
- Using `find_keypoints()` for image feature detection
- Drawing graphics over real video stream
- Working with Region of Interest (ROI)
- Creating real-time computer vision applications

**Run:**
```bash
python 02_draw_keypoints_camera.py
```

## 🎥 Image Processing Pipeline

```
Camera → Frame Capture (color + grayscale) → Keypoint Detection → Graphics Drawing → Display
```

## 💡 What are Keypoints?

**Keypoints** are distinctive features of an image that can be reliably detected under various conditions:
- Object corners
- Boundaries between areas of different brightness
- Textures and patterns
- High-contrast regions

**Applications:**
- Object recognition
- Motion tracking
- Stereo vision (depth estimation)
- Augmented reality
- Robot navigation

## 👤 For Users

1. Connect the K230 board to your computer
2. Upload one of the scripts to the board
3. Run the script via IDE or directly
4. Observe the result on the display

**For the camera script:**
- Point the camera at an object with distinct texture or corners
- Keypoints will be automatically detected and highlighted

## 👨‍💻 For Developers

**Useful Tips:**
- Coordinates (0, 0) are at the top-left corner of the screen
- Use (WIDTH//2, HEIGHT//2) for screen center
- Region of Interest (ROI) helps speed up detection and reduce false positives
- The `threshold` parameter affects sensitivity: lower value = more points
- Combine `draw_keypoints()` with other functions:
  - `draw_rectangle()` — highlighting areas
  - `draw_string()` — text labels
  - `draw_line()` — connecting points

**Project Ideas:**
- Object corner detector
- Moving object tracking system
- Gesture recognition
- Visual odometer for robots
- Interactive touch-sensitive board

## 🔗 Resources

- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)
- Official K230 Documentation

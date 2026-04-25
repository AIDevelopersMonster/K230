# Draw Line (K230)

## 📋 What is this

Examples of using `draw_line()` to draw lines on images and camera streams.

Based on documentation:
fileciteturn0file0

## 🧠 API

```python
img.draw_line(x0, y0, x1, y1, color=(R,G,B), thickness=1)
```

| Parameter | Description |
|----------|------------|
| x0, y0 | Start point |
| x1, y1 | End point |
| color | Line color (RGB) |
| thickness | Line width |

## 📁 Examples

### 01_draw_line_logo.py
- Draws "Yahboom" using lines
- No camera
- Good for learning

### 02_draw_line_camera.py
- Draws lines on live camera
- Real-world usage

## 🎥 Camera pipeline

```
camera → snapshot → draw_line → display
```

From repo examples:
- `sensor.snapshot()` gets frame
- `Display.show_image()` shows it fileciteturn1file0

## 💾 File read/write

### Save image

```python
img.save("/data/snapshot/test.jpg")
```

Example: saving every 100 frames fileciteturn4file0

### Load image

```python
img = image.Image("/data/snapshot/test.jpg")
Display.show_image(img)
```

## 🚀 Quick start

1. Connect camera
2. Run `02_draw_line_camera.py`
3. See lines on screen

## 💡 For developers

- Works on `image` object
- Combine with `draw_string`, etc.
- Real-time rendering

## 👤 For users

- Just run example
- Lines appear automatically
- Change color/thickness easily


# Draw Ellipse (K230)

## 📋 Description

Examples of using `draw_ellipse()`.
Based on PDF: fileciteturn8file0

## 🧠 API

```python
img.draw_ellipse(cx, cy, rx, ry, rot, color=(R,G,B), thickness=1)
```

## 📁 Examples

### 01_draw_ellipse_demo.py
- Random ellipse demo

### 02_draw_ellipse_camera.py
- Camera overlay

## 🎥 Pipeline

camera → snapshot → draw_ellipse → display

## 💾 File operations

### Save
img.save("/data/test.jpg")

### Load
img = image.Image("/data/test.jpg")

## 💡 Usage

- Run script

## 👨‍💻 Dev

- Use center and radii
- Supports rotation

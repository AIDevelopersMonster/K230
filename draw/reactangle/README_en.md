# Draw Rectangle (K230)

## 📋 Description

Examples of using `draw_rectangle()`.
Based on PDF: fileciteturn7file0

## 🧠 API

```python
img.draw_rectangle(x, y, w, h, color=(R,G,B), thickness=1, fill=False)
```

## 📁 Examples

### 01_draw_rectangle_demo.py
- Rectangle demo

### 02_draw_rectangle_camera.py
- Camera overlay

## 🎥 Pipeline

camera → snapshot → draw_rectangle → display

## 💾 File operations

### Save
img.save("/data/test.jpg")

### Load
img = image.Image("/data/test.jpg")

## 💡 Usage

- Run example

## 👨‍💻 Dev

- Combine with draw_line / draw_circle

# Draw Arrow (K230)

## 📋 Description

Examples of using `draw_arrow()`.
Based on PDF: fileciteturn9file0

## 🧠 API

```python
img.draw_arrow(x0, y0, x1, y1, color=(R,G,B), thickness=1)
```

## 📁 Examples

### 01_draw_arrow_demo.py
- Static arrows

### 02_draw_arrow_camera.py
- Camera overlay arrows

## 🎥 Pipeline

camera → snapshot → draw_arrow → display

## 💾 File operations

### Save
img.save("/data/test.jpg")

### Load
img = image.Image("/data/test.jpg")

## 💡 Usage

- Run script

## 👨‍💻 Dev

- Use start/end coordinates
- Useful for direction visualization

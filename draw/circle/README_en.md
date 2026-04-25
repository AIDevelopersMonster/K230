# Draw Circle (K230)

## 📋 Description

Examples of using `draw_circle()`.

Based on PDF: fileciteturn6file0

## 🧠 API

```python
img.draw_circle(x, y, radius, color=(R,G,B), thickness=1, fill=False)
```

## 📁 Examples

### 01_draw_circle_demo.py
- Mechanical wheel demo

### 02_draw_circle_camera.py
- Circles on camera stream

## 🎥 Pipeline

```
camera → snapshot → draw_circle → display
```

## 💾 File operations

### Save
```python
img.save("/data/test.jpg")
```

### Load
```python
img = image.Image("/data/test.jpg")
```

## 💡 Usage

- Run script
- See circles

## 👨‍💻 Dev

- Combine with draw_line
- Real-time rendering

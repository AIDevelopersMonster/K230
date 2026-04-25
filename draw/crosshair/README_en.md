# Draw Crosshair (K230)

## 📋 Description

Examples of using `draw_cross()`.
Based on PDF: fileciteturn10file0

## 🧠 API

```python
img.draw_cross(x, y, color=(R,G,B), size=5, thickness=1)
```

## 📁 Examples

### 01_draw_crosshair_demo.py
- Crosshair structure

### 02_draw_crosshair_camera.py
- Camera overlay crosshair

## 🎥 Pipeline

camera → snapshot → draw_cross → display

## 💾 File operations

### Save
img.save("/data/test.jpg")

### Load
img = image.Image("/data/test.jpg")

## 💡 Usage

- Run script

## 👨‍💻 Dev

- Use for targeting systems

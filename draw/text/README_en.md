# Draw Text (K230)

## 📋 Description

Examples of using `draw_string()` and `draw_string_advanced()`.
Based on PDF: fileciteturn11file0

## 🧠 API

```python
img.draw_string(x, y, text, color=(R,G,B), scale=1)
img.draw_string_advanced(x, y, size, text, color=(R,G,B))
```

## 📁 Examples

### 01_draw_text_demo.py
- Text rendering

### 02_draw_text_camera.py
- Camera overlay text

## 🎥 Pipeline

camera → snapshot → draw_string → display

## 💾 File operations

### Save
img.save("/data/test.jpg")

### Load
img = image.Image("/data/test.jpg")

## 💡 Usage

- Run example

## 👨‍💻 Dev

- Use advanced text rendering

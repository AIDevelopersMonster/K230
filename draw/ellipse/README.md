# Draw Ellipse (K230)

## 📋 Описание

Примеры использования `draw_ellipse()`.
Основано на PDF документации: fileciteturn8file0

## 🧠 API

```python
img.draw_ellipse(cx, cy, rx, ry, rot, color=(R,G,B), thickness=1)
```

## 📁 Примеры

### 01_draw_ellipse_demo.py
- Случайные эллипсы

### 02_draw_ellipse_camera.py
- Overlay на камере

## 🎥 Pipeline

camera → snapshot → draw_ellipse → display

## 💾 Файлы

### Сохранение
img.save("/data/test.jpg")

### Чтение
img = image.Image("/data/test.jpg")

## 👤 Пользователь
- Запусти пример

## 👨‍💻 Программист
- Используй центр (cx,cy) и радиусы (rx,ry)
- Можно вращать (rot)

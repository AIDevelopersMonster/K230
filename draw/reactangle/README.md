# Draw Rectangle (K230)

## 📋 Описание

Примеры использования `draw_rectangle()`.
Основано на PDF документации: fileciteturn7file0

## 🧠 API

```python
img.draw_rectangle(x, y, w, h, color=(R,G,B), thickness=1, fill=False)
```

## 📁 Примеры

### 01_draw_rectangle_demo.py
- Демонстрация прямоугольников

### 02_draw_rectangle_camera.py
- Overlay поверх камеры

## 🎥 Pipeline

camera → snapshot → draw_rectangle → display

## 💾 Файлы

### Сохранение
img.save("/data/test.jpg")

### Чтение
img = image.Image("/data/test.jpg")

## 👤 Пользователь
- Запусти пример

## 👨‍💻 Программист
- Используй координаты (x,y,w,h)
- Комбинируй с draw_circle

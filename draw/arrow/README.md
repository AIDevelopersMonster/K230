# Draw Arrow (K230)

## 📋 Описание

Примеры использования `draw_arrow()`.
Основано на PDF документации: fileciteturn9file0

## 🧠 API

```python
img.draw_arrow(x0, y0, x1, y1, color=(R,G,B), thickness=1)
```

## 📁 Примеры

### 01_draw_arrow_demo.py
- Статические стрелки

### 02_draw_arrow_camera.py
- Стрелки поверх камеры

## 🎥 Pipeline

camera → snapshot → draw_arrow → display

## 💾 Работа с файлами

### Сохранение
img.save("/data/test.jpg")

### Чтение
img = image.Image("/data/test.jpg")

## 👤 Пользователь
- Запусти пример

## 👨‍💻 Программист
- Используй координаты начала и конца
- Можно строить UI направления

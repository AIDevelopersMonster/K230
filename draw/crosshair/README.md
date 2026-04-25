# Draw Crosshair (K230)

## 📋 Описание

Примеры использования `draw_cross()`.
Основано на PDF документации: fileciteturn10file0

## 🧠 API

```python
img.draw_cross(x, y, color=(R,G,B), size=5, thickness=1)
```

## 📁 Примеры

### 01_draw_crosshair_demo.py
- Радиальная структура прицела

### 02_draw_crosshair_camera.py
- Прицел поверх камеры

## 🎥 Pipeline

camera → snapshot → draw_cross → display

## 💾 Работа с файлами

### Сохранение
img.save("/data/test.jpg")

### Чтение
img = image.Image("/data/test.jpg")

## 👤 Пользователь
- Запусти пример

## 👨‍💻 Программист
- Используй координаты и размер
- Подходит для прицелов

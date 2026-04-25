# Draw Text (K230)

## 📋 Описание

Примеры использования `draw_string()` и `draw_string_advanced()`.
Основано на PDF документации: fileciteturn11file0

## 🧠 API

```python
img.draw_string(x, y, text, color=(R,G,B), scale=1)
img.draw_string_advanced(x, y, size, text, color=(R,G,B))
```

## 📁 Примеры

### 01_draw_text_demo.py
- Текст на изображении

### 02_draw_text_camera.py
- Текст поверх камеры

## 🎥 Pipeline

camera → snapshot → draw_string → display

## 💾 Работа с файлами

### Сохранение
img.save("/data/test.jpg")

### Чтение
img = image.Image("/data/test.jpg")

## 👤 Пользователь
- Запусти пример

## 👨‍💻 Программист
- Используй draw_string и advanced

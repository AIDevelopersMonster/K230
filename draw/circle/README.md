# Draw Circle (K230)

## 📋 Описание

Примеры использования `draw_circle()` для рисования кругов.

Основано на PDF документации: fileciteturn6file0

## 🧠 API

```python
img.draw_circle(x, y, radius, color=(R,G,B), thickness=1, fill=False)
```

## 📁 Примеры

### 01_draw_circle_demo.py
- Рисует "механическое колесо"
- Использует несколько кругов

### 02_draw_circle_camera.py
- Рисует круги поверх камеры

## 🎥 Pipeline

```
camera → snapshot → draw_circle → display
```

## 💾 Работа с файлами

### Сохранение
```python
img.save("/data/test.jpg")
```

### Чтение
```python
img = image.Image("/data/test.jpg")
```

## 👤 Пользователь
- Запустите пример
- Наблюдайте круги

## 👨‍💻 Программист
- Используйте координаты и радиус
- Комбинируйте с draw_line

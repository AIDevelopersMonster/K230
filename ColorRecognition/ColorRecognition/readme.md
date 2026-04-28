# Color Recognition (K230)

## 📌 Описание

Модуль показывает как распознавать цвета с помощью:

```python
img.find_blobs()
```

Используется LAB цветовое пространство. fileciteturn26file0

---

## 🧠 Как работает

1. камера получает изображение
2. применяется LAB threshold
3. находятся цветовые области
4. рисуется прямоугольник и центр

---

## 🧪 Примеры

| Файл | Описание |
|------|----------|
| 01 | поиск одного цвета |
| 02 | несколько цветов |

---

## ⚙️ Настройка цвета

Используйте:

Tools → Machine Vision → Threshold Editor

Скопируйте LAB значения и добавьте в THRESHOLDS.

---

## 📂 Чтение файла

```python
with open("/sdcard/file.txt") as f:
    print(f.read())
```

## 📂 Запись

```python
with open("/sdcard/file.txt","w") as f:
    f.write("hello")
```

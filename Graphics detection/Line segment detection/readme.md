# Детекция отрезков (K230)

## Описание

Пример показывает как находить отрезки линий с помощью `find_line_segments()`.

Алгоритм использует LSD и преобразование Хафа fileciteturn0file0

---

## Для пользователя

1. Подключите K230
2. Откройте CanMV IDE
3. Запустите `01_line_segment_camera.py`
4. Наведите камеру на линии

---

## Для разработчика

```python
lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)
```

- merge_distance — объединение линий
- max_theta_diff — угол

---

## Чтение и запись файлов

### Чтение
```python
with open("file.txt", "r") as f:
    print(f.read())
```

### Запись
```python
with open("file.txt", "w") as f:
    f.write("Hello")
```

---

## Файлы

- 01_line_segment_camera.py
- 02_line_segment_static.py


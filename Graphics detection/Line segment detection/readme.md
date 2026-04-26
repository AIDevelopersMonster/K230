# Детекция отрезков линий (K230)

## Описание

Пример показывает, как находить отрезки линий с помощью `find_line_segments()` на Yahboom K230 / CanMV.

В папке есть два типа примеров:

1. работа с камерой;
2. работа с заранее подготовленными картинками из папки `img`.

В PDF описано, что `find_line_segments()` использует LSD / преобразование Хафа, возвращает список объектов `image.line`, а параметры `merge_distance` и `max_theta_diff` управляют объединением близких линий и линий с похожим углом. fileciteturn0file0

---

## Структура папки

```text
Graphics detection/Line segment detection/
├── 01_line_segment_camera.py
├── 02_line_segment_static.py
├── 03_line_segment_from_images.py
├── 04_detect_horizontal_lines.py
├── 05_detect_vertical_lines.py
├── 06_detect_all_lines_overlay.py
├── readme.md
├── readme_en.md
└── img/
    ├── horizontal_lines.png
    ├── vertical_lines.png
    ├── vertical_horizontal_lines.png
    └── mixed_lines.png
```

---

## Какой скрипт с какой картинкой

| Скрипт | Картинка | Что показывает |
|---|---|---|
| `01_line_segment_camera.py` | камера | Поиск линий в реальном времени с камеры |
| `02_line_segment_static.py` | без файла | Учебный пример: рисует линии в памяти и ищет их |
| `03_line_segment_from_images.py` | по умолчанию `vertical_horizontal_lines.png` или картинка из `IMAGE_PATH` | Универсальный пример: можно искать все, только горизонтальные или только вертикальные линии |
| `04_detect_horizontal_lines.py` | `img/horizontal_lines.png` | Ищет только горизонтальные линии |
| `05_detect_vertical_lines.py` | `img/vertical_lines.png` | Ищет только вертикальные линии |
| `06_detect_all_lines_overlay.py` | `img/mixed_lines.png` | Ищет все линии и раскрашивает: горизонтальные, вертикальные, наклонные |

Цвета в примерах:

- зелёный — горизонтальные линии;
- красный — вертикальные линии;
- синий — наклонные линии;
- жёлтый текст — количество найденных линий.

---

## Куда положить картинки

На компьютере картинки лежат в репозитории:

```text
Graphics detection/Line segment detection/img/
```

На плате K230 скопируйте их на SD-карту в такой же путь:

```text
/sdcard/Graphics detection/Line segment detection/img/
```

Если путь другой, измените строку `IMAGE_PATH` в нужном скрипте:

```python
IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/horizontal_lines.png"
```

---

## Как запускать

### Вариант 1. Камера

Запустите:

```text
01_line_segment_camera.py
```

Наведите камеру на объект с прямыми линиями. Найденные линии будут нарисованы поверх изображения.

### Вариант 2. Картинки

1. Скопируйте папку `img` на SD-карту K230.
2. Откройте нужный скрипт в CanMV IDE.
3. Проверьте `IMAGE_PATH`.
4. Запустите скрипт.
5. Смотрите результат на экране или во frame buffer.

---

## Настройка универсального скрипта

В `03_line_segment_from_images.py` можно менять режим:

```python
DETECT_MODE = "all"
```

Доступные варианты:

```python
DETECT_MODE = "all"         # искать все линии
DETECT_MODE = "horizontal"  # искать только горизонтальные
DETECT_MODE = "vertical"    # искать только вертикальные
```

Также можно менять картинку:

```python
IMAGE_PATH = "/sdcard/Graphics detection/Line segment detection/img/mixed_lines.png"
```

---

## Основной API

```python
lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)
```

- `merge_distance` — максимальное расстояние между двумя отрезками, при котором они могут быть объединены;
- `max_theta_diff` — максимальная разница углов для объединения отрезков;
- результат — список линий;
- координаты линии можно получить через `line.line()`.

Пример:

```python
for line in lines:
    coords = line.line()
    img.draw_line(coords, color=(0, 255, 0), thickness=3)
```

---

## Чтение и запись файлов

### Чтение текстового файла

```python
with open("/sdcard/data.txt", "r") as f:
    data = f.read()
print(data)
```

### Запись текстового файла

```python
with open("/sdcard/result.txt", "w") as f:
    f.write("Hello K230")
```

### Пример записи координат линий

```python
with open("/sdcard/lines.csv", "w") as f:
    f.write("x1,y1,x2,y2\n")
    for line in lines:
        x1, y1, x2, y2 = line.line()
        f.write("%d,%d,%d,%d\n" % (x1, y1, x2, y2))
```

---

## Если картинка не открывается

Проверьте:

1. файл действительно лежит на SD-карте;
2. имя файла совпадает с `IMAGE_PATH`;
3. расширение `.png` написано правильно;
4. путь не содержит лишних пробелов;
5. картинка имеет понятный формат, лучше `PNG`, `640x480`.

---

## Если линии не находятся

Попробуйте:

- сделать линии толще: 3–6 пикселей;
- использовать белые линии на чёрном фоне;
- увеличить `merge_distance`;
- увеличить `ANGLE_TOLERANCE_DEG` для фильтрации горизонтальных/вертикальных линий;
- проверить, что линии не касаются края изображения.

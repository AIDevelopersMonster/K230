# K230: AprilTag Recognition

Эта папка содержит демонстрационные примеры для **Yahboom K230 Vision Module** по теме распознавания AprilTag. Камера K230 получает изображение, ищет теги через `img.find_apriltags()`, определяет семейство тега, ID, координаты, центр и угол поворота.

AprilTag — это двумерная визуальная метка, которая часто используется в робототехнике, навигации, дополненной реальности, калибровке камер и визуальном позиционировании. В отличие от QR-кода, AprilTag обычно кодирует числовой ID и хорошо подходит для определения положения и ориентации объекта.

## Файлы

| Файл | Назначение |
| --- | --- |
| `01_apriltag_recognition.py` | Базовая демонстрация: поиск AprilTag, рамка, центр, family, ID, rotation и FPS. |
| `02_apriltag_uart.py` | Распознавание AprilTag + отправка координат, ID и rotation через UART/Yahboom protocol. |
| `03_apriltag_file_io.py` | Распознавание AprilTag + чтение ROI/семейств из файла и запись результата в файл. |
| `readme.md` | Инструкция на русском языке. |
| `readme_en.md` | Instruction in English. |

## Быстрый старт

1. Подготовьте AprilTag. Можно использовать теги из материалов Yahboom или генератор AprilTag в CanMV IDE.
2. Откройте `01_apriltag_recognition.py` в CanMV IDE.
3. Подключите K230 к компьютеру по USB.
4. Запустите скрипт.
5. Наведите камеру на AprilTag так, чтобы метка была хорошо видна и находилась в фокусе.
6. На экране появится красная рамка вокруг тега, зеленый крест в центре и подпись с семейством, ID и углом поворота.
7. В консоли CanMV IDE будет выводиться строка вида:

```text
Tag Family TAG36H11, Tag ID 0, rotation 2.836 degrees
```

## Как работает распознавание AprilTag

Основная функция:

```python
tags = img.find_apriltags(families=tag_families)
```

Она возвращает список объектов `image.apriltag`. Для каждого найденного тега можно получить:

```python
tag.rect()             # (x, y, w, h), рамка тега
tag.id()               # числовой ID внутри семейства
tag.family()           # семейство тега
tag.cx(), tag.cy()     # центр тега
tag.rotation()         # угол поворота в радианах
tag.decision_margin()  # уверенность распознавания
tag.hamming()          # допустимая/исправленная ошибка Хэмминга
```

Рамка и центр рисуются так:

```python
img.draw_rectangle(tag.rect(), color=(255, 0, 0), thickness=4)
img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0), thickness=2)
```

Угол поворота переводится в градусы:

```python
rotation_deg = (180.0 * tag.rotation()) / math.pi
```

## Семейства AprilTag

В примерах можно включать разные семейства:

```python
tag_families = 0
tag_families |= image.TAG16H5
tag_families |= image.TAG25H7
tag_families |= image.TAG25H9
tag_families |= image.TAG36H10
tag_families |= image.TAG36H11
tag_families |= image.ARTOOLKIT
```

Чем больше семейств включено одновременно, тем ниже может быть FPS. Для большинства демонстраций удобно использовать `TAG36H11`.

## ROI: ускорение поиска

По умолчанию пример ищет AprilTag по всему кадру:

```python
APRILTAG_ROI = None
```

Для ускорения можно ограничить область поиска:

```python
APRILTAG_ROI = (40, 20, 320, 200)
```

ROI имеет формат:

```python
(x, y, w, h)
```

Если тег всегда находится в центре кадра, ROI может повысить FPS.

## Пример с UART

Файл `02_apriltag_uart.py` отправляет данные через Yahboom protocol:

```python
pto_data = pto.get_apriltag_data(x, y, w, h, tag.id(), rotation_deg)
uart.send(pto_data)
```

UART инициализируется так:

```python
uart = YbUart(baudrate=115200)
```

Если в прошивке нет библиотек `libs.YbProtocol` или `ybUtils.YbUart`, пример не падает, а отключает UART и продолжает распознавание на экране.

## Чтение файлов на K230

Файл `03_apriltag_file_io.py` показывает чтение настроек из текстового файла.

Имя файла:

```text
apriltag_config.txt
```

Пример содержимого:

```text
# K230 AprilTag Recognition config
USE_ROI=0
ROI=40,20,320,200
FAMILIES=TAG36H11
```

Чтение файла:

```python
with open("/sdcard/apriltag_config.txt", "r") as f:
    text = f.read()
```

Разбор строки:

```python
key, value = line.split("=", 1)
```

Разбор ROI:

```python
parts = value.replace(" ", "").split(",")
roi = tuple([int(v) for v in parts])
```

Разбор семейств:

```python
FAMILIES=TAG16H5,TAG25H7,TAG36H11
```

На CanMV/K230 относительный путь иногда недоступен для записи при запуске из IDE. Поэтому пример сначала ищет доступную папку:

```python
FILE_DIR_CANDIDATES = ["/sdcard", "/data", "/flash", "/"]
```

Если файловая система недоступна для записи, пример продолжает работать со значениями по умолчанию.

## Запись файлов на K230

Запись выполняется через `open(..., "w")`:

```python
with open("/sdcard/apriltag_result.txt", "w") as f:
    f.write("family=TAG36H11\nid=0\n")
```

Режимы открытия:

| Режим | Что делает |
| --- | --- |
| `"r"` | Чтение существующего файла. |
| `"w"` | Запись с заменой старого содержимого. Если файла нет, он будет создан. |
| `"a"` | Добавление текста в конец файла. |

Файл результата `apriltag_result.txt` обновляется при распознавании:

```text
time_ms=123456
fps=45.500
family=TAG36H11
id=0
rotation_deg=2.836
x=120
y=70
w=95
h=95
cx=167
cy=117
decision_margin=48.2
hamming=0
```

Почему не записывать каждый кадр: один и тот же тег может распознаваться много раз подряд, поэтому в примере есть ограничение частоты записи.

## Рекомендации для хорошего распознавания

1. Используйте четко напечатанный AprilTag с высоким контрастом.
2. Держите метку в фокусе.
3. Уберите блики и сильные тени.
4. Не делайте метку слишком маленькой в кадре.
5. Для лучшего FPS включайте только нужное семейство, например `TAG36H11`.
6. Если тег всегда в одной области кадра, используйте ROI.
7. При сильной перспективе или плохом освещении увеличьте размер тега или улучшите свет.

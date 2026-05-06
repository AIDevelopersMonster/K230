# K230: FaceRecognition / GazeDirection

Эта папка содержит демонстрационные примеры для **Yahboom K230 Vision Module** по теме **Gaze direction detection** — определение направления взгляда.

Примеры сделаны по PDF **Gaze direction detection** и рабочему примеру производителя. В PDF указано, что исходный пример находится в `Source code/07.Face/05.eye_gaze.py`: после запуска K230 находит лицо, оценивает направление взгляда и показывает на экране стрелку, куда смотрят глаза.

## Важно: общий файл лежит в `libs`

В этих примерах общий код вынесен в библиотеку:

```text
libs/gaze_direction_common.py
```

На K230 этот файл нужно положить сюда:

```text
/sdcard/libs/gaze_direction_common.py
```

Примеры импортируют его так:

```python
from libs.gaze_direction_common import create_eye_gaze_app, safe_deinit
```

Если положить `gaze_direction_common.py` только рядом с примерами в `FaceRecognition/GazeDirection`, импорт `from libs.gaze_direction_common ...` его не найдет.

## Файлы

| Файл | Назначение |
| --- | --- |
| `../../libs/gaze_direction_common.py` | Общая библиотека: `FaceDetApp`, `EyeGazeApp`, `EyeGaze`, UART helpers. |
| `01_gaze_direction_basic.py` | Базовый пример: обнаружение лица, оценка взгляда и стрелка на экране. |
| `02_gaze_direction_uart.py` | Оценка взгляда + UART-вывод координат стрелки. |
| `03_gaze_direction_file_io.py` | Оценка взгляда + чтение конфига и запись результата в TXT/CSV. |
| `04_file_read_write_basic.py` | Простой учебный пример чтения и записи файлов без AI. |
| `readme.md` | Инструкция на русском. |
| `readme_en.md` | English instructions. |

## Что демонстрирует Gaze Direction Detection

Алгоритм выполняет два этапа:

```text
Face Detection → Eye Gaze Estimation
```

1. `FaceDetApp` находит лицо и возвращает рамку `x, y, w, h`.
2. `EyeGazeApp` вырезает область лица через `crop` и масштабирует ее до входа модели.
3. Модель `eye_gaze.kmodel` возвращает параметры `pitch` и `yaw`.
4. Код переводит `pitch/yaw` в 2D-вектор через тригонометрию.
5. `draw_result()` рисует стрелку направления взгляда на OSD-слое.

## Что нужно на TF-карте

Убедитесь, что на K230 есть модели и anchors:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/eye_gaze.kmodel
/sdcard/utils/prior_data_320.bin
```

Если пути отличаются, используйте `03_gaze_direction_file_io.py`: он создаст конфиг, где можно изменить пути.

## Быстрый старт

1. Скопируйте `libs/gaze_direction_common.py` из репозитория на K230:

```text
/sdcard/libs/gaze_direction_common.py
```

2. Скопируйте папку `FaceRecognition/GazeDirection` на TF-карту или откройте пример в CanMV IDE.
3. Подключите Yahboom K230 Vision Module по USB.
4. Запустите `01_gaze_direction_basic.py`.
5. Наведите камеру на лицо.
6. На экране должна появиться стрелка, показывающая направление взгляда.

## Как работает AI-пайплайн

Общий поток:

```text
Sensor → Frame → Face Detection → Eye Gaze AI → OSD → Display
```

В коде:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, eye_gaze_res = eg.run(img)
eg.draw_result(pl, det_boxes, eye_gaze_res)
pl.show_image()
```

`PipeLine` управляет камерой и дисплеем, поэтому в одной программе должен быть только один объект `PipeLine`.

## Почему используется pad перед resize

Для модели обнаружения лица preprocessing должен сохранить пропорции кадра:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

Если сделать только `resize`, рамка лица и стрелка взгляда могут сместиться.

## Почему используется crop для Eye Gaze

После обнаружения лица модель взгляда должна получить область лица:

```python
x, y, w, h = map(lambda v: int(round(v, 0)), det[:4])
self.ai2d.crop(x, y, w, h)
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

После inference вызывается:

```python
post_ret = aidemo.eye_gaze_post_process(results)
```

Она возвращает `pitch` и `yaw`.

## Как строится стрелка направления взгляда

Старт стрелки — центр найденного лица:

```python
center_x = x + w / 2.0
center_y = y + h / 2.0
```

Конец стрелки рассчитывается по `pitch` и `yaw`:

```python
dx = -length * math.sin(pitch) * math.cos(yaw)
target_x = int(center_x + dx)
dy = -length * math.sin(yaw)
target_y = int(center_y + dy)
```

Затем стрелка рисуется:

```python
pl.osd_img.draw_arrow(center_x, center_y, target_x, target_y)
```

## UART-вывод

`02_gaze_direction_uart.py` отправляет координаты стрелки через UART в формате:

```text
$x0,y0,x1,y1#
```

Где:

| Поле | Значение |
| --- | --- |
| `x0, y0` | начало стрелки |
| `x1, y1` | конец стрелки |

Если библиотеки Yahboom `YbProtocol` и `YbUart` доступны, используется:

```python
pto.get_eye_gaze_data(x0, y0, x1, y1)
uart.send(pto_data)
```

Если UART-библиотеки недоступны, пример продолжит рисовать стрелку и печатать текстовый пакет в консоль.

## Чтение файлов на K230

Файл читается через `open()` в режиме `"r"`:

```python
with open("/sdcard/FaceRecognition/GazeDirection/gaze_direction_config.txt", "r") as f:
    text = f.read()
```

В `03_gaze_direction_file_io.py` конфиг имеет вид:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
EYE_GAZE_KMODEL_PATH=/sdcard/kmodel/eye_gaze.kmodel
ANCHORS_PATH=/sdcard/utils/prior_data_320.bin
CONFIDENCE_THRESHOLD=0.50
NMS_THRESHOLD=0.20
WRITE_INTERVAL_MS=1000
```

Разбор строки:

```python
key, value = line.split("=", 1)
cfg[key.strip().upper()] = value.strip()
```

## Запись файлов на K230

Для записи используется режим `"w"`. Он создает файл или полностью перезаписывает старое содержимое:

```python
with open("/sdcard/FaceRecognition/GazeDirection/gaze_direction_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Для добавления строк в конец файла используется режим `"a"`:

```python
with open("/sdcard/FaceRecognition/GazeDirection/gaze_direction_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,x0,y0,x1,y1,pitch,yaw\n")
```

### Режимы open()

| Режим | Что делает |
| --- | --- |
| `"r"` | Чтение существующего файла. Если файла нет — ошибка. |
| `"w"` | Запись заново. Старое содержимое удаляется. |
| `"a"` | Добавление данных в конец файла. Старое содержимое сохраняется. |

## Какие файлы создает пример 03

При запуске `03_gaze_direction_file_io.py` создается папка:

```text
/sdcard/FaceRecognition/GazeDirection
```

В ней появляются:

```text
gaze_direction_config.txt       # настройки моделей и записи
gaze_direction_last_result.txt  # последний результат
gaze_direction_log.csv          # история результатов
```

Пример `gaze_direction_last_result.txt`:

```text
time_ms=123456
fps=18.500
face_count=1
x0=320
y0=240
x1=120
y1=200
pitch=0.123456
yaw=-0.234567
```

## Почему запись ограничена по времени

Gaze Direction Detection работает в бесконечном цикле. Если писать файл каждый кадр, TF-карта будет получать слишком много операций записи. Поэтому в конфиге есть параметр:

```text
WRITE_INTERVAL_MS=1000
```

Это означает: записывать результат не чаще одного раза в секунду.

## Советы

1. Используйте хорошее освещение.
2. Держите лицо достаточно крупно в кадре.
3. Используйте `rgb888p_size=[640, 480]` и `display_size=[640, 480]` для корректного вывода на LCD.
4. Если лицо не находится, уменьшите `CONFIDENCE_THRESHOLD`, например до `0.40`.
5. Если стрелка смещена, проверьте `pad → resize` для Face Detection и `crop → resize` для Eye Gaze.
6. Убедитесь, что на плате лежит свежий файл `/sdcard/libs/gaze_direction_common.py`.

---

**Автор:** AIDevelopersMonster  
**Плата:** Yahboom K230 Vision Module  
**Репозиторий:** https://github.com/AIDevelopersMonster/K230

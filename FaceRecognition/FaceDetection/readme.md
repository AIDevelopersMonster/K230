# K230: FaceRecognition / FaceDetection

Эта папка содержит демонстрационные примеры для **Yahboom K230 Vision Module** по теме **Face Detection** — обнаружение лиц на изображении.

Примеры сделаны по PDF **Face Detection** и используют структуру K230 AI Vision: камера получает кадр, `PipeLine` передает RGBP888-изображение в AI, модель выполняет inference, `aidemo.face_det_post_process()` возвращает координаты лиц, а результат рисуется на OSD-слое поверх изображения.

> В названии папки сохранено написание из запроса: `FaceDetection`.

## Файлы

| Файл | Назначение |
| --- | --- |
| `01_face_detection_basic.py` | Базовый пример: обнаружение лиц и желтые рамки на экране. |
| `02_face_detection_uart.py` | Обнаружение лиц + отправка координат рамки через UART. Формат: `$x,y,w,h#`. |
| `03_face_detection_file_io.py` | Обнаружение лиц + чтение настроек из файла и запись результата в TXT/CSV. |
| `04_file_read_write_basic.py` | Простой учебный пример чтения и записи файлов без AI. |
| `readme.md` | Инструкция на русском. |
| `readme_en.md` | English instructions. |

## Что демонстрирует Face Detection

Face Detection находит лица в кадре и возвращает прямоугольники:

```text
x, y, w, h
```

Где:

| Поле | Значение |
| --- | --- |
| `x` | координата левого верхнего угла рамки по X |
| `y` | координата левого верхнего угла рамки по Y |
| `w` | ширина рамки |
| `h` | высота рамки |

В примерах используется разрешение:

```python
rgb888p_size = [640, 480]
display_size = [640, 480]
```

Это важно: если AI-кадр и экран имеют разные пропорции, рамка может быть смещена.

## Что нужно на TF-карте

Убедитесь, что на K230 есть модель и anchors:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/utils/prior_data_320.bin
```

Если файлы лежат в другом месте, используйте пример `03_face_detection_file_io.py`: он создает конфиг, где можно изменить пути.

## Быстрый старт

1. Откройте `01_face_detection_basic.py` в CanMV IDE.
2. Подключите Yahboom K230 Vision Module по USB.
3. Запустите пример.
4. Наведите камеру на лицо.
5. На экране появится желтая рамка вокруг лица.

## Как работает AI-пайплайн

Общий поток:

```text
Sensor → Frame → AI → OSD → Display
```

В коде:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
res = face_det.run(img)
face_det.draw_result(pl, res)
pl.show_image()
```

`PipeLine` управляет камерой и дисплеем, поэтому в одной программе должен быть только один объект `PipeLine`.

## Почему используется pad перед resize

В примерах preprocessing сделан как у производителя Yahboom:

```python
top, bottom, left, right = self.get_padding_param()
self.ai2d.pad([0, 0, 0, 0, top, bottom, left, right], 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

`pad` нужен, чтобы сохранить пропорции исходного кадра перед приведением изображения к размеру модели `320x320`. Если сделать только `resize`, изображение может исказиться, и рамка будет рисоваться не вокруг лица.

## Основные части FaceDetectionApp

Класс `FaceDetectionApp` наследуется от `AIBase` и содержит:

1. `__init__()` — пути, thresholds, anchors, размеры кадра и дисплея.
2. `get_padding_param()` — расчет padding.
3. `config_preprocess()` — настройка AI2D: `pad` → `resize`.
4. `postprocess()` — вызов `aidemo.face_det_post_process()`.
5. `draw_result()` — отрисовка рамок на `pl.osd_img`.
6. `deinit()` — освобождение ресурсов модели.

## UART пример

`02_face_detection_uart.py` отправляет координаты лица в формате:

```text
$x,y,w,h#
```

Пример:

```text
$180,90,120,120#
```

Если на прошивке доступны `YbProtocol` и `YbUart`, пример использует Yahboom-протокол:

```python
pto.get_face_detect_data(x, y, w, h)
uart.send(pto_data)
```

Если эти библиотеки недоступны, пример продолжит работать на экране и будет печатать текстовый пакет в консоль.

## Чтение файлов на K230

Файл читается через `open()` в режиме `"r"`:

```python
with open("/sdcard/FaceRecognition/FaceDetectition/face_detection_config.txt", "r") as f:
    text = f.read()
```

В `03_face_detection_file_io.py` конфиг имеет вид:

```text
KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
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
with open("/sdcard/FaceRecognition/FaceDetectition/face_detection_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Для добавления строк в конец файла используется режим `"a"`:

```python
with open("/sdcard/FaceRecognition/FaceDetectition/face_detection_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,x,y,w,h\n")
```

### Режимы open()

| Режим | Что делает |
| --- | --- |
| `"r"` | Чтение существующего файла. Если файла нет — ошибка. |
| `"w"` | Запись заново. Старое содержимое удаляется. |
| `"a"` | Добавление данных в конец файла. Старое содержимое сохраняется. |

## Какие файлы создает пример 03

При запуске `03_face_detection_file_io.py` создается папка:

```text
/sdcard/FaceRecognition/FaceDetectition
```

В ней появляются:

```text
face_detection_config.txt       # настройки модели и записи
face_detection_last_result.txt  # последний результат обнаружения
face_detection_log.csv          # история результатов
```

Пример `face_detection_last_result.txt`:

```text
time_ms=123456
fps=22.500
face_count=1
x=180
y=90
w=120
h=120
```

## Почему запись ограничена по времени

Face Detection работает в бесконечном цикле. Если писать файл каждый кадр, TF-карта будет получать слишком много операций записи. Поэтому в конфиге есть параметр:

```text
WRITE_INTERVAL_MS=1000
```

Это означает: записывать результат не чаще одного раза в секунду.

## Советы

1. Используйте хорошее освещение.
2. Держите лицо достаточно крупно в кадре.
3. Используйте `rgb888p_size=[640, 480]` и `display_size=[640, 480]` для корректной рамки на LCD.
4. Если лицо не находится, уменьшите `CONFIDENCE_THRESHOLD`, например до `0.40`.
5. Если есть ложные срабатывания, увеличьте `CONFIDENCE_THRESHOLD`, например до `0.60`.
6. Если рамка смещается, проверьте наличие `pad` перед `resize` в `config_preprocess()`.

---

**Автор:** AIDevelopersMonster  
**Плата:** Yahboom K230 Vision Module  
**Репозиторий:** https://github.com/AIDevelopersMonster/K230

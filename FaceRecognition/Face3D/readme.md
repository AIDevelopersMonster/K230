# K230: FaceRecognition / Face3D

Эта папка содержит демонстрационные примеры для **Yahboom K230 Vision Module** по теме **Face 3D Network** — построение 3D-сетки лица.

Примеры сделаны по PDF **Face 3D Network** и рабочему примеру производителя. В PDF указано, что пример находится в `Source code summary/07.Face/04.face_mesh.py`: после запуска и наведения камеры на лицо экран покрывает лицо 3D-сеткой. Также в PDF отмечено, что модель Face 3D Network достаточно большая, поэтому в первые несколько секунд лицо может не распознаваться, а при большом количестве лиц на экране система может зависнуть.

## Важно: общий файл лежит в `libs`

В этих примерах общий код вынесен в библиотеку:

```text
libs/face3d_common.py
```

На K230 этот файл нужно положить сюда:

```text
/sdcard/libs/face3d_common.py
```

Примеры импортируют его так:

```python
from libs.face3d_common import create_face_mesh_app
```

Если положить `face3d_common.py` только рядом с примерами в `FaceRecognition/Face3D`, импорт `from libs.face3d_common ...` его не найдет.

## Файлы

| Файл | Назначение |
| --- | --- |
| `../../libs/face3d_common.py` | Общая библиотека: `FaceDetApp`, `FaceMeshApp`, `FaceMeshPostApp`, `FaceMesh`. |
| `01_face3d_basic.py` | Базовый пример: обнаружение лица, построение 3D-сетки и вывод на экран. |
| `02_face3d_file_io.py` | Face3D + чтение конфига и запись результата в TXT/CSV. |
| `03_file_read_write_basic.py` | Простой учебный пример чтения и записи файлов без AI. |
| `readme.md` | Инструкция на русском. |
| `readme_en.md` | English instructions. |

## Что демонстрирует Face 3D Network

Алгоритм выполняет несколько шагов:

```text
Face Detection → Face Mesh Params → Face Mesh Postprocess → OSD → Display
```

1. `FaceDetApp` находит лицо и возвращает рамку `x, y, w, h`.
2. `FaceMeshApp` рассчитывает ROI вокруг лица, делает `crop → resize` и запускает `face_alignment.kmodel`.
3. Результаты модели нормализуются через статистические параметры `param_mean` и `param_std`.
4. `FaceMeshPostApp` преобразует параметры лица в вершины 3D-сетки через `face_alignment_post.kmodel`.
5. `aidemo.face_mesh_post_process()` переносит точки в координаты экрана.
6. `aidemo.face_draw_mesh()` рисует 3D-сетку поверх лица.

## Что нужно на TF-карте

Убедитесь, что на K230 есть модели и anchors:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/face_alignment.kmodel
/sdcard/kmodel/face_alignment_post.kmodel
/sdcard/utils/prior_data_320.bin
```

Если пути отличаются, используйте `02_face3d_file_io.py`: он создаст конфиг, где можно изменить пути.

## Быстрый старт

1. Скопируйте `libs/face3d_common.py` из репозитория на K230:

```text
/sdcard/libs/face3d_common.py
```

2. Скопируйте папку `FaceRecognition/Face3D` на TF-карту или откройте пример в CanMV IDE.
3. Подключите Yahboom K230 Vision Module по USB.
4. Запустите `01_face3d_basic.py`.
5. Наведите камеру на лицо.
6. Через несколько секунд на лице должна появиться 3D-сетка.

## Почему первые секунды может не быть распознавания

В PDF отдельно указано: модель для Face 3D Network относительно большая, поэтому нормально, если лицо не распознается в первые несколько секунд после запуска.

## Почему не стоит показывать много лиц сразу

В PDF также указано: если на экране одновременно слишком много лиц, система может зависнуть. В таком случае нужно нажать **RST** для перезапуска. Чтобы избежать зависаний, можно ограничить количество обрабатываемых лиц в методе `run()`.

Например, обрабатывать только первое найденное лицо:

```python
for det_box in det_boxes[:1]:
    ...
```

## Как работает AI-пайплайн

В коде основной цикл выглядит так:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, mesh_res = fm.run(img)
fm.draw_result(pl, det_boxes, mesh_res)
pl.show_image()
```

`PipeLine` управляет камерой и дисплеем, поэтому в одной программе должен быть только один объект `PipeLine`.

## Почему используется pad перед resize

Для модели обнаружения лица preprocessing должен сохранить пропорции кадра:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

Если сделать только `resize`, рамка лица и последующая 3D-сетка могут сместиться.

## Почему используется crop для Face Mesh

После обнаружения лица `FaceMeshApp` рассчитывает область ROI вокруг лица:

```python
roi = self.parse_roi_box_from_bbox(det)
self.ai2d.crop(int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3]))
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

ROI немного расширяется и смещается вниз, чтобы захватить все лицо и подбородок.

## Чтение файлов на K230

Файл читается через `open()` в режиме `"r"`:

```python
with open("/sdcard/FaceRecognition/Face3D/face3d_config.txt", "r") as f:
    text = f.read()
```

В `02_face3d_file_io.py` конфиг имеет вид:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
FACE_MESH_KMODEL_PATH=/sdcard/kmodel/face_alignment.kmodel
FACE_MESH_POST_KMODEL_PATH=/sdcard/kmodel/face_alignment_post.kmodel
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
with open("/sdcard/FaceRecognition/Face3D/face3d_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Для добавления строк в конец файла используется режим `"a"`:

```python
with open("/sdcard/FaceRecognition/Face3D/face3d_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,mesh_count\n")
```

### Режимы open()

| Режим | Что делает |
| --- | --- |
| `"r"` | Чтение существующего файла. Если файла нет — ошибка. |
| `"w"` | Запись заново. Старое содержимое удаляется. |
| `"a"` | Добавление данных в конец файла. Старое содержимое сохраняется. |

## Какие файлы создает пример 02

При запуске `02_face3d_file_io.py` создается папка:

```text
/sdcard/FaceRecognition/Face3D
```

В ней появляются:

```text
face3d_config.txt       # настройки моделей и записи
face3d_last_result.txt  # последний результат
face3d_log.csv          # история результатов
```

Пример `face3d_last_result.txt`:

```text
time_ms=123456
fps=8.500
face_count=1
mesh_count=1
first_mesh_len=1434
```

## Почему запись ограничена по времени

Face 3D Network работает в бесконечном цикле. Если писать файл каждый кадр, TF-карта будет получать слишком много операций записи. Поэтому в конфиге есть параметр:

```text
WRITE_INTERVAL_MS=1000
```

Это означает: записывать результат не чаще одного раза в секунду.

## Где применяется Face 3D Network

В PDF перечислены сценарии применения: безопасная аутентификация, медицина, AR/VR, умная розница, анализ эмоций, игры и развлечения, телемедицина, виртуальный макияж и примерка очков.

## Советы

1. Используйте хорошее освещение.
2. Держите лицо достаточно крупно в кадре.
3. Используйте `rgb888p_size=[640, 480]` и `display_size=[640, 480]` для корректного вывода на LCD.
4. Не показывайте много лиц одновременно: модель тяжелая, система может зависнуть.
5. Если нужно повысить стабильность, обрабатывайте только первое лицо: `det_boxes[:1]`.
6. Убедитесь, что на плате лежит свежий файл `/sdcard/libs/face3d_common.py`.

---

**Автор:** AIDevelopersMonster  
**Плата:** Yahboom K230 Vision Module  
**Репозиторий:** https://github.com/AIDevelopersMonster/K230

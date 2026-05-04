# K230: FaceRecognition / KeyPointRecognition

Эта папка содержит демонстрационные примеры для **Yahboom K230 Vision Module** по теме **Facial key point recognition** — распознавание ключевых точек лица.

Примеры сделаны по PDF **Facial key point recognition** и рабочему примеру производителя. В PDF указано, что пример находится в `Source code/07.Face/02.face_landmark.py`: сначала выполняется Face Detection, затем для каждого найденного лица запускается модель ключевых точек, а результат рисуется на экране как контуры глаз, бровей, носа, губ и овала лица.

## Файлы

| Файл | Назначение |
| --- | --- |
| `01_face_landmark_basic.py` | Полный базовый пример распознавания ключевых точек лица. Можно запускать отдельно. |
| `keypoint_common.py` | Общий модуль с классами `FaceDetApp`, `FaceLandMarkApp`, `FaceLandMark`. Используется в примере 02. |
| `02_face_landmark_file_io.py` | Распознавание ключевых точек + чтение конфига и запись результата в TXT/CSV. |
| `03_file_read_write_basic.py` | Простой учебный пример чтения и записи файлов без AI. |
| `readme.md` | Инструкция на русском. |
| `readme_en.md` | English instructions. |

## Что демонстрирует Key Point Recognition

Алгоритм выполняет два шага:

```text
Face Detection → Face Landmark Recognition
```

1. `FaceDetApp` находит лицо и возвращает рамку `x, y, w, h`.
2. `FaceLandMarkApp` вырезает/нормализует область лица через affine transform.
3. Модель `face_landmark.kmodel` предсказывает ключевые точки.
4. Обратное affine-преобразование возвращает точки в координаты исходного изображения.
5. `draw_result()` рисует контуры лица на OSD-слое.

В примере используется 106 ключевых точек лица: брови, глаза, зрачки, нос, губы и контур лица.

## Что нужно на TF-карте

Убедитесь, что на K230 есть модели и anchors:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/face_landmark.kmodel
/sdcard/utils/prior_data_320.bin
```

Если файлы лежат в другом месте, используйте `02_face_landmark_file_io.py`: он создаст конфиг, где можно изменить пути.

## Быстрый старт

1. Откройте `01_face_landmark_basic.py` в CanMV IDE.
2. Подключите Yahboom K230 Vision Module по USB.
3. Запустите пример.
4. Наведите камеру на лицо.
5. На экране должны появиться цветные линии и точки на лице.

Для примера 02 нужно скопировать два файла в одну папку на TF-карте:

```text
/sdcard/FaceRecognition/KeyPointRecognition/keypoint_common.py
/sdcard/FaceRecognition/KeyPointRecognition/02_face_landmark_file_io.py
```

## Как работает AI-пайплайн

Общий поток:

```text
Sensor → Frame → Face Detection → Landmark AI → OSD → Display
```

В коде:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, landmark_res = flm.run(img)
flm.draw_result(pl, det_boxes, landmark_res)
pl.show_image()
```

`PipeLine` управляет камерой и дисплеем, поэтому в одной программе должен быть только один объект `PipeLine`.

## Почему используется pad перед resize

Для модели обнаружения лица preprocessing должен сохранить пропорции кадра:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

Если сделать только `resize`, рамка лица и точки могут сместиться.

## Почему используется affine transform

Для ключевых точек лица нужно подать в модель нормализованную область лица. Поэтому для каждого найденного лица создается affine matrix:

```python
self.matrix_dst = self.get_affine_matrix(det)
self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, affine_matrix)
```

После inference координаты ключевых точек возвращаются обратно через inverse affine transform:

```python
matrix_dst_inv = aidemo.invert_affine_transform(self.matrix_dst)
```

Это позволяет рисовать точки на правильных местах исходного кадра.

## Чтение файлов на K230

Файл читается через `open()` в режиме `"r"`:

```python
with open("/sdcard/FaceRecognition/KeyPointRecognition/keypoint_config.txt", "r") as f:
    text = f.read()
```

В `02_face_landmark_file_io.py` конфиг имеет вид:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
FACE_LANDMARK_KMODEL_PATH=/sdcard/kmodel/face_landmark.kmodel
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
with open("/sdcard/FaceRecognition/KeyPointRecognition/keypoint_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Для добавления строк в конец файла используется режим `"a"`:

```python
with open("/sdcard/FaceRecognition/KeyPointRecognition/keypoint_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,keypoint_count\n")
```

### Режимы open()

| Режим | Что делает |
| --- | --- |
| `"r"` | Чтение существующего файла. Если файла нет — ошибка. |
| `"w"` | Запись заново. Старое содержимое удаляется. |
| `"a"` | Добавление данных в конец файла. Старое содержимое сохраняется. |

## Какие файлы создает пример 02

При запуске `02_face_landmark_file_io.py` создается папка:

```text
/sdcard/FaceRecognition/KeyPointRecognition
```

В ней появляются:

```text
keypoint_config.txt       # настройки моделей и записи
keypoint_last_result.txt  # последний результат
keypoint_log.csv          # история результатов
```

Пример `keypoint_last_result.txt`:

```text
time_ms=123456
fps=12.500
face_count=1
keypoint_count=106
first_keypoint_x=180
first_keypoint_y=90
```

## Почему запись ограничена по времени

Распознавание работает в бесконечном цикле. Если писать файл каждый кадр, TF-карта будет получать слишком много операций записи. Поэтому в конфиге есть параметр:

```text
WRITE_INTERVAL_MS=1000
```

Это означает: записывать результат не чаще одного раза в секунду.

## Советы

1. Используйте хорошее освещение.
2. Держите лицо достаточно крупно в кадре.
3. Используйте `rgb888p_size=[640, 480]` и `display_size=[640, 480]` для корректного вывода на LCD.
4. Если лицо не находится, уменьшите `CONFIDENCE_THRESHOLD`, например до `0.40`.
5. Если точки смещены, проверьте `pad → resize` для Face Detection и affine transform для Landmark.
6. Для `02_face_landmark_file_io.py` убедитесь, что рядом лежит `keypoint_common.py`.

---

**Автор:** AIDevelopersMonster  
**Плата:** Yahboom K230 Vision Module  
**Репозиторий:** https://github.com/AIDevelopersMonster/K230

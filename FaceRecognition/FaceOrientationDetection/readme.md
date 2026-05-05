# K230: FaceRecognition / FaceOrientationDetection

Эта папка содержит демонстрационные примеры для **Yahboom K230 Vision Module** по теме **Face orientation detection** — определение ориентации/позы лица.

Примеры сделаны по PDF **Face orientation detection** и рабочему примеру производителя. В PDF указано, что исходный пример находится в `Source code/07.Face/03.face_pose.py`: программа сначала находит лицо, затем оценивает его позу и рисует на экране 3D-куб, показывающий направление лица.

## Файлы

| Файл | Назначение |
| --- | --- |
| `face_pose_common.py` | Общий модуль с классами `FaceDetApp`, `FacePoseApp`, `FacePose`. |
| `01_face_orientation_basic.py` | Базовый пример: обнаружение лица, оценка ориентации и 3D-куб на экране. |
| `02_face_orientation_file_io.py` | Ориентация лица + чтение конфига и запись углов `pitch/yaw/roll` в TXT/CSV. |
| `03_file_read_write_basic.py` | Простой учебный пример чтения и записи файлов без AI. |
| `readme.md` | Инструкция на русском. |
| `readme_en.md` | English instructions. |

## Что демонстрирует Face Orientation Detection

Алгоритм выполняет два шага:

```text
Face Detection → Face Pose Estimation
```

1. `FaceDetApp` находит лицо и возвращает рамку `x, y, w, h`.
2. `FacePoseApp` через affine transform нормализует область лица.
3. Модель `face_pose.kmodel` предсказывает матрицу вращения `R`.
4. `rotation_matrix_to_euler_angles()` переводит матрицу в углы Эйлера:
   - `pitch` — наклон головы вверх/вниз;
   - `yaw` — поворот головы влево/вправо;
   - `roll` — наклон головы к плечу.
5. `draw_result()` строит 3D-проекцию и рисует куб поверх лица.

## Что нужно на TF-карте

Убедитесь, что на K230 есть модели и anchors:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/face_pose.kmodel
/sdcard/utils/prior_data_320.bin
```

Если файлы лежат в другом месте, используйте `02_face_orientation_file_io.py`: он создаст конфиг, где можно изменить пути.

## Быстрый старт

1. Скопируйте папку `FaceRecognition/FaceOrientationDetection` на TF-карту.
2. Убедитесь, что `face_pose_common.py` лежит рядом с примерами:

```text
/sdcard/FaceRecognition/FaceOrientationDetection/face_pose_common.py
```

3. Откройте `01_face_orientation_basic.py` в CanMV IDE.
4. Подключите Yahboom K230 Vision Module по USB.
5. Запустите пример.
6. Наведите камеру на лицо.
7. На экране должен появиться красный 3D-куб, показывающий ориентацию лица.

## Как работает AI-пайплайн

Общий поток:

```text
Sensor → Frame → Face Detection → Face Pose AI → OSD → Display
```

В коде:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, pose_res = fp.run(img)
fp.draw_result(pl, det_boxes, pose_res)
pl.show_image()
```

`PipeLine` управляет камерой и дисплеем, поэтому в одной программе должен быть только один объект `PipeLine`.

## Почему используется pad перед resize

Для модели обнаружения лица preprocessing должен сохранить пропорции кадра:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

Если сделать только `resize`, рамка лица и последующая 3D-визуализация могут сместиться.

## Почему используется affine transform

Модель позы лица должна получить нормализованную область лица. Поэтому для каждого найденного лица строится affine matrix:

```python
matrix_dst = self.get_affine_matrix(det)
self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, matrix_dst)
```

После inference модель возвращает матрицу вращения, из которой вычисляются углы `pitch`, `yaw`, `roll`.

## Чтение файлов на K230

Файл читается через `open()` в режиме `"r"`:

```python
with open("/sdcard/FaceRecognition/FaceOrientationDetection/face_orientation_config.txt", "r") as f:
    text = f.read()
```

В `02_face_orientation_file_io.py` конфиг имеет вид:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
FACE_POSE_KMODEL_PATH=/sdcard/kmodel/face_pose.kmodel
ANCHORS_PATH=/sdcard/utils/prior_data_320.bin
CONFIDENCE_THRESHOLD=0.50
NMS_THRESHOLD=0.20
WRITE_INTERVAL_MS=1000
DRAW_ANGLES=1
```

Разбор строки:

```python
key, value = line.split("=", 1)
cfg[key.strip().upper()] = value.strip()
```

## Запись файлов на K230

Для записи используется режим `"w"`. Он создает файл или полностью перезаписывает старое содержимое:

```python
with open("/sdcard/FaceRecognition/FaceOrientationDetection/face_orientation_last_result.txt", "w") as f:
    f.write("yaw=0.0\n")
```

Для добавления строк в конец файла используется режим `"a"`:

```python
with open("/sdcard/FaceRecognition/FaceOrientationDetection/face_orientation_log.csv", "a") as f:
    f.write("time_ms,fps,face_count,pitch,yaw,roll\n")
```

### Режимы open()

| Режим | Что делает |
| --- | --- |
| `"r"` | Чтение существующего файла. Если файла нет — ошибка. |
| `"w"` | Запись заново. Старое содержимое удаляется. |
| `"a"` | Добавление данных в конец файла. Старое содержимое сохраняется. |

## Какие файлы создает пример 02

При запуске `02_face_orientation_file_io.py` создается папка:

```text
/sdcard/FaceRecognition/FaceOrientationDetection
```

В ней появляются:

```text
face_orientation_config.txt       # настройки моделей и записи
face_orientation_last_result.txt  # последний результат
face_orientation_log.csv          # история результатов
```

Пример `face_orientation_last_result.txt`:

```text
time_ms=123456
fps=20.000
face_count=1
pitch=1.234
yaw=-10.500
roll=2.100
```

## Почему запись ограничена по времени

Оценка ориентации лица работает в бесконечном цикле. Если писать файл каждый кадр, TF-карта будет получать слишком много операций записи. Поэтому в конфиге есть параметр:

```text
WRITE_INTERVAL_MS=1000
```

Это означает: записывать результат не чаще одного раза в секунду.

## Где применяется определение ориентации лица

В PDF перечислены типовые сценарии: мониторинг водителя, анализ внимания, человеко-компьютерное взаимодействие, VR/AR, безопасность, умная розница и помощь при съемке.

## Советы

1. Используйте хорошее освещение.
2. Держите лицо достаточно крупно в кадре.
3. Используйте `rgb888p_size=[640, 480]` и `display_size=[640, 480]` для корректного вывода на LCD.
4. Если лицо не находится, уменьшите `CONFIDENCE_THRESHOLD`, например до `0.40`.
5. Если куб смещен, проверьте `pad → resize` для Face Detection и `affine` для Face Pose.
6. Для примеров 01 и 02 убедитесь, что рядом лежит `face_pose_common.py`.

---

**Автор:** AIDevelopersMonster  
**Плата:** Yahboom K230 Vision Module  
**Репозиторий:** https://github.com/AIDevelopersMonster/K230

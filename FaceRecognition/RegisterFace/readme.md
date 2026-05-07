# K230: FaceRecognition / RegisterFace

Эта папка содержит демонстрационные примеры для **Yahboom K230 Vision Module** по теме **Register for face recognition** — регистрация лиц и последующее распознавание лиц.

Примеры сделаны по PDF **Register for face recognition** и рабочему примеру производителя. В PDF объясняется, что распознавание лиц состоит из двух частей: сначала нужно выполнить **Registration**, то есть зарегистрировать лицо по фотографиям, а затем выполнить **Recognition**, то есть распознавать лица с камеры.

## Важно: общий файл лежит в `libs`

В этих примерах общий код вынесен в библиотеку:

```text
libs/register_face_common.py
```

На K230 этот файл нужно положить сюда:

```text
/sdcard/libs/register_face_common.py
```

Примеры импортируют его так:

```python
from libs.register_face_common import create_recognition_app, safe_deinit
```

Если положить `register_face_common.py` только рядом с примерами в `FaceRecognition/RegisterFace`, импорт `from libs.register_face_common ...` его не найдет.

## Файлы

| Файл | Назначение |
| --- | --- |
| `../../libs/register_face_common.py` | Общая библиотека: Face Detection, Face Registration, Face Recognition, database helpers, UART helpers. |
| `01_register_faces_from_folder.py` | Регистрация лиц из папки с изображениями. Создает `.bin` файлы признаков. |
| `02_face_recognition_basic.py` | Распознавание лиц с камеры без UART. |
| `03_face_recognition_uart.py` | Распознавание лиц с UART-выводом результата. |
| `04_registerface_file_io.py` | Регистрация лиц + чтение конфигурации и запись отчета в TXT/CSV. |
| `05_file_read_write_basic.py` | Простой пример чтения и записи TXT/CSV/BIN без AI. |
| `readme.md` | Инструкция на русском. |
| `readme_en.md` | English instructions. |

## Что демонстрирует RegisterFace

Face Recognition состоит из двух этапов:

```text
Registration → Recognition
```

### 1. Registration

На этапе регистрации программа:

1. Читает изображения из папки с фотографиями.
2. Находит лицо на каждом изображении.
3. Проверяет, что на фотографии только одно лицо.
4. Использует 5 ключевых точек лица для выравнивания через affine transform.
5. Запускает `face_recognition.kmodel`.
6. Получает 128-мерный feature vector.
7. Сохраняет feature vector в `.bin` файл.

Имя `.bin` файла берется из имени фотографии:

```text
/data/photo/register/peter.jpg
→ /data/face_database/register/peter.bin
```

### 2. Recognition

На этапе распознавания программа:

1. Загружает `.bin` файлы из базы.
2. Получает кадр с камеры.
3. Находит лица.
4. Для каждого лица извлекает feature vector.
5. Сравнивает feature vector с базой.
6. Рисует результат на экране:
   - `unknown` — неизвестное лицо;
   - `name: ..., score: ...` — распознанное лицо.

## Что нужно на TF-карте

Убедитесь, что на K230 есть модели и anchors:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/kmodel/face_recognition.kmodel
/sdcard/utils/prior_data_320.bin
```

Также нужен общий файл:

```text
/sdcard/libs/register_face_common.py
```

## Подготовка фотографий

PDF рекомендует сначала сделать фотографии людей с помощью K230, а не брать случайные картинки напрямую. Причина: изображение с камеры K230 может отличаться от исходной картинки из-за освещения, матрицы камеры, баланса белого и других факторов. Поэтому фотографии, сделанные самим K230, лучше подходят для дальнейшего распознавания именно на этом модуле.

Положите фотографии в папку:

```text
/data/photo/register/
```

Переименуйте файлы в имена людей:

```text
peter.jpg
alex.jpg
maria.jpg
```

На каждой фотографии должно быть **только одно лицо**. Если на фотографии несколько лиц, регистрация этого файла будет пропущена.

## Быстрый старт: регистрация

1. Скопируйте `libs/register_face_common.py` на K230:

```text
/sdcard/libs/register_face_common.py
```

2. Положите фотографии в папку:

```text
/data/photo/register/
```

3. Запустите:

```text
FaceRecognition/RegisterFace/01_register_faces_from_folder.py
```

4. После успешного выполнения появятся `.bin` файлы базы, например:

```text
/data/face_database/register/peter.bin
/data/face_database/register/alex.bin
```

Если в `01_register_faces_from_folder.py` переменная `PHOTO_DIR` указывает на другую папку, то база создается в:

```text
/data/face_database/<имя_папки_с_фото>/
```

## Быстрый старт: распознавание

1. Проверьте путь к базе в `02_face_recognition_basic.py`:

```python
"DATABASE_DIR": "/data/face_database/register/"
```

2. Запустите:

```text
FaceRecognition/RegisterFace/02_face_recognition_basic.py
```

3. Наведите камеру на лицо.
4. Если лицо есть в базе, оно будет подписано именем и score.
5. Если лица нет в базе, будет показано `unknown`.

## UART-вывод

`03_face_recognition_uart.py` отправляет результат распознавания через UART.

Для неизвестного лица:

```text
$x,y,w,h,unknown#
```

Для распознанного лица:

```text
$x,y,w,h,name,score#
```

Где:

| Поле | Значение |
| --- | --- |
| `x, y, w, h` | координаты рамки лица на экране 640x480 |
| `unknown` | лицо не найдено в базе |
| `name` | имя из `.bin` файла базы |
| `score` | score совпадения; чем выше score, тем выше вероятность правильного распознавания |

Если библиотеки Yahboom `YbProtocol` и `YbUart` доступны, пример использует:

```python
pto.get_face_recoginiton_data(x, y, w, h, name, score)
uart.send(pto_data)
```

Если UART-библиотеки недоступны, пакет печатается в консоль.

## Как работает AI-пайплайн

Общий поток регистрации:

```text
Image file → Face Detection → Landmarks → Affine Align → Feature Extract → .bin database
```

Общий поток распознавания:

```text
Sensor → Frame → Face Detection → Feature Extract → Database Search → OSD → Display
```

В live-режиме основной цикл выглядит так:

```python
pl = PipeLine(rgb888p_size=[640, 480], display_size=[640, 480], display_mode="lcd")
pl.create()

img = pl.get_frame()
det_boxes, recg_res = fr.run(img)
fr.draw_result(pl, det_boxes, recg_res)
pl.show_image()
```

`PipeLine` управляет камерой и дисплеем, поэтому в одной программе должен быть только один объект `PipeLine`.

## Почему используется pad перед resize

Для модели обнаружения лица preprocessing должен сохранить пропорции кадра:

```python
self.ai2d.pad(self.get_pad_param(), 0, [104, 117, 123])
self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
```

Если сделать только `resize`, лицо и ключевые точки могут сместиться, а регистрация/распознавание будут хуже.

## Почему используется affine transform

Для распознавания лицо нужно привести к стандартному виду 112x112. Для этого используются 5 ключевых точек лица и Umeyama alignment:

```python
affine_matrix = self.get_affine_matrix(landm)
self.ai2d.affine(nn.interp_method.cv2_bilinear, 0, 0, 127, 1, affine_matrix)
```

После выравнивания `face_recognition.kmodel` извлекает feature vector.

## Как устроена база лиц

База лиц — это папка с `.bin` файлами:

```text
/data/face_database/register/
```

Пример:

```text
peter.bin
alex.bin
maria.bin
```

Каждый `.bin` файл содержит бинарный feature vector лица. Имя файла без расширения используется как имя человека.

## Как работает поиск в базе

Для каждого найденного лица программа:

1. Извлекает feature vector.
2. Нормализует его.
3. Сравнивает с каждым feature vector из базы через dot product.
4. Переводит score в диапазон через:

```python
v_score = np.dot(feature, db_feature) / 2 + 0.5
```

5. Если score ниже `FACE_RECOGNITION_THRESHOLD`, результат будет `unknown`.

Порог можно менять в конфиге или в примере:

```text
FACE_RECOGNITION_THRESHOLD=0.65
```

## Чтение файлов на K230

Файл читается через `open()` в режиме `"r"`:

```python
with open("/sdcard/FaceRecognition/RegisterFace/register_face_config.txt", "r") as f:
    text = f.read()
```

`04_registerface_file_io.py` создает конфиг:

```text
FACE_DET_KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
FACE_RECOGNITION_KMODEL_PATH=/sdcard/kmodel/face_recognition.kmodel
ANCHORS_PATH=/sdcard/utils/prior_data_320.bin
PHOTO_DIR=/data/photo/register/
DATABASE_ROOT=/data/face_database/
DATABASE_DIR=
CONFIDENCE_THRESHOLD=0.50
NMS_THRESHOLD=0.20
FACE_RECOGNITION_THRESHOLD=0.65
```

Разбор строки:

```python
key, value = line.split("=", 1)
cfg[key.strip().upper()] = value.strip()
```

## Запись файлов на K230

Для записи текста используется режим `"w"`. Он создает файл или полностью перезаписывает старое содержимое:

```python
with open("/sdcard/FaceRecognition/RegisterFace/register_face_last_result.txt", "w") as f:
    f.write("success_count=3\n")
```

Для добавления строк в конец файла используется режим `"a"`:

```python
with open("/sdcard/FaceRecognition/RegisterFace/register_face_log.csv", "a") as f:
    f.write("time_ms,photo_dir,success_count,failed_count\n")
```

Для записи feature vector используется бинарный режим `"wb"`:

```python
with open("/data/face_database/register/peter.bin", "wb") as f:
    f.write(reg_result.tobytes())
```

Для чтения `.bin` файла используется режим `"rb"`:

```python
with open("/data/face_database/register/peter.bin", "rb") as f:
    data = f.read()
```

### Режимы open()

| Режим | Что делает |
| --- | --- |
| `"r"` | Чтение текстового файла. Если файла нет — ошибка. |
| `"w"` | Запись текстового файла заново. Старое содержимое удаляется. |
| `"a"` | Добавление текста в конец файла. Старое содержимое сохраняется. |
| `"rb"` | Чтение бинарного файла. Используется для `.bin` признаков. |
| `"wb"` | Запись бинарного файла. Используется для сохранения `.bin` признаков. |

## Какие файлы создает пример 04

При запуске `04_registerface_file_io.py` создается папка:

```text
/sdcard/FaceRecognition/RegisterFace
```

В ней появляются:

```text
register_face_config.txt       # настройки регистрации
register_face_last_result.txt  # последний отчет
register_face_log.csv          # история запусков
```

Пример `register_face_last_result.txt`:

```text
time_ms=123456
photo_dir=/data/photo/register/
success_count=3
failed_count=0
```

## Ошибка ENOENT

Если появляется ошибка `OSError: [Errno 2] ENOENT`, значит путь к папке или файлу указан неправильно либо папка не создана. В PDF отдельно показано, что при обращении к несуществующей папке через `os` программа может завершиться ошибкой. Для этого в общем модуле используется `ensure_dir()`, который рекурсивно создает папки.

## Советы

1. Фотографируйте лица с K230, а не только берите изображения из интернета.
2. На каждой фотографии для регистрации должно быть одно лицо.
3. Имя фотографии станет именем человека в базе.
4. Используйте хорошее освещение.
5. Если много `unknown`, снизьте `FACE_RECOGNITION_THRESHOLD`, например до `0.60`.
6. Если появляются ложные совпадения, увеличьте `FACE_RECOGNITION_THRESHOLD`, например до `0.70`.
7. Убедитесь, что на плате лежит свежий файл `/sdcard/libs/register_face_common.py`.

---

**Автор:** AIDevelopersMonster  
**Плата:** Yahboom K230 Vision Module  
**Репозиторий:** https://github.com/AIDevelopersMonster/K230

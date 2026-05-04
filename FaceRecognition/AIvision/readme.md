# K230: FaceRecognition / AIvision

Эта папка содержит демонстрационные примеры для **Yahboom K230 Vision Module** по распознаванию лица через AI-пайплайн K230.

Примеры сделаны по структуре из PDF **AI vision processing code structure**: камера получает кадр, `PipeLine` передает RGBP888-изображение в AI, AI выполняет preprocessing → inference → postprocess, а результат рисуется на OSD-слое и выводится на экран.

## Файлы

| Файл | Назначение |
| --- | --- |
| `face_aivision_common.py` | Общий модуль: `FaceDetectionApp`, загрузка anchors, чтение/запись файлов, CSV-лог, отрисовка результата. |
| `01_face_detection_basic.py` | Базовый пример: запуск камеры, модели, inference и рамки вокруг лиц. |
| `02_face_detection_file_io.py` | Пример чтения настроек из файла и записи результата распознавания в файлы. |
| `03_face_detection_external_call.py` | Пример структуры, когда AI-рутина вызывается из другого кода через `exce_demo(pl)` и `exit_demo()`. |
| `readme.md` | Инструкция на русском. |
| `readme_en.md` | English instructions. |

## Что нужно на TF-карте

Убедитесь, что на K230 есть файлы модели и anchors:

```text
/sdcard/kmodel/face_detection_320.kmodel
/sdcard/utils/prior_data_320.bin
```

Если пути отличаются, запустите `02_face_detection_file_io.py` один раз. Он создаст файл конфигурации:

```text
/sdcard/FaceRecognition/AIvision/face_config.txt
```

Потом отредактируйте в нем `KMODEL_PATH` и `ANCHORS_PATH`.

## Быстрый старт

1. Скопируйте папку `FaceRecognition/AIvision` на K230 или откройте нужный `.py` файл в CanMV IDE.
2. Подключите Yahboom K230 Vision Module по USB.
3. Запустите `01_face_detection_basic.py`.
4. Наведите камеру на лицо.
5. На экране должна появиться желтая рамка вокруг лица.

## Как устроен AI-пайплайн

Главная идея:

```text
Sensor → Frame → AI → OSD → Display
```

В коде это выглядит так:

```python
pl = PipeLine(rgb888p_size=[640, 360], display_size=[640, 480], display_mode="lcd")
pl.create()

face_det = create_face_detection_app(pl)
img = pl.get_frame()
dets = face_det.run(img)
face_det.draw_result(pl, dets)
pl.show_image()
```

### Почему нужен только один PipeLine

`PipeLine` управляет камерой и дисплеем. Поэтому в одной программе нужно создавать только один экземпляр `PipeLine`, а AI-рутины должны получать его как параметр:

```python
def exce_demo(pl):
    face_det = create_face_detection_app(pl)
    ...
```

## Основные части FaceDetectionApp

`face_aivision_common.py` содержит класс:

```python
class FaceDetectionApp(AIBase):
```

Он повторяет типовую структуру AI-демо:

1. `__init__()` — путь к `.kmodel`, входной размер модели, anchors, thresholds.
2. `config_preprocess()` — настройка AI2D resize из кадра камеры в размер модели `320x320`.
3. `run()` — наследуется от `AIBase` и выполняет preprocessing → inference → postprocess.
4. `postprocess()` — вызывает `aidemo.face_det_post_process()`.
5. `draw_result()` — рисует рамки лиц на OSD-слое `pl.osd_img`.
6. `deinit()` — освобождает ресурсы модели.

## Чтение файлов на K230

Файл читается обычной функцией `open()` в режиме `"r"`:

```python
with open("/sdcard/FaceRecognition/AIvision/face_config.txt", "r") as f:
    text = f.read()
```

В примере `02_face_detection_file_io.py` читается конфигурация вида:

```text
KMODEL_PATH=/sdcard/kmodel/face_detection_320.kmodel
ANCHORS_PATH=/sdcard/utils/prior_data_320.bin
CONFIDENCE_THRESHOLD=0.50
NMS_THRESHOLD=0.20
DEBUG_MODE=0
SAVE_LOG=1
WRITE_INTERVAL_MS=1000
```

Разбор строки `KEY=VALUE`:

```python
key, value = line.split("=", 1)
cfg[key.strip().upper()] = value.strip()
```

## Запись файлов на K230

Для записи используется режим `"w"`. Он создает файл, если его нет, и перезаписывает старое содержимое:

```python
with open("/sdcard/FaceRecognition/AIvision/face_last_result.txt", "w") as f:
    f.write("face_count=1\n")
```

Для добавления строк в конец файла используется режим `"a"`:

```python
with open("/sdcard/FaceRecognition/AIvision/face_log.csv", "a") as f:
    f.write("time_ms,fps,face_count\n")
```

### Режимы open()

| Режим | Что делает |
| --- | --- |
| `"r"` | Читает существующий файл. Если файла нет — ошибка. |
| `"w"` | Записывает файл заново. Старое содержимое удаляется. |
| `"a"` | Дописывает данные в конец файла. Старое содержимое сохраняется. |

## Какие файлы создает пример 02

При запуске `02_face_detection_file_io.py` создается папка:

```text
/sdcard/FaceRecognition/AIvision
```

В ней появляются файлы:

```text
face_config.txt       # настройки модели и записи
face_last_result.txt  # последний результат
face_log.csv          # история результатов
```

Пример `face_last_result.txt`:

```text
time_ms=123456
fps=22.500
face_count=1
best_score=0.9210
x=180
y=90
w=120
h=120
```

Пример CSV-лога:

```text
time_ms,fps,face_count,best_score,x,y,w,h
123456,22.500,1,0.9210,180,90,120,120
```

## Почему запись ограничена по времени

Распознавание идет в бесконечном цикле. Если записывать файл каждый кадр, TF-карта будет получать слишком много операций записи. Поэтому в `face_config.txt` есть параметр:

```text
WRITE_INTERVAL_MS=1000
```

Это означает: писать результат не чаще одного раза в секунду.

## Советы по распознаванию лица

1. Используйте хорошее освещение.
2. Держите лицо достаточно крупно в кадре.
3. Не закрывайте лицо руками или предметами.
4. Если FPS низкий, уменьшите разрешение `rgb888p_size`.
5. Если рамки появляются на ложных объектах, увеличьте `CONFIDENCE_THRESHOLD`.
6. Если лицо не находится, уменьшите `CONFIDENCE_THRESHOLD`, например до `0.40`.

## Запуск из другого файла

`03_face_detection_external_call.py` показывает структуру, когда внешний код создает один `PipeLine`, а AI-рутина только использует его:

```python
pl = PipeLine(rgb888p_size=[640, 360], display_size=[640, 480], display_mode="lcd")
pl.create()
exce_demo(pl)
```

Для завершения вызывается:

```python
exit_demo()
```

Так удобнее объединять несколько AI-режимов в одном меню или GUI.

---

**Автор:** AIDevelopersMonster  
**Плата:** Yahboom K230 Vision Module  
**Репозиторий:** https://github.com/AIDevelopersMonster/K230

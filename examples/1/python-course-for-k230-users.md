# Python для пользователей K230: понятное введение перед MicroPython

Этот материал — не просто перевод справки, а переработанный вводный курс для тех, кто начинает работать с **K230 / CanMV / MicroPython**. Здесь меньше «академических» примеров и больше понятных объяснений, аккуратных комментариев и кода, который помогает быстро разобраться в синтаксисе.

Основа курса собрана и переработана по материалам из руководства **Micropython Quick Start**. fileciteturn0file0

## Как читать этот курс

- Сначала изучите базовый синтаксис Python.
- Затем переходите к примерам, похожим на реальные задачи для K230.
- Помните: **MicroPython очень похож на Python 3, но поддерживает не всё** из обычного Python.
- Для embedded-разработки особенно важны: переменные, условия, циклы, функции, списки, словари, работа с модулями и понимание классов.

---

# 1. Что такое MicroPython и зачем знать Python

**MicroPython** — это облегчённая реализация Python 3 для микроконтроллеров и встроенных систем. Синтаксис почти такой же, как у обычного Python, но стандартная библиотека меньше, а доступные модули зависят от конкретной платы и прошивки. Для K230 это удобно: можно быстро писать и запускать код, проверять идеи и работать с периферией без тяжёлой подготовки. fileciteturn0file0

Проще говоря:

- **Python 3** — общий язык.
- **MicroPython** — его облегчённая версия для железа.
- **CanMV / K230** — среда, где этот язык используется на практике.

---

# 2. Базовый синтаксис Python

## 2.1. Комментарии

Комментарий — это текст для человека, а не для интерпретатора.

```python
# Это однострочный комментарий

"""
Это многострочная строка.
Иногда её используют как описание модуля,
функции или класса.
"""
```

### Когда что использовать

- `#` — для обычных коротких пояснений.
- `""" ... """` — для документации и длинных описаний.

---

## 2.2. Числа и арифметика

```python
print(3)          # 3
print(1 + 1)      # 2
print(8 - 1)      # 7
print(10 * 2)     # 20
print(35 / 5)     # 7.0
```

### Важно понимать

Оператор `/` всегда даёт **число с плавающей точкой**:

```python
print(5 / 2)      # 2.5
```

Целочисленное деление — это `//`:

```python
print(5 // 2)     # 2
print(5 // 3)     # 1
print(-5 // 3)    # -2
```

Почему `-2`, а не `-1`? Потому что `//` округляет **вниз**, к меньшему числу.

Остаток от деления:

```python
print(7 % 3)      # 1
print(-7 % 3)     # 2
```

Степень:

```python
print(2 ** 3)     # 8
```

Приоритет операций можно менять скобками:

```python
print(1 + 3 * 2)    # 7
print((1 + 3) * 2)  # 8
```

### Пример для K230

Допустим, камера выдаёт изображение шириной 640 пикселей, а вы хотите взять центр:

```python
width = 640
center_x = width // 2
print(center_x)     # 320
```

Здесь `//` полезен, потому что координата обычно нужна как целое число.

---

## 2.3. Логические значения

```python
print(True)
print(False)
```

Отрицание:

```python
print(not True)     # False
print(not False)    # True
```

Логические операции:

```python
print(True and False)   # False
print(False or True)    # True
```

### В Python многие значения считаются истинными или ложными

Ложными считаются:

- `False`
- `None`
- `0`
- `""`
- `[]`
- `{}`
- `()`
- `set()`

Примеры:

```python
print(bool(0))      # False
print(bool(""))     # False
print(bool([]))     # False
print(bool(10))     # True
print(bool(-3))     # True
```

Это удобно в проверках:

```python
frames = []
if not frames:
    print("Список кадров пуст")
```

---

## 2.4. Сравнения

```python
print(1 == 1)   # True
print(2 != 1)   # True
print(1 < 10)   # True
print(2 >= 2)   # True
```

Можно делать цепочки сравнений:

```python
x = 5
print(1 < x < 10)   # True
```

### `==` и `is` — это не одно и то же

- `==` сравнивает **значения**.
- `is` проверяет, являются ли это **одним и тем же объектом**.

```python
a = [1, 2, 3]
b = a
c = [1, 2, 3]

print(a == b)   # True
print(a is b)   # True
print(a == c)   # True
print(a is c)   # False
```

### Как сравнивать с `None`

```python
value = None
print(value is None)      # True
```

С `None` лучше использовать именно `is`, а не `==`.

---

# 3. Строки

Строка — это текст.

```python
text1 = "Привет"
text2 = 'Мир'
print(text1, text2)
```

Склеивание строк:

```python
print("Hello " + "K230")
```

Доступ к символам:

```python
word = "Python"
print(word[0])    # P
print(word[-1])   # n
```

Длина строки:

```python
print(len("K230"))   # 4
```

## 3.1. Современное форматирование строк

Лучше всего использовать **f-строки**:

```python
name = "K230"
fps = 25
print(f"Плата {name} работает, FPS = {fps}")
```

Это проще и понятнее, чем старый `.format()`.

Ещё пример:

```python
temperature = 36.5
print(f"Температура сенсора: {temperature} °C")
```

---

# 4. Переменные

В Python переменную не нужно объявлять заранее.

```python
led_state = 1
board_name = "K230"
voltage = 3.3
```

Принятый стиль имён — **snake_case**:

```python
frame_count = 0
sensor_width = 640
model_name = "face_detection"
```

Плохой стиль:

```python
FrameCount = 0
sensorWidth = 640
```

Для Python-кода на embedded-устройствах хорошие имена особенно важны: код потом легче поддерживать и отлаживать.

---

# 5. Списки

Список хранит последовательность элементов.

```python
frames = []
values = [10, 20, 30]
```

Добавление элемента:

```python
values.append(40)
print(values)   # [10, 20, 30, 40]
```

Удаление последнего элемента:

```python
last_value = values.pop()
print(last_value)   # 40
print(values)       # [10, 20, 30]
```

Доступ по индексу:

```python
print(values[0])    # 10
print(values[-1])   # 30
```

## 5.1. Срезы

```python
nums = [0, 1, 2, 3, 4, 5]
print(nums[1:4])   # [1, 2, 3]
print(nums[:3])    # [0, 1, 2]
print(nums[3:])    # [3, 4, 5]
print(nums[::2])   # [0, 2, 4]
print(nums[::-1])  # [5, 4, 3, 2, 1, 0]
```

## 5.2. Полезные операции со списками

```python
items = [1, 2, 3]
items.insert(1, 99)
print(items)   # [1, 99, 2, 3]

items.remove(99)
print(items)   # [1, 2, 3]

print(2 in items)   # True
print(len(items))   # 3
```

## 5.3. Практический пример

Сохраним последние результаты распознавания:

```python
labels = []
labels.append("person")
labels.append("face")
labels.append("cat")

print(labels)
print(labels[-1])   # cat
```

---

# 6. Кортежи

Кортеж похож на список, но его нельзя изменять после создания.

```python
resolution = (640, 480)
print(resolution[0])   # 640
print(resolution[1])   # 480
```

Попытка изменить элемент вызовет ошибку.

Кортежи удобны, когда данные логически образуют неизменяемую группу: например, ширина и высота, координаты, цвет RGB.

```python
point = (120, 200)
```

Распаковка:

```python
width, height = (640, 480)
print(width)
print(height)
```

Обмен значений:

```python
a = 10
b = 20
a, b = b, a
print(a, b)   # 20 10
```

---

# 7. Словари

Словарь хранит пары **ключ → значение**.

```python
camera = {
    "width": 640,
    "height": 480,
    "fps": 30
}
```

Получение значения:

```python
print(camera["width"])   # 640
```

Безопасное получение через `get`:

```python
print(camera.get("fps"))        # 30
print(camera.get("format"))     # None
print(camera.get("format", "RGB565"))
```

Проверка наличия ключа:

```python
print("width" in camera)   # True
```

Добавление и изменение:

```python
camera["format"] = "RGB565"
camera["fps"] = 60
```

Удаление:

```python
del camera["format"]
```

## Практический пример

```python
result = {
    "label": "person",
    "score": 0.93,
    "x": 120,
    "y": 80
}

print(f"Найден объект: {result['label']}")
print(f"Достоверность: {result['score']}")
```

Словари очень часто используются для хранения параметров, конфигурации и результатов обработки.

---

# 8. Множества

Множество хранит **уникальные** элементы.

```python
classes = {"person", "cat", "person", "dog"}
print(classes)   # {'person', 'cat', 'dog'}
```

Добавление:

```python
classes.add("car")
```

Проверка наличия:

```python
print("cat" in classes)   # True
```

Операции над множествами:

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}

print(a & b)   # пересечение: {3, 4}
print(a | b)   # объединение: {1, 2, 3, 4, 5}
print(a - b)   # разность: {1, 2}
```

### Где это полезно

Например, если вы хотите быстро понять, какие классы объектов были обнаружены хотя бы раз:

```python
seen_labels = set()
seen_labels.add("person")
seen_labels.add("person")
seen_labels.add("face")
print(seen_labels)   # {'person', 'face'}
```

---

# 9. Условия

```python
temperature = 72

if temperature > 80:
    print("Перегрев")
elif temperature > 60:
    print("Температура повышенная")
else:
    print("Температура в норме")
```

## Важнейшее правило Python

**Отступы — часть синтаксиса.**

Правильно:

```python
if True:
    print("OK")
```

Неправильно:

```python
if True:
print("OK")
```

Обычно используют **4 пробела** на каждый уровень вложенности.

---

# 10. Циклы

## 10.1. Цикл `for`

```python
for name in ["camera", "display", "uart"]:
    print(name)
```

С `range()`:

```python
for i in range(5):
    print(i)
```

Это выведет числа от `0` до `4`.

Другие варианты:

```python
for i in range(2, 6):
    print(i)   # 2, 3, 4, 5

for i in range(0, 10, 2):
    print(i)   # 0, 2, 4, 6, 8
```

## 10.2. `enumerate()` — индекс и значение сразу

```python
ports = ["UART0", "UART1", "UART2"]
for index, name in enumerate(ports):
    print(index, name)
```

## 10.3. Цикл `while`

```python
count = 0
while count < 3:
    print(count)
    count += 1
```

### Практический пример для K230

```python
frame_id = 0
while frame_id < 5:
    print(f"Обрабатываем кадр {frame_id}")
    frame_id += 1
```

---

# 11. Исключения

Ошибки в Python можно перехватывать.

```python
try:
    value = int("123")
    print(value)
except ValueError:
    print("Не удалось преобразовать строку в число")
```

Ещё пример:

```python
data = [10, 20, 30]

try:
    print(data[5])
except IndexError:
    print("Индекс вне диапазона")
```

## Почему это важно на embedded-устройствах

Если вы читаете данные с датчика, открываете файл или работаете с устройством, ошибка может возникнуть в любой момент. Лучше обработать её аккуратно, чем получить падение программы.

---

# 12. Файлы

В обычном Python можно читать и записывать файлы так:

```python
with open("config.txt", "w", encoding="utf-8") as file:
    file.write("mode=demo\n")
```

Чтение:

```python
with open("config.txt", "r", encoding="utf-8") as file:
    text = file.read()
    print(text)
```

## Почему `with` удобен

После выхода из блока файл автоматически закрывается.

### Замечание для MicroPython

На платах и в embedded-среде файловая система может быть ограниченной, а параметры `open()` иногда отличаются от настольного Python. Но сама идея работы с файлами остаётся той же.

---

# 13. Итерируемые объекты и итераторы

Это тема не самая простая, но полезно знать основу.

**Итерируемый объект** — это то, по чему можно пройти циклом `for`.

Например:

- список
- строка
- словарь
- диапазон `range()`

```python
for ch in "K230":
    print(ch)
```

Можно создать итератор вручную:

```python
values = [10, 20, 30]
it = iter(values)

print(next(it))   # 10
print(next(it))   # 20
print(next(it))   # 30
```

Когда элементы закончатся, возникнет `StopIteration`.

На практике обычно достаточно понимать так:

- `for` работает с итерируемыми объектами;
- `range()` не создаёт сразу огромный список чисел;
- это экономит память.

А для embedded-устройств экономия памяти особенно важна.

---

# 14. Функции

Функция помогает не повторять один и тот же код.

```python
def add(x, y):
    return x + y

print(add(5, 6))   # 11
```

## 14.1. Параметры и возврат значения

```python
def show_status(name, state):
    print(f"{name}: {state}")

show_status("camera", "ready")
```

Именованные аргументы:

```python
show_status(state="ready", name="display")
```

## 14.2. Значения по умолчанию

```python
def connect_uart(port="UART0", baudrate=115200):
    print(f"Подключение к {port}, скорость {baudrate}")

connect_uart()
connect_uart("UART1", 9600)
```

## 14.3. Произвольное число аргументов

```python
def log_values(*args):
    print(args)

log_values(10, 20, 30)
```

И именованных аргументов:

```python
def print_options(**kwargs):
    print(kwargs)

print_options(width=640, height=480, fps=30)
```

## 14.4. Области видимости

```python
x = 10

def show_local():
    x = 99
    print("Локальная x:", x)

show_local()
print("Глобальная x:", x)
```

### Осторожно с `global`

Использовать `global` можно, но без необходимости лучше не делать — код становится менее предсказуемым.

---

# 15. Функции как объекты

В Python функцию можно передать в другую функцию или вернуть из неё.

```python
def create_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

mul2 = create_multiplier(2)
print(mul2(5))   # 10
```

Эта тема уже не базовая, но полезно знать, что Python умеет и так.

---

# 16. Лямбда, `map`, `filter`, генераторы списков

## 16.1. Лямбда

```python
square = lambda x: x * x
print(square(4))   # 16
```

Но для читаемого кода часто лучше обычная `def`.

## 16.2. Генераторы списков

Очень полезная конструкция:

```python
numbers = [1, 2, 3, 4, 5]
squares = [x * x for x in numbers]
print(squares)
```

С условием:

```python
even_numbers = [x for x in numbers if x % 2 == 0]
print(even_numbers)   # [2, 4]
```

## Почему это полезно

Такой синтаксис часто удобнее, чем длинный цикл.

Например, можно получить список обнаруженных объектов с высокой уверенностью:

```python
scores = [0.91, 0.42, 0.87, 0.65]
good_scores = [s for s in scores if s > 0.8]
print(good_scores)
```

---

# 17. Модули

Модуль — это файл с Python-кодом, который можно импортировать.

```python
import math
print(math.sqrt(16))
```

Импорт отдельных объектов:

```python
from math import ceil, floor
print(ceil(3.2))
print(floor(3.8))
```

Псевдоним:

```python
import math as m
print(m.sqrt(25))
```

## Важно для MicroPython

В обычном Python многие привыкли к `pip install ...`, но в **MicroPython так делать нельзя**. Доступность модуля зависит от прошивки, сборки и того, что уже есть на устройстве. Это прямо отмечено и в исходном материале. fileciteturn0file0

То есть:

- не любой модуль из интернета можно поставить на K230;
- часто нужно использовать встроенные модули CanMV / MicroPython;
- иногда код из обычного Python приходится адаптировать.

---

# 18. Классы

Класс — это способ описать собственный тип данных.

```python
class Device:
    def __init__(self, name):
        self.name = name
        self.enabled = False

    def enable(self):
        self.enabled = True
        print(f"{self.name} включён")

    def disable(self):
        self.enabled = False
        print(f"{self.name} выключен")
```

Создание объекта:

```python
camera = Device("Camera")
camera.enable()
```

## Что здесь важно

- `class Device:` — объявление класса.
- `__init__` — конструктор, вызывается при создании объекта.
- `self` — ссылка на текущий объект.
- `self.name`, `self.enabled` — атрибуты объекта.

## 18.1. Атрибуты класса и объекта

```python
class Sensor:
    sensor_type = "generic"

    def __init__(self, name):
        self.name = name
```

- `sensor_type` — атрибут класса, общий для всех объектов.
- `name` — атрибут конкретного экземпляра.

---

# 19. Наследование

Наследование позволяет создать новый класс на основе существующего.

```python
class Device:
    def __init__(self, name):
        self.name = name

    def info(self):
        print(f"Устройство: {self.name}")


class Camera(Device):
    def capture(self):
        print(f"{self.name}: захват кадра")
```

Использование:

```python
cam = Camera("OV2640")
cam.info()
cam.capture()
```

## Зачем это нужно

Если у вас есть несколько похожих устройств — камера, дисплей, UART, датчик — можно вынести общую логику в базовый класс.

---

# 20. Что стоит помнить именно пользователю K230

## 20.1. Не весь Python 3 доступен в MicroPython

Синтаксис в основном такой же, но:

- библиотек меньше;
- некоторые модули отсутствуют;
- часть возможностей может работать иначе;
- объём памяти ограничен.

## 20.2. Пишите проще

Для embedded-кода обычно лучше:

- короткие функции;
- понятные имена;
- меньше лишних абстракций;
- минимум тяжёлых структур данных;
- аккуратное использование памяти.

## 20.3. Проверяйте код маленькими шагами

На K230 удобно идти так:

1. импорт модуля;
2. инициализация устройства;
3. короткий тест;
4. цикл обработки;
5. добавление логики.

---

# 21. Небольшой тренировочный блок

## Пример 1. Проверка порога уверенности

```python
score = 0.82

if score > 0.8:
    print("Объект найден уверенно")
else:
    print("Уверенность низкая")
```

## Пример 2. Обработка нескольких кадров

```python
for frame_id in range(3):
    print(f"Кадр {frame_id} обработан")
```

## Пример 3. Функция для вывода параметров

```python
def print_resolution(width, height):
    print(f"Разрешение: {width}x{height}")

print_resolution(640, 480)
```

## Пример 4. Словарь с параметрами камеры

```python
camera_config = {
    "width": 640,
    "height": 480,
    "pixformat": "RGB565"
}

print(camera_config["pixformat"])
```

## Пример 5. Класс простого устройства

```python
class LED:
    def __init__(self, pin):
        self.pin = pin
        self.state = 0

    def on(self):
        self.state = 1
        print(f"LED на пине {self.pin} включён")

    def off(self):
        self.state = 0
        print(f"LED на пине {self.pin} выключен")

led = LED(12)
led.on()
led.off()
```

---

# 22. Что можно пропустить на старте

Если ваша цель — быстрее начать писать код для K230, на первом этапе можно не углубляться в:

- итераторы и `next()`;
- замыкания;
- декораторы;
- сложное наследование;
- функциональный стиль через `map` и `filter`.

Сначала уверенно освоите:

- переменные;
- строки;
- списки и словари;
- `if`, `for`, `while`;
- функции;
- импорт модулей;
- базовые классы.

---

# 23. Итог

Чтобы комфортно работать с K230 и MicroPython, достаточно хорошо понимать основы Python:

- типы данных;
- условия и циклы;
- функции;
- коллекции;
- модули;
- основы классов.

Как только это станет привычным, дальше будет гораздо проще разбираться уже с конкретными API CanMV: камерой, дисплеем, GPIO, UART, AI-моделями и примерами распознавания.

---

# 24. Что дальше изучать после этого курса

Следующий логичный шаг для пользователя K230:

1. импорт модулей CanMV / MicroPython;
2. запуск простого скрипта в IDE;
3. работа с камерой;
4. вывод изображения;
5. запуск готового AI-примера;
6. разбор API платы.

Если продолжать этот материал, следующим разделом стоит сделать уже отдельный практический курс: **«MicroPython на K230: от запуска скрипта до работы с камерой и AI-примерами»**.


# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230                  
#
# Описание:
# Статический пример использования img.draw_line().
# Рисует логотип "Yahboom" с помощью линий на белом фоне.
#
# Используется:
# - image.Image / Display / MediaManager
#
# ============================================

import time
import os
import image
from media.display import *
from media.media import *

# Размеры дисплея (ширина и высота в пикселях)
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480


def draw_yahboom_lines(img, start_x, start_y, color, thickness):
    """
    Рисует слово 'Yahboom' используя только прямые линии.
    
    Параметры:
    - img: объект изображения, на котором рисуем
    - start_x, start_y: координаты начальной точки (левый верхний угол)
    - color: цвет линий в формате (R, G, B)
    - thickness: толщина линий в пикселях
    """
    # Буква Y
    # Левая наклонная линия
    img.draw_line(start_x, start_y, start_x + 20, start_y + 20, color=color, thickness=thickness)
    # Правая наклонная линия
    img.draw_line(start_x + 40, start_y, start_x + 20, start_y + 20, color=color, thickness=thickness)
    # Вертикальная линия внизу
    img.draw_line(start_x + 20, start_y + 20, start_x + 20, start_y + 45, color=color, thickness=thickness)

    # Буква a
    x = start_x + 55
    # Верхняя горизонтальная линия
    img.draw_line(x, start_y + 20, x + 25, start_y + 20, color=color, thickness=thickness)
    # Правая вертикальная линия
    img.draw_line(x + 25, start_y + 20, x + 25, start_y + 45, color=color, thickness=thickness)
    # Нижняя горизонтальная линия
    img.draw_line(x + 25, start_y + 45, x, start_y + 45, color=color, thickness=thickness)
    # Левая вертикальная линия (частично)
    img.draw_line(x, start_y + 45, x, start_y + 30, color=color, thickness=thickness)
    # Средняя горизонтальная линия (перекладина)
    img.draw_line(x, start_y + 30, x + 25, start_y + 30, color=color, thickness=thickness)

    # Буква h
    x = start_x + 95
    # Левая вертикальная линия
    img.draw_line(x, start_y, x, start_y + 45, color=color, thickness=thickness)
    # Средняя горизонтальная линия
    img.draw_line(x, start_y + 25, x + 25, start_y + 25, color=color, thickness=thickness)
    # Правая вертикальная линия
    img.draw_line(x + 25, start_y + 25, x + 25, start_y + 45, color=color, thickness=thickness)

    # Буква b
    x = start_x + 135
    # Левая вертикальная линия
    img.draw_line(x, start_y, x, start_y + 45, color=color, thickness=thickness)
    # Средняя горизонтальная линия
    img.draw_line(x, start_y + 20, x + 25, start_y + 20, color=color, thickness=thickness)
    # Правая вертикальная линия
    img.draw_line(x + 25, start_y + 20, x + 25, start_y + 45, color=color, thickness=thickness)
    # Нижняя горизонтальная линия
    img.draw_line(x + 25, start_y + 45, x, start_y + 45, color=color, thickness=thickness)

    # Буква o (две штуки)
    for x in (start_x + 175, start_x + 215):
        # Верхняя горизонтальная линия
        img.draw_line(x, start_y + 20, x + 25, start_y + 20, color=color, thickness=thickness)
        # Правая вертикальная линия
        img.draw_line(x + 25, start_y + 20, x + 25, start_y + 45, color=color, thickness=thickness)
        # Нижняя горизонтальная линия
        img.draw_line(x + 25, start_y + 45, x, start_y + 45, color=color, thickness=thickness)
        # Левая вертикальная линия
        img.draw_line(x, start_y + 45, x, start_y + 20, color=color, thickness=thickness)

    # Буква m
    x = start_x + 255
    # Левая вертикальная линия
    img.draw_line(x, start_y + 20, x, start_y + 45, color=color, thickness=thickness)
    # Первая наклонная линия (вверх)
    img.draw_line(x, start_y + 20, x + 12, start_y + 32, color=color, thickness=thickness)
    # Вторая наклонная линия (вниз)
    img.draw_line(x + 12, start_y + 32, x + 24, start_y + 20, color=color, thickness=thickness)
    # Правая вертикальная линия
    img.draw_line(x + 24, start_y + 20, x + 24, start_y + 45, color=color, thickness=thickness)


def main():
    """
    Основная функция программы.
    Создаёт изображение, рисует на нём логотип и выводит на дисплей.
    """
    # Создаём пустое изображение нужного размера с форматом цвета ARGB8888
    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    # Очищаем изображение (заливаем чёрным)
    img.clear()
    # Рисуем белый прямоугольник на весь экран (фон)
    img.draw_rectangle(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, color=(255, 255, 255), fill=True)

    # Инициализируем дисплей (ST7701 - контроллер экрана)
    # width и height - размеры экрана, to_ide=True позволяет видеть вывод в IDE
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    # Инициализируем медиа-менеджер для работы с мультимедиа
    MediaManager.init()

    try:
        # Задаём цвет линий (голубой в формате RGB)
        color = (0, 191, 255)
        # Задаём толщину линий в пикселях
        thickness = 4
        # Рисуем логотип "Yahboom" начиная с координат (170, 210)
        draw_yahboom_lines(img, 170, 210, color, thickness)
        # Добавляем подпись с описанием функции draw_line
        img.draw_string(10, 10, "draw_line(x0,y0,x1,y1,color,thickness)", color=(0, 0, 0))
        # Показываем изображение на дисплее
        Display.show_image(img)

        # Бесконечный цикл для удержания изображения на экране
        while True:
            # Проверяем точку выхода (для корректной остановки)
            os.exitpoint()
            # Ждём 100 миллисекунд
            time.sleep_ms(100)

    except KeyboardInterrupt as e:
        # Обрабатываем прерывание от пользователя (Ctrl+C)
        print("Пользователь остановил:", e)
    except Exception as e:
        # Обрабатываем любые другие ошибки
        print("Ошибка:", e)
    finally:
        # Освобождаем ресурсы независимо от того, была ли ошибка
        Display.deinit()  # Деинициализируем дисплей
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)  # Разрешаем системе перейти в спящий режим
        time.sleep_ms(100)  # Небольшая задержка
        MediaManager.deinit()  # Деинициализируем медиа-менеджер


if __name__ == "__main__":
    # Настраиваем точку выхода при запуске скрипта
    os.exitpoint(os.EXITPOINT_ENABLE)
    # Запускаем основную функцию
    main()

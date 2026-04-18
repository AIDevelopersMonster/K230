# ============================================
# K230 Example
# Демонстрация режимов работы с файлами
# ============================================

# Запись
with open('/sdcard/modes.txt', 'w') as f:
    f.write('line1\n')
    f.write('line2\n')

# Добавление
with open('/sdcard/modes.txt', 'a') as f:
    f.write('line3\n')

# Чтение построчно
with open('/sdcard/modes.txt', 'r') as f:
    for line in f.readlines():
        print('LINE:', line)

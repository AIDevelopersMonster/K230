# ============================================
# K230 Example
# Базовая запись и чтение файла
# ============================================

# Запись файла
with open('/sdcard/test.txt', 'w') as f:
    f.write('Hello K230')

print('File written')

# Чтение файла
with open('/sdcard/test.txt', 'r') as f:
    data = f.read()

print('Read data:', data)

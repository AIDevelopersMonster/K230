# ============================================
# K230 Example
# Работа с файловой системой
# ============================================

import os

# список файлов
print('Files:', os.listdir('/sdcard'))

# проверка файла
try:
    os.stat('/sdcard/test.txt')
    print('File exists')
except:
    print('File not found')

# переименование
try:
    os.rename('/sdcard/test.txt', '/sdcard/test_renamed.txt')
    print('Renamed file')
except:
    pass

# удаление
try:
    os.remove('/sdcard/test_renamed.txt')
    print('File removed')
except:
    pass

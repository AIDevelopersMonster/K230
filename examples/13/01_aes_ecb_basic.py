# ============================================
# K230 Example
# Автор: AIDevelopersMonster
# Плата: Yahboom K230
# GitHub: https://github.com/AIDevelopersMonster/K230         
#
# Описание:
# Базовый пример AES-128 в режиме ECB для K230.
# Показывает создание AES-объекта, шифрование 
# 16-байтного блока, расшифровку и проверку результата.
#
# Используется:
# - ucryptolib (библиотека криптографии)
# ============================================

# Импортируем библиотеку криптографии для работы с AES
import ucryptolib

# Импортируем модуль для работы с шестнадцатеричным представлением
# Сначала пробуем стандартный binascii, если не работает - используем ubinascii
try:
    import binascii
except ImportError:
    import ubinascii as binascii


def to_hex(data):
    """
    Преобразует байтовые данные в шестнадцатеричную строку.
    
    Args:
        data: байтовые данные для преобразования
    
    Returns:
        Строка с шестнадцатеричным представлением данных
    """
    # binascii.hexlify возвращает байты, поэтому декодируем в строку
    value = binascii.hexlify(data)
    if isinstance(value, bytes):
        return value.decode()
    return value


# Ключ шифрования - должен быть ровно 16 байт для AES-128
# Используем префикс 'b' чтобы создать байтовую строку
key = b'1234567890abcdef'          # 16 bytes -> AES-128

# Открытый текст (данные для шифрования) - тоже должен быть кратен 16 байтам
plaintext = b'This is 16 bytes'    # exactly 16 bytes

# Создаём объект шифра с ключом и режимом ECB
# MODE_ECB - самый простой режим, каждый блок шифруется независимо
cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)

# Шифруем данные - получаем зашифрованный блок
encrypted = cipher.encrypt(plaintext)

# Для расшифровки создаём новый объект шифра с тем же ключом
# Это важно - шифр нужно создавать заново для каждой операции
cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)

# Расшифровываем данные - должны получить исходный текст
decrypted = cipher.decrypt(encrypted)

# Выводим результаты для наглядности
print('key       =', key)
print('plaintext =', plaintext)
print('encrypted =', encrypted)
print('encrypted(hex) =', to_hex(encrypted))
print('decrypted =', decrypted)

# Проверяем что расшифрованные данные совпадают с исходными
# Если нет - будет ошибка с сообщением
assert decrypted == plaintext, 'AES-128 ECB failed'
print('PASS')

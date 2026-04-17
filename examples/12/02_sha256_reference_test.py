import hashlib

try:
    import binascii
except ImportError:
    import ubinascii as binascii


def to_hex(data):
    value = binascii.hexlify(data)
    if isinstance(value, bytes):
        return value.decode()
    return value


print("=== K230 SHA-256 reference test ===")

a = bytes([0] * 65)
b = hashlib.sha256()
b.update(a)
b.update(a)
c = b.digest()
print("test #1 digest =", c)
print("test #1 hex    =", to_hex(hashlib.sha256(a + a).digest()))

expected1 = b"\xe5Z\\'sj\x87a\xc8\xe9j\xce\xc0r\x10#%\xe0\x8c\xb2\xd0\xdb\xb4\xd4p,\xfe8\xf8\xab\x07\t"
if c != expected1:
    raise Exception("error #1! {}".format(c))

a = bytes([0] * 1024)
b = hashlib.sha256(a)
c = b.digest()
print("test #2 digest =", c)
print("test #2 hex    =", to_hex(c))

expected2 = b'_p\xbf\x18\xa0\x86\x00p\x16\xe9H\xb0J\xed;\x82\x10:6\xbe\xa4\x17U\xb6\xcd\xdf\xaf\x10\xac\xe3\xc6\xef'
if c != expected2:
    raise Exception("error #2! {}".format(c))

print("PASS")

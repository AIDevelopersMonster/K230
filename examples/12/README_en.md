# SHA-256 examples for K230

## What is SHA-256

**SHA-256** is a cryptographic hash function from the SHA-2 family.
It accepts input data of any length and produces a fixed-size result:

- **256 bits**
- **32 bytes**
- **64 hex characters** when shown as text

SHA-256 is not encryption. In practice, you cannot recover the original message from the hash.

## Main SHA-256 properties

- **Deterministic** — the same input always produces the same hash
- **Avalanche effect** — changing even one character changes the final hash dramatically
- **Fixed output size** — digest is always 32 bytes
- **Useful for integrity checks** — you can verify that a file or message was not modified

## How SHA-256 can be used on K230

On K230, SHA-256 is useful for:

- checking file integrity on an SD card;
- detecting changes in configuration files;
- validating transferred data over UART, Wi-Fi, or network links;
- preparing data for signing and verification;
- educational security and cryptography demos.

## Important note for CanMV / K230

On some K230 firmware versions, the object returned by `hashlib.sha256(...)` may not support `hexdigest()`.
Because of that, these examples use a K230-safe approach:

```python
import hashlib
import binascii

digest = hashlib.sha256(data).digest()
hex_text = binascii.hexlify(digest)
```

If `hexlify()` returns `bytes`, convert it to text with `.decode()`.

## Files in this folder

| File | Description | Used modules |
|------|-------------|--------------|
| `01_sha256_basic.py` | Basic example: digest, hex output, and determinism check | hashlib, binascii |
| `02_sha256_reference_test.py` | Reference test with zero-filled byte arrays and expected digests | hashlib, binascii |
| `03_sha256_avalanche.py` | Avalanche effect demo: changing one character changes the hash strongly | hashlib, binascii |

## Quick start

Run any example on the K230 board:

```python
# example 1
%run 01_sha256_basic.py

# example 2
%run 02_sha256_reference_test.py

# example 3
%run 03_sha256_avalanche.py
```

## What the examples demonstrate

### 1. Basic example
Shows the difference between binary `digest()` and its hex representation.

### 2. Reference test
Shows that SHA-256 can be calculated incrementally with `update()` and that the result matches a known reference value.

### 3. Avalanche effect
Shows that changing only one character can produce a dramatically different hash.

## Why plain SHA-256 is not recommended for passwords

SHA-256 is fast. That is great for integrity checks, but not ideal for password storage by itself.
For passwords, developers usually use:

- **Argon2**
- **bcrypt**
- **scrypt**
- **PBKDF2**

## Practical takeaway

If you want to:

- verify that a file was not modified;
- compare data by hash;
- demonstrate a cryptography concept;
- understand determinism and the avalanche effect,

then SHA-256 on K230 is a very good choice.

## See also

- Other examples in the `examples/` folder
- Repository: https://github.com/AIDevelopersMonster/K230

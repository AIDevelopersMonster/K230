# SHA-256 Examples for K230

## 📚 What is SHA-256

**SHA-256** is a cryptographic hash function from the SHA-2 family.
It accepts input data of any length and produces a fixed-size result:

- **256 bits**
- **32 bytes**
- **64 hex characters** when shown as text

> ⚠️ **Important:** SHA-256 is not encryption. In practice, you cannot recover the original message from the hash.

## 🔑 Main SHA-256 Properties

| Property | Description |
|----------|-------------|
| **Deterministic** | The same input always produces the same hash |
| **Avalanche effect** | Changing even one bit changes the final hash dramatically (about 50% of bits) |
| **Fixed output size** | Digest is always 32 bytes regardless of input size |
| **Fast** | Hash computation happens very quickly |
| **One-way function** | You cannot recover original data from the hash |

## 💡 How SHA-256 Can Be Used on K230

On K230, SHA-256 is useful for:

- ✅ Checking file integrity on an SD card;
- ✅ Detecting changes in configuration files;
- ✅ Validating transferred data over UART, Wi-Fi, or network links;
- ✅ Preparing data for digital signing and verification;
- ✅ Educational security and cryptography demos;
- ✅ Creating unique identifiers for data.

## ⚙️ Important Note for CanMV / K230

On some K230 firmware versions, the object returned by `hashlib.sha256(...)` may not support `hexdigest()`.
Because of that, these examples use a K230-safe approach:

```python
import hashlib
import binascii

digest = hashlib.sha256(data).digest()  # get 32 bytes
hex_text = binascii.hexlify(digest)     # convert to hex string
```

If `hexlify()` returns `bytes`, convert it to text with `.decode()`.

## 📁 Files in This Folder

| File | Description | For Whom |
|------|-------------|----------|
| `01_sha256_basic.py` | Basic example: digest, hex output, and determinism check | For beginners |
| `02_sha256_reference_test.py` | Reference test with expected values, using update() | For intermediate users |
| `03_sha256_avalanche.py` | Avalanche effect demo: changing one character changes the hash strongly | For everyone |

## 🚀 Quick Start

Run any example on the K230 board:

```python
# Example 1: Basic SHA-256 usage
%run 01_sha256_basic.py

# Example 2: Reference test with expected values
%run 02_sha256_reference_test.py

# Example 3: Avalanche effect
%run 03_sha256_avalanche.py
```

## 📖 What the Examples Demonstrate

### 1️⃣ Basic Example (`01_sha256_basic.py`)
Shows the difference between binary `digest()` and its hex representation.
You will learn:
- How to compute a hash of a string;
- That identical data produces identical hash;
- How 32 bytes of hash look in different formats.

### 2️⃣ Reference Test (`02_sha256_reference_test.py`)
Shows that SHA-256 can be calculated incrementally with `update()` and that the result matches a known reference value.
You will learn:
- How to feed data in chunks;
- How to verify hash function correctness;
- How to work with large amounts of data.

### 3️⃣ Avalanche Effect (`03_sha256_avalanche.py`)
Shows that changing only one character can produce a dramatically different hash (about 128 bits out of 256).
This demonstrates the cryptographic strength of SHA-256.

## ❓ Why Plain SHA-256 Is Not Recommended for Passwords

SHA-256 is fast. That is great for integrity checks, but not ideal for password storage by itself.
An attacker can quickly brute-force millions of password variants.

For passwords, developers usually use specialized functions:

| Function | Feature |
|----------|---------|
| **Argon2** | Winner of Password Hashing Competition, resistant to GPU attacks |
| **bcrypt** | Uses salt and adaptive cost factor |
| **scrypt** | Memory-hard, making hardware attacks difficult |
| **PBKDF2** | Multiple iterations of hash function |

## 💼 Practical Applications

If you want to:

- ✅ Verify that a file was not modified after download;
- ✅ Compare two datasets by hash;
- ✅ Demonstrate a cryptography concept;
- ✅ Understand determinism and the avalanche effect;
- ✅ Create a checksum for configuration,

then SHA-256 on K230 is a very good choice.

## 🔍 Real-World Usage Examples

```python
# Check file integrity
def check_file_integrity(filename, expected_hash):
    with open(filename, 'rb') as f:
        data = f.read()
    actual_hash = hashlib.sha256(data).digest()
    return actual_hash == expected_hash

# Create unique ID for data
def create_data_id(data):
    return hashlib.sha256(data).digest()
```

## 📚 Additional Resources

- [Wikipedia: SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [NIST: Secure Hash Standard](https://csrc.nist.gov/publications/detail/fips/180/4/final)
- Other examples in the `examples/` folder
- Repository: https://github.com/AIDevelopersMonster/K230

## 🤝 Contributing to the Project

If you find a bug or want to improve the examples, please create a Pull Request in the repository.

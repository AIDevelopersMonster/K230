# AES Examples for K230

## What is AES

**AES (Advanced Encryption Standard)** is a symmetric block cipher that encrypts data in 16-byte (128-bit) blocks. The same key is used for both encryption and decryption.

### Key Properties

- **Block cipher** — processes data in fixed 16-byte blocks
- **Key sizes**: 16 bytes (AES-128), 24 bytes (AES-192), 32 bytes (AES-256)
- **Symmetric** — single key for encryption and decryption
- **Reversible function** — unlike hash functions (SHA), original data can be recovered

## AES Modes of Operation

| Mode | Name | Description | Security |
|------|------|-------------|----------|
| **ECB** | Electronic Codebook | Each block encrypted independently | ❌ Insecure |
| **CBC** | Cipher Block Chaining | Each block depends on previous one | ✅ Secure |
| **CTR** | Counter | Stream mode based on counter | ✅ Secure |
| **GCM** | Galois/Counter Mode | CTR + data authentication | ✅ Most Secure |

## Examples in This Folder

| File | Description | Use Case |
|------|-------------|----------|
| `01_aes_ecb_basic.py` | Basic encryption and decryption | Learning AES basics |
| `02_aes_validation_tests.py` | Error validation (key and data length) | Exception handling |
| `03_aes_ecb_pattern_demo.py` | ECB vulnerability demonstration | Understanding ECB risks |

## Quick Start

### Running Examples

```bash
# Basic example
python 01_aes_ecb_basic.py

# Validation tests
python 02_aes_validation_tests.py

# ECB vulnerability demo
python 03_aes_ecb_pattern_demo.py
```

### Minimal Encryption Code

```python
import ucryptolib

key = b'1234567890abcdef'  # 16 bytes = AES-128
plaintext = b'Data to encrypt!'  # Must be multiple of 16 bytes

# Encryption
cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)
encrypted = cipher.encrypt(plaintext)

# Decryption
cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)
decrypted = cipher.decrypt(encrypted)
```

## Important Notes

### ⚠️ ECB Mode is Insecure!

**ECB (Electronic Codebook)** mode produces identical ciphertext blocks for identical plaintext blocks. This allows attackers to:
- Analyze patterns in encrypted data
- Identify repeated elements
- Perform cryptanalysis

**Use CBC, CTR, or GCM modes for real applications!**

### Data Requirements

1. **Key**: Must be exactly 16, 24, or 32 bytes
2. **Data**: Length must be multiple of 16 bytes (for ECB and CBC)
3. **For CBC mode**: Initialization Vector (IV) is required

## AES vs SHA Comparison

| Characteristic | AES | SHA |
|----------------|-----|-----|
| Type | Encryption | Hashing |
| Reversibility | ✅ Reversible | ❌ Irreversible |
| Key Required | Yes | No |
| Purpose | Confidentiality | Data Integrity |

## Additional Resources

- [MicroPython ucryptolib Documentation](https://docs.micropython.org/)
- [Wikipedia: AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)


---

**Author**: AIDevelopersMonster  
**Board**: Yahboom K230  
**GitHub**: https://github.com/AIDevelopersMonster/K230

# AES examples for K230

## What is AES

AES is a symmetric block cipher that encrypts data in 16-byte blocks.
The same key is used for encryption and decryption. fileciteturn30file0

## Key properties

- Block cipher (16 bytes)
- Key sizes: 16 / 24 / 32 bytes
- Reversible (unlike SHA)

## Modes

- ECB — simple but insecure
- CBC — chaining mode
- CTR — stream-like mode
- GCM — authenticated encryption fileciteturn30file0

## Examples

| File | Description |
|------|------------|
| 01_aes_ecb_basic.py | basic encrypt/decrypt |
| 02_aes_validation_tests.py | error validation |
| 03_aes_ecb_pattern_demo.py | ECB weakness demo |

## Important

ECB mode is insecure because identical blocks produce identical ciphertext.

## Usage

```python
cipher = ucryptolib.aes(key, ucryptolib.MODE_ECB)
```

## Summary

AES is reversible encryption, unlike hash functions.

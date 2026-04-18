# File Read and Write on K230

## What is it

File read/write operations allow saving data and reusing it later.

Examples:
- saving sensor data
- logging
- configuration storage

As described in documentation, many operations rely on file system fileciteturn33file0

## Path

On K230 files are stored in:

```python
/sdcard/
```

## Basic operations

### Write
```python
with open('/sdcard/file.txt', 'w') as f:
    f.write('hello')
```

### Read
```python
with open('/sdcard/file.txt', 'r') as f:
    data = f.read()
```

## Modes

- r — read
- w — write
- a — append
- rb — binary

## Why use with

- file auto closes
- safe on errors fileciteturn33file0

## Limitations

- avoid large file reads
- limited memory fileciteturn33file0

## Examples

- 01 basic read/write
- 02 modes
- 03 file system

## Summary

File IO is fundamental for any embedded system

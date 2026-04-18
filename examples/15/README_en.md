# File Read and Write on K230

## 📖 What is it

File read/write operations allow saving data to the device storage and reusing it later.

**Use cases:**
- 📊 Saving sensor data
- 📝 Application logging
- ⚙️ Device configuration storage
- 💾 Storing computation results

All operations on K230 (module loading, photo saving, logging) rely on the file system.

## 📁 Where files are stored

On Yahboom K230 board, files are stored at:

```python
/sdcard/
```

This path corresponds to the SD card installed in the board.

## 🔧 Basic operations

### Writing a file
```python
# Open file in write mode ('w' — write)
# If file exists — it will be overwritten
# If file doesn't exist — it will be created
with open('/sdcard/file.txt', 'w') as f:
    f.write('Hello K230!')
# File will be automatically closed after exiting the with block
```

### Reading a file
```python
# Open file in read mode ('r' — read)
with open('/sdcard/file.txt', 'r') as f:
    data = f.read()  # Read entire file content
print(data)
```

### Appending to a file
```python
# Open file in append mode ('a' — append)
# Data is added to the end of the file
with open('/sdcard/file.txt', 'a') as f:
    f.write('New line\n')
```

## 📋 File modes

| Mode | Description |
|------|-------------|
| `r` | Read (file must exist) |
| `w` | Write (file is created or overwritten) |
| `a` | Append (data is written at the end) |
| `rb` | Read in binary mode (for images, audio) |
| `wb` | Write in binary mode |

## ❓ Why use `with` statement?

```python
# ✅ Correct (with 'with'):
with open('/sdcard/file.txt', 'r') as f:
    data = f.read()
# File closes automatically, even if an error occurs

# ❌ Incorrect (without 'with'):
f = open('/sdcard/file.txt', 'r')
data = f.read()
f.close()  # Must remember to close manually!
```

**Advantages of `with`:**
- ✅ File closes automatically
- ✅ Safe when errors occur
- ✅ Cleaner and more readable code

## ⚠️ Limitations and recommendations

1. **Don't read large files entirely** — K230 memory is limited
   ```python
   # Better to read line by line:
   with open('/sdcard/large.txt', 'r') as f:
       for line in f:
           print(line)
   ```

2. **Always check SD card presence** before writing

3. **Use try-except** for error handling:
   ```python
   try:
       with open('/sdcard/file.txt', 'r') as f:
           data = f.read()
   except FileNotFoundError:
       print('File not found!')
   ```

## 📁 Example scripts

| File | Description |
|------|-------------|
| `01_file_basic.py` | Basic text read and write |
| `02_file_modes.py` | Demonstration of w, a, r modes |
| `03_file_system.py` | File system operations (os module) |

## 🚀 Quick start

1. Make sure SD card is inserted in the board
2. Run the example `01_file_basic.py`
3. Check the console output

## 💡 Summary

File I/O is a fundamental skill for K230 development.
Files allow you to persist data between program runs, maintain logs, and store device settings.

---
**Author:** AIDevelopersMonster  
**Board:** Yahboom K230  
**GitHub:** https://github.com/AIDevelopersMonster/K230

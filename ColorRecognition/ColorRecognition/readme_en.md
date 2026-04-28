# Color Recognition (K230)

## 📌 Description

This project demonstrates color recognition using the **Yahboom K230** board and **CanMV** framework.

The module shows how to recognize colors using the method:

```python
img.find_blobs()
```

It uses the **LAB color space**, which is better suited for color detection under varying lighting conditions.

---

## 🧠 How It Works

1. **Camera captures image** — the sensor captures a frame at 640x480 resolution.
2. **LAB threshold is applied** — thresholds are set to isolate the desired color.
3. **Color blobs are found** — the `find_blobs()` method searches for pixels within the specified range.
4. **Rectangle and center are drawn** — detected objects are highlighted on the screen.

### What is LAB?

- **L** — Lightness (from 0 to 100)
- **A** — From green to red
- **B** — From blue to yellow

---

## 🧪 Script Examples

| File | Description |
|------|----------|
| `01_color_recognition_camera.py` | Search for a single selected color (red, green, blue, or YAHBOOM cyan) |
| `02_multi_color_tracking.py` | Simultaneous search for multiple colors |

---

## ⚙️ Color Configuration

For precise color threshold tuning, use the built-in CanMV tool:

**Tools → Machine Vision → Threshold Editor**

1. Connect K230 to your computer.
2. Open Threshold Editor.
3. Point the camera at the object with the desired color.
4. Adjust L, A, B values.
5. Copy the obtained values and add them to the `THRESHOLDS` list in the code.

Threshold example:
```python
THRESHOLDS = [
    (0, 66, 7, 127, 3, 127),          # red
    (42, 100, -128, -17, 6, 66),      # green
    (43, 99, -43, -4, -56, -7),       # blue
]
```

---

## 🚀 Running the Script

1. Open CanMV IDE.
2. Connect the K230 board via USB.
3. Open the `.py` file in the editor.
4. Click **Run** (green button).
5. Point the camera at an object of the desired color.

---

## 📂 Working with Files on SD Card

### Reading a File

```python
with open("/sdcard/file.txt") as f:
    print(f.read())
```

### Writing to a File

```python
with open("/sdcard/file.txt", "w") as f:
    f.write("hello")
```

---

## 🔧 Useful Tips

- **Improve lighting** — colors are detected worse in poor light.
- **Remove glare** — reflections can distort color.
- **Adjust thresholds** — each object may require individual tuning.
- **Use merge=True** — to merge nearby areas of the same color.

---

## 📞 Contact

Author: **AIDevelopersMonster**  
GitHub: [https://github.com/AIDevelopersMonster/K230](https://github.com/AIDevelopersMonster/K230)

# Line Segment Detection (K230)

## 📋 Description

This example demonstrates how to detect straight line segments using `find_line_segments()` on Yahboom K230.

Based on official documentation (LSD + Hough Transform).

---

## 🎯 For Beginners

This example shows:
- What line segments are
- How to detect them from camera
- How to display them
- How to adjust detection parameters

---

## 🧠 API

### find_line_segments()

```python
lines = img.find_line_segments(merge_distance=15, max_theta_diff=10)
```

**Parameters:**
- `merge_distance` — merge close segments
- `max_theta_diff` — max angle difference

**Returns:** list of line objects

---

## 📁 Examples

| File | Description |
|------|------------|
| 01_line_segment_camera.py | Real-time detection |
| 02_line_segment_static.py | Static image example |

---

## 🎥 How it works

```
Camera → Image → Line Detection → Draw → Display
```

---

## 💡 Theory

Line detection uses LSD (Line Segment Detector) and Hough Transform fileciteturn0file0

---

## 👤 For Users

1. Connect K230
2. Open CanMV IDE
3. Run script
4. Point camera at lines

---

## 👨‍💻 For Developers

- Detection works faster on low resolution (160x120)
- Then scale to 640x480
- Use ROI to optimize

---

## 📂 File Reading/Writing

### Read file
```python
with open("data.txt", "r") as f:
    data = f.read()
```

### Write file
```python
with open("data.txt", "w") as f:
    f.write("Hello K230")
```

---

## 🔗 Repo
https://github.com/AIDevelopersMonster/K230

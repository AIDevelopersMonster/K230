# Color Recognition (K230)

## 📌 Description

This module demonstrates how to recognize colors using the K230 camera with LAB color space.

The module contains two examples:
- **01_color_recognition_camera.py** - Basic single color recognition with bounding box and center point display
- **02_multi_color_tracking.py** - Simultaneous recognition of multiple colors

---

## 🔧 How it works

1. **Image Capture** - Camera captures an image at 640x480 pixels resolution
2. **LAB Filtering** - LAB thresholds are applied to isolate the desired color
3. **Object Detection** - The `img.find_blobs()` function finds areas of the specified color
4. **Drawing** - A rectangle is drawn around detected objects with a cross at the center
5. **Display** - Result is shown on the display with FPS indication

### What is LAB Color Space?

LAB consists of three components:
- **L (Lightness)** - brightness from 0 (black) to 100 (white)
- **A** - green-red component from -128 (green) to 127 (red)
- **B** - blue-yellow component from -128 (blue) to 127 (yellow)

---

## 🧪 Examples

| File | Description |
|------|----------|
| `01_color_recognition_camera.py` | Single color detection with bounding box and center |
| `02_multi_color_tracking.py` | Multiple color detection simultaneously |

---

## ⚙️ Color Setup

### Using Threshold Editor

1. Open CanMV IDE
2. Go to **Tools → Machine Vision → Threshold Editor**
3. Point the camera at the object of the desired color
4. Adjust L, A, B values until the object is highlighted
5. Copy the obtained values
6. Add them to the `THRESHOLDS` list in the code

### Color Threshold Structure

```python
(L Min, L Max, A Min, A Max, B Min, B Max)
```

Example for red color:
```python
(0, 66, 7, 127, 3, 127)
```

---

## 🚀 Quick Start

### For Example 01 (single color):

1. Open file `01_color_recognition_camera.py` in CanMV IDE
2. Select the desired color by changing the `COLOR_INDEX` variable:
   - `0` - red
   - `1` - green
   - `2` - blue
   - `3` - cyan/YAHBOOM
3. Connect K230 board to computer via USB
4. Run the script with the **Run** button

### For Example 02 (multiple colors):

1. Open file `02_multi_color_tracking.py` in CanMV IDE
2. Adjust color thresholds in the `THRESHOLDS` list if needed
3. Connect K230 board to computer via USB
4. Run the script with the **Run** button

---

## 💡 Tips for Beginners

### If color detection is poor:

1. **Improve lighting** - make sure the object is well lit
2. **Remove glare** - avoid light reflections from the object
3. **Adjust thresholds** - use Threshold Editor for precise tuning
4. **Modify thresholds** - adjust values for your lighting conditions

### Useful functions:

```python
# Reading a file from SD card
with open("/sdcard/file.txt") as f:
    print(f.read())

# Writing a file to SD card
with open("/sdcard/file.txt", "w") as f:
    f.write("hello")
```

---

## 📚 Additional Resources

- [CanMV Documentation](https://canmv.kendryte.com/)
- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)
- [LAB Color Space (Wikipedia)](https://en.wikipedia.org/wiki/Lab_color_space)

---

## 👤 Author

**AIDevelopersMonster**  
Board: Yahboom K230  
GitHub: https://github.com/AIDevelopersMonster/K230

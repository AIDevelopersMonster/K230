# Circle Detection for Yahboom K230

## 📋 Description

This folder contains scripts for circle detection using the camera on the **Yahboom K230** board (CanMV). The scripts capture images from the camera, detect circles, and display results on the LCD screen and in the terminal.

## 📁 Files

| File | Description |
|------|----------|
| `01_circle_detection_lcd_light_dark.py` | Detects **black circles on a white background**. Displays circle count, radius, and coordinates. |
| `02_circle_detection_dark_mode.py` | Detects **white circles on a black background**. Uses binarization to improve contrast. |
| `img/` | Folder with test images (black and white circles). |

## 🚀 How to Use

### Requirements
- **Yahboom K230** board
- Connected camera (ID=2)
- ST7701 LCD display (640x480)
- CanMV IDE or direct board connection

### Running the Script

1. Connect the K230 board to your computer via USB.
2. Open CanMV IDE.
3. Copy one of the scripts (`01_...py` or `02_...py`) to the IDE.
4. Click the **Run** button (or F5).

### Configuring Parameters

At the beginning of each script, there's a **PARAMETER SETTINGS** section where you can modify:

```python
PICTURE_WIDTH = 400      # Camera image width
PICTURE_HEIGHT = 240     # Camera image height
CIRCLE_THRESHOLD = 3500  # Circle detection threshold
```

**Tip:** 
- Decrease `CIRCLE_THRESHOLD` if circles are not detected.
- Increase `CIRCLE_THRESHOLD` if there are many false positives.

## 🔍 How It Works

### Main Algorithm:

1. **Camera Initialization** — Configure resolution and pixel format.
2. **Display Initialization** — Prepare the LCD screen for output.
3. **Frame Capture** — Get image from the camera.
4. **Circle Detection** — The `find_circles()` function analyzes the image.
5. **Draw Results** — Detected circles are outlined with a cross at the center.
6. **Display Information** — Circle count and FPS shown on screen and in terminal.

### For Dark Background (`02_...py`):
Additionally, image **binarization** is applied:
```python
img.binary([(200, 255)])  # Keep only bright pixels
```
This helps to better highlight white circles on a black background.

## 📊 Output Information

On the screen you will see:
- **Circle outline** — Blue (for light background) or white (for dark background).
- **Center cross** — Red marker at circle center.
- **Label** — Circle number and radius (e.g., "C1 R25").
- **Statistics** — Circle count and FPS in the top-left corner.

In the terminal:
```
[Circle Detection Start]
count: 2
Circle 1 (x, y, r)
Circle 2 (x, y, r)
FPS: 30.5
```

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Circles not detected | Decrease `CIRCLE_THRESHOLD` to 2000-2500 |
| Many false positives | Increase `CIRCLE_THRESHOLD` to 4000-5000 |
| Image not centered | Check `DISPLAY_WIDTH` and `DISPLAY_HEIGHT` values |
| Script won't run | Ensure camera is connected to port ID=2 |

## 📚 Additional Resources

## 👨‍💻 Author

**AIDevelopersMonster**  
GitHub: [https://github.com/AIDevelopersMonster/K230](https://github.com/AIDevelopersMonster/K230)

---
*Scripts include detailed comments in Russian for beginner-friendly learning.*

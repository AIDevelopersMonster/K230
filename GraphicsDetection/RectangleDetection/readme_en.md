# Rectangle Detection

## 📋 Description

This project demonstrates rectangle detection on the **Yahboom K230** board using a camera and displaying results on an LCD screen.

The script captures images from the camera, detects rectangular objects using the `find_rects()` algorithm, and displays results on the screen with visual highlighting:
- Rectangle borders (blue frames)
- Rectangle corners (circles at vertices)
- Numbering of detected objects
- Statistics (rectangle count and FPS)

## 🛠️ Components Used

| Component | Description |
|-----------|----------|
| **Sensor** | Camera for image capture |
| **Display (ST7701)** | LCD screen for displaying results |
| **MediaManager** | Media manager for resource management |

## 📁 Project Structure

```
RectangleDetection/
├── 01_rectangle_detection_lcd_demo.py  # Main script
└── img/
    └── rectangle.png                    # Example image
```

## ⚙️ Settings

You can modify the following parameters at the beginning of the script:

| Parameter | Default Value | Description |
|-----------|--------------|----------|
| `PICTURE_WIDTH` | 400 | Width of captured image |
| `PICTURE_HEIGHT` | 240 | Height of captured image |
| `DISPLAY_WIDTH` | 640 | Width of LCD screen |
| `DISPLAY_HEIGHT` | 480 | Height of LCD screen |
| `RECT_THRESHOLD` | 8000 | Detection threshold (higher = more contrast rectangles detected) |

## 🚀 Getting Started

1. Connect the Yahboom K230 board to your computer
2. Open CanMV IDE
3. Upload the `01_rectangle_detection_lcd_demo.py` script to the board
4. Run the script through the IDE

## 📝 How It Works

1. **Initialization**: The script initializes the camera and LCD display
2. **Frame Capture**: The camera captures the current image
3. **Rectangle Detection**: The `find_rects()` algorithm analyzes the image and finds rectangular objects
4. **Rendering**: Detected rectangles are highlighted on the image
5. **Display**: The image is shown on the LCD screen
6. **Repeat**: The cycle repeats for the next frame

## 🔧 Adjusting Detection Threshold

The `RECT_THRESHOLD` parameter controls detection sensitivity:
- **Low value** (e.g., 3000): Will detect more rectangles, including less contrast ones
- **High value** (e.g., 15000): Will detect only the most contrast and clear rectangles

Adjust the value according to your lighting conditions and task requirements.

## 📷 Example Output

On the screen you will see:
- Camera view centered on the screen
- Blue frames around detected rectangles
- Circles at the corners of each rectangle
- Number of each detected object (RECT 1, RECT 2, ...)
- Statistics in the top-left corner (rectangle count and FPS)

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| Not detecting rectangles | Decrease `RECT_THRESHOLD` or improve lighting |
| Detecting too much noise | Increase `RECT_THRESHOLD` |
| Low FPS | Reduce camera resolution (`PICTURE_WIDTH`/`PICTURE_HEIGHT`) |

## 📄 License

Project created by AIDevelopersMonster for educational purposes.

## 🔗 Resources

- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)
- [K230 Documentation](https://wiki.yahboom.com/)

# Camera K230 - Camera Examples

## 📋 What is this?

This folder contains camera examples for the Yahboom K230 board. Here you will find three basic scripts that demonstrate the main camera capabilities: displaying images on the screen, saving snapshots, and overlaying text on images.

## 🎯 Example Descriptions

### 01_camera_preview.py - Basic Preview
**What it does:** Captures images from the camera and displays them on the screen in real-time.

**Main functions:**
- `sensor.reset()` - reset camera settings to default
- `sensor.set_framesize()` - set resolution (640x480)
- `sensor.set_pixformat()` - set color format (RGB565)
- `sensor.snapshot()` - capture a single frame
- `Display.show_image()` - display on screen

### 02_camera_snapshot_save.py - Save Snapshots
**What it does:** Displays camera images and automatically saves every 100th frame as a JPG file.

**Features:**
- Snapshots are saved to `/data/snapshot/` directory
- File names: 100.jpg, 200.jpg, 300.jpg, etc.
- Uses 10ms delay between frames for stability

**Main functions:**
- `img.save(path)` - save image to file
- `time.sleep_ms(10)` - delay in milliseconds
- `print()` - output information to console

### 03_camera_overlay_info.py - Text Overlay
**What it does:** Displays camera images with overlaid text (title and frame counter).

**Features:**
- Text is drawn directly on the image before display
- Yellow "Camera" text at the top
- Green text with frame counter

**Main functions:**
- `img.draw_string(x, y, text, color)` - draw text
- Coordinates are specified in pixels from the top-left corner
- Color is specified in RGB format as a tuple (R, G, B)

## 🔧 How it Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Camera    │ ──→ │  Processing  │ ──→ │   Display   │
│  (Sensor)   │     │  (Snapshot)  │     │  (Display)  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ↓
                    ┌──────────────┐
                    │    Saving    │
                    │   (Save)     │
                    └──────────────┘
```

## 📝 Main Components

### Sensor (Camera)
- **Initialization:** `sensor = Sensor()`
- **Configuration:** `sensor.reset()`, `sensor.set_framesize()`, `sensor.set_pixformat()`
- **Start:** `sensor.run()`
- **Capture frame:** `sensor.snapshot(chn=CAM_CHN_ID_1)`

### Display (Screen)
- **Initialization:** `Display.init(Display.ST7701, width=640, height=480, to_ide=True)`
- **Display:** `Display.show_image(img)`

### MediaManager
- **Initialization:** `MediaManager.init()` - required for media resource management

## ⚠️ Important Notes

1. **Image format:** RGB565 (16-bit color)
2. **Camera channel:** Use `CAM_CHN_ID_1` for the main channel
3. **Resolution:** 640x480 pixels is optimal for the display
4. **Camera start:** Always call `sensor.run()` before the loop
5. **Exit point:** `os.exitpoint()` is needed for proper termination via IDE

## 📁 File Structure

```
examples/20/
├── 01_camera_preview.py      # Basic preview example
├── 02_camera_snapshot_save.py # Example with snapshot saving
├── 03_camera_overlay_info.py  # Example with text overlay
├── README.md                  # Russian version
└── README_en.md               # This file (English version)
```

## 🚀 Quick Start

1. Connect the camera to the K230 board
2. Upload any example to the board
3. Run the script via IDE
4. Observe the result on the display

## 💡 Tips for Beginners

- Start with `01_camera_preview.py` - it's the simplest example
- Study the code comments - they explain each line
- Experiment with parameters (resolution, colors, text coordinates)
- Check the console for error messages

## 📚 Additional Resources

- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)
- Yahboom K230 Documentation
- Media module usage examples

---
**Author:** AIDevelopersMonster  
**Board:** Yahboom K230

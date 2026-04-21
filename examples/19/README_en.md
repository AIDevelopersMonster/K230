# Camera Image Flip (K230)

## 📋 What is it

Examples of camera image orientation control on the Yahboom K230 board.

**Image flip** changes the camera image orientation:
- **Horizontal Mirror (hmirror)** — left-right mirror reflection
- **Vertical Flip (vflip)** — top-bottom inversion
- **Double Flip** — combination of both effects (180° rotation)

## 🔧 How it works

```
camera → sensor → flip/vflip → snapshot → display
```

Processing happens at the camera sensor level, providing high performance without additional CPU load.

## 📦 Key Functions

| Function | Description | Parameter |
|----------|-------------|-----------|
| `sensor.set_hmirror(True)` | Horizontal mirror | `True` — enable, `False` — disable |
| `sensor.set_vflip(True)` | Vertical flip | `True` — enable, `False` — disable |

## 📁 Examples

| File | Description | When to use |
|------|-------------|-------------|
| `01_camera_basic_channel.py` | Normal image without modifications | Basic camera example |
| `02_camera_hmirror.py` | Horizontal mirror | Camera mounted backwards or for selfie mode |
| `03_camera_vflip.py` | Vertical flip | Camera mounted upside down |
| `04_camera_flip_both.py` | Full 180° rotation | Camera mounted at 180° angle |

## ⚠️ Important Notes

- **Use Channel 1**: `chn=CAM_CHN_ID_1` — main channel for image processing
- **Color Format**: `RGB565` — 16-bit format (Red 5 bits, Green 6 bits, Blue 5 bits)
- **Sensor Start**: `sensor.run()` is required before capturing frames
- **Resource Cleanup**: Always call `sensor.stop()`, `Display.deinit()`, and `MediaManager.deinit()` when finished

## 🚀 Quick Start

1. Connect the camera to the K230 board
2. Run any example through the IDE
3. View the image on the display

```python
# Minimal example
from media.sensor import *
from media.display import *
from media.media import *

sensor = Sensor()
sensor.reset()
sensor.set_framesize(width=640, height=480, chn=CAM_CHN_ID_1)
sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_1)
sensor.set_hmirror(True)  # Enable horizontal mirror

Display.init(Display.ST7701, width=640, height=480, to_ide=True)
MediaManager.init()
sensor.run()

while True:
    img = sensor.snapshot(chn=CAM_CHN_ID_1)
    Display.show_image(img)
```

## 💡 Tips

- **Orientation Setup**: Experiment with `set_hmirror()` and `set_vflip()` to achieve desired orientation
- **Performance**: Sensor-level processing does not affect FPS
- **Debugging**: Use `to_ide=True` to output images to the IDE

## 📚 Additional Information

- All examples use 640x480 resolution
- Display: ST7701 with 640x480 resolution
- `MediaManager` initialization is required for proper operation

---
**Author**: AIDevelopersMonster  
**Board**: Yahboom K230  
**GitHub**: https://github.com/AIDevelopersMonster/K230

# Image Display on K230

## What is it

Image display is showing images on the Yahboom K230 device screen.

Used for:
- Creating graphical user interfaces (UI)
- Camera output display
- Data visualization and algorithm results
- Game development and interactive applications

Images are loaded from the SD card and displayed on the screen via the ST7701 controller.

## File Structure

### Main Resources Path
```python
/sdcard/resources/
```

### Recommended File Formats
| Format | Support | Recommendation |
|--------|---------|----------------|
| PNG    | Excellent | Recommended (24/32 bit) |
| JPEG   | Limited | May work worse |
| BMP    | Good | Alternative to PNG |

## Important Requirements

- **Format**: Use PNG 24-bit or 32-bit recommended
- **Resolution**: Maximum 640x480 pixels (matches screen size)
- **Color Depth**: PNG 8-bit not supported, use 24/32 bit
- **Location**: Files must be on SD card in `/sdcard/resources/` folder

## Main Workflow Steps

1. **Display Initialization** - Configure controller and resolution
2. **MediaManager Initialization** - Prepare media subsystem
3. **Image Loading** - Read file from SD card
4. **RGB888 Conversion** - Convert to display format
5. **Display** - Show image on screen

## Code Examples

| File | Description | For Beginners |
|------|-------------|---------------|
| `01_image_display_basic.py` | Basic image display from file | Start here |
| `02_image_convert_and_show.py` | Color format conversion demo | Learn color handling |
| `03_image_generated.py` | Adding text to image | Drawing overlay |

## How to Run Examples

1. Copy image files to `/sdcard/resources/`
2. Connect display to K230 board
3. Run script via IDE or console

Minimal code example:
```python
from media.display import *
from media.media import *
import image

# Initialization
Display.init(Display.ST7701, width=640, height=480, osd_num=1, to_ide=True)
MediaManager.init()

# Load and display
img = image.Image('/sdcard/resources/wp.png', copy_to_fb=True)
img = img.to_rgb888()
Display.show_image(img)
```

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Image not displaying | PNG 8-bit format | Convert to 24/32 bit |
| Black screen | File not found | Check `/sdcard/resources/` path |
| Distorted colors | No conversion | Use `to_rgb888()` method |
| Program exits | No loop | Add `while True: time.sleep(1)` |

## Useful Methods

- `image.Image(path, copy_to_fb=True)` - Load image from file
- `img.to_rgb888()` - Convert to RGB888 format
- `Display.show_image(img)` - Display image on screen
- `img.draw_string_advanced(x, y, size, text, color)` - Draw text on image

## Additional Resources

- [K230 Documentation](https://github.com/AIDevelopersMonster/K230)
- [Display Examples](../)

## Summary

Working with images is a fundamental skill for K230 development.
These examples will help you create graphical interfaces, visualize data,
or develop your own application with UI elements.

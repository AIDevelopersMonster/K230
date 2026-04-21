# Touch Display on K230

## What is it

Touch Display is a touchscreen that responds to user touch input.

This allows you to:
- create graphical user interfaces (GUI)
- control the device with your finger or stylus
- build interactive applications with buttons and UI elements
- implement drawing and gesture recognition

## Core Concept

```text
finger → coordinates (x, y) → processing → action
```

The touchscreen is continuously scanned for touch events. When you touch the screen,
the controller returns the coordinates of the touch point, which can be used for:
- detecting button presses
- drawing lines and shapes
- moving objects
- selecting menu items

## Basic Workflow

1. **Initialize touch** - `TOUCH(0)` - prepare the touch controller
2. **Read coordinates** - `tp.read(1)` - get current touch coordinates
3. **Process** - check coordinates, determine actions
4. **Display result** - update the screen based on input

## API Reference

### machine.TOUCH(0)
Initializes the touch controller. Creates an object for working with the touchscreen.
For Yahboom K230, use `TOUCH(0)`.

### tp.read(n)
Returns a list of touch points (maximum n points).
Each point contains:
- `x` - horizontal coordinate (0..screen_width-1)
- `y` - vertical coordinate (0..screen_height-1)
- `event` - event type:
  - `0` or `TOUCH.EVENT_DOWN` - touch started (finger touched the screen)
  - `1` or `TOUCH.EVENT_MOVE` - finger moved on the screen
  - `2` or `TOUCH.EVENT_UP` - touch ended (finger lifted from screen)

## Examples

| File | Description | Difficulty | What You'll Learn |
|------|-------------|------------|-------------------|
| [01_touch_basic.py](01_touch_basic.py) | Basic touch reading, displays circle at touch point | ⭐ Beginner | Touch basics, coordinates, display layers |
| [02_touch_draw.py](02_touch_draw.py) | Drawing with finger on screen (like Paint) | ⭐⭐ Intermediate | Touch events, line drawing, canvas persistence |
| [03_touch_buttons.py](03_touch_buttons.py) | Creating interactive button with press handling | ⭐⭐ Intermediate | Area hit detection, GUI element creation |

## How It Works (for Beginners)

### Typical Program Structure:

```python
# 1. Import libraries
from media.display import *
from media.media import *
from machine import TOUCH
import image

# 2. Initialization
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
tp = TOUCH(0)  # Create touch controller object
Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
MediaManager.init()

# 3. Create image buffer
img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
img.clear()

# 4. Main loop
while True:
    os.exitpoint()  # Check exit flag
    
    # Clear buffer
    img.clear()
    
    # Read touch
    points = tp.read(1)
    
    # If touch detected - process it
    if len(points):
        pt = points[0]
        x, y = pt.x, pt.y
        print(f"Touch: x={x}, y={y}")
        # ... your logic here ...
    
    # Display result on screen
    Display.show_image(img)
    time.sleep(0.05)  # Small delay

# 5. Cleanup
Display.deinit()
MediaManager.deinit()
```

## Important Notes

- **tp.read(1)** returns a list of points only when touch is detected
- **Infinite loop is required** to continuously poll the touchscreen
- **Screen must be updated** after each image change
- **Loop delay** (`time.sleep()`) helps reduce CPU load
- **Coordinate system starts at top-left corner** (0, 0)
  - X increases right (0..639 for 640px screen)
  - Y increases down (0..479 for 480px screen)
- **Display layers**: you can use multiple layers (LAYER_OSD2, etc.) for overlaying graphics

## Tips for Beginners

1. **Start with `01_touch_basic.py`** - it's the simplest example showing the basics
2. **Use `print()` for debugging** - output coordinates and events to console
3. **Remember the coordinate system**: X increases right, Y increases down from top-left corner
4. **For buttons, check if coordinates fall within a rectangular area**:
   ```python
   if x_min < pt.x < x_max and y_min < pt.y < y_max:
       print("Button pressed!")
   ```
5. **Use separate overlay layers** for temporary graphics - this simplifies animation
6. **Don't forget to clean up resources** at the end: `Display.deinit()`, `MediaManager.deinit()`

## Running Instructions

1. Connect Yahboom K230 board to computer via USB
2. Open CanMV IDE and connect to the board
3. Select desired example (e.g., `01_touch_basic.py`)
4. Click the run button (▶) in IDE
5. Touch the screen to see the result

## Summary

Touch Display transforms your K230 into a modern device with an interface
similar to a smartphone or tablet. This opens up possibilities for creating:
- control panels and dashboards
- calculators and navigation menus
- graphics editors and drawing apps
- games with touch controls
- interactive information kiosks

---

## Useful Links

- **K230 Documentation**: https://wiki.k230.com/
- **CanMV IDE**: https://canmv.k230.com/
- **GitHub Repository**: https://github.com/AIDevelopersMonster/K230

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230  
**GitHub:** https://github.com/AIDevelopersMonster/K230

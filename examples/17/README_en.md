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

1. **Initialize touch** - `Touch.init()` - prepare the touch controller
2. **Read coordinates** - `Touch.read()` - get current touch coordinates
3. **Process** - check coordinates, determine actions
4. **Display result** - update the screen based on input

## API Reference

### Touch.init()
Initializes the touch controller. Should be called once at the beginning of the program.

### Touch.read()
Returns touch coordinates as `[x, y]` or `None` if no touch is detected.
- `x` - horizontal coordinate (0..screen_width-1)
- `y` - vertical coordinate (0..screen_height-1)

## Examples

| File | Description | Difficulty |
|------|-------------|------------|
| 01_touch_basic.py | Basic touch reading, displays circle at touch point | ⭐ Beginner |
| 02_touch_draw.py | Drawing with finger on screen (like Paint) | ⭐⭐ Intermediate |
| 03_touch_buttons.py | Creating interactive button with press handling | ⭐⭐ Intermediate |

## How It Works (for Beginners)

### Typical Program Structure:

```python
# 1. Import libraries
from media.display import *
from media.touch import *
import image

# 2. Initialization
Display.init(...)
Touch.init()

# 3. Create image buffer
img = image.Image(640, 480, image.RGB565)

# 4. Main loop
while True:
    # Clear buffer
    img.clear()
    
    # Read touch
    point = Touch.read()
    
    # If touch detected - process it
    if point:
        x, y = point[0], point[1]
        # ... your logic here ...
    
    # Display result on screen
    Display.show_image(img)
```

## Important Notes

- **Touch.read()** returns coordinates only when touch is detected
- **Infinite loop is required** to continuously poll the touchscreen
- **Screen must be updated** after each image change
- **Loop delay** (`time.sleep()`) helps reduce CPU load
- **Coordinate system starts at top-left corner** (0, 0)

## Tips for Beginners

1. Start with `01_touch_basic.py` - it's the simplest example
2. Use `print()` for debugging - output coordinates to console
3. Remember the coordinate system: X increases right, Y increases down
4. For buttons, check if coordinates fall within a rectangular area

## Summary

Touch Display transforms your K230 into a modern device with an interface
similar to a smartphone or tablet. This opens up possibilities for creating:
- control panels
- calculators and menus
- graphics editors
- games with touch controls

---

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230  
**GitHub:** https://github.com/AIDevelopersMonster/K230

# RGB Lights for K230

This folder contains simple examples of controlling the onboard RGB LED on the YAHBOOM K230 board.

## Contents

- `03_1_basic_rgb.py` — basic example: turn on a color and then turn it off
- `03_2_breathing_rgb.py` — smooth breathing effect using `math.sin()`
- `03_3_color_cycle_rgb.py` — cycling through multiple colors

## Requirements

- YAHBOOM K230 board
- CanMV IDE
- `ybUtils.YbRGB` library

## Quick Start

1. Connect your K230 to the computer
2. Open CanMV IDE
3. Create a new file or open one of the examples
4. Upload and run the code

## RGB Control Basics

Control is done using the `YbRGB` object:

```python
from ybUtils.YbRGB import YbRGB
rgb = YbRGB()
rgb.show_rgb((255, 0, 0))
```

Color format: `(R, G, B)` where each value is from `0` to `255`

Examples:

- `(255, 0, 0)` — red
- `(0, 255, 0)` — green
- `(0, 0, 255)` — blue
- `(255, 255, 255)` — white
- `(0, 0, 0)` — off

## Important Note

Internally, the WS2812B LED may use `GRB` order instead of `RGB`, but the `show_rgb()` function abstracts this, so you can use standard RGB format.

## Tips

- Fast color switching may look like flickering
- Use small `time.sleep()` delays for smooth animations
- Always turn off the LED when finishing:

```python
rgb.show_rgb((0, 0, 0))
```

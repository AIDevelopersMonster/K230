# Camera Display on K230

## What is it

Camera display shows camera image on screen. This example demonstrates three main ways to work with the camera:
- Basic image output to display
- Text overlay on video stream
- Frame capture to SD card

## How it works

```
camera → sensor.snapshot() → Display.show_image()
```

1. **Camera initialization**: Create `Sensor` object, configure resolution and pixel format
2. **Display initialization**: Connect ST7701 display with specified resolution
3. **Start streaming**: Call `sensor.run()` to begin image capture
4. **Main loop**: Continuously get frames and display them on screen

## Examples

| File | Description | Features |
|------|----------|-------------|
| `01_camera_basic.py` | Basic display | Simple camera video display with FPS counter |
| `02_camera_overlay.py` | Text overlay | Add text over image using `draw_string_advanced()` |
| `03_camera_capture_save.py` | Save frames | Periodic frame capture to SD card in JPG format |

## Default Settings

- **Pixel format**: RGB565 (16 bits per pixel)
- **Resolution**: 640×480 pixels
- **Display**: ST7701
- **Frame delay**: 5 ms

## Important Notes

- ⚠️ **`sensor.run()` is required** - camera won't capture images without it
- ⚠️ **`MediaManager.init()`** is necessary for proper media stream operation
- ⚠️ SD card required for saving files
- ⚠️ Don't forget to call `gc.collect()` to free memory

## Use Cases

- Computer vision and AI systems
- Video surveillance and monitoring
- Operator interfaces
- Photo and video recorders
- Educational robotics projects

## Code Structure

Each script contains:
1. Header with description and author info
2. Import of required libraries
3. Parameter configuration (resolution, format)
4. Hardware initialization
5. Main frame processing loop

## Additional Resources

- [K230 Documentation](https://github.com/AIDevelopersMonster/K230)
- [Sensor Usage Examples](../)
- [Display Operations](../)

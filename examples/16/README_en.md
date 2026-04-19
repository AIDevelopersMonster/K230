# Image Display on K230

## What is it

Image display is showing images on the device screen.

Used for:
- UI interfaces
- camera output
- visualization

Images are loaded from SD card and displayed fileciteturn34file0

## Path

```python
/sdcard/resources/
```

## Important

- PNG recommended
- JPEG worse quality fileciteturn34file0
- max resolution 640x480

## Steps

1. Init display
2. Load image
3. Convert to RGB888
4. Show image

## Examples

- 01 basic
- 02 conversion
- 03 generated

## Errors

- PNG 8-bit not supported
- use 24/32 bit fileciteturn34file0

## Summary

Image display is key for AI and UI

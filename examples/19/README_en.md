# Camera Image Flip (K230)

## What is it

Image flip changes camera orientation:
- horizontal mirror
- vertical flip

## Pipeline

camera → sensor → flip → snapshot → display

## Functions

- sensor.set_hmirror(True)
- sensor.set_vflip(True)

## Examples

| File | Description |
|------|------------|
| 01 | normal |
| 02 | mirror |
| 03 | vertical flip |
| 04 | both |

## Notes

- use channel 1
- RGB565 format
- sensor.run() required

## Summary

Flip is done at sensor level for performance

# Edge Detection (K230)

## Description
Edge detection demo using K230.

Uses:
image.find_edges()

## Examples
- 01_edge_detection_lcd.py
- 02_edge_detection_image_io.py

## File IO
Read:
img = image.Image("/sd/input.jpg")

Write:
img.save("/sd/output_edges.jpg")

## Parameters
threshold = (50, 80)

White pixels = detected edges

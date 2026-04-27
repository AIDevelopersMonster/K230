# Static image example for line segment detection (no camera required)
# Demonstrates how to draw and detect lines on a synthetic image.

import image

WIDTH = 320
HEIGHT = 240

img = image.Image(WIDTH, HEIGHT, image.RGB888)
img.clear()

# Draw some test lines
img.draw_line((10, 10, 200, 10), color=(255, 255, 255), thickness=2)
img.draw_line((20, 20, 200, 100), color=(255, 255, 255), thickness=2)
img.draw_line((50, 200, 300, 100), color=(255, 255, 255), thickness=2)

# Detect line segments
lines = img.find_line_segments(merge_distance=10, max_theta_diff=10)

# Draw results
for ln in lines:
    img.draw_line(ln.line(), color=(255, 0, 0), thickness=2)

print("Detected lines:", len(lines))

# If display available
try:
    from media.display import *
    Display.show_image(img)
except:
    pass

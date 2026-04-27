# Edge detection with file IO example
# Read image -> detect edges -> save result

import image

INPUT_PATH = "/sd/input.jpg"
OUTPUT_PATH = "/sd/output_edges.jpg"

print("Loading:", INPUT_PATH)
img = image.Image(INPUT_PATH)

# Convert to grayscale for edge detection
img.to_grayscale()

img.find_edges(image.EDGE_CANNY, threshold=(50, 80))

print("Saving:", OUTPUT_PATH)
img.save(OUTPUT_PATH)

print("Done")

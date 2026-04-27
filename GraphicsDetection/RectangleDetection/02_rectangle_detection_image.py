import image

INPUT_PATH = "/sd/input.jpg"
OUTPUT_PATH = "/sd/output.jpg"

img = image.Image(INPUT_PATH)

rects = img.find_rects(threshold=8000)

for r in rects:
    img.draw_rectangle(r.rect(), color=(255,255,255), thickness=2)
    for p in r.corners():
        img.draw_circle(p[0], p[1], 4, color=(255,0,0))

img.save(OUTPUT_PATH)

print("rectangles:", len(rects))

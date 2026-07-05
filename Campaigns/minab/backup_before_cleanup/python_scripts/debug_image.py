#!/usr/bin/env python3
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

img = Image.open("final-minab--01_scmx.jpg")
print(f"Mode: {img.mode}")
print(f"Size: {img.size}")

# Convert to RGB
img_rgb = img.convert("RGB")

# Sample pixels at borders (assuming borders are at edges)
width, height = img.size

# Sample top edge
for x in range(0, width, width//20):
    r, g, b = img_rgb.getpixel((x, 0))
    print(f"Top ({x},0): RGB({r},{g},{b})")

# Sample left edge
for y in range(0, height, height//20):
    r, g, b = img_rgb.getpixel((0, y))
    print(f"Left (0,{y}): RGB({r},{g},{b})")

# Sample middle area maybe
mid_x = width // 2
mid_y = height // 2
for dx in [-100, 0, 100]:
    for dy in [-100, 0, 100]:
        r, g, b = img_rgb.getpixel((mid_x + dx, mid_y + dy))
        print(f"Middle ({mid_x+dx},{mid_y+dy}): RGB({r},{g},{b})")

# Let's also look for red pixels by scanning a small region
# Take a 100x100 region at top-left corner
region = img_rgb.crop((0, 0, 100, 100))
pixels = list(region.getdata())
# Find distinct colors
distinct = set(pixels[:1000])
print(f"Distinct colors in region (first 1000 pixels): {len(distinct)}")
for color in list(distinct)[:10]:
    print(f"  {color}")

# Check if any pixel is reddish
reddish = [(r,g,b) for (r,g,b) in pixels if r > 200 and g < 100 and b < 100]
print(f"Reddish pixels in region: {len(reddish)}")
if reddish:
    print(f"Example reddish: {reddish[0]}")
#!/usr/bin/env python3
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

img = Image.open("final-minab--01_scmx.jpg")
print(f"Mode: {img.mode}")
width, height = img.size

# We'll scan along a few vertical and horizontal lines
# Save coordinates where pixel appears red

def is_red_cmyk(pixel):
    """Check if CMYK pixel is red."""
    c, m, y, k = pixel
    # Red: low cyan, high magenta, high yellow, low black
    return c < 50 and m > 200 and y > 200 and k < 50

def is_red_rgb(pixel):
    r, g, b = pixel
    return r > 200 and g < 100 and b < 100

# Convert to RGB for comparison
img_rgb = img.convert("RGB")

# Scan vertical line at x = 1000
x = 1000
print(f"\nScanning vertical line at x={x}")
for y in range(0, height, 100):
    cmyk = img.getpixel((x, y))
    rgb = img_rgb.getpixel((x, y))
    if is_red_cmyk(cmyk):
        print(f"  Red CMYK at ({x},{y}): {cmyk}")
    if is_red_rgb(rgb):
        print(f"  Red RGB at ({x},{y}): {rgb}")

# Scan horizontal line at y = 1000
y = 1000
print(f"\nScanning horizontal line at y={y}")
for x in range(0, width, 100):
    cmyk = img.getpixel((x, y))
    rgb = img_rgb.getpixel((x, y))
    if is_red_cmyk(cmyk):
        print(f"  Red CMYK at ({x},{y}): {cmyk}")
    if is_red_rgb(rgb):
        print(f"  Red RGB at ({x},{y}): {rgb}")

# Let's also try to find edges by looking at color changes
# Sample a grid
print("\nSampling grid 10x10")
for xi in range(0, width, width//10):
    for yi in range(0, height, height//10):
        cmyk = img.getpixel((xi, yi))
        if is_red_cmyk(cmyk):
            print(f"  Red at ({xi},{yi}): {cmyk}")
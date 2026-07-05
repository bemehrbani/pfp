#!/usr/bin/env python3
"""Test dimension checking for files in children_named."""

import os
from PIL import Image

src_dir = "children_named"
count = 0
dimension_count = 0
error_count = 0

for fname in os.listdir(src_dir):
    if fname.lower().endswith('.jpg'):
        count += 1
        path = os.path.join(src_dir, fname)
        if os.path.isfile(path) and not os.path.islink(path):
            try:
                img = Image.open(path)
                w, h = img.size
                print(f"{fname}: {w}x{h}")
                if 350 <= w <= 450 and 600 <= h <= 750:
                    dimension_count += 1
                else:
                    print(f"  Wrong dimensions: {w}x{h}")
            except Exception as e:
                error_count += 1
                print(f"  Error checking {fname}: {e}")

print(f"\n=== Summary ===")
print(f"Total .jpg files: {count}")
print(f"Files with correct dimensions: {dimension_count}")
print(f"Error count: {error_count}")
#!/usr/bin/env python3
import os
import shutil
from PIL import Image

src_dir = "splitted_final"
dst_dir = "children_final"
os.makedirs(dst_dir, exist_ok=True)

valid_count = 0
for fname in os.listdir(src_dir):
    if not fname.lower().endswith('.jpg'):
        continue
    path = os.path.join(src_dir, fname)
    try:
        img = Image.open(path)
        w, h = img.size
        # Filter by expected child photo dimensions
        if 350 <= w <= 450 and 600 <= h <= 750:
            # Rename to child_XXX.jpg
            new_name = f"child_{valid_count:03d}.jpg"
            shutil.copy2(path, os.path.join(dst_dir, new_name))
            print(f"Kept {fname} -> {new_name} ({w}x{h})")
            valid_count += 1
        else:
            print(f"Skipped {fname} ({w}x{h})")
    except Exception as e:
        print(f"Error processing {fname}: {e}")

print(f"\nTotal valid child photos: {valid_count}")
print(f"Saved in {dst_dir}")
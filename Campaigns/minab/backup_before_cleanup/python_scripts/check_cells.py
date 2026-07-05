#!/usr/bin/env python3
import os
from PIL import Image

output_dir = "splitted_photos_grid"
files = sorted([f for f in os.listdir(output_dir) if f.startswith("child_") and f.endswith(".jpg")])
for f in files[:30]:
    path = os.path.join(output_dir, f)
    img = Image.open(path)
    print(f"{f}: {img.size}")
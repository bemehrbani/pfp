#!/usr/bin/env python3
"""
Extract child names from filtered photos using OCR (Farsi).
"""

import os
import cv2
import numpy as np
import pytesseract
from PIL import Image

input_dir = "children_final"
output_dir = "children_named"
os.makedirs(output_dir, exist_ok=True)

# Mapping file
mapping = []

for fname in sorted(os.listdir(input_dir)):
    if not fname.lower().endswith('.jpg'):
        continue
    path = os.path.join(input_dir, fname)
    img = cv2.imread(path)
    if img is None:
        continue

    height, width = img.shape[:2]
    # Crop bottom 20% of image where name likely appears
    bottom_start = int(height * 0.8)
    bottom_region = img[bottom_start:height, 0:width]

    # Preprocess: convert to grayscale, threshold
    gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)
    # Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    # Threshold
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Try OCR with Farsi
    config = '--psm 7 -l fas+ara+eng'
    try:
        text = pytesseract.image_to_string(thresh, config=config)
        text = text.strip()
    except:
        text = ""

    # If no text, try whole image
    if not text:
        gray_full = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh_full = cv2.threshold(gray_full, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(thresh_full, config=config)
        text = text.strip()

    # Clean text: keep Persian/Arabic letters, spaces, numbers
    # Persian letters range: \u0600-\u06FF
    import re
    cleaned = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u0041-\u005A\u0061-\u007A\u0030-\u0039\s]', '', text)
    cleaned = cleaned.strip()

    # If still empty, use placeholder
    if not cleaned:
        cleaned = f"child_{fname}"

    # Create safe filename
    safe = cleaned.replace(' ', '_').replace('/', '_').replace('\\', '_')
    safe = safe[:50]  # limit length
    if not safe:
        safe = f"child_{fname}"

    # Ensure unique filename
    base = safe
    ext = '.jpg'
    counter = 1
    new_path = os.path.join(output_dir, base + ext)
    while os.path.exists(new_path):
        new_path = os.path.join(output_dir, f"{base}_{counter}{ext}")
        counter += 1

    # Copy file
    import shutil
    shutil.copy2(path, new_path)
    mapping.append((fname, cleaned, os.path.basename(new_path)))
    print(f"{fname} -> {os.path.basename(new_path)} ('{cleaned}')")

# Save mapping
with open(os.path.join(output_dir, "name_mapping.txt"), "w", encoding='utf-8') as f:
    for orig, name, new in mapping:
        f.write(f"{orig}\t{name}\t{new}\n")

print(f"\nProcessed {len(mapping)} images.")
print(f"Output in {output_dir}")
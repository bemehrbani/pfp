#!/usr/bin/env python3
"""Test OCR for index 94 which had Farsi text."""

import cv2
import numpy as np
import pytesseract
from PIL import Image

def load_image():
    input_path = "final-minab--01_scmx.jpg"
    img_bgr = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        pil_img = Image.open(input_path)
        if pil_img.mode == 'CMYK':
            pil_img = pil_img.convert('RGB')
        img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return img_bgr

def main():
    img = load_image()
    height, width = img.shape[:2]

    # Read coordinates for index 94
    coords_file = "children_with_names/coordinates.txt"
    with open(coords_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue

        idx = parts[0]
        if idx != "94":
            continue

        x = int(parts[1])
        y = int(parts[2])
        w = int(parts[3])
        h = int(parts[4])
        print(f"Index 94: ({x},{y},{w},{h})")

        # Extract multiple regions
        regions = [
            ("below_200", x, min(height-1, y+h), w, 200),
            ("below_400", x, min(height-1, y+h), w, 400),
            ("above_100", x, max(0, y-100), w, min(100, y)),
            ("inside_bottom", x+20, y+h-100, w-40, 80),
        ]

        # OCR configs
        configs = [
            ("eng6", "--psm 6 -l eng"),
            ("eng7", "--psm 7 -l eng"),
            ("eng8", "--psm 8 -l eng"),
            ("fas6", "--psm 6 -l fas"),
            ("fas7", "--psm 7 -l fas"),
            ("fas+ara6", "--psm 6 -l fas+ara"),
            ("fas+ara7", "--psm 7 -l fas+ara"),
            ("ara6", "--psm 6 -l ara"),
            ("ara7", "--psm 7 -l ara"),
        ]

        for region_name, rx, ry, rw, rh in regions:
            if rw <= 0 or rh <= 0:
                continue
            if ry + rh > height or rx + rw > width:
                continue

            region = img[ry:ry+rh, rx:rx+rw]
            if region.size == 0:
                continue

            # Convert to grayscale
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

            # Multiple preprocessing
            preprocess = [
                ("otsu", lambda g: cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
                ("otsu_inv", lambda g: cv2.threshold(g, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]),
                ("adaptive", lambda g: cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)),
                ("adaptive_inv", lambda g: cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)),
            ]

            print(f"\n--- {region_name} ({rw}x{rh}) ---")
            for prep_name, prep_func in preprocess:
                prepped = prep_func(gray)
                cv2.imwrite(f"test_94_{region_name}_{prep_name}.jpg", prepped)

                for config_name, config in configs:
                    try:
                        text = pytesseract.image_to_string(prepped, config=config)
                        text = text.strip()
                        if text and len(text) > 1:
                            # Check if it looks like text (has letters)
                            if any(c.isalpha() for c in text):
                                print(f"  {prep_name}/{config_name}: {text[:60]}")
                    except:
                        pass

        break

if __name__ == "__main__":
    main()
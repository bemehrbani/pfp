#!/usr/bin/env python3
"""Examine failed OCR cases more closely."""

import cv2
import numpy as np
from PIL import Image
import os

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

    # Read coordinates
    coords_file = "children_with_names/coordinates.txt"
    with open(coords_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip header
    if len(lines) < 2:
        return

    # Create directory for examination
    os.makedirs("failed_examination", exist_ok=True)

    # Test first 10 indices that are not successful
    successful_indices = ["96", "97", "99", "101", "102", "103", "94"]
    test_indices = []
    for i in range(10):
        idx = str(i)
        if idx not in successful_indices:
            test_indices.append(idx)

    # Also test index 94 (has Farsi text)
    if "94" not in test_indices:
        test_indices.append("94")

    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue

        idx = parts[0]
        if idx not in test_indices:
            continue

        x = int(parts[1])
        y = int(parts[2])
        w = int(parts[3])
        h = int(parts[4])

        print(f"\n=== Examining index {idx} ===")

        # Define search regions
        regions = [
            ("below_200", x, min(height-1, y+h), w, 200),
            ("below_400", x, min(height-1, y+h), w, 400),
            ("above_100", x, max(0, y-100), w, min(100, y)),
            ("left_100", max(0, x-100), y, min(100, x), h),
            ("right_100", min(width-1, x+w), y, 100, h),
            ("inside_bottom", x+20, y+h-100, w-40, 80),  # Bottom inside border
        ]

        for region_name, rx, ry, rw, rh in regions:
            # Check bounds
            if rw <= 0 or rh <= 0:
                continue
            if ry + rh > height or rx + rw > width:
                continue

            region = img[ry:ry+rh, rx:rx+rw]
            if region.size == 0:
                continue

            # Save original region
            cv2.imwrite(f"failed_examination/{idx}_{region_name}.jpg", region)

            # Convert to grayscale
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

            # Multiple preprocessing
            # 1. Otsu
            _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            cv2.imwrite(f"failed_examination/{idx}_{region_name}_otsu.jpg", otsu)

            # 2. Adaptive
            adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 2)
            cv2.imwrite(f"failed_examination/{idx}_{region_name}_adaptive.jpg", adaptive)

            # 3. Inverted (white text on black background)
            _, otsu_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            cv2.imwrite(f"failed_examination/{idx}_{region_name}_otsu_inv.jpg", otsu_inv)

            print(f"  Saved {region_name} region and preprocessed images")

        # Also try MSER text detection on below_400 region
        below_start = min(height-1, y+h)
        below_end = min(height-1, below_start + 400)
        below_region = img[below_start:below_end, x:x+w]

        if below_region.size > 0:
            # Try MSER
            gray_below = cv2.cvtColor(below_region, cv2.COLOR_BGR2GRAY)
            mser = cv2.MSER_create()
            regions_mser, _ = mser.detectRegions(gray_below)

            # Draw regions
            mser_vis = below_region.copy()
            for reg in regions_mser:
                # Get bounding box
                x_reg, y_reg, w_reg, h_reg = cv2.boundingRect(reg.reshape(-1, 1, 2))
                # Filter by size
                if 20 < w_reg < 500 and 10 < h_reg < 200:
                    cv2.rectangle(mser_vis, (x_reg, y_reg), (x_reg+w_reg, y_reg+h_reg), (0, 255, 0), 2)

            cv2.imwrite(f"failed_examination/{idx}_mser.jpg", mser_vis)
            print(f"  MSER found {len(regions_mser)} regions")

    print("\nExamination images saved to failed_examination/")
    print("Manually inspect these images to see where text might be located.")

if __name__ == "__main__":
    main()
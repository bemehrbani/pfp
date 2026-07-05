#!/usr/bin/env python3
"""Examine text regions around successful border extraction."""

import cv2
import numpy as np
import os
from PIL import Image

def main():
    input_path = "final-minab--01_scmx.jpg"

    # Load original image
    print("Loading image...")
    img_bgr = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        # Try with PIL
        pil_img = Image.open(input_path)
        if pil_img.mode == 'CMYK':
            pil_img = pil_img.convert('RGB')
        img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Coordinates for Hami Sadeghi (index 96 from coordinates.txt)
    # Actually index 97 in file, but filename Hami_Sadeghi_097.jpg
    x, y, w, h = 5261, 10089, 752, 1018

    # Create output directory
    os.makedirs("text_regions_debug", exist_ok=True)

    # Save the border region itself
    border_region = img_bgr[y:y+h, x:x+w]
    cv2.imwrite("text_regions_debug/00_border_region.jpg", border_region)

    # Define search regions (relative to border)
    regions = [
        ("above", x, max(0, y-200), w, min(200, y)),  # 200 pixels above
        ("below", x, y+h, w, 200),  # 200 pixels below
        ("left", max(0, x-200), y, min(200, x), h),  # 200 pixels left
        ("right", x+w, y, 200, h),  # 200 pixels right
        ("above_100", x, max(0, y-100), w, min(100, y)),
        ("below_100", x, y+h, w, 100),
        ("above_300", x, max(0, y-300), w, min(300, y)),
        ("below_300", x, y+h, w, 300),
    ]

    # Extract and save each region
    for name, rx, ry, rw, rh in regions:
        # Check bounds
        if rw <= 0 or rh <= 0:
            continue
        if ry + rh > img_bgr.shape[0] or rx + rw > img_bgr.shape[1]:
            continue

        region = img_bgr[ry:ry+rh, rx:rx+rw]
        if region.size > 0:
            cv2.imwrite(f"text_regions_debug/{name}.jpg", region)
            print(f"Saved {name}: {rx},{ry},{rw},{rh}")

    # Also try bottom part of the border region itself (inside border)
    # Maybe name is inside the photo?
    border_thickness = 20
    x_inner = x + border_thickness
    y_inner = y + border_thickness
    w_inner = w - 2 * border_thickness
    h_inner = h - 2 * border_thickness

    if w_inner > 0 and h_inner > 0:
        inner_region = img_bgr[y_inner:y_inner+h_inner, x_inner:x_inner+w_inner]
        cv2.imwrite("text_regions_debug/inner_region.jpg", inner_region)

        # Check bottom 20% of inner region
        inner_height = inner_region.shape[0]
        bottom_start = int(inner_height * 0.8)
        bottom_region = inner_region[bottom_start:, :]
        cv2.imwrite("text_regions_debug/inner_bottom.jpg", bottom_region)

    print("\nRegions saved to text_regions_debug/")
    print("Now examine these images to see where the text 'Hami Sadeghi' appears.")

if __name__ == "__main__":
    main()
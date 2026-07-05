#!/usr/bin/env python3
"""Find text regions in child photos."""

import cv2
import numpy as np
from PIL import Image
import os

def find_text_regions(image_path):
    """Detect potential text regions using OpenCV."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load {image_path}")
        return []

    height, width = img.shape[:2]

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Try multiple preprocessing methods
    methods = []

    # 1. Simple threshold
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    methods.append(("otsu", thresh))

    # 2. Adaptive threshold
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)
    methods.append(("adaptive", adaptive))

    # 3. Edge detection (Canny)
    edges = cv2.Canny(gray, 50, 150)
    methods.append(("canny", edges))

    # 4. Contrast enhancement
    enhanced = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    _, enhanced_thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    methods.append(("enhanced_otsu", enhanced_thresh))

    # Save debug images
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    for method_name, method_img in methods:
        cv2.imwrite(f"debug_{base_name}_{method_name}.jpg", method_img)

    print(f"\n=== {os.path.basename(image_path)} ===")
    print(f"Size: {width}x{height}")

    # Check different regions for text
    regions = [
        ("bottom 30%", 0.7, 1.0, 0.0, 1.0),
        ("bottom 20%", 0.8, 1.0, 0.0, 1.0),
        ("bottom 10%", 0.9, 1.0, 0.0, 1.0),
        ("top 10%", 0.0, 0.1, 0.0, 1.0),
        ("top 20%", 0.0, 0.2, 0.0, 1.0),
        ("left side", 0.0, 1.0, 0.0, 0.3),
        ("right side", 0.0, 1.0, 0.7, 1.0),
        ("center bottom", 0.8, 1.0, 0.3, 0.7),
    ]

    for region_name, y_start, y_end, x_start, x_end in regions:
        y1 = int(height * y_start)
        y2 = int(height * y_end)
        x1 = int(width * x_start)
        x2 = int(width * x_end)

        if y2 - y1 <= 0 or x2 - x1 <= 0:
            continue

        region = gray[y1:y2, x1:x2]
        region_enhanced = cv2.convertScaleAbs(region, alpha=2.0, beta=0)
        _, region_thresh = cv2.threshold(region_enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Save region for visual inspection
        region_filename = f"debug_{base_name}_{region_name.replace(' ', '_')}.jpg"
        cv2.imwrite(region_filename, region_thresh)

        print(f"\nRegion: {region_name} ({x1},{y1})-({x2},{y2}) size: {x2-x1}x{y2-y1}")

def main():
    # Test on first 5 child photos
    child_dir = "final_children"
    files = sorted([f for f in os.listdir(child_dir) if f.startswith("child_") and f.endswith(".jpg")])

    for i, fname in enumerate(files[:5]):
        path = os.path.join(child_dir, fname)
        find_text_regions(path)
        if i >= 2:  # Just do 3 for now
            break

    print("\nDebug images saved. Check for text in regions.")

if __name__ == "__main__":
    main()
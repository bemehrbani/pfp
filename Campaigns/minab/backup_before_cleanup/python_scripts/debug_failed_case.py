#!/usr/bin/env python3
"""Debug a failed OCR case."""

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

def ocr_region(img, region_name, x, y, w, h):
    """OCR a specific region."""
    if w <= 0 or h <= 0:
        return

    region = img[y:y+h, x:x+w]
    if region.size == 0:
        return

    # Save region for visual inspection
    cv2.imwrite(f"debug_{region_name}.jpg", region)

    # Preprocess
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    # Multiple preprocessing
    methods = []
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    methods.append(("otsu", otsu))

    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    methods.append(("adaptive", adaptive))

    enhanced = cv2.convertScaleAbs(gray, alpha=2.0, beta=0)
    _, enhanced_thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    methods.append(("enhanced", enhanced_thresh))

    # OCR configs
    configs = [
        ("eng6", "--psm 6 -l eng"),
        ("eng7", "--psm 7 -l eng"),
        ("eng8", "--psm 8 -l eng"),
        ("fas6", "--psm 6 -l fas"),
        ("fas7", "--psm 7 -l fas"),
    ]

    print(f"\n=== {region_name} ({x},{y},{w},{h}) ===")

    for prep_name, prep_img in methods:
        cv2.imwrite(f"debug_{region_name}_{prep_name}.jpg", prep_img)
        for config_name, config in configs:
            try:
                text = pytesseract.image_to_string(prep_img, config=config)
                text = text.strip()
                if text and len(text) > 1:
                    print(f"  {prep_name}/{config_name}: {text[:60]}")
            except:
                pass

def main():
    img = load_image()

    # Failed case: index 0
    x, y, w, h = 8920, 478, 566, 752
    print(f"Debugging failed case at {x},{y},{w},{h}")

    # Check various regions
    regions = [
        ("border", x, y, w, h),
        ("above_100", x, max(0, y-100), w, min(100, y)),
        ("above_200", x, max(0, y-200), w, min(200, y)),
        ("below_100", x, y+h, w, 100),
        ("below_200", x, y+h, w, 200),
        ("below_300", x, y+h, w, 300),
        ("left_100", max(0, x-100), y, min(100, x), h),
        ("right_100", x+w, y, 100, h),
        ("inside", x+20, y+20, w-40, h-40),  # Inside border
        ("inside_bottom", x+20, y+h-100, w-40, 80),  # Bottom inside
    ]

    for region_name, rx, ry, rw, rh in regions:
        ocr_region(img, region_name, rx, ry, rw, rh)

    print("\n=== Also checking successful case for comparison ===")
    # Successful case: Hami Sadeghi
    x2, y2, w2, h2 = 5261, 10089, 752, 1018
    ocr_region(img, "success_below_200", x2, y2+h2, w2, 200)

if __name__ == "__main__":
    main()
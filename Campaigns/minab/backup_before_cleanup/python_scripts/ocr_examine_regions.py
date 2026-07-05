#!/usr/bin/env python3
"""OCR examine regions to find where text is."""

import cv2
import numpy as np
import os
import pytesseract
from PIL import Image

def preprocess_for_ocr(image):
    """Preprocess image for OCR."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Try multiple preprocessing methods
    results = []

    # 1. Simple threshold
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 2. Adaptive threshold
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)

    # 3. Contrast enhancement
    enhanced = cv2.convertScaleAbs(gray, alpha=2.0, beta=0)
    _, enhanced_thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return [("otsu", thresh), ("adaptive", adaptive), ("enhanced", enhanced_thresh)]

def ocr_image(image, config="--psm 6 -l eng"):
    """Run OCR on image."""
    try:
        text = pytesseract.image_to_string(image, config=config)
        return text.strip()
    except:
        return ""

def main():
    input_path = "final-minab--01_scmx.jpg"

    # Load original image
    print("Loading image...")
    img_bgr = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        pil_img = Image.open(input_path)
        if pil_img.mode == 'CMYK':
            pil_img = pil_img.convert('RGB')
        img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Coordinates for Hami Sadeghi
    x, y, w, h = 5261, 10089, 752, 1018

    # Define search regions
    regions = [
        ("above", x, max(0, y-200), w, min(200, y)),
        ("below", x, y+h, w, 200),
        ("left", max(0, x-200), y, min(200, x), h),
        ("right", x+w, y, 200, h),
        ("above_100", x, max(0, y-100), w, min(100, y)),
        ("below_100", x, y+h, w, 100),
        ("above_300", x, max(0, y-300), w, min(300, y)),
        ("below_300", x, y+h, w, 300),
    ]

    # OCR configurations to try
    configs = [
        ("eng", "--psm 6 -l eng"),
        ("eng_psm7", "--psm 7 -l eng"),
        ("fas", "--psm 6 -l fas"),
        ("fas_psm7", "--psm 7 -l fas"),
        ("fas+ara", "--psm 6 -l fas+ara"),
        ("fas+ara_psm7", "--psm 7 -l fas+ara"),
    ]

    print("\n=== OCR Results ===")

    for name, rx, ry, rw, rh in regions:
        # Check bounds
        if rw <= 0 or rh <= 0:
            continue
        if ry + rh > img_bgr.shape[0] or rx + rw > img_bgr.shape[1]:
            continue

        region = img_bgr[ry:ry+rh, rx:rx+rw]
        if region.size == 0:
            continue

        print(f"\n--- Region: {name} ({rx},{ry},{rw},{rh}) ---")

        # Preprocess
        preprocessed = preprocess_for_ocr(region)

        for prep_name, prep_img in preprocessed:
            # Try each OCR config
            for config_name, config in configs:
                text = ocr_image(prep_img, config)
                if text and len(text) > 2:  # At least 3 chars
                    # Check if text looks like a name (contains letters)
                    has_letters = any(c.isalpha() for c in text)
                    if has_letters:
                        print(f"  {prep_name}/{config_name}: {text[:50]}")

    # Also check inside border
    border_thickness = 20
    x_inner = x + border_thickness
    y_inner = y + border_thickness
    w_inner = w - 2 * border_thickness
    h_inner = h - 2 * border_thickness

    if w_inner > 0 and h_inner > 0:
        inner_region = img_bgr[y_inner:y_inner+h_inner, x_inner:x_inner+w_inner]
        print(f"\n--- Inner region ({x_inner},{y_inner},{w_inner},{h_inner}) ---")

        preprocessed = preprocess_for_ocr(inner_region)
        for prep_name, prep_img in preprocessed:
            for config_name, config in configs:
                text = ocr_image(prep_img, config)
                if text and len(text) > 2:
                    has_letters = any(c.isalpha() for c in text)
                    if has_letters:
                        print(f"  {prep_name}/{config_name}: {text[:50]}")

    print("\n=== Checking bottom part of inner region ===")
    if w_inner > 0 and h_inner > 0:
        inner_height = inner_region.shape[0]
        bottom_start = int(inner_height * 0.8)
        bottom_region = inner_region[bottom_start:, :]

        preprocessed = preprocess_for_ocr(bottom_region)
        for prep_name, prep_img in preprocessed:
            for config_name, config in configs:
                text = ocr_image(prep_img, config)
                if text and len(text) > 2:
                    has_letters = any(c.isalpha() for c in text)
                    if has_letters:
                        print(f"  {prep_name}/{config_name}: {text[:50]}")

if __name__ == "__main__":
    main()
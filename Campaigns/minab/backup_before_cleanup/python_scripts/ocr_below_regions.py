#!/usr/bin/env python3
"""OCR text from below-border regions for multiple indices."""

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

def preprocess_for_ocr(image):
    """Preprocess image for OCR."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Multiple preprocessing methods
    results = []

    # 1. Otsu threshold
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    results.append(("otsu", otsu))

    # 2. Adaptive threshold
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    results.append(("adaptive", adaptive))

    # 3. Enhanced contrast
    enhanced = cv2.convertScaleAbs(gray, alpha=2.0, beta=0)
    _, enhanced_thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    results.append(("enhanced", enhanced_thresh))

    # 4. Denoising + Otsu
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    _, denoised_thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    results.append(("denoised", denoised_thresh))

    return results

def ocr_image(image, config="--psm 6 -l eng"):
    """Run OCR on image."""
    try:
        text = pytesseract.image_to_string(image, config=config)
        return text.strip()
    except:
        return ""

def main():
    img = load_image()
    height, width = img.shape[:2]
    print(f"Image size: {width}x{height}")

    # Read coordinates
    coords_file = "children_with_names/coordinates.txt"
    with open(coords_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip header
    if len(lines) < 2:
        print("No coordinates found")
        return

    # Test indices: some failed (0, 1, 2) and successful (96, 97, 99, 101, 102, 103)
    test_indices = ["0", "1", "2", "96", "97", "99", "101", "102", "103"]

    # OCR configurations
    configs = [
        ("eng6", "--psm 6 -l eng"),
        ("eng7", "--psm 7 -l eng"),
        ("eng8", "--psm 8 -l eng"),
        ("fas6", "--psm 6 -l fas"),
        ("fas7", "--psm 7 -l fas"),
        ("fas+ara6", "--psm 6 -l fas+ara"),
        ("fas+ara7", "--psm 7 -l fas+ara"),
    ]

    # Find coordinates for each test index
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

        print(f"\n=== Index {idx} ({x},{y},{w},{h}) ===")

        # Extract region 200-400 pixels below border
        below_start = min(height-1, y + h)
        below_end = min(height-1, below_start + 400)
        below_region = img[below_start:below_end, x:x+w]

        if below_region.size == 0:
            print("  No below region (out of bounds)")
            continue

        # Save for visual inspection
        cv2.imwrite(f"below_{idx}.jpg", below_region)
        print(f"  Saved below_{idx}.jpg ({w}x{below_end-below_start})")

        # Preprocess
        preprocessed = preprocess_for_ocr(below_region)

        # Try each preprocessing and config
        best_text = ""
        best_score = 0

        for prep_name, prep_img in preprocessed:
            # Save preprocessing result
            cv2.imwrite(f"below_{idx}_{prep_name}.jpg", prep_img)

            for config_name, config in configs:
                text = ocr_image(prep_img, config)
                if text and len(text) > 2:
                    # Simple scoring: longer text with letters gets higher score
                    letter_count = sum(c.isalpha() for c in text)
                    digit_count = sum(c.isdigit() for c in text)
                    score = letter_count * 2 - digit_count * 0.5 + len(text) * 0.1

                    if score > best_score:
                        best_score = score
                        best_text = text

                    print(f"    {prep_name}/{config_name}: {text[:60]}")

        if best_text:
            print(f"  Best text: {best_text[:80]}")
        else:
            print("  No text found")

if __name__ == "__main__":
    main()
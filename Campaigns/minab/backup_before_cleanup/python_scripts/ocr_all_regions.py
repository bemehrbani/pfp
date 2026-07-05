#!/usr/bin/env python3
"""OCR on all regions with multiple configurations."""

import cv2
import numpy as np
import pytesseract
import os

def preprocess_image(img):
    """Multiple preprocessing pipelines."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    pipelines = []

    # 1. Simple Otsu
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    pipelines.append(("otsu", otsu))

    # 2. Adaptive Gaussian
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)
    pipelines.append(("adaptive", adaptive))

    # 3. Enhanced + Otsu
    enhanced = cv2.convertScaleAbs(gray, alpha=2.0, beta=0)
    _, enhanced_otsu = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    pipelines.append(("enhanced_otsu", enhanced_otsu))

    # 4. Denoising
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    _, denoised_otsu = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    pipelines.append(("denoised_otsu", denoised_otsu))

    # 5. Morphological closing (for broken text)
    kernel = np.ones((2,2), np.uint8)
    closed = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel)
    pipelines.append(("closed", closed))

    return pipelines

def ocr_with_configs(image, configs):
    """Run OCR with multiple configurations."""
    results = {}
    for config_name, config in configs:
        try:
            text = pytesseract.image_to_string(image, config=config)
            text = text.strip()
            if text:
                results[config_name] = text
        except Exception as e:
            results[config_name] = f"ERROR: {e}"
    return results

def main():
    child_dir = "final_children"
    files = sorted([f for f in os.listdir(child_dir) if f.startswith("child_") and f.endswith(".jpg")])

    # OCR configurations to try
    configs = [
        ("psm7_fas", "--psm 7 -l fas"),
        ("psm8_fas", "--psm 8 -l fas"),
        ("psm6_fas", "--psm 6 -l fas"),
        ("psm7_ara", "--psm 7 -l ara"),
        ("psm8_ara", "--psm 8 -l ara"),
        ("psm6_ara", "--psm 6 -l ara"),
        ("psm7_fas+ara", "--psm 7 -l fas+ara"),
        ("psm8_fas+ara", "--psm 8 -l fas+ara"),
        ("psm7_fas+ara+eng", "--psm 7 -l fas+ara+eng"),
        ("psm8_fas+ara+eng", "--psm 8 -l fas+ara+eng"),
        ("psm13", "--psm 13"),  # Raw line
        ("psm10", "--psm 10"),  # Single character
    ]

    # Define regions to check (y_start, y_end, x_start, x_end, name)
    regions = [
        (0.7, 1.0, 0.0, 1.0, "bottom_30"),
        (0.8, 1.0, 0.0, 1.0, "bottom_20"),
        (0.9, 1.0, 0.0, 1.0, "bottom_10"),
        (0.0, 0.2, 0.0, 1.0, "top_20"),
        (0.0, 0.1, 0.0, 1.0, "top_10"),
        (0.0, 1.0, 0.0, 0.3, "left_side"),
        (0.0, 1.0, 0.7, 1.0, "right_side"),
        (0.8, 1.0, 0.3, 0.7, "center_bottom"),
    ]

    output_file = "ocr_results.txt"
    with open(output_file, "w", encoding="utf-8") as f_out:
        for fname in files[:10]:  # Try first 10
            path = os.path.join(child_dir, fname)
            img = cv2.imread(path)
            if img is None:
                continue

            height, width = img.shape[:2]
            f_out.write(f"\n{'='*60}\n")
            f_out.write(f"File: {fname} ({width}x{height})\n")
            f_out.write(f"{'='*60}\n")

            print(f"Processing {fname}...")

            for y_start, y_end, x_start, x_end, region_name in regions:
                y1 = int(height * y_start)
                y2 = int(height * y_end)
                x1 = int(width * x_start)
                x2 = int(width * x_end)

                if y2 - y1 <= 10 or x2 - x1 <= 10:
                    continue

                region = img[y1:y2, x1:x2]

                # Skip if region is too small
                if region.size == 0:
                    continue

                f_out.write(f"\n--- Region: {region_name} ({x1},{y1})-({x2},{y2}) {x2-x1}x{y2-y1} ---\n")

                # Preprocess
                pipelines = preprocess_image(region)

                for prep_name, preprocessed in pipelines:
                    # Save debug image
                    debug_name = f"ocr_{fname[:-4]}_{region_name}_{prep_name}.jpg"
                    cv2.imwrite(debug_name, preprocessed)

                    # OCR
                    results = ocr_with_configs(preprocessed, configs)

                    if results:
                        f_out.write(f"  Preprocessing: {prep_name}\n")
                        for config_name, text in results.items():
                            if text and not text.startswith("ERROR"):
                                f_out.write(f"    {config_name}: {text}\n")
                        f_out.write("\n")

    print(f"\nOCR results saved to {output_file}")
    print(f"Debug images saved as ocr_*.jpg")

if __name__ == "__main__":
    main()
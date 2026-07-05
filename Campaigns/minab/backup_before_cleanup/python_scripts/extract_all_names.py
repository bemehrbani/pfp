#!/usr/bin/env python3
"""Extract names from all borders using optimized OCR configuration."""

import cv2
import numpy as np
import pytesseract
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

def preprocess_for_ocr(image, method='adaptive'):
    """Preprocess image for OCR."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    if method == 'otsu':
        _, processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method == 'otsu_inv':
        _, processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    elif method == 'adaptive':
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 11, 2)
    elif method == 'adaptive_inv':
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 11, 2)
    else:
        processed = gray

    return processed

def ocr_with_configs(image):
    """OCR image with multiple configurations, return best results."""
    configs = [
        # English configs (for Latin names)
        ("eng", "--psm 7 -l eng"),
        ("eng6", "--psm 6 -l eng"),
        # Arabic configs (for Arabic/Farsi names)
        ("ara7", "--psm 7 -l ara"),
        ("ara6", "--psm 6 -l ara"),
        ("fas+ara7", "--psm 7 -l fas+ara"),
        ("fas+ara6", "--psm 6 -l fas+ara"),
    ]

    results = []
    for config_name, config in configs:
        try:
            text = pytesseract.image_to_string(image, config=config)
            text = text.strip()
            if text and len(text) > 1:
                # Simple scoring
                letter_count = sum(c.isalpha() for c in text)
                digit_count = sum(c.isdigit() for c in text)
                space_count = text.count(' ')
                # Penalize excessive digits unless it's a date
                score = letter_count * 2 + space_count * 0.5 - digit_count * 0.5 + len(text) * 0.1
                results.append((score, text, config_name))
        except Exception as e:
            pass

    # Sort by score descending
    results.sort(key=lambda x: x[0], reverse=True)
    return results

def is_likely_name(text):
    """Improved name detection for both Latin and Arabic/Persian names."""
    if not text:
        return False

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Check length
    if len(text) < 3 or len(text) > 50:
        return False

    # Check for excessive numbers (more than 30% digits)
    digit_count = sum(c.isdigit() for c in text)
    if digit_count > len(text) * 0.3:
        return False

    # Check for letters
    has_letters = any(c.isalpha() for c in text)
    if not has_letters:
        return False

    # Check for Arabic/Persian letters
    arabic_persian_range = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
    import re
    has_arabic_persian = bool(re.search(arabic_persian_range, text))

    # Check for Latin letters
    has_latin = bool(re.search(r'[A-Za-z]', text))

    # Must have either Latin or Arabic/Persian letters
    if not (has_latin or has_arabic_persian):
        return False

    # For Latin names: check capitalization pattern
    if has_latin and not has_arabic_persian:
        words = text.split()
        if len(words) > 4:  # Too many words for a name
            return False
        # At least one word should start with capital
        capital_words = sum(1 for w in words if w and w[0].isupper())
        if capital_words == 0:
            return False

    # For Arabic/Persian names: check character count
    if has_arabic_persian:
        # Typically 2-20 characters per word
        words = text.split()
        for w in words:
            if len(w) > 25:  # Too long for a name
                return False

    return True

def main():
    img = load_image()
    height, width = img.shape[:2]
    print(f"Image size: {width}x{height}")

    # Read coordinates
    coords_file = "children_with_names/coordinates.txt"
    with open(coords_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) < 2:
        print("No coordinates found")
        return

    # Create output directory
    output_dir = "extracted_names"
    os.makedirs(output_dir, exist_ok=True)

    # Process each border
    all_results = []
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue

        idx = parts[0]
        x = int(parts[1])
        y = int(parts[2])
        w = int(parts[3])
        h = int(parts[4])

        print(f"\nProcessing index {idx}...")

        # Extract region 200-400 pixels below border
        below_start = min(height-1, y + h)
        below_end = min(height-1, below_start + 400)
        below_region = img[below_start:below_end, x:x+w]

        if below_region.size == 0:
            print(f"  No below region for index {idx}")
            all_results.append((idx, "", "no_region"))
            continue

        # Save region for reference
        cv2.imwrite(f"{output_dir}/below_{idx}.jpg", below_region)

        # Try multiple preprocessing methods
        best_overall = None
        best_score = -1000

        for prep_method in ['adaptive', 'adaptive_inv', 'otsu', 'otsu_inv']:
            preprocessed = preprocess_for_ocr(below_region, prep_method)
            cv2.imwrite(f"{output_dir}/below_{idx}_{prep_method}.jpg", preprocessed)

            # OCR with configs
            results = ocr_with_configs(preprocessed)
            if results:
                score, text, config_name = results[0]
                if score > best_score:
                    best_score = score
                    best_overall = (text, prep_method, config_name)

                # Print top 1 result for this preprocessing
                print(f"  {prep_method}: {results[0][1][:40]} ({results[0][2]})")

        if best_overall:
            best_text, best_method, best_config = best_overall
            print(f"  Best: '{best_text}' ({best_method}/{best_config})")

            # Check if it looks like a name
            if is_likely_name(best_text):
                print(f"  ✓ Likely name!")
                all_results.append((idx, best_text, "name"))
            else:
                print(f"  ✗ Not a name pattern")
                all_results.append((idx, best_text, "not_name"))
        else:
            print(f"  No text found")
            all_results.append((idx, "", "no_text"))

    # Save all results
    with open(f"{output_dir}/all_extracted.txt", "w", encoding="utf-8") as f:
        f.write("index\ttext\tstatus\n")
        for idx, text, status in all_results:
            f.write(f"{idx}\t{text}\t{status}\n")

    # Count statistics
    names = [r for r in all_results if r[2] == "name"]
    not_names = [r for r in all_results if r[2] == "not_name"]
    no_text = [r for r in all_results if r[2] in ["no_text", "no_region"]]

    print(f"\n=== Summary ===")
    print(f"Total borders: {len(all_results)}")
    print(f"Likely names: {len(names)}")
    print(f"Not names: {len(not_names)}")
    print(f"No text: {len(no_text)}")

    print(f"\n=== Likely Names ===")
    for idx, text, status in names:
        print(f"{idx}: {text}")

    print(f"\n=== Not Names (but has text) ===")
    for idx, text, status in not_names[:20]:  # First 20
        print(f"{idx}: {text}")

if __name__ == "__main__":
    main()
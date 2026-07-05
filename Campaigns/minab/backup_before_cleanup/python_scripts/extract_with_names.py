#!/usr/bin/env python3
"""Extract child photos with names by including area below red borders."""

import os
import sys
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Increase PIL image pixel limit
Image.MAX_IMAGE_PIXELS = None

def load_image_opencv(path):
    """Load image using OpenCV, convert to RGB."""
    # OpenCV reads as BGR
    img_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        # Try using PIL as fallback
        pil_img = Image.open(path)
        if pil_img.mode == 'CMYK':
            pil_img = pil_img.convert('RGB')
        img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return img_bgr

def create_red_mask(img_bgr):
    """Create mask for red borders using HSV color space."""
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Define red color ranges in HSV
    # Red wraps around 0, so we need two ranges
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Morphological operations to close gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    closed = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    return closed

def find_border_contours(mask, min_area=5000, max_area=500000):
    """Find contours of red borders."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area or area > max_area:
            continue
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(cnt)
        # Aspect ratio filter (portrait photos)
        aspect = h / w
        if aspect < 0.5 or aspect > 3.0:
            continue
        filtered.append((cnt, (x, y, w, h)))

    # Sort by y then x
    filtered.sort(key=lambda item: (item[1][1], item[1][0]))
    return filtered

def extract_text_from_bottom_region(img_bgr, rect, extra_bottom=100):
    """Extract text from bottom region of expanded rectangle."""
    x, y, w, h = rect

    # Expand downward to include potential name below the border
    y_expanded = y
    h_expanded = h + extra_bottom

    # Make sure we don't go beyond image bounds
    img_height = img_bgr.shape[0]
    if y_expanded + h_expanded > img_height:
        h_expanded = img_height - y_expanded

    # Extract the bottom part (last extra_bottom pixels or so)
    bottom_start = y + h  # Start at bottom of original rectangle
    bottom_end = min(y + h + extra_bottom, img_height)

    if bottom_end <= bottom_start:
        return ""

    bottom_region = img_bgr[bottom_start:bottom_end, x:x+w]

    if bottom_region.size == 0:
        return ""

    # Convert to grayscale
    gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)

    # Multiple preprocessing attempts
    results = []

    # Try different preprocessing methods
    methods = [
        ("otsu", lambda g: cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
        ("adaptive", lambda g: cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                    cv2.THRESH_BINARY, 11, 2)),
        ("enhanced_otsu", lambda g: cv2.threshold(cv2.convertScaleAbs(g, alpha=2.0, beta=0),
                                                  0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
    ]

    # OCR configurations
    configs = [
        ("fas", "--psm 7 -l fas"),
        ("ara", "--psm 7 -l ara"),
        ("fas+ara", "--psm 7 -l fas+ara"),
        ("fas+ara+eng", "--psm 7 -l fas+ara+eng"),
        ("psm6_fas", "--psm 6 -l fas"),
        ("psm8_fas", "--psm 8 -l fas"),
    ]

    for method_name, preprocess_func in methods:
        preprocessed = preprocess_func(gray)

        for config_name, config in configs:
            try:
                text = pytesseract.image_to_string(preprocessed, config=config)
                text = text.strip()
                if text and len(text) > 1:  # At least 2 characters
                    # Clean text: keep Persian/Arabic letters, spaces, numbers
                    import re
                    cleaned = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u0041-\u005A\u0061-\u007A\u0030-\u0039\s]', '', text)
                    cleaned = cleaned.strip()
                    if cleaned:
                        results.append((method_name, config_name, cleaned))
            except:
                pass

    # Return the most common result or first result
    if results:
        # Group by text
        from collections import Counter
        text_counter = Counter([text for _, _, text in results])
        most_common = text_counter.most_common(1)[0][0]
        return most_common

    return ""

def main():
    input_path = "final-minab--01_scmx.jpg"
    output_dir = "children_with_names"
    os.makedirs(output_dir, exist_ok=True)

    print("Loading image...")
    img_bgr = load_image_opencv(input_path)
    if img_bgr is None:
        print("Failed to load image.")
        sys.exit(1)

    original_height, original_width = img_bgr.shape[:2]
    print(f"Image size: {original_width}x{original_height}")

    # Downscale for processing (max dimension 2000)
    max_dim = 2000
    scale = min(max_dim / original_width, max_dim / original_height)
    if scale < 1:
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        print(f"Downscaling to {new_width}x{new_height}")
        img_small = cv2.resize(img_bgr, (new_width, new_height), interpolation=cv2.INTER_AREA)
    else:
        img_small = img_bgr
        scale = 1.0

    print("Creating red mask...")
    mask = create_red_mask(img_small)
    print(f"Red mask pixels: {np.sum(mask > 0)}")

    print("Finding contours...")
    contours = find_border_contours(mask, min_area=1000, max_area=200000)
    print(f"Found {len(contours)} candidate border contours")

    if len(contours) == 0:
        print("No contours found. Try adjusting parameters.")
        sys.exit(1)

    # Scale bounding boxes back to original coordinates
    inv_scale = 1.0 / scale

    # Load original image via PIL for cropping (better quality)
    pil_img = Image.open(input_path)
    if pil_img.mode == 'CMYK':
        pil_img = pil_img.convert('RGB')

    # Save coordinates and names
    coordinates_file = os.path.join(output_dir, "coordinates.txt")
    with open(coordinates_file, "w", encoding="utf-8") as f:
        f.write("index\tx\ty\tw\th\tname\tfilename\n")

    for idx, (cnt, rect) in enumerate(contours):
        x, y, w, h = rect
        # Scale up
        x = int(x * inv_scale)
        y = int(y * inv_scale)
        w = int(w * inv_scale)
        h = int(h * inv_scale)

        # Try to extract name from area below the border
        child_name = ""
        extra_bottom = int(150 * inv_scale)  # Look 150 pixels below border

        # Convert region to OpenCV for OCR
        region_cv = img_bgr[y:y+h+extra_bottom, x:x+w] if y+h+extra_bottom <= img_bgr.shape[0] else img_bgr[y:, x:x+w]
        if region_cv.size > 0:
            child_name = extract_text_from_bottom_region(img_bgr, (x, y, w, h), extra_bottom)

        # Crop the actual child photo (inside border, like before)
        border_thickness = int(20 * inv_scale)
        x_inner = x + border_thickness
        y_inner = y + border_thickness
        w_inner = w - 2 * border_thickness
        h_inner = h - 2 * border_thickness

        if w_inner <= 0 or h_inner <= 0:
            x_inner, y_inner, w_inner, h_inner = x, y, w, h

        # Crop region from original image
        region = pil_img.crop((x_inner, y_inner, x_inner + w_inner, y_inner + h_inner))

        # Create filename based on extracted name or use index
        if child_name and len(child_name) > 1:
            # Sanitize filename
            safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in child_name)
            safe_name = safe_name.strip().replace(' ', '_')
            if safe_name:
                filename = f"{safe_name}_{idx:03d}.jpg"
            else:
                filename = f"child_{idx:03d}.jpg"
        else:
            filename = f"child_{idx:03d}.jpg"

        # Save
        output_path = os.path.join(output_dir, filename)
        region.save(output_path, quality=95)

        # Write coordinates
        with open(coordinates_file, "a", encoding="utf-8") as f:
            f.write(f"{idx}\t{x}\t{y}\t{w}\t{h}\t{child_name}\t{filename}\n")

        print(f"Saved {filename} ({w_inner}x{h_inner}) - Name: '{child_name}'")

    print(f"\nProcessed {len(contours)} regions.")
    print(f"Output directory: {output_dir}")
    print(f"Coordinates saved to: {coordinates_file}")

if __name__ == "__main__":
    main()
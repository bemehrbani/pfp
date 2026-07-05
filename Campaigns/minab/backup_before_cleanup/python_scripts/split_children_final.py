#!/usr/bin/env python3
"""
Split child photos using red borders with OpenCV contour detection.
Optionally extract child names via OCR.
"""

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

def extract_text_from_region(img_bgr, rect):
    """Extract text using OCR from region."""
    x, y, w, h = rect
    # Add padding to avoid border
    pad = 20
    x1 = max(0, x + pad)
    y1 = max(0, y + pad)
    x2 = min(img_bgr.shape[1], x + w - pad)
    y2 = min(img_bgr.shape[0], y + h - pad)

    region = img_bgr[y1:y2, x1:x2]
    if region.size == 0:
        return ""

    # Convert to grayscale
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Use pytesseract
    try:
        text = pytesseract.image_to_string(thresh, config='--psm 6')
        text = text.strip()
        return text
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

def main():
    input_path = "final-minab--01_scmx.jpg"
    output_dir = "splitted_final"
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

    # Save mask for debugging
    cv2.imwrite(os.path.join(output_dir, "red_mask_final.png"), mask)

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

    for idx, (cnt, rect) in enumerate(contours):
        x, y, w, h = rect
        # Scale up
        x = int(x * inv_scale)
        y = int(y * inv_scale)
        w = int(w * inv_scale)
        h = int(h * inv_scale)

        # Expand slightly to include border? Actually we want inside border
        # Shrink by estimated border thickness (e.g., 20 pixels)
        border_thickness = int(20 * inv_scale)
        x_inner = x + border_thickness
        y_inner = y + border_thickness
        w_inner = w - 2 * border_thickness
        h_inner = h - 2 * border_thickness

        if w_inner <= 0 or h_inner <= 0:
            x_inner, y_inner, w_inner, h_inner = x, y, w, h

        # Crop region from original image
        region = pil_img.crop((x_inner, y_inner, x_inner + w_inner, y_inner + h_inner))

        # Try OCR to get child name
        child_name = ""
        if w_inner > 100 and h_inner > 100:
            # Convert region to OpenCV for OCR
            region_cv = cv2.cvtColor(np.array(region), cv2.COLOR_RGB2BGR)
            child_name = extract_text_from_region(region_cv, (0, 0, w_inner, h_inner))

        # Sanitize filename
        if child_name:
            # Keep only alphanumeric and spaces
            safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in child_name)
            safe_name = safe_name.strip()
            if len(safe_name) > 0:
                filename = f"{safe_name}_{idx:03d}.jpg"
            else:
                filename = f"child_{idx:03d}.jpg"
        else:
            filename = f"child_{idx:03d}.jpg"

        # Save
        output_path = os.path.join(output_dir, filename)
        region.save(output_path, quality=95)
        print(f"Saved {filename} ({w_inner}x{h_inner})")

    print(f"\nProcessed {len(contours)} regions.")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()
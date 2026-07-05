#!/usr/bin/env python3
"""Detect text regions in image using OpenCV MSER."""

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

def detect_text_regions(img):
    """Detect text regions using MSER."""
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Create MSER detector
    mser = cv2.MSER_create()

    # Detect regions
    regions, _ = mser.detectRegions(gray)

    # Convert regions to bounding boxes
    boxes = []
    for region in regions:
        x, y, w, h = cv2.boundingRect(region.reshape(-1, 1, 2))

        # Filter by size
        if w < 20 or h < 10:  # Too small for text
            continue
        if w > 500 or h > 200:  # Too large for text
            continue
        if w / h > 10 or h / w > 5:  # Wrong aspect ratio
            continue

        boxes.append((x, y, w, h))

    # Merge overlapping boxes
    if boxes:
        boxes = merge_boxes(boxes)

    return boxes

def merge_boxes(boxes):
    """Merge overlapping bounding boxes."""
    if not boxes:
        return []

    # Convert to list of [x, y, w, h]
    boxes = [list(b) for b in boxes]

    # Sort by x coordinate
    boxes.sort(key=lambda b: b[0])

    merged = []
    current = boxes[0]

    for box in boxes[1:]:
        x1, y1, w1, h1 = current
        x2, y2, w2, h2 = box

        # Check overlap
        x_overlap = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
        y_overlap = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))

        if x_overlap > 0 and y_overlap > 0:
            # Merge
            new_x = min(x1, x2)
            new_y = min(y1, y2)
            new_w = max(x1 + w1, x2 + w2) - new_x
            new_h = max(y1 + h1, y2 + h2) - new_y
            current = [new_x, new_y, new_w, new_h]
        else:
            merged.append(current)
            current = box

    merged.append(current)
    return merged

def extract_text_from_boxes(img, boxes):
    """Extract text from detected regions."""
    import pytesseract

    text_regions = []

    for i, (x, y, w, h) in enumerate(boxes):
        # Extract region
        region = img[y:y+h, x:x+w]

        if region.size == 0:
            continue

        # Preprocess
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Try OCR with multiple configs
        configs = [
            "--psm 7 -l eng",
            "--psm 7 -l fas",
            "--psm 6 -l eng",
            "--psm 6 -l fas",
        ]

        best_text = ""
        for config in configs:
            try:
                text = pytesseract.image_to_string(thresh, config=config)
                text = text.strip()
                if text and len(text) > len(best_text):
                    best_text = text
            except:
                pass

        if best_text and len(best_text) > 1:
            text_regions.append((x, y, w, h, best_text))

    return text_regions

def main():
    print("Loading image...")
    img = load_image()
    height, width = img.shape[:2]
    print(f"Image size: {width}x{height}")

    # Downscale for faster processing
    scale = 0.25
    new_width = int(width * scale)
    new_height = int(height * scale)
    img_small = cv2.resize(img, (new_width, new_height))

    print("Detecting text regions...")
    boxes = detect_text_regions(img_small)

    # Scale boxes back up
    boxes = [(int(x/scale), int(y/scale), int(w/scale), int(h/scale))
             for (x, y, w, h) in boxes]

    print(f"Found {len(boxes)} text regions")

    # Extract text from a sample of boxes (first 20)
    sample = boxes[:20]
    print(f"\nExtracting text from {len(sample)} regions...")

    text_regions = extract_text_from_boxes(img, sample)

    print(f"\n=== Text Found ===")
    for i, (x, y, w, h, text) in enumerate(text_regions):
        print(f"Region {i}: ({x},{y},{w},{h}): {text}")

    # Save visualizations
    vis = img.copy()
    for x, y, w, h, text in text_regions:
        cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 255, 0), 3)
        # Put text
        cv2.putText(vis, f"{text[:20]}...", (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imwrite("text_detection.jpg", vis)
    print(f"\nVisualization saved to text_detection.jpg")

    # Also save individual text regions
    os.makedirs("text_regions", exist_ok=True)
    for i, (x, y, w, h, text) in enumerate(text_regions):
        region = img[y:y+h, x:x+w]
        if region.size > 0:
            # Clean text for filename
            safe_text = "".join(c if c.isalnum() else "_" for c in text)[:30]
            filename = f"text_regions/region_{i}_{safe_text}.jpg"
            cv2.imwrite(filename, region)

    print(f"Individual regions saved to text_regions/")

if __name__ == "__main__":
    main()
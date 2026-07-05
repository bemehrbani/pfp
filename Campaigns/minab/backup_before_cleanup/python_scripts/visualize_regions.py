#!/usr/bin/env python3
"""Visualize text search regions for debugging."""

import cv2
import numpy as np
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

    # Create visualization image (downscaled for display)
    scale = 0.1
    small_width = int(width * scale)
    small_height = int(height * scale)
    vis = cv2.resize(img, (small_width, small_height))

    # Draw regions for first 5 borders
    for i, line in enumerate(lines[1:6]):
        parts = line.strip().split('\t')
        if len(parts) < 4:
            continue

        idx = parts[0]
        x = int(parts[1])
        y = int(parts[2])
        w = int(parts[3])
        h = int(parts[4])

        # Scale coordinates
        sx = int(x * scale)
        sy = int(y * scale)
        sw = int(w * scale)
        sh = int(h * scale)

        # Draw border rectangle (red)
        cv2.rectangle(vis, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)

        # Draw region 200 pixels below (green)
        below_y = min(height-1, y + h)
        below_h = 200
        sb_y = int(below_y * scale)
        sb_h = int(below_h * scale)
        cv2.rectangle(vis, (sx, sb_y), (sx+sw, sb_y+sb_h), (0, 255, 0), 1)

        # Draw region 400 pixels below (blue)
        below_h2 = 400
        sb_y2 = int(below_y * scale)
        sb_h2 = int(below_h2 * scale)
        cv2.rectangle(vis, (sx, sb_y2), (sx+sw, sb_y2+sb_h2), (255, 0, 0), 1)

        # Put index
        cv2.putText(vis, str(idx), (sx, sy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Save visualization
    cv2.imwrite("regions_visualization.jpg", vis)
    print("Saved regions_visualization.jpg")

    # Also create close-up for index 97 (Hami Sadeghi)
    # Find index 97
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) < 4:
            continue
        idx = parts[0]
        if idx == "97":
            x = int(parts[1])
            y = int(parts[2])
            w = int(parts[3])
            h = int(parts[4])

            # Extract border region and below region
            border = img[y:y+h, x:x+w]
            below_start = min(height-1, y+h)
            below_end = min(height-1, below_start + 400)
            below = img[below_start:below_end, x:x+w]

            # Save
            cv2.imwrite("border_97.jpg", border)
            cv2.imwrite("below_97.jpg", below)
            print(f"Saved border_97.jpg ({w}x{h}) and below_97.jpg ({w}x{below_end-below_start})")
            break

if __name__ == "__main__":
    main()
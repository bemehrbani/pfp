#!/usr/bin/env python3
"""
Detect red borders in CMYK image and split into cells.
"""

import os
import sys
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = None

def is_red(c, m, y, k):
    """Check if CMYK pixel is red."""
    return c < 60 and m > 180 and y > 180 and k < 60

def detect_lines(image):
    """Detect vertical and horizontal red lines.
    Returns (vertical_positions, horizontal_positions)
    """
    width, height = image.size
    pix = image.load()  # pixel access object

    # Sample step
    step = 100

    # Count red pixels per column (sampled rows)
    col_red_counts = np.zeros(width // step + 1, dtype=int)
    # Actually we need counts for each column index, but we can sample columns too.
    # Let's sample columns and rows.
    # We'll create arrays for column and row densities.
    col_density = np.zeros(width, dtype=int)
    row_density = np.zeros(height, dtype=int)

    # To make it faster, we'll sample rows and columns with step
    # and only increment where we find red.
    # We'll iterate over sampled rows and columns.
    print("Scanning for red pixels...")
    # Scan columns (vertical lines)
    for x in range(0, width, step):
        if x % 1000 == 0:
            print(f"  column {x}/{width}")
        for y in range(0, height, step):
            c, m, yc, k = pix[x, y]
            if is_red(c, m, yc, k):
                col_density[x] += 1
                row_density[y] += 1

    # Find columns with high red density (peaks)
    # Use threshold: at least 5 red pixels in sampled rows
    col_threshold = 5
    col_candidates = np.where(col_density >= col_threshold)[0]
    print(f"Column candidates: {len(col_candidates)}")

    # Group consecutive columns
    vertical_groups = []
    if len(col_candidates) > 0:
        current = [col_candidates[0]]
        for col in col_candidates[1:]:
            if col == current[-1] + step:  # since we sampled with step, consecutive indices may be step apart
                current.append(col)
            else:
                vertical_groups.append(current)
                current = [col]
        vertical_groups.append(current)

    vertical_positions = [int(np.median(group)) for group in vertical_groups]

    # Find rows with high red density
    row_threshold = 5
    row_candidates = np.where(row_density >= row_threshold)[0]
    print(f"Row candidates: {len(row_candidates)}")

    horizontal_groups = []
    if len(row_candidates) > 0:
        current = [row_candidates[0]]
        for row in row_candidates[1:]:
            if row == current[-1] + step:
                current.append(row)
            else:
                horizontal_groups.append(current)
                current = [row]
        horizontal_groups.append(current)

    horizontal_positions = [int(np.median(group)) for group in horizontal_groups]

    return vertical_positions, horizontal_positions

def split_image(image, vertical_pos, horizontal_pos, output_dir):
    """Split image into cells based on line positions."""
    width, height = image.size
    v_bounds = [0] + sorted(vertical_pos) + [width]
    h_bounds = [0] + sorted(horizontal_pos) + [height]

    cell_count = 0
    for i in range(len(v_bounds) - 1):
        for j in range(len(h_bounds) - 1):
            left = v_bounds[i]
            right = v_bounds[i + 1]
            top = h_bounds[j]
            bottom = h_bounds[j + 1]

            cell_width = right - left
            cell_height = bottom - top
            if cell_width < 50 or cell_height < 50:
                continue

            cell_img = image.crop((left, top, right, bottom))
            # Save as JPEG
            cell_img.save(os.path.join(output_dir, f"cell_{cell_count:03d}.jpg"))
            print(f"Saved cell {cell_count}: {cell_width}x{cell_height}")
            cell_count += 1

    return cell_count

def main():
    input_path = "final-minab--01_scmx.jpg"
    output_dir = "splitted_photos"

    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading {input_path}...")
    img = Image.open(input_path)
    print(f"Image mode: {img.mode}, size: {img.size}")

    # Ensure CMYK
    if img.mode != "CMYK":
        img = img.convert("CMYK")

    vertical, horizontal = detect_lines(img)
    print(f"Vertical lines at: {vertical}")
    print(f"Horizontal lines at: {horizontal}")

    # If no lines detected, try different thresholds
    if len(vertical) == 0 and len(horizontal) == 0:
        print("No lines detected. Trying alternative detection...")
        # Fallback: assume grid of equal size? Not implemented.
        return

    # Split image
    count = split_image(img, vertical, horizontal, output_dir)
    print(f"\nSplit into {count} cells.")

    # Also save line positions for reference
    with open(os.path.join(output_dir, "lines.txt"), "w") as f:
        f.write(f"Vertical: {vertical}\n")
        f.write(f"Horizontal: {horizontal}\n")

if __name__ == "__main__":
    main()
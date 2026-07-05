#!/usr/bin/env python3
"""
Detect grid of red borders and split image into cells.
"""

import os
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None

def is_red_cmyk(c, m, y, k):
    """Check if CMYK pixel is red."""
    return (c < 70) & (m > 160) & (y > 160) & (k < 70)

def create_red_mask_cmyk(img_cmyk):
    """Create mask of red pixels from CMYK image."""
    width, height = img_cmyk.size
    # Convert to numpy array (height, width, 4)
    arr = np.array(img_cmyk)
    c = arr[:,:,0]
    m = arr[:,:,1]
    y = arr[:,:,2]
    k = arr[:,:,3]
    mask = is_red_cmyk(c, m, y, k)
    return mask

def find_lines(mask, min_length_ratio=0.1):
    """Find vertical and horizontal lines from red mask.
    Returns (vertical_positions, horizontal_positions)
    """
    height, width = mask.shape
    # Project onto axes
    col_sum = np.sum(mask, axis=0)  # shape (width,)
    row_sum = np.sum(mask, axis=1)  # shape (height,)

    # Threshold: line must have at least min_length_ratio of the dimension
    col_threshold = height * min_length_ratio
    row_threshold = width * min_length_ratio

    # Find columns that exceed threshold
    col_candidates = np.where(col_sum >= col_threshold)[0]
    row_candidates = np.where(row_sum >= row_threshold)[0]

    # Group consecutive candidates
    def group_consecutive(indices, max_gap=1):
        groups = []
        if len(indices) == 0:
            return groups
        current = [indices[0]]
        for idx in indices[1:]:
            if idx <= current[-1] + max_gap:
                current.append(idx)
            else:
                groups.append(current)
                current = [idx]
        groups.append(current)
        return groups

    col_groups = group_consecutive(col_candidates, max_gap=5)
    row_groups = group_consecutive(row_candidates, max_gap=5)

    # Compute median of each group as line position
    vertical = [int(np.median(g)) for g in col_groups]
    horizontal = [int(np.median(g)) for g in row_groups]

    # Filter lines that are too close (merge within 10 pixels)
    def merge_close(positions, threshold=10):
        if len(positions) == 0:
            return []
        positions = sorted(positions)
        merged = []
        current = positions[0]
        current_list = [current]
        for pos in positions[1:]:
            if pos - current <= threshold:
                current_list.append(pos)
            else:
                merged.append(int(np.median(current_list)))
                current_list = [pos]
            current = pos
        merged.append(int(np.median(current_list)))
        return merged

    vertical = merge_close(vertical, threshold=10)
    horizontal = merge_close(horizontal, threshold=10)

    return vertical, horizontal

def split_image(img, vertical, horizontal, output_dir, prefix="child"):
    """Split image into cells and save."""
    width, height = img.size
    v_bounds = [0] + sorted(vertical) + [width]
    h_bounds = [0] + sorted(horizontal) + [height]

    cell_count = 0
    for i in range(len(v_bounds) - 1):
        for j in range(len(h_bounds) - 1):
            left = v_bounds[i]
            right = v_bounds[i + 1]
            top = h_bounds[j]
            bottom = h_bounds[j + 1]

            cell_width = right - left
            cell_height = bottom - top
            # Skip cells that are too small (likely border thickness)
            if cell_width < 50 or cell_height < 50:
                continue

            cell = img.crop((left, top, right, bottom))
            # Save as JPEG
            cell.save(os.path.join(output_dir, f"{prefix}_{cell_count:03d}.jpg"))
            cell_count += 1

    return cell_count

def main():
    input_path = "final-minab--01_scmx.jpg"
    output_dir = "splitted_photos_grid"
    os.makedirs(output_dir, exist_ok=True)

    print("Loading image...")
    img = Image.open(input_path)
    print(f"Original size: {img.size}, mode: {img.mode}")

    # Work in CMYK for red detection
    if img.mode != "CMYK":
        img_cmyk = img.convert("CMYK")
    else:
        img_cmyk = img

    # Downscale for processing (max dimension 3000)
    max_dim = 3000
    scale_factor = min(max_dim / img_cmyk.size[0], max_dim / img_cmyk.size[1])
    if scale_factor < 1:
        new_size = (int(img_cmyk.size[0] * scale_factor), int(img_cmyk.size[1] * scale_factor))
        print(f"Downscaling to {new_size[0]}x{new_size[1]} (scale {scale_factor:.3f})")
        img_small = img_cmyk.resize(new_size, Image.Resampling.LANCZOS)
    else:
        img_small = img_cmyk
        scale_factor = 1.0

    print("Creating red mask...")
    mask = create_red_mask_cmyk(img_small)
    print(f"Red pixels: {np.sum(mask)}")

    # Save mask for debugging
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))
    mask_img.save(os.path.join(output_dir, "red_mask_grid.png"))

    # Find lines
    vertical, horizontal = find_lines(mask, min_length_ratio=0.05)
    print(f"Vertical lines: {len(vertical)} positions: {vertical}")
    print(f"Horizontal lines: {len(horizontal)} positions: {horizontal}")

    if len(vertical) == 0 and len(horizontal) == 0:
        print("No lines detected. Exiting.")
        return

    # Scale line positions back to original coordinates
    if scale_factor < 1:
        inv_scale = 1.0 / scale_factor
        vertical = [int(v * inv_scale) for v in vertical]
        horizontal = [int(h * inv_scale) for h in horizontal]

    # Split original image (RGB)
    img_rgb = img.convert("RGB")
    count = split_image(img_rgb, vertical, horizontal, output_dir, prefix="child")
    print(f"Split into {count} cells.")

    # Save grid info
    with open(os.path.join(output_dir, "grid_info.txt"), "w") as f:
        f.write(f"Vertical lines: {vertical}\n")
        f.write(f"Horizontal lines: {horizontal}\n")
        f.write(f"Cell count: {count}\n")

if __name__ == "__main__":
    main()
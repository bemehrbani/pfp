#!/usr/bin/env python3
"""
Split final-minab--01_scmx.jpg into individual child photos using red borders.
Save each photo in splitted_photos folder with child's name.
"""

import os
import sys
from PIL import Image
import numpy as np

# Increase PIL image pixel limit to handle large image
Image.MAX_IMAGE_PIXELS = None

def main():
    # Paths
    input_image = "final-minab--01_scmx.jpg"
    output_dir = "splitted_photos"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load image
    if not os.path.exists(input_image):
        print(f"Error: Input image '{input_image}' not found.")
        sys.exit(1)

    print(f"Loading image: {input_image}")
    img = Image.open(input_image)
    width, height = img.size
    print(f"Image size: {width}x{height}")

    # Convert to RGB array
    img_rgb = img.convert("RGB")
    pixels = np.array(img_rgb)

    # Define red color range (RGB)
    # Red borders likely pure red: (255, 0, 0) or similar
    # We'll look for pixels where R > 200, G < 50, B < 50
    red_threshold = 200
    green_blue_threshold = 50

    # Create a mask of red pixels
    red_mask = (pixels[:, :, 0] > red_threshold) & \
               (pixels[:, :, 1] < green_blue_threshold) & \
               (pixels[:, :, 2] < green_blue_threshold)

    print(f"Red pixels found: {np.sum(red_mask)}")

    # Find vertical and horizontal lines
    # Sum red pixels along columns and rows
    red_col_sums = np.sum(red_mask, axis=0)  # shape (width,)
    red_row_sums = np.sum(red_mask, axis=1)  # shape (height,)

    # Threshold to consider a column/row as border line
    line_threshold = height * 0.1  # at least 10% of height for vertical lines
    # Actually, red borders might be thin lines, not necessarily continuous across entire dimension.
    # Let's instead detect clusters of red pixels.

    # For simplicity, let's visualize the mask
    # Save red mask as image for debugging
    mask_img = Image.fromarray((red_mask * 255).astype(np.uint8))
    mask_img.save(os.path.join(output_dir, "red_mask.png"))
    print(f"Red mask saved to {output_dir}/red_mask.png")

    # Find connected components of red pixels to identify border rectangles
    from scipy import ndimage
    # Label connected components
    labeled_array, num_features = ndimage.label(red_mask)
    print(f"Number of red connected components: {num_features}")

    # For each component, get bounding box
    # But borders may be separate lines, not closed rectangles.
    # Instead, we can look for vertical and horizontal lines separately.

    # Project red pixels onto x and y axes
    # Find columns with significant red density
    col_density = red_col_sums / height
    # Threshold for vertical line
    vertical_lines = np.where(col_density > 0.05)[0]  # columns where >5% pixels are red
    print(f"Vertical line candidates at columns: {vertical_lines}")

    # Group consecutive columns
    vertical_groups = []
    if len(vertical_lines) > 0:
        current_group = [vertical_lines[0]]
        for col in vertical_lines[1:]:
            if col == current_group[-1] + 1:
                current_group.append(col)
            else:
                vertical_groups.append(current_group)
                current_group = [col]
        vertical_groups.append(current_group)

    print(f"Vertical line groups: {vertical_groups}")

    # Similarly for horizontal lines
    row_density = red_row_sums / width
    horizontal_lines = np.where(row_density > 0.05)[0]
    print(f"Horizontal line candidates at rows: {horizontal_lines}")

    horizontal_groups = []
    if len(horizontal_lines) > 0:
        current_group = [horizontal_lines[0]]
        for row in horizontal_lines[1:]:
            if row == current_group[-1] + 1:
                current_group.append(row)
            else:
                horizontal_groups.append(current_group)
                current_group = [row]
        horizontal_groups.append(current_group)

    print(f"Horizontal line groups: {horizontal_groups}")

    # Determine grid boundaries
    # Use median of each group as line position
    vertical_positions = [np.median(group).astype(int) for group in vertical_groups]
    horizontal_positions = [np.median(group).astype(int) for group in horizontal_groups]

    print(f"Vertical line positions: {vertical_positions}")
    print(f"Horizontal line positions: {horizontal_positions}")

    # Sort positions
    vertical_positions.sort()
    horizontal_positions.sort()

    # If we have a grid, we can split into cells
    # For now, let's just split along vertical lines if we have them
    # Actually, we need to extract regions between borders

    # If borders are lines, children photos are in cells between lines
    # We'll assume vertical lines divide columns, horizontal lines divide rows

    # Generate cell boundaries
    v_bounds = [0] + vertical_positions + [width]
    h_bounds = [0] + horizontal_positions + [height]

    print(f"Vertical boundaries: {v_bounds}")
    print(f"Horizontal boundaries: {h_bounds}")

    # Extract each cell
    cell_count = 0
    for i in range(len(v_bounds) - 1):
        for j in range(len(h_bounds) - 1):
            left = v_bounds[i]
            right = v_bounds[i + 1]
            top = h_bounds[j]
            bottom = h_bounds[j + 1]

            # Skip if cell too small (likely border thickness)
            cell_width = right - left
            cell_height = bottom - top
            if cell_width < 10 or cell_height < 10:
                continue

            # Crop cell
            cell_img = img.crop((left, top, right, bottom))

            # Save with sequential name for now
            # Later we can add OCR for child names
            cell_img.save(os.path.join(output_dir, f"child_{cell_count:03d}.jpg"))
            print(f"Saved cell {cell_count}: {left},{top}-{right},{bottom} ({cell_width}x{cell_height})")
            cell_count += 1

    print(f"\nTotal cells extracted: {cell_count}")
    print(f"Images saved to {output_dir}/")

if __name__ == "__main__":
    main()
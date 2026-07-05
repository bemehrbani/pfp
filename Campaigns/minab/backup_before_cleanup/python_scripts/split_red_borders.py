#!/usr/bin/env python3
"""
Split image using red borders by detecting red rectangles.
Uses downscaling for performance.
"""

import os
import sys
import numpy as np
from PIL import Image
from scipy import ndimage
import math

Image.MAX_IMAGE_PIXELS = None

def create_red_mask(img_rgb):
    """Create mask of red pixels from RGB image."""
    # Convert to numpy array
    arr = np.array(img_rgb, dtype=np.float32) / 255.0

    # Convert to HSV
    # Using simplified conversion
    # Source: https://en.wikipedia.org/wiki/HSL_and_HSV
    maxc = arr.max(axis=2)
    minc = arr.min(axis=2)
    diff = maxc - minc
    hue = np.zeros_like(maxc)
    sat = np.zeros_like(maxc)
    val = maxc

    # Avoid division by zero
    np.divide(diff, maxc, out=sat, where=maxc > 0)

    # Compute hue
    rc = np.where(maxc == arr[:,:,0], (arr[:,:,1] - arr[:,:,2]) / diff, 0)
    gc = np.where(maxc == arr[:,:,1], 2.0 + (arr[:,:,2] - arr[:,:,0]) / diff, 0)
    bc = np.where(maxc == arr[:,:,2], 4.0 + (arr[:,:,0] - arr[:,:,1]) / diff, 0)

    hue = (rc + gc + bc) / 6.0
    hue = hue % 1.0

    # Red hue: near 0 or near 1 (0-0.05 or 0.95-1.0)
    red_hue_mask = (hue < 0.05) | (hue > 0.95)
    # High saturation and value
    red_sat_mask = sat > 0.5
    red_val_mask = val > 0.3

    red_mask = red_hue_mask & red_sat_mask & red_val_mask

    # Also check for high R, low G, low B
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    rgb_red_mask = (r > 0.6) & (g < 0.4) & (b < 0.4)

    # Combine
    final_mask = red_mask | rgb_red_mask

    return final_mask

def find_border_rectangles(mask, min_area=1000):
    """Find rectangles formed by red borders.
    Returns list of (top, bottom, left, right) boundaries.
    """
    # Close gaps in mask
    closed = ndimage.binary_closing(mask, structure=np.ones((3,3)))
    # Fill holes
    filled = ndimage.binary_fill_holes(closed)

    # Label connected components
    labeled, num_features = ndimage.label(filled)
    print(f"Found {num_features} connected components")

    # Get bounding boxes
    slices = ndimage.find_objects(labeled)
    rectangles = []
    for i, slice_obj in enumerate(slices):
        rows, cols = slice_obj
        top, bottom = rows.start, rows.stop
        left, right = cols.start, cols.stop
        area = (bottom - top) * (right - left)
        if area >= min_area:
            rectangles.append((top, bottom, left, right))

    # Sort by top then left
    rectangles.sort(key=lambda x: (x[0], x[2]))
    return rectangles

def main():
    input_path = "final-minab--01_scmx.jpg"
    output_dir = "splitted_photos_v2"
    os.makedirs(output_dir, exist_ok=True)

    print("Loading image...")
    img = Image.open(input_path)
    print(f"Original size: {img.size}, mode: {img.mode}")

    # Convert to RGB if needed
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Downscale for processing (max dimension 2000)
    max_dim = 2000
    scale_factor = min(max_dim / img.size[0], max_dim / img.size[1])
    if scale_factor < 1:
        new_width = int(img.size[0] * scale_factor)
        new_height = int(img.size[1] * scale_factor)
        print(f"Downscaling to {new_width}x{new_height} (scale {scale_factor:.3f})")
        img_small = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    else:
        img_small = img
        scale_factor = 1.0

    print("Creating red mask...")
    mask = create_red_mask(img_small)
    print(f"Red pixels: {np.sum(mask)}")

    # Save mask for debugging
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))
    mask_img.save(os.path.join(output_dir, "red_mask_debug.png"))

    # Find rectangles
    rectangles = find_border_rectangles(mask, min_area=100)
    print(f"Found {len(rectangles)} rectangles")

    if len(rectangles) == 0:
        print("No rectangles found. Trying different thresholds.")
        return

    # Scale rectangles back to original coordinates
    if scale_factor < 1:
        inv_scale = 1.0 / scale_factor
        rectangles = [
            (
                int(top * inv_scale),
                int(bottom * inv_scale),
                int(left * inv_scale),
                int(right * inv_scale)
            )
            for (top, bottom, left, right) in rectangles
        ]

    # Extract each rectangle region from original image
    for idx, (top, bottom, left, right) in enumerate(rectangles):
        # Ensure within bounds
        top = max(0, top)
        left = max(0, left)
        bottom = min(img.size[1], bottom)
        right = min(img.size[0], right)

        width = right - left
        height = bottom - top
        if width < 50 or height < 50:
            continue

        print(f"Cropping rectangle {idx}: ({left},{top})-({right},{bottom}) {width}x{height}")
        region = img.crop((left, top, right, bottom))
        region.save(os.path.join(output_dir, f"child_{idx:03d}.jpg"))

    print(f"Saved {len(rectangles)} images to {output_dir}")

if __name__ == "__main__":
    main()
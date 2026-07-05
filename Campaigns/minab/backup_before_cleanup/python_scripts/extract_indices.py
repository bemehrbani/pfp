#!/usr/bin/env python3
"""Extract border index from filenames in children_with_names folder."""

import os
import re

def main():
    src_dir = "children_with_names"
    files = [f for f in os.listdir(src_dir) if f.lower().endswith('.jpg')]

    index_to_filename = {}

    for fname in files:
        # Try to extract index from filename
        # Pattern: something_###.jpg where ### is 3 digits
        match = re.search(r'_(\d{3})\.jpg$', fname)
        if match:
            idx = match.group(1).lstrip('0')
            if not idx:  # "000"
                idx = "0"
            index_to_filename[idx] = fname
            print(f"Filename {fname} -> index {idx}")
        else:
            print(f"Warning: Could not extract index from {fname}")

    print(f"\nFound {len(index_to_filename)} files with indices")

    # Check each file for dimensions
    valid_indices = []
    for idx, fname in sorted(index_to_filename.items(), key=lambda x: int(x[0])):
        path = os.path.join(src_dir, fname)
        try:
            from PIL import Image
            img = Image.open(path)
            w, h = img.size
            # Same filter as filter_children.py
            if 350 <= w <= 450 and 600 <= h <= 750:
                valid_indices.append(idx)
                print(f"Index {idx}: {fname} ({w}x{h}) - VALID")
            else:
                print(f"Index {idx}: {fname} ({w}x{h}) - INVALID (size mismatch)")
        except Exception as e:
            print(f"Error processing {fname}: {e}")

    print(f"\nValid indices (child photos): {len(valid_indices)}")
    print("Indices:", valid_indices)

    # Create mapping: border index -> child_final index (0-based)
    mapping = {}
    for child_idx, border_idx in enumerate(valid_indices):
        mapping[border_idx] = child_idx

    # Save mapping
    with open("border_to_child_mapping_fixed.txt", "w", encoding="utf-8") as f:
        f.write("border_index\tchild_index\n")
        for border_idx, child_idx in sorted(mapping.items(), key=lambda x: int(x[0])):
            f.write(f"{border_idx}\t{child_idx}\n")

    print("\nMapping saved to border_to_child_mapping_fixed.txt")

    # Also map child_index -> border_index
    reverse_mapping = {child_idx: border_idx for border_idx, child_idx in mapping.items()}
    with open("child_to_border_mapping_fixed.txt", "w", encoding="utf-8") as f:
        f.write("child_index\tborder_index\n")
        for child_idx, border_idx in sorted(reverse_mapping.items()):
            f.write(f"{child_idx}\t{border_idx}\n")

    print("Reverse mapping saved to child_to_border_mapping_fixed.txt")

if __name__ == "__main__":
    main()
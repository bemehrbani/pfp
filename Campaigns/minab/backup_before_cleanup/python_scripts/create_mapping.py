#!/usr/bin/env python3
"""Create mapping from border index to child_final index based on size filtering."""

import os
from PIL import Image

def main():
    # Directory with original split photos (with index in filename)
    src_dir = "children_with_names"

    # Read coordinates.txt to get index->filename mapping
    coords_file = "children_with_names/coordinates.txt"
    index_to_filename = {}

    with open(coords_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip header
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) < 6:
            continue
        idx = parts[0]
        filename = parts[5] if len(parts) > 5 else ""
        if filename:
            index_to_filename[idx] = filename

    print(f"Found {len(index_to_filename)} indices in coordinates.txt")

    # Check each file for dimensions
    valid_indices = []
    for idx, fname in sorted(index_to_filename.items(), key=lambda x: int(x[0])):
        path = os.path.join(src_dir, fname)
        if not os.path.exists(path):
            print(f"Warning: File {fname} not found for index {idx}")
            continue

        try:
            img = Image.open(path)
            w, h = img.size
            # Same filter as filter_children.py
            if 350 <= w <= 450 and 600 <= h <= 750:
                valid_indices.append(idx)
                print(f"Index {idx}: {fname} ({w}x{h}) - VALID")
            else:
                print(f"Index {idx}: {fname} ({w}x{h}) - INVALID")
        except Exception as e:
            print(f"Error processing {fname}: {e}")

    print(f"\nValid indices (child photos): {len(valid_indices)}")
    print("Indices:", valid_indices)

    # Create mapping: border index -> child_final index (0-based)
    mapping = {}
    for child_idx, border_idx in enumerate(valid_indices):
        mapping[border_idx] = child_idx

    # Save mapping
    with open("border_to_child_mapping.txt", "w", encoding="utf-8") as f:
        f.write("border_index\tchild_index\n")
        for border_idx, child_idx in sorted(mapping.items(), key=lambda x: int(x[0])):
            f.write(f"{border_idx}\t{child_idx}\n")

    print("\nMapping saved to border_to_child_mapping.txt")

    # Also map child_index -> border_index
    reverse_mapping = {child_idx: border_idx for border_idx, child_idx in mapping.items()}
    with open("child_to_border_mapping.txt", "w", encoding="utf-8") as f:
        f.write("child_index\tborder_index\n")
        for child_idx, border_idx in sorted(reverse_mapping.items()):
            f.write(f"{child_idx}\t{border_idx}\n")

    print("Reverse mapping saved to child_to_border_mapping.txt")

if __name__ == "__main__":
    main()
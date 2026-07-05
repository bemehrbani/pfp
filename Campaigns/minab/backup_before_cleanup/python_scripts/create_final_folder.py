#!/usr/bin/env python3
"""Create clean final folder with properly named child photos."""

import os
import shutil
import re

def main():
    # Read child to border mapping
    child_to_border = {}
    with open("child_to_border_mapping_fixed.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[1:]:
        if line.strip():
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                child_idx = int(parts[0])
                border_idx = parts[1]
                child_to_border[child_idx] = border_idx

    print(f"Loaded mapping for {len(child_to_border)} children")

    # Scan children_named for renamed files
    renamed_files = {}
    src_dir = "children_named"
    for fname in os.listdir(src_dir):
        if fname.lower().endswith('.jpg'):
            # Check if matches pattern *_{border_idx}.jpg
            match = re.search(r'_(\d{1,3})\.jpg$', fname)
            if match:
                border_idx = match.group(1)
                # Ensure it's a regular file (not symlink)
                path = os.path.join(src_dir, fname)
                if os.path.isfile(path) and not os.path.islink(path):
                    renamed_files[border_idx] = fname

    print(f"Found {len(renamed_files)} renamed files")

    # Create final folder
    dest_dir = "final_children_named"
    os.makedirs(dest_dir, exist_ok=True)

    # Process each child
    copied_count = 0
    renamed_count = 0
    numbered_count = 0

    for child_idx in range(100):
        border_idx = child_to_border.get(child_idx)

        # Determine source file
        src_path = None
        dest_name = None

        if border_idx and border_idx in renamed_files:
            # Use renamed file
            src_path = os.path.join("children_named", renamed_files[border_idx])
            dest_name = renamed_files[border_idx]
            renamed_count += 1
        else:
            # Use numbered file from final_output
            src_path = os.path.join("final_output", f"child_{child_idx+1:03d}.jpg")
            dest_name = f"child_{child_idx+1:03d}.jpg"
            numbered_count += 1

        if not os.path.exists(src_path):
            print(f"Warning: Source file not found: {src_path}")
            continue

        # Copy to destination
        dest_path = os.path.join(dest_dir, dest_name)
        shutil.copy2(src_path, dest_path)
        copied_count += 1

    print(f"\n=== Summary ===")
    print(f"Total children: 100")
    print(f"Renamed files used: {renamed_count}")
    print(f"Numbered files used: {numbered_count}")
    print(f"Copied to: {dest_dir}")

    # Create a mapping file
    mapping_path = os.path.join(dest_dir, "name_mapping.csv")
    with open(mapping_path, "w", encoding="utf-8") as f:
        f.write("child_index,border_index,filename,name_if_renamed\n")
        for child_idx in range(100):
            border_idx = child_to_border.get(child_idx, "")
            filename = f"child_{child_idx+1:03d}.jpg"
            name_if_renamed = ""
            if border_idx and border_idx in renamed_files:
                filename = renamed_files[border_idx]
                # Extract name part (remove _border_idx.jpg)
                match = re.match(r'(.+)_\d+\.jpg$', filename)
                if match:
                    name_if_renamed = match.group(1).replace('_', ' ')

            f.write(f"{child_idx},{border_idx},{filename},{name_if_renamed}\n")

    print(f"Mapping saved to: {mapping_path}")

if __name__ == "__main__":
    main()
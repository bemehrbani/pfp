#!/usr/bin/env python3
"""Debug version of create_splitted_photos.py."""

import os
import shutil
import re
from PIL import Image

def is_valid_name_strict(text):
    """Stricter validation for person names."""
    # Simplified for debugging
    if not text:
        return False
    text = ' '.join(text.split())
    if len(text) < 3 or len(text) > 50:
        return False
    return True

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
    print("First 5 mappings:", {k: child_to_border[k] for k in list(child_to_border.keys())[:5]})

    # Scan children_named for renamed files that are child photos
    renamed_files = {}
    src_dir = "children_named"
    print(f"\nScanning {src_dir} for .jpg files...")

    file_count = 0
    for fname in os.listdir(src_dir):
        if fname.lower().endswith('.jpg'):
            file_count += 1
            # Check if matches pattern *_{border_idx}.jpg
            match = re.search(r'_(\d{1,3})\.jpg$', fname)
            if match:
                border_idx = match.group(1)
                path = os.path.join(src_dir, fname)
                # Must be regular file (not symlink)
                if os.path.isfile(path) and not os.path.islink(path):
                    # Check dimensions to ensure it's a child photo
                    try:
                        img = Image.open(path)
                        w, h = img.size
                        # Child photo dimensions
                        if 350 <= w <= 450 and 600 <= h <= 750:
                            if border_idx in renamed_files:
                                print(f"  WARNING: Duplicate border_idx {border_idx}: already have {renamed_files[border_idx]}, now {fname}")
                            renamed_files[border_idx] = fname
                        else:
                            print(f"  Skipping {fname}: wrong dimensions {w}x{h}")
                    except Exception as e:
                        print(f"  Error checking {fname}: {e}")
            else:
                print(f"  No border_idx pattern match: {fname}")

    print(f"\nTotal .jpg files in {src_dir}: {file_count}")
    print(f"Found {len(renamed_files)} renamed child photo files")
    print("Sample renamed files:", list(renamed_files.items())[:5])

    # Create splitted_photos folder
    dest_dir = "splitted_photos_debug"
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)

    # Process each child
    copied_count = 0
    renamed_count = 0
    numbered_count = 0

    print("\nProcessing children 0-99:")
    for child_idx in range(100):
        border_idx = child_to_border.get(child_idx)
        print(f"\nChild {child_idx}, border_idx: {border_idx}")

        # Determine source file and destination name
        src_path = None
        dest_name = None
        name_used = ""
        name_source = "numbered"

        if border_idx and border_idx in renamed_files:
            # Use renamed file
            src_path = os.path.join("children_named", renamed_files[border_idx])
            dest_name = renamed_files[border_idx]
            # Extract name part
            match = re.match(r'(.+)_\d+\.jpg$', dest_name)
            if match:
                name_used = match.group(1).replace('_', ' ')
                name_source = "extracted"
                renamed_count += 1
                print(f"  Using renamed file: {dest_name}, name: {name_used}")
        else:
            # Use numbered file from final_output
            src_path = os.path.join("final_output", f"child_{child_idx+1:03d}.jpg")
            dest_name = f"child_{child_idx+1:03d}.jpg"
            numbered_count += 1
            print(f"  Using numbered file: {dest_name}")

        if not os.path.exists(src_path):
            print(f"  WARNING: Source file not found: {src_path}")
            continue

        # Copy to destination
        dest_path = os.path.join(dest_dir, dest_name)
        shutil.copy2(src_path, dest_path)
        copied_count += 1
        print(f"  Copied to: {dest_name}")

    print(f"\n=== Summary ===")
    print(f"Total children: 100")
    print(f"Renamed files used: {renamed_count}")
    print(f"Numbered files used: {numbered_count}")
    print(f"Total copied: {copied_count}")
    print(f"Output directory: {dest_dir}")

    # Count files in output directory
    output_files = len([f for f in os.listdir(dest_dir) if f.lower().endswith('.jpg')])
    print(f"Files in output directory: {output_files}")

if __name__ == "__main__":
    main()
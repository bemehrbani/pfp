#!/usr/bin/env python3
"""Clean filenames in splitted_photos folder and update mapping files."""

import os
import re
import shutil

def clean_filename(filename):
    """Clean a filename by removing leading/trailing weird characters."""
    # Extract border index suffix pattern _DDD.jpg
    match = re.search(r'_(\d{1,3})\.jpg$', filename)
    if not match:
        return filename  # shouldn't happen

    border_idx = match.group(1)
    name_part = filename[:match.start()]

    # Remove leading/trailing hyphens, underscores, spaces, fancy quotes
    # Define characters to strip from start and end
    strip_chars = " -_ـ'\"'‘’“”"
    name_part = name_part.strip(strip_chars)

    # Remove any remaining leading/trailing underscores
    name_part = name_part.strip('_')

    # Replace multiple underscores with single underscore
    name_part = re.sub(r'_+', '_', name_part)

    # If name_part is empty after stripping, use 'child'
    if not name_part:
        name_part = 'child'

    # Reconstruct filename
    new_filename = f"{name_part}_{border_idx}.jpg"
    return new_filename

def main():
    splitted_dir = "splitted_photos"

    # Read mapping.txt to get current mapping
    mapping_path = os.path.join(splitted_dir, "mapping.txt")
    if not os.path.exists(mapping_path):
        print("Error: mapping.txt not found")
        return

    lines = []
    with open(mapping_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # First line is header
    header = lines[0]
    data_lines = lines[1:]

    # Parse data lines
    entries = []
    for line in data_lines:
        if not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            child_num = parts[0]
            border_idx = parts[1]
            filename = parts[2]
            name = parts[3] if len(parts) > 3 else ''
            entries.append({
                'child_num': child_num,
                'border_idx': border_idx,
                'filename': filename,
                'name': name,
                'original_line': line
            })

    # Process each entry
    rename_map = {}
    for entry in entries:
        old_filename = entry['filename']
        new_filename = clean_filename(old_filename)

        if new_filename != old_filename:
            rename_map[old_filename] = new_filename
            print(f"Rename: {old_filename} -> {new_filename}")

            # Update entry
            entry['filename'] = new_filename
            # Also update name if it matches the name part (extracted from filename)
            # For simplicity, we'll keep the original name field

    # Apply renames
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(splitted_dir, old_name)
        new_path = os.path.join(splitted_dir, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"  Renamed file: {old_name} -> {new_name}")
        else:
            print(f"  Warning: File not found: {old_name}")

    # Write updated mapping.txt
    with open(mapping_path, 'w', encoding='utf-8') as f:
        f.write(header)
        for entry in entries:
            # Reconstruct line
            line = f"{entry['child_num']}\t{entry['border_idx']}\t{entry['filename']}\t{entry['name']}\n"
            f.write(line)
    print(f"\nUpdated mapping.txt")

    # Also update name_correction.csv if exists
    csv_path = os.path.join(splitted_dir, "name_correction.csv")
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            csv_lines = f.readlines()

        # Update filenames in CSV (column 3)
        updated_csv_lines = []
        for line in csv_lines:
            if line.startswith('child_index'):
                updated_csv_lines.append(line)
                continue
            parts = line.strip().split(',')
            if len(parts) >= 3:
                old_csv_filename = parts[2]
                if old_csv_filename in rename_map:
                    parts[2] = rename_map[old_csv_filename]
                    # Also update name_used if it's the same as filename without suffix?
                    # For now just update filename
                updated_csv_lines.append(','.join(parts) + '\n')
            else:
                updated_csv_lines.append(line)

        with open(csv_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_csv_lines)
        print(f"Updated name_correction.csv")

    print(f"\nTotal files renamed: {len(rename_map)}")

if __name__ == "__main__":
    main()
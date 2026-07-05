#!/usr/bin/env python3
"""Rename child photos with extracted names where possible."""

import os
import re
import shutil

def is_valid_name(text):
    """Check if text looks like a valid person name."""
    if not text:
        return False

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Check length
    if len(text) < 3 or len(text) > 50:
        return False

    # Check for excessive numbers (more than 2 digits)
    digit_count = sum(c.isdigit() for c in text)
    if digit_count > 2:
        return False

    # Must contain letters
    if not any(c.isalpha() for c in text):
        return False

    # Check for common name patterns
    # Should not contain obvious non-name characters
    non_name_chars = ['=', '|', '\\', '/', ':', ';', '°', '¬', '~', '`', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '[', ']', '{', '}', '<', '>']
    for char in non_name_chars:
        if char in text:
            return False

    # Check for Arabic/Persian letters
    arabic_persian_range = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
    has_arabic_persian = bool(re.search(arabic_persian_range, text))

    # Check for Latin letters
    has_latin = bool(re.search(r'[A-Za-z]', text))

    # Must have either Latin or Arabic/Persian letters
    if not (has_latin or has_arabic_persian):
        return False

    # For Latin names: check capitalization pattern
    if has_latin and not has_arabic_persian:
        words = text.split()
        if len(words) > 3:  # Too many words for a name
            return False
        # At least one word should start with capital
        capital_words = sum(1 for w in words if w and w[0].isupper())
        if capital_words == 0:
            return False

    return True

def clean_name(text):
    """Clean up name for use as filename."""
    if not text:
        return ""

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Replace problematic characters
    text = text.replace('\\', '').replace('/', '').replace(':', '').replace(';', '')
    text = text.replace('|', '').replace('*', '').replace('?', '').replace('"', '')
    text = text.replace('<', '').replace('>', '').replace('[', '').replace(']', '')
    text = text.replace('{', '').replace('}', '').replace('(', '').replace(')', '')

    # Replace spaces with underscores
    text = text.replace(' ', '_')

    return text

def main():
    # Read mapping
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

    # Read extracted names
    extracted_names = {}
    with open("extracted_names/all_extracted.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[1:]:
        if line.strip():
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                idx = parts[0]
                text = parts[1]
                status = parts[2]
                extracted_names[idx] = (text, status)

    print(f"Loaded {len(extracted_names)} extracted names")

    # Check original filenames in children_with_names for good names
    original_names = {}
    src_dir = "children_with_names"
    for fname in os.listdir(src_dir):
        if fname.lower().endswith('.jpg'):
            # Extract index from filename
            match = re.search(r'_(\d{3})\.jpg$', fname)
            if match:
                idx = match.group(1).lstrip('0')
                if not idx:
                    idx = "0"

                # Extract potential name part (before the last underscore)
                name_part = fname.rsplit('_', 1)[0]
                # Remove any digits and special characters to see if there's a name
                # Simple check: if name_part contains at least 3 letters
                letter_count = sum(c.isalpha() for c in name_part)
                if letter_count >= 3:
                    original_names[idx] = name_part

    print(f"Found {len(original_names)} potential names from original filenames")

    # Prepare to rename files in final_output
    src_dir = "final_output"
    dest_dir = "children_named"
    os.makedirs(dest_dir, exist_ok=True)

    renamed_count = 0
    kept_count = 0

    # Process each child
    for child_idx in range(100):  # 0 to 99
        src_filename = f"child_{child_idx+1:03d}.jpg"
        src_path = os.path.join(src_dir, src_filename)

        if not os.path.exists(src_path):
            print(f"Warning: Source file {src_filename} not found")
            continue

        # Get corresponding border index
        border_idx = child_to_border.get(child_idx)
        if not border_idx:
            print(f"Warning: No border index for child {child_idx}")
            dest_filename = src_filename
        else:
            # Try to get a good name
            best_name = None

            # First, check original filename name
            if border_idx in original_names:
                orig_name = original_names[border_idx]
                if is_valid_name(orig_name):
                    best_name = clean_name(orig_name)
                    print(f"Child {child_idx+1} (border {border_idx}): Using original filename name: {orig_name}")

            # If not, check extracted text
            if not best_name and border_idx in extracted_names:
                text, status = extracted_names[border_idx]
                if status == "name" and is_valid_name(text):
                    best_name = clean_name(text)
                    print(f"Child {child_idx+1} (border {border_idx}): Using extracted name: {text}")

            # If we have a name, use it
            if best_name:
                # Ensure name is not empty after cleaning
                if best_name.strip():
                    dest_filename = f"{best_name}_{border_idx}.jpg"
                    renamed_count += 1
                else:
                    dest_filename = src_filename
                    kept_count += 1
            else:
                dest_filename = src_filename
                kept_count += 1

        # Copy file
        dest_path = os.path.join(dest_dir, dest_filename)
        shutil.copy2(src_path, dest_path)

        # Also create a symbolic link with the original numbering for reference
        link_path = os.path.join(dest_dir, src_filename)
        if not os.path.exists(link_path):
            os.symlink(dest_filename, link_path)

    print(f"\n=== Summary ===")
    print(f"Total children: 100")
    print(f"Renamed with names: {renamed_count}")
    print(f"Kept numbered names: {kept_count}")
    print(f"Output directory: {dest_dir}")

    # Create a mapping file
    with open(os.path.join(dest_dir, "name_mapping.txt"), "w", encoding="utf-8") as f:
        f.write("child_index\tborder_index\tfilename\tname_source\n")
        for child_idx in range(100):
            src_filename = f"child_{child_idx+1:03d}.jpg"
            border_idx = child_to_border.get(child_idx, "")

            # Find actual dest filename
            dest_filename = src_filename
            for fname in os.listdir(dest_dir):
                if fname.startswith(f"child_{child_idx+1:03d}.jpg"):
                    dest_filename = fname
                    break

            name_source = "numbered"
            if border_idx:
                if border_idx in original_names and is_valid_name(original_names[border_idx]):
                    name_source = "original_filename"
                elif border_idx in extracted_names and extracted_names[border_idx][1] == "name":
                    name_source = "extracted_text"

            f.write(f"{child_idx}\t{border_idx}\t{dest_filename}\t{name_source}\n")

    print(f"Mapping saved to {dest_dir}/name_mapping.txt")

if __name__ == "__main__":
    main()
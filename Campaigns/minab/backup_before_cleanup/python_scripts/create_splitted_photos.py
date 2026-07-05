#!/usr/bin/env python3
"""Create final splitted_photos folder with best available names."""

import os
import shutil
import re
from PIL import Image

def is_valid_name_strict(text):
    """Stricter validation for person names."""
    if not text:
        return False

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Check length
    if len(text) < 3 or len(text) > 50:
        return False

    # Check for excessive numbers (more than 1 digit)
    digit_count = sum(c.isdigit() for c in text)
    if digit_count > 1:
        return False

    # Must contain letters
    if not any(c.isalpha() for c in text):
        return False

    # Check for common name patterns
    # Should not contain obvious non-name characters
    non_name_chars = ['=', '|', '\\\\', '/', ':', ';', '°', '¬', '~', '`', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '[', ']', '{', '}', '<', '>', '?', '!', '"', '\'', '\\', '\\', '\\', '\\']
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

    # For Latin names: stricter rules
    if has_latin and not has_arabic_persian:
        words = text.split()
        if len(words) > 3:  # Too many words for a name
            return False
        # Each word should start with capital letter (allow Mc, Mac, etc.)
        for word in words:
            if not word[0].isupper():
                # Allow prefixes like "al-", "el-", "bin", "bint"
                if word.lower() in ['al', 'el', 'bin', 'bint', 'de', 'di', 'da', 'del', 'della', 'van', 'von', 'der', 'ter', 'ten']:
                    continue
                # Allow "Mc", "Mac"
                if word.lower().startswith('mc') or word.lower().startswith('mac'):
                    continue
                return False
        # Should not contain digits at all (already checked digit_count > 1)
        if digit_count > 0:
            # Allow single digit only if it's part of roman numeral? Probably not
            return False

    # For Arabic/Persian names: should not contain Latin letters mixed
    if has_arabic_persian and has_latin:
        # Mixed script - likely OCR error
        return False

    return True

def clean_name_for_filename(text):
    """Clean up name for use as filename."""
    if not text:
        return ""

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Replace problematic characters with underscore
    problematic = ['\\', '/', ':', ';', '|', '*', '?', '"', '<', '>', '[', ']', '{', '}', '(', ')', '&', '$', '#', '@', '!', '~', '`', '\'', '+', '=', '%', '^']
    for char in problematic:
        text = text.replace(char, '')

    # Replace spaces with underscores
    text = text.replace(' ', '_')

    return text

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

    # Scan children_named for renamed files that are child photos
    renamed_files = {}
    src_dir = "children_named"
    for fname in os.listdir(src_dir):
        if fname.lower().endswith('.jpg'):
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
                            renamed_files[border_idx] = fname
                        else:
                            print(f"  Skipping {fname}: wrong dimensions {w}x{h}")
                    except Exception as e:
                        print(f"  Error checking {fname}: {e}")

    print(f"Found {len(renamed_files)} renamed child photo files")

    # Create splitted_photos folder
    dest_dir = "splitted_photos"
    os.makedirs(dest_dir, exist_ok=True)

    # Process each child
    copied_count = 0
    renamed_count = 0
    numbered_count = 0

    # For manual correction CSV
    correction_data = []

    for child_idx in range(100):
        border_idx = child_to_border.get(child_idx)

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

        # Add to correction data
        correction_data.append({
            'child_index': child_idx,
            'border_index': border_idx or '',
            'filename': dest_name,
            'name_used': name_used,
            'name_source': name_source,
            'needs_correction': 'YES' if name_source == 'extracted' and not is_valid_name_strict(name_used) else 'NO'
        })

    print(f"\n=== Summary ===")
    print(f"Total children: 100")
    print(f"Renamed files used: {renamed_count}")
    print(f"Numbered files used: {numbered_count}")
    print(f"Copied to: {dest_dir}")

    # Create correction CSV
    correction_path = os.path.join(dest_dir, "name_correction.csv")
    with open(correction_path, "w", encoding="utf-8") as f:
        f.write("child_index,border_index,filename,name_used,name_source,needs_correction,suggested_correction\n")
        for item in correction_data:
            f.write(f"{item['child_index']},{item['border_index']},{item['filename']},{item['name_used']},{item['name_source']},{item['needs_correction']},\n")

    print(f"Correction CSV saved to: {correction_path}")

    # Also create a simple mapping file
    mapping_path = os.path.join(dest_dir, "mapping.txt")
    with open(mapping_path, "w", encoding="utf-8") as f:
        f.write("Child\tBorder\tFilename\tName\n")
        for item in correction_data:
            f.write(f"{item['child_index']+1}\t{item['border_index']}\t{item['filename']}\t{item['name_used']}\n")

    print(f"Mapping saved to: {mapping_path}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Filter real names from OCR results."""

import os
import re

def is_likely_name(text):
    """Check if text looks like a person name."""
    if not text:
        return False

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Check length
    if len(text) < 4 or len(text) > 50:
        return False

    # Check for excessive numbers
    digit_count = sum(c.isdigit() for c in text)
    if digit_count > len(text) * 0.2:  # More than 20% digits
        return False

    # Check for Persian/Arabic letters
    persian_arabic_range = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
    has_persian_arabic = bool(re.search(persian_arabic_range, text))

    # Check for Latin letters
    has_latin = bool(re.search(r'[A-Za-z]', text))

    # Name should have either Latin or Persian/Arabic letters
    if not (has_latin or has_persian_arabic):
        return False

    # If Latin, check for name pattern (capitalized words)
    if has_latin:
        words = text.split()
        if len(words) < 1 or len(words) > 4:  # Typically 1-4 words
            return False

        # Check if most words start with capital letter
        capital_words = sum(1 for w in words if w and w[0].isupper())
        if capital_words < len(words) * 0.5:  # At least half should be capitalized
            return False

        # Check for invalid characters
        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -'.")
        if any(c not in valid_chars for c in text):
            # Allow some non-Latin if mixed
            non_latin = [c for c in text if c not in valid_chars]
            # Check if non-Latin are Persian/Arabic
            for c in non_latin:
                if not re.match(persian_arabic_range, c):
                    return False

    # If Persian/Arabic, check for reasonable length
    if has_persian_arabic and not has_latin:
        # Persian names typically 2-10 characters per word
        words = text.split()
        for w in words:
            if len(w) > 15:  # Too long for a name
                return False

    return True

def main():
    coords_file = "children_with_names/coordinates.txt"

    if not os.path.exists(coords_file):
        print("Coordinates file not found.")
        return

    with open(coords_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip header
    if len(lines) < 2:
        print("No data in file.")
        return

    valid_names = []
    invalid_names = []

    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) < 6:
            continue

        idx = parts[0]
        name = parts[5]
        filename = parts[6] if len(parts) > 6 else ""

        if is_likely_name(name):
            valid_names.append((idx, name, filename))
            print(f"✓ Valid name: {name} (index {idx})")
        else:
            invalid_names.append((idx, name, filename))
            if name.strip():
                print(f"✗ Invalid: '{name}' (index {idx})")

    print(f"\n=== Summary ===")
    print(f"Valid names: {len(valid_names)}")
    print(f"Invalid names: {len(invalid_names)}")
    print(f"Total: {len(valid_names) + len(invalid_names)}")

    print("\n=== Valid Names ===")
    for idx, name, filename in valid_names:
        print(f"{idx}: {name} -> {filename}")

    # Create a clean folder
    clean_dir = "children_named_clean"
    os.makedirs(clean_dir, exist_ok=True)

    # Copy valid files
    source_dir = "children_with_names"
    for idx, name, filename in valid_names:
        src = os.path.join(source_dir, filename)
        if os.path.exists(src):
            # Create clean filename
            clean_name = name.replace(' ', '_')
            clean_filename = f"{clean_name}.jpg"
            dest = os.path.join(clean_dir, clean_filename)

            # Copy file
            import shutil
            shutil.copy2(src, dest)
            print(f"Copied: {src} -> {dest}")

    print(f"\nCopied {len(valid_names)} files to {clean_dir}/")

if __name__ == "__main__":
    main()
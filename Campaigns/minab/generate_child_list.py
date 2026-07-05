#!/usr/bin/env python3
"""Generate a list of splitted photos for each child with known names."""

import csv
import os

def main():
    csv_path = "splitted_photos/name_correction.csv"
    if not os.path.exists(csv_path):
        print("Error: CSV file not found")
        return

    # Read CSV
    children = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            children.append(row)

    print(f"Loaded {len(children)} children")

    # Determine "known name": name_used not empty and name_source == 'extracted'
    known = []
    unknown = []
    for c in children:
        if c['name_used'] and c['name_source'] == 'extracted':
            known.append(c)
        else:
            unknown.append(c)

    print(f"Children with extracted names: {len(known)}")
    print(f"Children with numbered names: {len(unknown)}")

    # Output known names list
    with open('children_with_known_names.txt', 'w', encoding='utf-8') as f:
        f.write("ChildIndex\tBorderIndex\tFilename\tName\tNeedsCorrection\n")
        for c in known:
            f.write(f"{c['child_index']}\t{c['border_index']}\t{c['filename']}\t{c['name_used']}\t{c['needs_correction']}\n")

    # Output full list
    with open('children_full_list.txt', 'w', encoding='utf-8') as f:
        f.write("ChildIndex\tBorderIndex\tFilename\tName\tNameSource\tNeedsCorrection\n")
        for c in children:
            f.write(f"{c['child_index']}\t{c['border_index']}\t{c['filename']}\t{c['name_used']}\t{c['name_source']}\t{c['needs_correction']}\n")

    # Also create a simple mapping for frontend maybe JSON
    import json
    mapping = {}
    for c in children:
        mapping[c['child_index']] = {
            'border_index': c['border_index'],
            'filename': c['filename'],
            'name': c['name_used'],
            'name_source': c['name_source'],
            'needs_correction': c['needs_correction']
        }
    with open('children_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print("\nGenerated files:")
    print("- children_with_known_names.txt")
    print("- children_full_list.txt")
    print("- children_mapping.json")

if __name__ == "__main__":
    main()
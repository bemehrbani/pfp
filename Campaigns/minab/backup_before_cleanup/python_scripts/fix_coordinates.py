#!/usr/bin/env python3
"""Fix malformed coordinates.txt file with newlines in middle of records."""

import re

def main():
    input_file = "children_with_names/coordinates.txt"
    output_file = "children_with_names/coordinates_fixed.txt"

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # First line is header
    header = lines[0].strip()
    print(f"Header: {header}")

    # Process remaining lines
    fixed_records = []
    current_record = []

    for i, line in enumerate(lines[1:]):
        line = line.strip()
        if not line:
            continue

        # Check if line starts with a digit (index)
        if re.match(r'^\d+\t', line):
            # New record starts
            if current_record:
                fixed_records.append("\t".join(current_record))
            current_record = [line]
        else:
            # Continuation of previous record
            if current_record:
                current_record.append(line)
            else:
                # Should not happen, but handle
                print(f"Warning: Line {i+2} doesn't start with index but no current record: {line[:50]}")

    # Add last record
    if current_record:
        fixed_records.append("\t".join(current_record))

    print(f"Found {len(fixed_records)} records")

    # Write fixed file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for record in fixed_records:
            f.write(record + "\n")

    # Verify each record has right number of fields
    with open(output_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    errors = 0
    for i, line in enumerate(lines[1:]):
        parts = line.strip().split('\t')
        if len(parts) != 7:
            print(f"Line {i+2}: Has {len(parts)} parts (expected 7): {parts}")
            errors += 1

    print(f"\nFixed coordinates saved to {output_file}")
    print(f"Errors: {errors}")

    # Also create a simplified version with just index, filename
    with open("children_with_names/index_to_filename.txt", "w", encoding="utf-8") as f:
        f.write("index\tfilename\n")
        for line in lines[1:]:
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                idx = parts[0]
                filename = parts[6]
                f.write(f"{idx}\t{filename}\n")

if __name__ == "__main__":
    main()
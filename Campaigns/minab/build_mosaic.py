#!/usr/bin/env python3
"""
Concept #3: Interactive Mosaic — Build Script
Injects the photo file list into the HTML template to create a self-contained
interactive mosaic page.
"""

import json
from pathlib import Path

PHOTO_DIR = Path(__file__).parent / "splitted_photos"
TEMPLATE = Path(__file__).parent / "mosaic_template.html"
OUTPUT = Path(__file__).parent / "interactive_mosaic.html"


def main() -> None:
    """Build the interactive mosaic HTML."""
    photos = sorted(
        [p.name for p in PHOTO_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")],
    )

    print(f"Found {len(photos)} photos")

    html = TEMPLATE.read_text()
    html = html.replace("PHOTO_LIST_PLACEHOLDER", json.dumps(photos))

    OUTPUT.write_text(html)
    print(f"🎉 Interactive mosaic built: {OUTPUT}")
    print(f"   Open in browser: file://{OUTPUT.resolve()}")


if __name__ == "__main__":
    main()

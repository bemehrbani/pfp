#!/usr/bin/env python3
"""
Concept #2: "Before You Scroll" — Single-Child Spotlight Cards
Generates 1080×1080 emotional social media cards from Minab children photos.

Each card features:
- Dark gradient background
- Child's portrait (centered, softly bordered)
- Child's name (if available)
- Emotional caption text
- PFP branding + hashtag bar
"""

import os
import random
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# --- Configuration ---
CARD_SIZE = (1080, 1080)
PHOTO_DIR = Path(__file__).parent / "splitted_photos"
OUTPUT_DIR = Path(__file__).parent / "spotlight_cards"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"
FONT_FUTURA = "/System/Library/Fonts/Supplemental/Futura.ttc"

# Brand colors
BG_DARK = (15, 15, 25)
ACCENT_GOLD = (232, 190, 92)
ACCENT_WARM = (220, 120, 60)
TEXT_WHITE = (255, 255, 255)
TEXT_DIM = (180, 180, 190)
HASHTAG_COLOR = (140, 160, 220)

# Emotional captions — rotated across cards
CAPTIONS = [
    "Before you scroll past —\nthis child has a name.",
    "100 children.\n100 stolen futures.",
    "She doesn't know what\n'normal' looks like.",
    "His biggest dream?\nGoing to school without fear.",
    "Sanctions don't just\nhurt economies.\nThey steal childhoods.",
    "This face is not a statistic.",
    "What would you do\nif this was your child?",
    "Every child deserves a\nchance to dream.",
    "Peace is not political.\nIt's personal.",
    "Behind every sanction\nis a child who suffers.",
    "Their only crime?\nBeing born in the wrong place.",
    "She wants to be a doctor.\nWill the world let her?",
    "This is what\nindifference looks like.",
    "One voice can't change the world.\nBut silence guarantees nothing will.",
    "They didn't choose this.\nBut you can choose to care.",
]


def extract_name(filename: str) -> str | None:
    """Extract a readable child name from the filename, return None if not a real name."""
    stem = Path(filename).stem

    # Skip numbered fallback names
    if re.match(r"^child_\d+$", stem):
        return None

    # Skip Arabic/Farsi garbled OCR names
    if any("\u0600" <= ch <= "\u06FF" for ch in stem):
        return None

    # Extract name parts (before the trailing number)
    parts = re.sub(r"_\d+$", "", stem).split("_")
    # Clean up fragments — only keep parts that look like names
    clean_parts = []
    for part in parts:
        cleaned = re.sub(r"[^a-zA-Z]", "", part)
        if len(cleaned) >= 2:
            clean_parts.append(cleaned.capitalize())

    if not clean_parts:
        return None

    return " ".join(clean_parts)


def create_gradient_background(size: tuple[int, int]) -> Image.Image:
    """Create a dark cinematic gradient background."""
    img = Image.new("RGB", size, BG_DARK)
    draw = ImageDraw.Draw(img)

    # Radial-ish warm glow in center
    center_x, center_y = size[0] // 2, size[1] // 3
    for radius in range(400, 0, -1):
        opacity = int(12 * (radius / 400))
        color = (
            BG_DARK[0] + min(opacity * 2, 30),
            BG_DARK[1] + min(opacity, 15),
            BG_DARK[2] + min(opacity, 20),
        )
        draw.ellipse(
            [
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
            ],
            fill=color,
        )

    return img


def add_photo_to_card(
    card: Image.Image, photo_path: Path, card_draw: ImageDraw.Draw
) -> None:
    """Place the child's photo on the card with rounded corners and soft shadow."""
    photo = Image.open(photo_path).convert("RGB")

    # Target photo height on card
    target_height = 620
    aspect = photo.width / photo.height
    target_width = int(target_height * aspect)
    photo = photo.resize((target_width, target_height), Image.LANCZOS)

    # Enhance slightly
    enhancer = ImageEnhance.Contrast(photo)
    photo = enhancer.enhance(1.1)
    enhancer = ImageEnhance.Brightness(photo)
    photo = enhancer.enhance(1.05)

    # Create rounded rectangle mask
    mask = Image.new("L", photo.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (photo.width - 1, photo.height - 1)], radius=16, fill=255
    )

    # Soft shadow
    shadow_offset = 6
    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    photo_x = (card.width - target_width) // 2
    photo_y = 60
    shadow_draw.rounded_rectangle(
        [
            (photo_x + shadow_offset, photo_y + shadow_offset),
            (
                photo_x + target_width + shadow_offset,
                photo_y + target_height + shadow_offset,
            ),
        ],
        radius=16,
        fill=(0, 0, 0, 80),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=12))
    card.paste(
        Image.new("RGB", card.size, BG_DARK), mask=shadow.split()[3]
    )  # darken behind shadow

    # Paste photo with mask
    card.paste(photo, (photo_x, photo_y), mask)

    # Thin gold border
    card_draw.rounded_rectangle(
        [(photo_x - 2, photo_y - 2), (photo_x + target_width + 1, photo_y + target_height + 1)],
        radius=18,
        outline=(*ACCENT_GOLD, 120),
        width=2,
    )

    return photo_y + target_height  # return bottom y of photo


def render_text_block(
    card: Image.Image,
    draw: ImageDraw.Draw,
    name: str | None,
    caption: str,
    photo_bottom_y: int,
) -> None:
    """Render the name, caption, and branding text onto the card."""
    y_cursor = photo_bottom_y + 24

    # --- Child's name ---
    if name:
        try:
            font_name = ImageFont.truetype(FONT_BOLD, 36)
        except OSError:
            font_name = ImageFont.load_default()
        # Gold accent line
        draw.line(
            [(CARD_SIZE[0] // 2 - 60, y_cursor), (CARD_SIZE[0] // 2 + 60, y_cursor)],
            fill=ACCENT_GOLD,
            width=2,
        )
        y_cursor += 12
        bbox = draw.textbbox((0, 0), name, font=font_name)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((CARD_SIZE[0] - text_width) // 2, y_cursor),
            name,
            font=font_name,
            fill=ACCENT_GOLD,
        )
        y_cursor += (bbox[3] - bbox[1]) + 16

    # --- Caption ---
    try:
        font_caption = ImageFont.truetype(FONT_REGULAR, 26)
    except OSError:
        font_caption = ImageFont.load_default()

    for line in caption.split("\n"):
        bbox = draw.textbbox((0, 0), line, font=font_caption)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((CARD_SIZE[0] - text_width) // 2, y_cursor),
            line,
            font=font_caption,
            fill=TEXT_WHITE,
        )
        y_cursor += (bbox[3] - bbox[1]) + 6

    # --- Bottom branding bar ---
    bar_y = CARD_SIZE[1] - 60
    try:
        font_small = ImageFont.truetype(FONT_REGULAR, 18)
    except OSError:
        font_small = ImageFont.load_default()

    # Separator line
    draw.line(
        [(80, bar_y - 16), (CARD_SIZE[0] - 80, bar_y - 16)],
        fill=(60, 60, 80),
        width=1,
    )

    branding = "People for Peace"
    hashtags = "#100FacesOfPeace  #PeopleForPeace"

    bbox_brand = draw.textbbox((0, 0), branding, font=font_small)
    draw.text(
        (40, bar_y),
        branding,
        font=font_small,
        fill=TEXT_DIM,
    )

    bbox_hash = draw.textbbox((0, 0), hashtags, font=font_small)
    hash_width = bbox_hash[2] - bbox_hash[0]
    draw.text(
        (CARD_SIZE[0] - hash_width - 40, bar_y),
        hashtags,
        font=font_small,
        fill=HASHTAG_COLOR,
    )


def generate_card(photo_path: Path, index: int) -> Path:
    """Generate a single spotlight card and save it."""
    name = extract_name(photo_path.name)
    caption = CAPTIONS[index % len(CAPTIONS)]

    # Create card
    card = create_gradient_background(CARD_SIZE)
    draw = ImageDraw.Draw(card, "RGBA")

    # Add photo
    photo_bottom = add_photo_to_card(card, photo_path, draw)

    # Add text
    render_text_block(card, draw, name, caption, photo_bottom)

    # Save
    safe_name = re.sub(r"[^\w\-.]", "_", photo_path.stem)
    output_path = OUTPUT_DIR / f"card_{index + 1:03d}_{safe_name}.jpg"
    card.convert("RGB").save(output_path, "JPEG", quality=92)
    return output_path


def main() -> None:
    """Generate all spotlight cards."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Get all child photos (skip non-image files)
    photos = sorted(
        [p for p in PHOTO_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")],
        key=lambda p: p.name,
    )

    print(f"Found {len(photos)} child photos")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    generated = 0
    for i, photo_path in enumerate(photos):
        try:
            out = generate_card(photo_path, i)
            generated += 1
            if generated <= 5 or generated % 20 == 0:
                name = extract_name(photo_path.name)
                label = name if name else f"(unnamed #{i + 1})"
                print(f"  ✅ [{generated:3d}] {label} → {out.name}")
        except Exception as e:
            print(f"  ❌ [{i + 1:3d}] {photo_path.name}: {e}")

    print(f"\n🎉 Generated {generated} spotlight cards in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()

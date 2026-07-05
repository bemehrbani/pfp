#!/usr/bin/env python3
"""
Concept #4: "Count to 100" — Countdown Story Series Cards
Generates numbered countdown cards (100/100 → 1/100) for serial posting.

Each card features:
- Countdown number prominently displayed
- Child's portrait
- Child's name
- Sequential caption
- Progress bar showing countdown position
- PFP branding + #100FacesOfPeace
"""

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# --- Configuration ---
CARD_SIZE = (1080, 1350)  # 4:5 portrait for Instagram
PHOTO_DIR = Path(__file__).parent / "splitted_photos"
OUTPUT_DIR = Path(__file__).parent / "countdown_cards"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

BG_DARK = (12, 12, 20)
ACCENT_GOLD = (232, 190, 92)
ACCENT_WARM = (220, 120, 60)
TEXT_WHITE = (255, 255, 255)
TEXT_DIM = (160, 160, 170)
PROGRESS_BG = (40, 40, 55)
PROGRESS_FILL = (232, 190, 92)
HASHTAG_COLOR = (140, 160, 220)

CAPTIONS = [
    "wants to grow up in a world without fear.",
    "dreams of going to school every day.",
    "has never known peace — but deserves it.",
    "doesn't understand why the world forgot.",
    "wants to be a doctor someday.",
    "believes in a better tomorrow.",
    "has a smile that sanctions can't erase.",
    "is waiting for someone to care.",
    "hopes the world will listen.",
    "deserves the same chances as every other child.",
]


def extract_name(filename: str) -> str | None:
    """Extract a readable child name from the filename."""
    stem = Path(filename).stem
    if re.match(r"^child_\d+$", stem):
        return None
    if any("\u0600" <= ch <= "\u06FF" for ch in stem):
        return None
    parts = re.sub(r"_\d+$", "", stem).split("_")
    clean_parts = [
        re.sub(r"[^a-zA-Z]", "", p).capitalize()
        for p in parts
        if len(re.sub(r"[^a-zA-Z]", "", p)) >= 2
    ]
    return " ".join(clean_parts) if clean_parts else None


def generate_countdown_card(photo_path: Path, countdown_num: int, total: int) -> Path:
    """Generate a single countdown card."""
    card = Image.new("RGB", CARD_SIZE, BG_DARK)
    draw = ImageDraw.Draw(card)

    try:
        font_counter = ImageFont.truetype(FONT_BOLD, 72)
        font_name = ImageFont.truetype(FONT_BOLD, 34)
        font_caption = ImageFont.truetype(FONT_REGULAR, 24)
        font_small = ImageFont.truetype(FONT_REGULAR, 18)
        font_tiny = ImageFont.truetype(FONT_REGULAR, 16)
    except OSError:
        font_counter = font_name = font_caption = font_small = font_tiny = ImageFont.load_default()

    y_cursor = 40

    # --- Counter badge ---
    counter_text = f"{countdown_num}/{total}"
    bbox = draw.textbbox((0, 0), counter_text, font=font_counter)
    counter_w = bbox[2] - bbox[0]
    counter_h = bbox[3] - bbox[1]

    # Draw counter background pill
    pill_w = counter_w + 60
    pill_h = counter_h + 24
    pill_x = (CARD_SIZE[0] - pill_w) // 2
    draw.rounded_rectangle(
        [(pill_x, y_cursor), (pill_x + pill_w, y_cursor + pill_h)],
        radius=pill_h // 2,
        fill=(30, 30, 45),
        outline=ACCENT_GOLD,
        width=2,
    )
    draw.text(
        ((CARD_SIZE[0] - counter_w) // 2, y_cursor + 8),
        counter_text,
        font=font_counter,
        fill=ACCENT_GOLD,
    )
    y_cursor += pill_h + 30

    # --- Photo ---
    photo = Image.open(photo_path).convert("RGB")
    enhancer = ImageEnhance.Contrast(photo)
    photo = enhancer.enhance(1.1)

    target_h = 680
    aspect = photo.width / photo.height
    target_w = int(target_h * aspect)
    photo = photo.resize((target_w, target_h), Image.LANCZOS)

    # Rounded mask
    mask = Image.new("L", (target_w, target_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (target_w - 1, target_h - 1)], radius=20, fill=255)

    photo_x = (CARD_SIZE[0] - target_w) // 2
    photo_y = y_cursor
    card.paste(photo, (photo_x, photo_y), mask)

    # Gold border
    draw.rounded_rectangle(
        [(photo_x - 2, photo_y - 2), (photo_x + target_w + 1, photo_y + target_h + 1)],
        radius=22,
        outline=ACCENT_GOLD,
        width=2,
    )
    y_cursor = photo_y + target_h + 30

    # --- Name ---
    name = extract_name(photo_path.name)
    if name:
        # Gold line
        draw.line(
            [(CARD_SIZE[0] // 2 - 50, y_cursor), (CARD_SIZE[0] // 2 + 50, y_cursor)],
            fill=ACCENT_GOLD,
            width=2,
        )
        y_cursor += 12
        bbox = draw.textbbox((0, 0), name, font=font_name)
        name_w = bbox[2] - bbox[0]
        draw.text(
            ((CARD_SIZE[0] - name_w) // 2, y_cursor),
            name,
            font=font_name,
            fill=ACCENT_GOLD,
        )
        y_cursor += (bbox[3] - bbox[1]) + 10

    # --- Caption ---
    caption = CAPTIONS[(total - countdown_num) % len(CAPTIONS)]
    if name:
        full_caption = f"{name.split()[0]} {caption}"
    else:
        full_caption = f"This child {caption}"

    # Word wrap
    words = full_caption.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font_caption)
        if (bbox[2] - bbox[0]) > CARD_SIZE[0] - 120:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test
    if current_line:
        lines.append(current_line)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_caption)
        line_w = bbox[2] - bbox[0]
        draw.text(
            ((CARD_SIZE[0] - line_w) // 2, y_cursor),
            line,
            font=font_caption,
            fill=TEXT_WHITE,
        )
        y_cursor += (bbox[3] - bbox[1]) + 6

    # --- Progress bar ---
    bar_y = CARD_SIZE[1] - 100
    bar_x = 60
    bar_w = CARD_SIZE[0] - 120
    bar_h = 10
    progress = (total - countdown_num + 1) / total

    draw.rounded_rectangle(
        [(bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h)],
        radius=5,
        fill=PROGRESS_BG,
    )
    fill_w = int(bar_w * progress)
    if fill_w > 0:
        draw.rounded_rectangle(
            [(bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h)],
            radius=5,
            fill=PROGRESS_FILL,
        )

    # Progress label
    progress_label = f"{total - countdown_num + 1} of {total} children"
    bbox = draw.textbbox((0, 0), progress_label, font=font_tiny)
    draw.text(
        ((CARD_SIZE[0] - (bbox[2] - bbox[0])) // 2, bar_y + bar_h + 8),
        progress_label,
        font=font_tiny,
        fill=TEXT_DIM,
    )

    # --- Bottom branding ---
    bottom_y = CARD_SIZE[1] - 45
    draw.line(
        [(60, bottom_y - 10), (CARD_SIZE[0] - 60, bottom_y - 10)],
        fill=(40, 40, 55),
        width=1,
    )

    branding = "People for Peace"
    draw.text((60, bottom_y), branding, font=font_small, fill=TEXT_DIM)

    hashtag = "#100FacesOfPeace"
    bbox = draw.textbbox((0, 0), hashtag, font=font_small)
    hash_w = bbox[2] - bbox[0]
    draw.text(
        (CARD_SIZE[0] - hash_w - 60, bottom_y),
        hashtag,
        font=font_small,
        fill=HASHTAG_COLOR,
    )

    # Save
    safe_name = re.sub(r"[^\w\-.]", "_", photo_path.stem)
    output_path = OUTPUT_DIR / f"countdown_{countdown_num:03d}_{safe_name}.jpg"
    card.save(output_path, "JPEG", quality=92)
    return output_path


def main() -> None:
    """Generate all countdown cards."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    photos = sorted(
        [p for p in PHOTO_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")],
        key=lambda p: p.name,
    )

    total = len(photos)
    print(f"Found {total} photos")
    print(f"Output: {OUTPUT_DIR}")
    print()

    generated = 0
    for i, photo_path in enumerate(photos):
        countdown_num = total - i  # 100, 99, 98, ...
        try:
            out = generate_countdown_card(photo_path, countdown_num, total)
            generated += 1
            if generated <= 3 or generated % 25 == 0:
                name = extract_name(photo_path.name)
                label = name if name else f"(unnamed)"
                print(f"  ✅ [{countdown_num:3d}/{total}] {label} → {out.name}")
        except Exception as exc:
            print(f"  ❌ [{countdown_num}/{total}] {photo_path.name}: {exc}")

    print(f"\n🎉 Generated {generated} countdown cards in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()

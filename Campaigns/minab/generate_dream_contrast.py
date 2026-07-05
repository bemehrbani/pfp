#!/usr/bin/env python3
"""
Concept #6: "What They Dream" — AI-Generated Contrast Cards
Creates side-by-side comparison cards: real child photo (left) vs dream future (right).

Caption: "Sanctions don't just hurt economies. They steal futures."
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
CARD_SIZE = (1080, 1080)
PHOTO_DIR = Path(__file__).parent / "splitted_photos"
DREAM_DIR = Path.home() / ".gemini/antigravity/brain/c49f6f92-91d8-4cfd-89f4-16b945de70b3"
OUTPUT_DIR = Path(__file__).parent / "dream_contrast_cards"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

BG_DARK = (12, 12, 20)
ACCENT_GOLD = (232, 190, 92)
TEXT_WHITE = (255, 255, 255)
TEXT_DIM = (160, 160, 170)
HASHTAG_COLOR = (140, 160, 220)
LABEL_REALITY = (180, 80, 70)
LABEL_DREAM = (80, 180, 120)

# Map real children to dream images and professions
PAIRINGS = [
    ("Parsa_Mokhtar_34.jpg", "dream_doctor", "Doctor", "Parsa"),
    ("Zahra_Sharafi_24.jpg", "dream_teacher", "Teacher", "Zahra"),
    ("Amirali_Jadav_71.jpg", "dream_engineer", "Engineer", "Amirali"),
    ("Asma_Zakeri_41.jpg", "dream_artist", "Artist", "Asma"),
    ("Sobhan_Ahmai_47.jpg", "dream_scientist", "Scientist", "Sobhan"),
]


def find_dream_image(dream_prefix: str) -> Path | None:
    """Find the AI dream image by prefix."""
    for p in DREAM_DIR.iterdir():
        if p.name.startswith(dream_prefix) and p.suffix in (".png", ".jpg"):
            return p
    return None


def generate_contrast_card(
    real_photo_path: Path,
    dream_photo_path: Path,
    profession: str,
    child_name: str,
    index: int,
) -> Path:
    """Generate a side-by-side contrast card."""
    card = Image.new("RGB", CARD_SIZE, BG_DARK)
    draw = ImageDraw.Draw(card)

    try:
        font_title = ImageFont.truetype(FONT_BOLD, 30)
        font_caption = ImageFont.truetype(FONT_REGULAR, 22)
        font_label = ImageFont.truetype(FONT_BOLD, 18)
        font_small = ImageFont.truetype(FONT_REGULAR, 17)
        font_name = ImageFont.truetype(FONT_BOLD, 36)
    except OSError:
        font_title = font_caption = font_label = font_small = font_name = ImageFont.load_default()

    y_top = 40

    # --- Name ---
    bbox = draw.textbbox((0, 0), child_name, font=font_name)
    name_w = bbox[2] - bbox[0]
    draw.text(
        ((CARD_SIZE[0] - name_w) // 2, y_top),
        child_name,
        font=font_name,
        fill=ACCENT_GOLD,
    )
    y_top += (bbox[3] - bbox[1]) + 20

    # --- Side by side images ---
    half_w = (CARD_SIZE[0] - 40) // 2  # 20px padding on each side, 10px gap
    img_height = 550
    gap = 10

    # Real photo (left)
    real_photo = Image.open(real_photo_path).convert("RGB")
    real_aspect = real_photo.width / real_photo.height
    real_target_w = min(half_w - 10, int(img_height * real_aspect))
    real_photo = real_photo.resize((real_target_w, img_height), Image.LANCZOS)

    # Dream photo (right)
    dream_photo = Image.open(dream_photo_path).convert("RGB")
    dream_aspect = dream_photo.width / dream_photo.height
    dream_target_w = min(half_w - 10, int(img_height * dream_aspect))
    dream_photo = dream_photo.resize((dream_target_w, img_height), Image.LANCZOS)

    # Rounded masks
    for img in [real_photo, dream_photo]:
        mask = Image.new("L", img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (img.width - 1, img.height - 1)], radius=14, fill=255)

    # Position
    left_x = (CARD_SIZE[0] // 2 - gap // 2) - real_target_w
    right_x = CARD_SIZE[0] // 2 + gap // 2
    img_y = y_top

    # Create masks
    mask_left = Image.new("L", real_photo.size, 0)
    ImageDraw.Draw(mask_left).rounded_rectangle(
        [(0, 0), (real_photo.width - 1, real_photo.height - 1)], radius=14, fill=255
    )
    mask_right = Image.new("L", dream_photo.size, 0)
    ImageDraw.Draw(mask_right).rounded_rectangle(
        [(0, 0), (dream_photo.width - 1, dream_photo.height - 1)], radius=14, fill=255
    )

    card.paste(real_photo, (left_x, img_y), mask_left)
    card.paste(dream_photo, (right_x, img_y), mask_right)

    # Borders
    draw.rounded_rectangle(
        [(left_x - 2, img_y - 2), (left_x + real_target_w + 1, img_y + img_height + 1)],
        radius=16,
        outline=LABEL_REALITY,
        width=2,
    )
    draw.rounded_rectangle(
        [(right_x - 2, img_y - 2), (right_x + dream_target_w + 1, img_y + img_height + 1)],
        radius=16,
        outline=LABEL_DREAM,
        width=2,
    )

    # Labels
    label_y = img_y + img_height + 10
    reality_label = "REALITY"
    bbox = draw.textbbox((0, 0), reality_label, font=font_label)
    label_w = bbox[2] - bbox[0]
    draw.text(
        (left_x + (real_target_w - label_w) // 2, label_y),
        reality_label,
        font=font_label,
        fill=LABEL_REALITY,
    )

    dream_label = f"DREAM: {profession.upper()}"
    bbox = draw.textbbox((0, 0), dream_label, font=font_label)
    label_w = bbox[2] - bbox[0]
    draw.text(
        (right_x + (dream_target_w - label_w) // 2, label_y),
        dream_label,
        font=font_label,
        fill=LABEL_DREAM,
    )

    # --- Arrow between images ---
    arrow_y = img_y + img_height // 2
    arrow_x = CARD_SIZE[0] // 2
    draw.text(
        (arrow_x - 8, arrow_y - 16),
        "→",
        font=font_title,
        fill=ACCENT_GOLD,
    )

    # --- Caption ---
    caption_y = label_y + 40
    caption = "Sanctions don't just hurt economies."
    bbox = draw.textbbox((0, 0), caption, font=font_caption)
    draw.text(
        ((CARD_SIZE[0] - (bbox[2] - bbox[0])) // 2, caption_y),
        caption,
        font=font_caption,
        fill=TEXT_WHITE,
    )
    caption2 = "They steal futures."
    bbox = draw.textbbox((0, 0), caption2, font=font_caption)
    draw.text(
        ((CARD_SIZE[0] - (bbox[2] - bbox[0])) // 2, caption_y + 32),
        caption2,
        font=font_caption,
        fill=ACCENT_GOLD,
    )

    # --- Bottom branding ---
    bottom_y = CARD_SIZE[1] - 45
    draw.line(
        [(60, bottom_y - 10), (CARD_SIZE[0] - 60, bottom_y - 10)],
        fill=(40, 40, 55),
        width=1,
    )
    draw.text((40, bottom_y), "People for Peace", font=font_small, fill=TEXT_DIM)
    hashtag = "#100FacesOfPeace  #SanctionsStealFutures"
    bbox = draw.textbbox((0, 0), hashtag, font=font_small)
    draw.text(
        (CARD_SIZE[0] - (bbox[2] - bbox[0]) - 40, bottom_y),
        hashtag,
        font=font_small,
        fill=HASHTAG_COLOR,
    )

    # Save
    output_path = OUTPUT_DIR / f"dream_contrast_{index + 1:02d}_{child_name}_{profession}.jpg"
    card.save(output_path, "JPEG", quality=92)
    return output_path


def main() -> None:
    """Generate all dream contrast cards."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Generating dream contrast cards...")
    generated = 0

    for i, (real_name, dream_prefix, profession, child_name) in enumerate(PAIRINGS):
        real_path = PHOTO_DIR / real_name
        dream_path = find_dream_image(dream_prefix)

        if not real_path.exists():
            print(f"  ❌ Real photo not found: {real_name}")
            continue
        if dream_path is None:
            print(f"  ❌ Dream image not found: {dream_prefix}")
            continue

        out = generate_contrast_card(real_path, dream_path, profession, child_name, i)
        generated += 1
        print(f"  ✅ {child_name} → {profession} → {out.name}")

    print(f"\n🎉 Generated {generated} dream contrast cards in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()

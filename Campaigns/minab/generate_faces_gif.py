#!/usr/bin/env python3
"""
Concept #1: "100 Faces of Peace" — Animated Photo Grid GIF
Creates a rapid-fire montage of all 100 children's faces with a closing text card.

Output: A GIF that cycles through face close-ups synced to a heartbeat-like rhythm,
ending with a powerful closing message.
"""

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# --- Configuration ---
PHOTO_DIR = Path(__file__).parent / "splitted_photos"
OUTPUT_DIR = Path(__file__).parent / "animated_gifs"

FRAME_SIZE = (640, 640)  # square for social media
FACE_DISPLAY_MS = 120    # milliseconds per face (heartbeat pace)
CLOSING_DISPLAY_MS = 3000  # hold closing card for 3 seconds

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

BG_DARK = (15, 15, 25)
ACCENT_GOLD = (232, 190, 92)
TEXT_WHITE = (255, 255, 255)


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


def create_face_frame(photo_path: Path) -> Image.Image:
    """Create a single face frame: dark bg with centered, cropped face."""
    frame = Image.new("RGB", FRAME_SIZE, BG_DARK)

    photo = Image.open(photo_path).convert("RGB")

    # Crop to focus on face (upper 70% of photo to get face area)
    face_crop_height = int(photo.height * 0.7)
    photo_face = photo.crop((0, 0, photo.width, face_crop_height))

    # Resize to fill frame width, maintaining aspect
    scale = FRAME_SIZE[0] / photo_face.width
    new_w = FRAME_SIZE[0]
    new_h = int(photo_face.height * scale)
    photo_face = photo_face.resize((new_w, new_h), Image.LANCZOS)

    # Center vertically
    y_offset = (FRAME_SIZE[1] - new_h) // 2
    frame.paste(photo_face, (0, max(0, y_offset)))

    # Subtle vignette overlay
    vignette = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    vignette_draw = ImageDraw.Draw(vignette)
    # Dark edges
    for i in range(80):
        alpha = int(120 * (1 - i / 80))
        vignette_draw.rectangle(
            [(i, i), (FRAME_SIZE[0] - i, FRAME_SIZE[1] - i)],
            outline=(0, 0, 0, alpha),
        )
    frame_rgba = frame.convert("RGBA")
    frame_rgba = Image.alpha_composite(frame_rgba, vignette)
    frame = frame_rgba.convert("RGB")

    # Add name at bottom if available
    name = extract_name(photo_path.name)
    if name:
        draw = ImageDraw.Draw(frame)
        try:
            font = ImageFont.truetype(FONT_BOLD, 22)
        except OSError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), name, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        # Semi-transparent bar at bottom
        bar_y = FRAME_SIZE[1] - text_h - 24
        draw.rectangle(
            [(0, bar_y - 4), (FRAME_SIZE[0], FRAME_SIZE[1])],
            fill=(15, 15, 25),
        )
        draw.text(
            ((FRAME_SIZE[0] - text_w) // 2, bar_y + 2),
            name,
            font=font,
            fill=ACCENT_GOLD,
        )

    return frame


def create_closing_frame() -> Image.Image:
    """Create the powerful closing text card."""
    frame = Image.new("RGB", FRAME_SIZE, BG_DARK)
    draw = ImageDraw.Draw(frame)

    try:
        font_big = ImageFont.truetype(FONT_BOLD, 44)
        font_medium = ImageFont.truetype(FONT_BOLD, 28)
        font_small = ImageFont.truetype(FONT_REGULAR, 20)
    except OSError:
        font_big = font_medium = font_small = ImageFont.load_default()

    # Gold accent line
    line_y = 200
    draw.line(
        [(FRAME_SIZE[0] // 2 - 80, line_y), (FRAME_SIZE[0] // 2 + 80, line_y)],
        fill=ACCENT_GOLD,
        width=3,
    )

    # Main text
    lines = [
        ("100 children.", font_big, TEXT_WHITE, 230),
        ("100 dreams.", font_big, TEXT_WHITE, 290),
        ("One demand:", font_medium, ACCENT_GOLD, 370),
        ("Peace.", font_big, ACCENT_GOLD, 410),
    ]

    for text, font, color, y_pos in lines:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text(((FRAME_SIZE[0] - text_w) // 2, y_pos), text, font=font, fill=color)

    # Bottom bar
    hashtag = "#100FacesOfPeace"
    bbox = draw.textbbox((0, 0), hashtag, font=font_small)
    text_w = bbox[2] - bbox[0]
    draw.text(
        ((FRAME_SIZE[0] - text_w) // 2, 540),
        hashtag,
        font=font_small,
        fill=(140, 160, 220),
    )

    branding = "People for Peace"
    bbox = draw.textbbox((0, 0), branding, font=font_small)
    text_w = bbox[2] - bbox[0]
    draw.text(
        ((FRAME_SIZE[0] - text_w) // 2, 580),
        branding,
        font=font_small,
        fill=(180, 180, 190),
    )

    return frame


def create_intro_frame() -> Image.Image:
    """Create an intro frame."""
    frame = Image.new("RGB", FRAME_SIZE, BG_DARK)
    draw = ImageDraw.Draw(frame)

    try:
        font_big = ImageFont.truetype(FONT_BOLD, 36)
        font_small = ImageFont.truetype(FONT_REGULAR, 22)
    except OSError:
        font_big = font_small = ImageFont.load_default()

    text = "100 Faces of Peace"
    bbox = draw.textbbox((0, 0), text, font=font_big)
    text_w = bbox[2] - bbox[0]
    draw.text(
        ((FRAME_SIZE[0] - text_w) // 2, FRAME_SIZE[1] // 2 - 30),
        text,
        font=font_big,
        fill=ACCENT_GOLD,
    )

    sub = "Minab, Iran"
    bbox = draw.textbbox((0, 0), sub, font=font_small)
    text_w = bbox[2] - bbox[0]
    draw.text(
        ((FRAME_SIZE[0] - text_w) // 2, FRAME_SIZE[1] // 2 + 30),
        sub,
        font=font_small,
        fill=TEXT_WHITE,
    )

    return frame


def main() -> None:
    """Generate the animated GIF."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    photos = sorted(
        [p for p in PHOTO_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")],
        key=lambda p: p.name,
    )

    print(f"Found {len(photos)} photos")
    print("Generating frames...")

    frames: list[Image.Image] = []
    durations: list[int] = []

    # Intro frame
    print("  → Intro frame")
    frames.append(create_intro_frame())
    durations.append(2000)

    # Face frames
    for i, photo in enumerate(photos):
        face_frame = create_face_frame(photo)
        frames.append(face_frame)

        # Heartbeat rhythm: alternate fast/slow
        if i % 2 == 0:
            durations.append(FACE_DISPLAY_MS)
        else:
            durations.append(FACE_DISPLAY_MS + 40)

        if (i + 1) % 20 == 0:
            print(f"  → {i + 1}/{len(photos)} faces processed")

    # Closing frame
    print("  → Closing frame")
    frames.append(create_closing_frame())
    durations.append(CLOSING_DISPLAY_MS)

    # Save GIF
    output_path = OUTPUT_DIR / "100_faces_of_peace.gif"
    print(f"\nSaving GIF to {output_path}...")

    # Convert frames to palette mode for GIF
    palette_frames = [f.quantize(colors=256, method=Image.Quantize.MEDIANCUT) for f in frames]

    palette_frames[0].save(
        output_path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    total_duration_s = sum(durations) / 1000
    print(f"\n🎉 GIF created: {output_path}")
    print(f"   Size: {file_size_mb:.1f} MB")
    print(f"   Duration: {total_duration_s:.1f}s")
    print(f"   Frames: {len(frames)}")


if __name__ == "__main__":
    main()

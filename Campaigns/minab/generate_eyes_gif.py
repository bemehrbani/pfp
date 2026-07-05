#!/usr/bin/env python3
"""
Concept #5: "Eyes That Ask" — Close-Crop Eye Portraits
Crops just the eye region from each child's photo and sequences them into
a haunting GIF where the eyes "look at the viewer" one by one.

Since these are passport-style photos with consistent framing,
we use proportional cropping (eyes are ~25-40% from top of face).
"""

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# --- Configuration ---
FRAME_SIZE = (800, 400)  # widescreen cinematic aspect
PHOTO_DIR = Path(__file__).parent / "splitted_photos"
OUTPUT_DIR = Path(__file__).parent / "animated_gifs"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

BG_DARK = (8, 8, 14)
ACCENT_GOLD = (232, 190, 92)
TEXT_WHITE = (255, 255, 255)

EYE_DISPLAY_MS = 200    # hold each eye pair
CLOSING_MS = 4000        # closing frame hold


def create_eye_frame(photo_path: Path) -> Image.Image:
    """Crop the eye region from a portrait photo."""
    frame = Image.new("RGB", FRAME_SIZE, BG_DARK)

    photo = Image.open(photo_path).convert("RGB")

    # For passport-style photos, eyes are roughly at 25-38% from top
    # Crop a horizontal strip that captures the eye region
    eye_top = int(photo.height * 0.20)
    eye_bottom = int(photo.height * 0.42)
    eye_strip = photo.crop((0, eye_top, photo.width, eye_bottom))

    # Scale to fill frame width
    scale = FRAME_SIZE[0] / eye_strip.width
    new_w = FRAME_SIZE[0]
    new_h = int(eye_strip.height * scale)
    eye_strip = eye_strip.resize((new_w, new_h), Image.LANCZOS)

    # Enhance to make eyes pop
    enhancer = ImageEnhance.Contrast(eye_strip)
    eye_strip = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Sharpness(eye_strip)
    eye_strip = enhancer.enhance(1.5)

    # Center vertically
    y_offset = (FRAME_SIZE[1] - new_h) // 2
    frame.paste(eye_strip, (0, max(0, y_offset)))

    # Cinematic black bars (top and bottom)
    draw = ImageDraw.Draw(frame)
    bar_height = 30
    # Top gradient bar
    for i in range(bar_height):
        alpha = int(255 * (1 - i / bar_height))
        draw.line([(0, i), (FRAME_SIZE[0], i)], fill=(8, 8, 14))
    # Fade top
    for i in range(bar_height, bar_height + 20):
        blend = (i - bar_height) / 20
        draw.line(
            [(0, i), (FRAME_SIZE[0], i)],
            fill=(
                int(8 * (1 - blend) + frame.getpixel((FRAME_SIZE[0] // 2, i))[0] * blend),
                int(8 * (1 - blend) + frame.getpixel((FRAME_SIZE[0] // 2, i))[1] * blend),
                int(14 * (1 - blend) + frame.getpixel((FRAME_SIZE[0] // 2, i))[2] * blend),
            ),
        )

    # Bottom bar
    for i in range(FRAME_SIZE[1] - bar_height, FRAME_SIZE[1]):
        draw.line([(0, i), (FRAME_SIZE[0], i)], fill=(8, 8, 14))

    # Vignette edges (left and right)
    for x in range(60):
        alpha_factor = x / 60
        for y in range(FRAME_SIZE[1]):
            px = frame.getpixel((x, y))
            frame.putpixel((x, y), tuple(int(c * alpha_factor) for c in px))
            px_r = frame.getpixel((FRAME_SIZE[0] - 1 - x, y))
            frame.putpixel(
                (FRAME_SIZE[0] - 1 - x, y),
                tuple(int(c * alpha_factor) for c in px_r),
            )

    return frame


def create_closing_frame() -> Image.Image:
    """Create the closing message frame."""
    frame = Image.new("RGB", FRAME_SIZE, BG_DARK)
    draw = ImageDraw.Draw(frame)

    try:
        font_big = ImageFont.truetype(FONT_BOLD, 42)
        font_medium = ImageFont.truetype(FONT_BOLD, 28)
        font_small = ImageFont.truetype(FONT_REGULAR, 20)
    except OSError:
        font_big = font_medium = font_small = ImageFont.load_default()

    # Main text
    lines = [
        ("They're watching.", font_big, TEXT_WHITE, 120),
        ("Are you?", font_big, ACCENT_GOLD, 175),
    ]

    for text, font, color, y_pos in lines:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text(((FRAME_SIZE[0] - text_w) // 2, y_pos), text, font=font, fill=color)

    # Decorative line
    draw.line(
        [(FRAME_SIZE[0] // 2 - 60, 260), (FRAME_SIZE[0] // 2 + 60, 260)],
        fill=ACCENT_GOLD,
        width=2,
    )

    # Hashtag
    hashtag = "#100FacesOfPeace  ·  People for Peace"
    bbox = draw.textbbox((0, 0), hashtag, font=font_small)
    text_w = bbox[2] - bbox[0]
    draw.text(
        ((FRAME_SIZE[0] - text_w) // 2, 290),
        hashtag,
        font=font_small,
        fill=(140, 160, 220),
    )

    return frame


def main() -> None:
    """Generate the eyes-that-ask GIF."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    photos = sorted(
        [p for p in PHOTO_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")],
        key=lambda p: p.name,
    )

    print(f"Found {len(photos)} photos")
    print("Extracting eye regions...")

    frames: list[Image.Image] = []
    durations: list[int] = []

    for i, photo_path in enumerate(photos):
        try:
            eye_frame = create_eye_frame(photo_path)
            frames.append(eye_frame)
            durations.append(EYE_DISPLAY_MS)

            if (i + 1) % 25 == 0:
                print(f"  → {i + 1}/{len(photos)} eyes processed")
        except Exception as exc:
            print(f"  ⚠️ Skipped {photo_path.name}: {exc}")

    # Closing frame
    print("  → Closing frame")
    frames.append(create_closing_frame())
    durations.append(CLOSING_MS)

    # Save GIF
    output_path = OUTPUT_DIR / "eyes_that_ask.gif"
    print(f"\nSaving GIF to {output_path}...")

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
    total_s = sum(durations) / 1000
    print(f"\n🎉 GIF created: {output_path}")
    print(f"   Size: {file_size_mb:.1f} MB")
    print(f"   Duration: {total_s:.1f}s")
    print(f"   Frames: {len(frames)}")


if __name__ == "__main__":
    main()

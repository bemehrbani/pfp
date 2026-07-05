#!/usr/bin/env python3
"""
Concept #7: "The Ripple" — Animated Share Chain
Creates a GIF showing children's faces appearing in expanding ripple rings,
visualizing how one share creates a wave of awareness.

Pure Pillow implementation — no external animation library needed.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
FRAME_SIZE = (800, 800)
PHOTO_DIR = Path(__file__).parent / "splitted_photos"
OUTPUT_DIR = Path(__file__).parent / "animated_gifs"
NUM_FRAMES = 60  # total animation frames
FRAME_DURATION_MS = 100

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

BG_DARK = (10, 10, 18)
ACCENT_GOLD = (232, 190, 92)
TEXT_WHITE = (255, 255, 255)
RING_COLOR = (232, 190, 92)


def load_face_thumbnails(photo_dir: Path, thumb_size: int = 60) -> list[Image.Image]:
    """Load and create circular face thumbnails."""
    photos = sorted(
        [p for p in photo_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")],
        key=lambda p: p.name,
    )

    thumbnails = []
    for photo_path in photos[:50]:  # use first 50 for performance
        try:
            img = Image.open(photo_path).convert("RGB")
            # Crop to face region (upper portion)
            face_height = int(img.height * 0.55)
            face = img.crop((0, 0, img.width, face_height))
            # Make square
            size = min(face.width, face.height)
            left = (face.width - size) // 2
            top = 0
            face = face.crop((left, top, left + size, top + size))
            face = face.resize((thumb_size, thumb_size), Image.LANCZOS)

            # Circular mask
            mask = Image.new("L", (thumb_size, thumb_size), 0)
            ImageDraw.Draw(mask).ellipse([(0, 0), (thumb_size - 1, thumb_size - 1)], fill=255)
            face.putalpha(mask)

            thumbnails.append(face)
        except Exception:
            pass

    return thumbnails


def create_ripple_frame(
    frame_num: int,
    total_frames: int,
    thumbnails: list[Image.Image],
) -> Image.Image:
    """Create a single frame of the ripple animation."""
    frame = Image.new("RGBA", FRAME_SIZE, (*BG_DARK, 255))
    draw = ImageDraw.Draw(frame)
    cx, cy = FRAME_SIZE[0] // 2, FRAME_SIZE[1] // 2

    progress = frame_num / total_frames  # 0.0 → 1.0

    # Draw expanding ripple rings
    max_rings = 5
    rings_visible = int(progress * max_rings) + 1

    for ring in range(rings_visible):
        ring_progress = min(1.0, (progress * max_rings - ring))
        if ring_progress <= 0:
            continue

        radius = int(60 + ring * 120 * ring_progress)
        alpha = max(20, int(180 * (1 - ring_progress * 0.6)))

        # Draw ripple circle
        for w in range(2):
            draw.ellipse(
                [(cx - radius - w, cy - radius - w), (cx + radius + w, cy + radius + w)],
                outline=(*RING_COLOR, alpha),
            )

        # Place face thumbnails around this ring
        if ring < len(thumbnails) // 6:
            faces_per_ring = 6 + ring * 4
            start_idx = sum(6 + r * 4 for r in range(ring))
            for j in range(faces_per_ring):
                if start_idx + j >= len(thumbnails):
                    break
                angle = (2 * math.pi * j / faces_per_ring) - math.pi / 2
                face_x = int(cx + radius * math.cos(angle)) - 30
                face_y = int(cy + radius * math.sin(angle)) - 30

                # Only show if this ring is sufficiently expanded
                if ring_progress > 0.3:
                    thumb = thumbnails[start_idx + j]
                    face_alpha = min(255, int(255 * (ring_progress - 0.3) / 0.7))
                    if face_alpha > 50:
                        # Create alpha-adjusted version
                        temp = Image.new("RGBA", thumb.size, (0, 0, 0, 0))
                        temp.paste(thumb, (0, 0))
                        alpha_channel = temp.split()[3]
                        alpha_channel = alpha_channel.point(lambda p: int(p * face_alpha / 255))
                        temp.putalpha(alpha_channel)

                        if (0 <= face_x < FRAME_SIZE[0] - 60 and 0 <= face_y < FRAME_SIZE[1] - 60):
                            frame.paste(temp, (face_x, face_y), temp)

    # Center face (first child — the "drop")
    if thumbnails:
        center_thumb = thumbnails[0].resize((80, 80), Image.LANCZOS)
        # Gold border circle
        draw.ellipse(
            [(cx - 42, cy - 42), (cx + 42, cy + 42)],
            outline=ACCENT_GOLD,
            width=3,
        )
        frame.paste(center_thumb, (cx - 40, cy - 40), center_thumb)

    return frame.convert("RGB")


def create_closing_frame() -> Image.Image:
    """Create closing text frame."""
    frame = Image.new("RGB", FRAME_SIZE, BG_DARK)
    draw = ImageDraw.Draw(frame)

    try:
        font_big = ImageFont.truetype(FONT_BOLD, 38)
        font_medium = ImageFont.truetype(FONT_BOLD, 26)
        font_small = ImageFont.truetype(FONT_REGULAR, 20)
    except OSError:
        font_big = font_medium = font_small = ImageFont.load_default()

    lines = [
        ("One share creates a ripple.", font_big, TEXT_WHITE, 280),
        ("100 shares create a wave.", font_big, ACCENT_GOLD, 340),
    ]
    for text, font, color, y in lines:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((FRAME_SIZE[0] - w) // 2, y), text, font=font, fill=color)

    # Gold line
    draw.line(
        [(FRAME_SIZE[0] // 2 - 60, 420), (FRAME_SIZE[0] // 2 + 60, 420)],
        fill=ACCENT_GOLD,
        width=2,
    )

    hashtag = "#100FacesOfPeace  ·  People for Peace"
    bbox = draw.textbbox((0, 0), hashtag, font=font_small)
    w = bbox[2] - bbox[0]
    draw.text(
        ((FRAME_SIZE[0] - w) // 2, 450),
        hashtag,
        font=font_small,
        fill=(140, 160, 220),
    )

    return frame


def main() -> None:
    """Generate the ripple animation GIF."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Loading face thumbnails...")
    thumbnails = load_face_thumbnails(PHOTO_DIR, thumb_size=60)
    print(f"  Loaded {len(thumbnails)} face thumbnails")

    print("Generating ripple frames...")
    frames: list[Image.Image] = []
    durations: list[int] = []

    for i in range(NUM_FRAMES):
        ripple_frame = create_ripple_frame(i, NUM_FRAMES, thumbnails)
        frames.append(ripple_frame)
        durations.append(FRAME_DURATION_MS)

        if (i + 1) % 15 == 0:
            print(f"  → {i + 1}/{NUM_FRAMES} frames")

    # Hold last ripple frame briefly
    frames.append(frames[-1])
    durations.append(1500)

    # Closing frame
    print("  → Closing frame")
    frames.append(create_closing_frame())
    durations.append(4000)

    # Save GIF
    output_path = OUTPUT_DIR / "ripple_share_chain.gif"
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

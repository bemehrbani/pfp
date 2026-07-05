#!/usr/bin/env python3
"""
Final Video V3 — Second Suno track (more professional) + grid video.

Creates the final 1080x1080 MP4:
1. 3×3 grid with children's faces + names overlaid
2. Suno vocal track as primary audio
3. Our synthesized beat mixed underneath at low volume for depth
4. Karaoke lyrics (synced to actual Suno track), beat pulse effects

Source of truth: ../frontend/public/memorial-data.js
Photos: ../frontend/public/images/children/child_rXX_cXX.jpg
"""

import math
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# --- Configuration ---
VIDEO_SIZE = (1080, 1080)
FPS = 30
BPM = 85
BEAT_DURATION = 60.0 / BPM

# Duration matches the second Suno track
TOTAL_DURATION = 180.7
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

PHOTO_DIR = Path(__file__).parent.parent / "frontend" / "public" / "images" / "children"
MEMORIAL_DATA_JS = Path(__file__).parent.parent / "frontend" / "public" / "memorial-data.js"
VOCAL_FILE = Path(__file__).parent / "music" / "100 Faces of Peace — Rap Lyrics (2).mp3"
BEAT_FILE = Path(__file__).parent / "music" / "100_faces_beat.wav"
OUTPUT_DIR = Path(__file__).parent / "music"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

BG_COLOR = (8, 8, 16)
GOLD = (232, 190, 92)
GOLD_DIM = (180, 148, 72)
WHITE = (255, 255, 255)
DIM = (130, 130, 145)
LYRIC_BG = (8, 8, 16)

# Grid layout
GRID_COLS = 3
GRID_ROWS = 3
GRID_GAP = 4
GRID_PADDING = 16
TOP_AREA = 70
BOTTOM_AREA = 130

# Face change interval (in beats) — every 4 beats (1 bar)
CHANGE_INTERVAL_BEATS = 4
CHANGE_INTERVAL_SEC = CHANGE_INTERVAL_BEATS * BEAT_DURATION

# --- Lyrics sync (from RMS audio analysis of second Suno track) ---
# Structure: intro(0-11), verse1(12-43), break(43-47), hook1(47-65),
#            break(66-67), verse2(68-85), break(85-90), hook2(90-111),
#            bridge(111-124), build(125-134), final(135-170), fade(170+)
LYRICS_TIMED = [
    # Intro (0-11s — instrumental)
    (0.0, ""),
    # Verse 1 (12-43s — vocals come in)
    (12.0, "Look at their eyes, look at their face"),
    (14.5, "A hundred children from a forgotten place"),
    (17.0, "Minab to the world, we carry their voice"),
    (19.5, "Peace ain't a privilege — it's a right, not a choice"),
    (22.0, ""),
    (23.0, "Zahra wants a pencil, Parsa wants a book"),
    (25.5, "Amirali dreams of a future — take a look"),
    (28.0, "Asma paints in colors that the world won't see"),
    (30.5, "Sobhan's in a classroom where he can't be free"),
    (33.0, "A hundred names, a hundred faces on the wall"),
    (35.5, "Every single one of them too young to fall"),
    (38.0, "Reza, Makan, Sina — do you hear them call?"),
    (40.5, "From Minab to the world, we speak for them all"),
    # Hook 1 (47-65s)
    (43.0, ""),
    (47.0, "\ud83d\udd0a Dub dub dub — DISH — can you hear the beat?"),
    (49.5, "A hundred hearts are marching down the street"),
    (52.0, "\ud83d\udd0a Dub dub dub — DISH — every face you see"),
    (54.5, "Is a child who's asking: Won't you fight for me?"),
    (57.0, "\ud83d\udd0a Dub dub dub — DISH — can you hear the beat?"),
    (59.5, "A hundred hearts are marching down the street"),
    (62.0, "\ud83d\udd0a Dub dub dub — DISH — every face you see"),
    (64.0, "Is a child who's asking: Won't you fight for me?"),
    # Verse 2 (68-85s)
    (66.0, ""),
    (68.0, "Sanctions hit the hospitals, the schools, the bread"),
    (70.5, "Politicians sleeping while the children aren't fed"),
    (73.0, "She was gonna be a doctor, he was gonna fly"),
    (75.5, "But the world looked away and nobody asked why"),
    (78.0, "Every face a statistic, every name erased"),
    (80.5, "Every dream is broken, every hope displaced"),
    (82.5, "But we don't scroll past — nah, we stop and stare"),
    (84.5, "'Cause a hundred children need to know we care"),
    # Hook 2 (90-111s)
    (86.0, ""),
    (90.5, "\ud83d\udd0a Dub dub dub — DISH — can you hear the beat?"),
    (93.0, "A hundred hearts are marching down the street"),
    (95.5, "\ud83d\udd0a Dub dub dub — DISH — every face you see"),
    (98.0, "Is a child who's asking: Won't you fight for me?"),
    (100.5, "\ud83d\udd0a Dub dub dub — DISH — can you hear the beat?"),
    (103.0, "A hundred hearts are marching down the street"),
    (105.5, "\ud83d\udd0a Dub dub dub — DISH — every face you see"),
    (108.0, "Is a child who's asking: Won't you fight for me?"),
    # Bridge (111-124s — quiet)
    (111.0, ""),
    (113.0, "One share is a ripple, a hundred is a wave"),
    (118.0, "One voice in the silence might be all it takes to save"),
    (122.0, "Look 'em in the eyes — they're watching you"),
    # Final Section (125-170s — biggest section)
    (125.0, ""),
    (126.0, "A hundred faces... a hundred dreams..."),
    (129.0, "People for Peace — that's what it means"),
    (132.0, "What are you gonna do?"),
    (134.0, ""),
    (136.0, "Minab to the world, we won't be ignored"),
    (139.0, "Every. Child. Deserves. More."),
    (143.0, "\ud83d\udd0a Dub dub dub — DISH — can you hear the beat?"),
    (146.0, "A hundred hearts are marching down the street"),
    (149.0, "\ud83d\udd0a Dub dub dub — DISH — every face you see"),
    (152.0, "Is a child who's asking: Won't you fight for me?"),
    (155.0, "Every. Child. Deserves. More."),
    (160.0, "\ud83d\udd0a Dub dub dub — DISH — can you hear the beat?"),
    (163.0, "A hundred hearts are marching down the street"),
    (166.0, "Is a child who's asking: Won't you fight for me?"),
    # Fade (170+)
    (170.0, ""),
    (172.0, "#100FacesOfPeace  ·  People for Peace"),
    (178.0, ""),
]


def parse_memorial_data() -> list[dict]:
    """Parse memorial-data.js to get verified children with photoGrid."""
    text = MEMORIAL_DATA_JS.read_text(encoding="utf-8")
    children: list[dict] = []
    for match in re.finditer(
        r'\{\s*id:\s*"([^"]+)".*?name:\s*"([^"]+)".*?'
        r'photoGrid:\s*"(r\d+_c\d+)"',
        text,
        re.DOTALL,
    ):
        child_id, name, grid = match.groups()
        photo_file = f"child_{grid}.jpg"
        children.append({"id": child_id, "name": name, "photo": photo_file, "grid": grid})
    # Sort by grid position (row, col)
    children.sort(
        key=lambda c: (int(c["grid"].split("_")[0][1:]), int(c["grid"].split("_")[1][1:]))
    )
    return children


def load_photos(photo_dir: Path) -> tuple[list[Image.Image], list[str | None]]:
    """Load child photos from memorial images + verified names from memorial-data.js."""
    memorial_children = parse_memorial_data()
    print(f"  Memorial data: {len(memorial_children)} children with photos")

    cell_w = (VIDEO_SIZE[0] - 2 * GRID_PADDING - (GRID_COLS - 1) * GRID_GAP) // GRID_COLS
    cell_h = (
        VIDEO_SIZE[1] - TOP_AREA - BOTTOM_AREA - 2 * GRID_PADDING - (GRID_ROWS - 1) * GRID_GAP
    ) // GRID_ROWS

    photos = []
    names = []
    named_count = 0
    for child in memorial_children:
        photo_path = photo_dir / child["photo"]
        if not photo_path.exists():
            print(f"  ⚠ Photo not found: {child['photo']}")
            continue
        try:
            img = Image.open(photo_path).convert("RGB")
            img_ratio = img.width / img.height
            cell_ratio = cell_w / cell_h
            if img_ratio > cell_ratio:
                new_w = int(img.height * cell_ratio)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))
            else:
                new_h = int(img.width / cell_ratio)
                img = img.crop((0, 0, img.width, new_h))
            img = img.resize((cell_w, cell_h), Image.LANCZOS)
            photos.append(img)
            names.append(child["name"])
            named_count += 1
        except Exception as exc:
            print(f"  ⚠ Error loading {child['photo']}: {exc}")

    print(f"  Named: {named_count} / {len(photos)}")
    return photos, names


def get_current_lyric(time_s: float) -> str:
    """Get the lyric line for the current time."""
    current_lyric = ""
    for t, lyric in LYRICS_TIMED:
        if time_s >= t:
            current_lyric = lyric
        else:
            break
    return current_lyric


def create_frame(
    photos: list[Image.Image],
    names: list[str | None],
    frame_time: float,
    cell_w: int,
    cell_h: int,
) -> Image.Image:
    """Create a single polished video frame."""
    frame = Image.new("RGB", VIDEO_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(frame)

    try:
        font_title = ImageFont.truetype(FONT_BOLD, 26)
        font_lyrics = ImageFont.truetype(FONT_BOLD, 20)
        font_small = ImageFont.truetype(FONT_REGULAR, 14)
        font_counter = ImageFont.truetype(FONT_BOLD, 16)
        font_name = ImageFont.truetype(FONT_BOLD, 13)
    except OSError:
        font_title = font_lyrics = font_small = font_counter = font_name = ImageFont.load_default()

    # --- Current beat phase ---
    beat_phase = (frame_time / BEAT_DURATION) % 1.0
    bar_phase = (frame_time / (BEAT_DURATION * 4)) % 1.0
    current_beat_in_bar = int((frame_time / BEAT_DURATION) % 4)

    # --- Which set of 9 faces to show ---
    change_index = int(frame_time / CHANGE_INTERVAL_SEC)
    transition_time = frame_time % CHANGE_INTERVAL_SEC
    transition_progress = min(1.0, transition_time / 0.2)  # 0.2s fade

    # --- Title bar ---
    # Subtle pulse on the title
    title_alpha_mult = 0.85 + 0.15 * math.sin(frame_time * 1.5)
    title = "100 FACES OF PEACE"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = bbox[2] - bbox[0]
    title_color = tuple(int(c * title_alpha_mult) for c in GOLD)
    draw.text(((VIDEO_SIZE[0] - title_w) // 2, 22), title, font=font_title, fill=title_color)

    # Thin gold line under title
    draw.line([(40, TOP_AREA - 6), (VIDEO_SIZE[0] - 40, TOP_AREA - 6)], fill=GOLD_DIM, width=1)

    # --- 3×3 Grid ---
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            idx = row * GRID_COLS + col
            x = GRID_PADDING + col * (cell_w + GRID_GAP)
            y = TOP_AREA + GRID_PADDING + row * (cell_h + GRID_GAP)

            # Current photo
            photo_idx = (change_index * 9 + idx) % len(photos)
            photo = photos[photo_idx]

            # Previous photo for cross-fade
            if transition_progress < 1.0:
                prev_idx = ((change_index - 1) * 9 + idx) % len(photos)
                prev_photo = photos[prev_idx]
                blended = Image.blend(prev_photo, photo, transition_progress)
                frame.paste(blended, (x, y))
            else:
                frame.paste(photo, (x, y))

            # --- Name overlay with gradient strip ---
            child_name = names[photo_idx]
            if child_name:
                # Draw a gradient strip at bottom of cell
                strip_h = 28
                strip_y = y + cell_h - strip_h
                # Semi-transparent dark gradient via RGBA overlay
                overlay = Image.new("RGBA", (cell_w, strip_h), (0, 0, 0, 0))
                ov_draw = ImageDraw.Draw(overlay)
                for gy in range(strip_h):
                    alpha = int(180 * (gy / strip_h))  # gradient: top transparent, bottom opaque
                    ov_draw.line([(0, gy), (cell_w, gy)], fill=(0, 0, 0, alpha))
                # Paste with alpha
                frame.paste(overlay, (x, strip_y), overlay)
                # Draw name text
                # Use first name only for space efficiency
                first_name = child_name.split()[0]
                name_bbox = draw.textbbox((0, 0), first_name, font=font_name)
                name_w = name_bbox[2] - name_bbox[0]
                draw.text(
                    (x + (cell_w - name_w) // 2, strip_y + strip_h - 18),
                    first_name,
                    font=font_name,
                    fill=(255, 255, 255, 230),
                )

            # Beat pulse border effect
            # Flash on kick (beats 0, 1, 2) and snare (beat 3)
            beat_frac = (frame_time / BEAT_DURATION) % 1.0
            if beat_frac < 0.08:
                intensity = int(200 * (1 - beat_frac / 0.08))
                if current_beat_in_bar < 3:
                    # Kick pulse — subtle white
                    border_color = (intensity // 2, intensity // 2, intensity // 2)
                else:
                    # Snare pulse — gold flash
                    border_color = (intensity, int(intensity * 0.75), int(intensity * 0.3))

                draw.rectangle(
                    [(x - 1, y - 1), (x + cell_w, y + cell_h)],
                    outline=border_color,
                    width=2,
                )

    # --- Vignette effect on grid edges ---
    # (subtle darkening at edges — done via semi-transparent overlays)
    grid_bottom = TOP_AREA + GRID_PADDING + GRID_ROWS * (cell_h + GRID_GAP)

    # --- Lyrics area ---
    lyrics_area_y = VIDEO_SIZE[1] - BOTTOM_AREA

    # Dark backdrop
    draw.rectangle(
        [(0, lyrics_area_y), (VIDEO_SIZE[0], VIDEO_SIZE[1])],
        fill=LYRIC_BG,
    )

    # Gold divider
    draw.line(
        [(30, lyrics_area_y + 4), (VIDEO_SIZE[0] - 30, lyrics_area_y + 4)],
        fill=GOLD_DIM,
        width=1,
    )

    # Current lyric
    lyric = get_current_lyric(frame_time)
    if lyric:
        # Text glow effect: measure and center
        bbox = draw.textbbox((0, 0), lyric, font=font_lyrics)
        lyric_w = bbox[2] - bbox[0]
        lyric_h = bbox[3] - bbox[1]
        lyric_x = max(15, (VIDEO_SIZE[0] - lyric_w) // 2)
        lyric_y = lyrics_area_y + 25

        # Main text
        draw.text((lyric_x, lyric_y), lyric, font=font_lyrics, fill=WHITE)

    # --- Beat visualizer bar ---
    viz_y = lyrics_area_y + 65
    viz_width = VIDEO_SIZE[0] - 80
    viz_x = 40

    # Draw 4 beat indicators
    beat_block_w = viz_width // 4 - 4
    for b in range(4):
        bx = viz_x + b * (beat_block_w + 4)
        is_active = current_beat_in_bar == b and beat_frac < 0.15
        if is_active:
            if b < 3:
                color = GOLD
            else:
                color = (255, 120, 80)  # snare flash — orange-red
            draw.rounded_rectangle(
                [(bx, viz_y), (bx + beat_block_w, viz_y + 8)],
                radius=4,
                fill=color,
            )
        else:
            draw.rounded_rectangle(
                [(bx, viz_y), (bx + beat_block_w, viz_y + 8)],
                radius=4,
                fill=(30, 30, 40),
            )

    # Beat labels
    for b, label in enumerate(["DUB", "DUB", "DUB", "DISH"]):
        bx = viz_x + b * (beat_block_w + 4)
        label_bbox = draw.textbbox((0, 0), label, font=font_small)
        label_w = label_bbox[2] - label_bbox[0]
        label_color = GOLD_DIM if current_beat_in_bar == b and beat_frac < 0.15 else (50, 50, 60)
        draw.text(
            (bx + (beat_block_w - label_w) // 2, viz_y + 12),
            label,
            font=font_small,
            fill=label_color,
        )

    # --- Progress bar ---
    prog_y = VIDEO_SIZE[1] - 22
    progress = frame_time / TOTAL_DURATION
    prog_w = VIDEO_SIZE[0] - 80
    draw.rounded_rectangle(
        [(40, prog_y), (40 + prog_w, prog_y + 4)],
        radius=2,
        fill=(25, 25, 35),
    )
    filled_w = int(prog_w * progress)
    if filled_w > 0:
        draw.rounded_rectangle(
            [(40, prog_y), (40 + filled_w, prog_y + 4)],
            radius=2,
            fill=GOLD,
        )

    # Time display
    minutes = int(frame_time // 60)
    seconds = int(frame_time % 60)
    total_min = int(TOTAL_DURATION // 60)
    total_sec = int(TOTAL_DURATION % 60)
    time_str = f"{minutes}:{seconds:02d} / {total_min}:{total_sec:02d}"
    time_bbox = draw.textbbox((0, 0), time_str, font=font_small)
    draw.text(
        (VIDEO_SIZE[0] - (time_bbox[2] - time_bbox[0]) - 40, prog_y - 16),
        time_str,
        font=font_small,
        fill=DIM,
    )

    # Branding
    brand = "People for Peace"
    draw.text((40, prog_y - 16), brand, font=font_small, fill=DIM)

    return frame


def main() -> None:
    """Generate the final V3 video with verified memorial data."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("🎬 Building Final Video V3 (memorial-data.js source of truth)...")
    print(f"   Duration: {TOTAL_DURATION:.1f}s ({TOTAL_DURATION / 60:.1f} min)")
    print(f"   Frames: {TOTAL_FRAMES}")
    print(f"   Resolution: {VIDEO_SIZE[0]}×{VIDEO_SIZE[1]}")
    print()

    print("Loading photos...")
    photos, names = load_photos(PHOTO_DIR)
    print(f"  Loaded {len(photos)} photos ({sum(1 for n in names if n)} with names)")

    # Calculate cell dimensions
    cell_w = (VIDEO_SIZE[0] - 2 * GRID_PADDING - (GRID_COLS - 1) * GRID_GAP) // GRID_COLS
    cell_h = (
        VIDEO_SIZE[1] - TOP_AREA - BOTTOM_AREA - 2 * GRID_PADDING - (GRID_ROWS - 1) * GRID_GAP
    ) // GRID_ROWS

    # --- Step 1: Mix audio ---
    print("\nStep 1: Mixing audio tracks...")
    mixed_audio = OUTPUT_DIR / "_mixed_temp.wav"

    # Mix: Suno vocals (full volume) + our beat (15% volume for subtle depth)
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", str(VOCAL_FILE),
        "-i", str(BEAT_FILE),
        "-filter_complex",
        "[0:a]volume=1.0,aformat=sample_rates=44100:channel_layouts=stereo[vocals];"
        "[1:a]volume=0.15,aformat=sample_rates=44100:channel_layouts=stereo[beat];"
        "[vocals][beat]amix=inputs=2:duration=first:normalize=0[out]",
        "-map", "[out]",
        "-ac", "2",
        "-ar", "44100",
        str(mixed_audio),
    ]
    result = subprocess.run(mix_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ⚠ Beat mix failed, using vocals only: {result.stderr[-200:]}")
        mixed_audio = VOCAL_FILE
    else:
        print("  ✅ Audio mixed (vocals + subtle beat)")

    # --- Step 2: Generate video frames → pipe to ffmpeg ---
    output_path = OUTPUT_DIR / "100_faces_FINAL_V3.mp4"

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{VIDEO_SIZE[0]}x{VIDEO_SIZE[1]}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(mixed_audio),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",  # higher quality for final
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",  # web-optimized
        str(output_path),
    ]

    print(f"\nStep 2: Encoding video ({TOTAL_FRAMES} frames)...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    for frame_num in range(TOTAL_FRAMES):
        frame_time = frame_num / FPS
        frame = create_frame(photos, names, frame_time, cell_w, cell_h)
        proc.stdin.write(frame.tobytes())

        if (frame_num + 1) % (FPS * 15) == 0:
            elapsed_s = (frame_num + 1) / FPS
            pct = (frame_num + 1) / TOTAL_FRAMES * 100
            print(f"  → {elapsed_s:.0f}s / {TOTAL_DURATION:.0f}s ({pct:.0f}%)")

    proc.stdin.close()
    stderr = proc.communicate()[1]

    # Cleanup temp
    temp_audio = OUTPUT_DIR / "_mixed_temp.wav"
    if temp_audio.exists():
        temp_audio.unlink()

    if proc.returncode != 0:
        print(f"❌ ffmpeg error:\n{stderr.decode()[-500:]}")
    else:
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\n🎉 FINAL VIDEO V3: {output_path}")
        print(f"   Size: {file_size_mb:.1f} MB")
        print(f"   Duration: {TOTAL_DURATION:.1f}s ({TOTAL_DURATION / 60:.1f} min)")
        print(f"   Resolution: {VIDEO_SIZE[0]}×{VIDEO_SIZE[1]}")
        print(f"   Audio: Suno track 2 + subtle beat mix")
        print(f"   Names: overlaid on each child's photo")
        print(f"   Lyrics: synced from audio waveform analysis")
        print(f"\n   Ready to upload! 🚀")


if __name__ == "__main__":
    main()

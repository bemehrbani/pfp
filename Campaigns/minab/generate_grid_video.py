#!/usr/bin/env python3
"""
3×3 Grid Video Generator for "100 Faces of Peace" rap.
Creates an MP4 video where children's faces are displayed in a 3×3 grid,
changing every snare hit (beat 4 + 4.5, the "dish at dish").

Synced to the beat at 85 BPM.
Uses Pillow for frame generation + ffmpeg for MP4 encoding.
"""

import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# --- Configuration ---
VIDEO_SIZE = (1080, 1080)
FPS = 30
BPM = 85
BEAT_DURATION = 60.0 / BPM  # ~0.706s
BAR_DURATION = BEAT_DURATION * 4  # ~2.824s
TOTAL_BARS = 48
TOTAL_DURATION = TOTAL_BARS * BAR_DURATION  # ~135.5s

PHOTO_DIR = Path(__file__).parent / "splitted_photos"
MUSIC_FILE = Path(__file__).parent / "music" / "100_faces_beat.wav"
OUTPUT_DIR = Path(__file__).parent / "music"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Helvetica.ttc"

BG_COLOR = (10, 10, 18)
GRID_LINE_COLOR = (232, 190, 92, 100)  # gold, semi-transparent
TEXT_BG = (10, 10, 18, 200)
GOLD = (232, 190, 92)
WHITE = (255, 255, 255)
DIM = (160, 160, 170)

# Grid layout
GRID_COLS = 3
GRID_ROWS = 3
GRID_GAP = 6
GRID_PADDING = 20
TOP_AREA = 80  # space for title
BOTTOM_AREA = 120  # space for lyrics

# --- Lyrics sync (bar number → lyrics line) ---
LYRICS_SYNC = {
    # INTRO (bars 0-7)
    0: "Look at their eyes, look at their face",
    1: "A hundred children from a forgotten place",
    2: "Minab to the world, we carry their voice",
    3: "Peace ain't a privilege — it's a right, not a choice",
    4: "",
    5: "",
    6: "",
    7: "",
    # VERSE 1 (bars 8-15)
    8: "Zahra wants a pencil, Parsa wants a book",
    9: "Amirali dreams of a future — take a look",
    10: "Asma paints in colors that the world won't see",
    11: "Sobhan's in a classroom where he can't be free",
    12: "A hundred names, a hundred faces on the wall",
    13: "Every single one of them too young to fall",
    14: "Reza, Makan, Sina — do you hear them call?",
    15: "From Minab to the world, we speak for them all",
    # HOOK 1 (bars 16-23)
    16: "🔊 Dub dub dub — DISH — can you hear the beat?",
    17: "A hundred hearts are marching down the street",
    18: "🔊 Dub dub dub — DISH — every face you see",
    19: "Is a child who's asking: Won't you fight for me?",
    20: "🔊 Dub dub dub — DISH — can you hear the beat?",
    21: "A hundred hearts are marching down the street",
    22: "🔊 Dub dub dub — DISH — every face you see",
    23: "Is a child who's asking: Won't you fight for me?",
    # VERSE 2 (bars 24-31)
    24: "Sanctions hit the hospitals, the schools, the bread",
    25: "Politicians sleeping while the children aren't fed",
    26: "She was gonna be a doctor, he was gonna fly",
    27: "But the world looked away and nobody asked why",
    28: "Every face a statistic, every name erased",
    29: "Every dream is broken, every hope displaced",
    30: "But we don't scroll past — nah, we stop and stare",
    31: "'Cause a hundred children need to know we care",
    # HOOK 2 (bars 32-39)
    32: "🔊 Dub dub dub — DISH — can you hear the beat?",
    33: "A hundred hearts are marching down the street",
    34: "🔊 Dub dub dub — DISH — every face you see",
    35: "Is a child who's asking: Won't you fight for me?",
    36: "🔊 Dub dub dub — DISH — can you hear the beat?",
    37: "A hundred hearts are marching down the street",
    38: "🔊 Dub dub dub — DISH — every face you see",
    39: "Is a child who's asking: Won't you fight for me?",
    # BRIDGE (bars 40-43)
    40: "One share is a ripple, a hundred is a wave",
    41: "One voice in the silence might be all it takes to save",
    42: "Look 'em in the eyes — they're watching you",
    43: "What are you gonna do?",
    # OUTRO (bars 44-47)
    44: "A hundred faces... a hundred dreams...",
    45: "People for Peace — that's what it means",
    46: "Minab to the world, we won't be ignored",
    47: "Every. Child. Deserves. More.",
}


def load_photos(photo_dir: Path) -> list[Image.Image]:
    """Load all child photos as square-cropped thumbnails."""
    photo_paths = sorted(
        [p for p in photo_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")],
        key=lambda p: p.name,
    )

    cell_w = (VIDEO_SIZE[0] - 2 * GRID_PADDING - (GRID_COLS - 1) * GRID_GAP) // GRID_COLS
    cell_h = (
        VIDEO_SIZE[1] - TOP_AREA - BOTTOM_AREA - 2 * GRID_PADDING - (GRID_ROWS - 1) * GRID_GAP
    ) // GRID_ROWS

    photos = []
    for pp in photo_paths:
        try:
            img = Image.open(pp).convert("RGB")
            # Crop to fill the cell
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
        except Exception:
            pass

    return photos


def get_face_set(photos: list[Image.Image], set_index: int) -> list[Image.Image]:
    """Get 9 photos for the grid, cycling through the collection."""
    result = []
    for i in range(9):
        idx = (set_index * 9 + i) % len(photos)
        result.append(photos[idx])
    return result


def create_frame(
    photos: list[Image.Image],
    face_set: list[Image.Image],
    prev_face_set: list[Image.Image] | None,
    transition_progress: float,
    current_bar: int,
    beat_in_bar: float,
    frame_time: float,
) -> Image.Image:
    """Create a single video frame."""
    frame = Image.new("RGBA", VIDEO_SIZE, (*BG_COLOR, 255))
    draw = ImageDraw.Draw(frame)

    try:
        font_title = ImageFont.truetype(FONT_BOLD, 28)
        font_lyrics = ImageFont.truetype(FONT_BOLD, 22)
        font_small = ImageFont.truetype(FONT_REGULAR, 16)
    except OSError:
        font_title = font_lyrics = font_small = ImageFont.load_default()

    # --- Title bar ---
    title = "100 FACES OF PEACE"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = bbox[2] - bbox[0]
    draw.text(
        ((VIDEO_SIZE[0] - title_w) // 2, 25),
        title,
        font=font_title,
        fill=GOLD,
    )

    # --- 3×3 grid ---
    cell_w = (VIDEO_SIZE[0] - 2 * GRID_PADDING - (GRID_COLS - 1) * GRID_GAP) // GRID_COLS
    cell_h = (
        VIDEO_SIZE[1] - TOP_AREA - BOTTOM_AREA - 2 * GRID_PADDING - (GRID_ROWS - 1) * GRID_GAP
    ) // GRID_ROWS

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            idx = row * GRID_COLS + col
            x = GRID_PADDING + col * (cell_w + GRID_GAP)
            y = TOP_AREA + GRID_PADDING + row * (cell_h + GRID_GAP)

            # Get current photo (with optional transition)
            photo = face_set[idx]

            if prev_face_set is not None and transition_progress < 1.0:
                # Cross-fade between old and new face set
                old_photo = prev_face_set[idx]
                blended = Image.blend(old_photo, photo, transition_progress)
                frame.paste(blended.convert("RGBA"), (x, y))
            else:
                frame.paste(photo.convert("RGBA"), (x, y))

            # Beat pulse effect — flash border on kick hits
            beat_phase = beat_in_bar % 1.0
            if beat_phase < 0.1:  # just hit a beat
                # Gold border glow
                glow_alpha = int(180 * (1 - beat_phase / 0.1))
                draw.rectangle(
                    [(x - 2, y - 2), (x + cell_w + 1, y + cell_h + 1)],
                    outline=(*GOLD, glow_alpha),
                    width=2,
                )

    # --- Grid lines (subtle gold) ---
    for col in range(1, GRID_COLS):
        line_x = GRID_PADDING + col * (cell_w + GRID_GAP) - GRID_GAP // 2
        draw.line(
            [(line_x, TOP_AREA + GRID_PADDING), (line_x, VIDEO_SIZE[1] - BOTTOM_AREA - GRID_PADDING)],
            fill=(40, 36, 20),
            width=1,
        )

    # --- Lyrics overlay ---
    lyrics_y = VIDEO_SIZE[1] - BOTTOM_AREA + 10

    # Dark background for lyrics area
    draw.rectangle(
        [(0, VIDEO_SIZE[1] - BOTTOM_AREA), (VIDEO_SIZE[0], VIDEO_SIZE[1])],
        fill=(10, 10, 18, 230),
    )

    # Divider line
    draw.line(
        [(30, lyrics_y - 5), (VIDEO_SIZE[0] - 30, lyrics_y - 5)],
        fill=GOLD,
        width=1,
    )

    lyric_line = LYRICS_SYNC.get(current_bar, "")
    if lyric_line:
        bbox = draw.textbbox((0, 0), lyric_line, font=font_lyrics)
        lyric_w = bbox[2] - bbox[0]
        lyric_x = max(20, (VIDEO_SIZE[0] - lyric_w) // 2)
        draw.text(
            (lyric_x, lyrics_y + 15),
            lyric_line,
            font=font_lyrics,
            fill=WHITE,
        )

    # Bottom branding
    brand = "People for Peace  ·  #100FacesOfPeace"
    bbox = draw.textbbox((0, 0), brand, font=font_small)
    brand_w = bbox[2] - bbox[0]
    draw.text(
        ((VIDEO_SIZE[0] - brand_w) // 2, VIDEO_SIZE[1] - 30),
        brand,
        font=font_small,
        fill=DIM,
    )

    return frame.convert("RGB")


def main() -> None:
    """Generate the 3×3 grid video."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Loading photos...")
    photos = load_photos(PHOTO_DIR)
    print(f"  Loaded {len(photos)} photos")

    total_frames = int(TOTAL_DURATION * FPS)
    print(f"  Total frames: {total_frames}")
    print(f"  Duration: {TOTAL_DURATION:.1f}s")

    # Calculate snare hit times (when faces change)
    snare_times = []
    for bar in range(TOTAL_BARS):
        bar_start = bar * BAR_DURATION
        # Snare on beat 4 (index 3)
        snare_times.append(bar_start + 3 * BEAT_DURATION)
        # Second snare on beat 4.5 ("dish at dish")
        snare_times.append(bar_start + 3.5 * BEAT_DURATION)

    # Face change happens on every other snare (every bar basically)
    face_change_times = [bar * BAR_DURATION for bar in range(TOTAL_BARS)]

    # Pipe frames directly to ffmpeg
    output_path = OUTPUT_DIR / "100_faces_grid_video.mp4"

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{VIDEO_SIZE[0]}x{VIDEO_SIZE[1]}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(MUSIC_FILE),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        str(output_path),
    ]

    print(f"\nStarting ffmpeg encode → {output_path}")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    current_face_set_idx = 0
    prev_face_set = None
    current_face_set = get_face_set(photos, 0)
    last_change_time = 0

    transition_duration = 0.15  # seconds for cross-fade

    for frame_num in range(total_frames):
        frame_time = frame_num / FPS

        # Current bar and beat
        current_bar = min(int(frame_time / BAR_DURATION), TOTAL_BARS - 1)
        beat_in_bar = (frame_time % BAR_DURATION) / BEAT_DURATION

        # Check if we should change faces (on snare hit / every bar)
        if current_bar != int(last_change_time / BAR_DURATION):
            current_face_set_idx += 1
            prev_face_set = current_face_set
            current_face_set = get_face_set(photos, current_face_set_idx)
            last_change_time = frame_time

        # Transition progress
        time_since_change = frame_time - (current_bar * BAR_DURATION)
        if time_since_change < transition_duration:
            transition_progress = time_since_change / transition_duration
        else:
            transition_progress = 1.0
            prev_face_set = None

        frame = create_frame(
            photos,
            current_face_set,
            prev_face_set,
            transition_progress,
            current_bar,
            beat_in_bar,
            frame_time,
        )

        proc.stdin.write(frame.tobytes())

        if (frame_num + 1) % (FPS * 10) == 0:
            elapsed_s = (frame_num + 1) / FPS
            print(f"  → {elapsed_s:.0f}s / {TOTAL_DURATION:.0f}s ({(frame_num + 1) / total_frames * 100:.0f}%)")

    proc.stdin.close()
    stderr = proc.communicate()[1]
    if proc.returncode != 0:
        print(f"ffmpeg error:\n{stderr.decode()}")
    else:
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\n🎉 Video generated: {output_path}")
        print(f"   Size: {file_size_mb:.1f} MB")
        print(f"   Duration: {TOTAL_DURATION:.1f}s")
        print(f"   Resolution: {VIDEO_SIZE[0]}×{VIDEO_SIZE[1]}")
        print(f"   FPS: {FPS}")


if __name__ == "__main__":
    main()

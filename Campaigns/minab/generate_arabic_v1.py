#!/usr/bin/env python3
"""
Arabic Version — مئة وجه للسلام (100 Faces of Peace)

Creates the Arabic 1080x1080 MP4:
1. 3×3 grid with children's faces + names overlaid
2. Suno Arabic vocal track as primary audio
3. Our synthesized beat mixed underneath at low volume
4. Synced Arabic lyrics (actual Suno lyrics), beat pulse effects

Source of truth: ../frontend/public/memorial-data.js
Photos: ../frontend/public/images/children/child_rXX_cXX.jpg
"""

import math
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
VIDEO_SIZE = (1080, 1080)
FPS = 30
BPM = 85
BEAT_DURATION = 60.0 / BPM

# Duration matches the Arabic Suno track
TOTAL_DURATION = 204.5
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

PHOTO_DIR = Path(__file__).parent.parent / "frontend" / "public" / "images" / "children"
MEMORIAL_DATA_JS = Path(__file__).parent.parent / "frontend" / "public" / "memorial-data.js"
VOCAL_FILE = Path(__file__).parent / "music" / "# مئة وجه للسلام — كلمات راب عربي.mp3"
BEAT_FILE = Path(__file__).parent / "music" / "100_faces_beat.wav"
OUTPUT_DIR = Path(__file__).parent / "music"

# Fonts
FONT_LATIN_REG = "/System/Library/Fonts/Helvetica.ttc"
FONT_ARABIC = "/System/Library/Fonts/GeezaPro.ttc"

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
BOTTOM_AREA = 120  # Room for lyrics

CHANGE_INTERVAL_BEATS = 4
CHANGE_INTERVAL_SEC = CHANGE_INTERVAL_BEATS * BEAT_DURATION


# --- Actual Arabic lyrics synced to the Suno track ---
# Audio: intro 0-10s (instrumental), vocals ~10-136s, bridge ~136-155s, final ~158-203s
# Structure: V1(12 lines ~10-50s) → H1(8 lines ~50-78s) → V2(12 lines ~78-118s)
#          → H2(8 lines ~118-146s) → Bridge(3 lines ~146-158s) → Final(~158-200s)
LYRICS_TIMED = [
    # [Intro - instrumental, 10 seconds]
    (0.0, ""),

    # [Verse 1] — 12 lines, ~10s to ~50s (~3.3s per line)
    (10.0, "بُصّ في عيونهم، شوف وُشوشهم"),
    (13.5, "مية طفل من بلاد بعيدة، مية حلم"),
    (17.0, "من ميناب للعالم، إحنا صوتهم بنوصّله"),
    (20.5, "السلام حقّنا — مش هدية، مش تفضّل"),
    (24.0, ""),  # stanza break

    (25.0, "زهرة عايزة قلم، بارسا عايز كتاب"),
    (28.5, "أمير علي بيحلم بمستقبل — يا ترى مين جاب?"),
    (32.0, "أسماء بترسم ألوان العالم مش شايفها"),
    (35.5, "سبحان في فصل ما فيه حرية واقفة"),
    (39.0, ""),  # stanza break

    (40.0, "مية اسم، مية وجه عالحيطان"),
    (43.5, "كل واحد فيهم صغير على هالزمان"),
    (47.0, "رضا، مكان، سينا — سامع صوتهم?"),
    (50.5, "من ميناب للعالم، إحنا بنتكلم عنهم"),

    # [Hook 1] — 8 lines, ~53s to ~78s
    (53.0, ""),
    (54.0, "مية وجه، مية صوت — إحنا لسّه هون"),
    (57.5, "مية قلب تحت الرُكام، لسّه كلّه حنون"),
    (61.0, "مية حلم ضاع بنُصّه — لا تنساهم"),
    (64.5, "طفل بيقولّك: مش هتحارب عشاني?"),
    (68.0, ""),
    (69.0, "مية وجه، مية صوت — إحنا لسّه هون"),
    (72.5, "مية قلب تحت الرُكام، لسّه كلّه حنون"),
    (76.0, "مية حلم ضاع بنُصّه — لا تنساهم"),
    (79.0, "طفل بيقولّك: مش هتحارب عشاني?"),

    # [Verse 2] — 12 lines, ~81s to ~118s (~3.1s per line)
    (81.0, ""),
    (82.0, "من غزة لميناب، نفس الدمعة بتنزل"),
    (85.0, "أطفال ما رجعوش من المدرسة، نفس المشهد"),
    (88.0, "هناك بنت كانت بدها تصير دكتورة"),
    (91.0, "وهون ولد كان بده يطير — بس الدنيا مظلومة"),
    (94.0, ""),

    (95.0, "الحصار ضرب المستشفى، المدرسة، الخبز"),
    (98.0, "سياسيين نايمين والأطفال جوعانة بنفس الوقت"),
    (101.0, "كل وجه صار رقم، كل اسم انمحى"),
    (104.0, "كل حلم انكسر، كل أمل انطفى"),
    (107.0, ""),

    (108.0, "بس إحنا ما بنعدّي — لأ، بنوقف ونشوف"),
    (111.0, "لأن مية طفل لازم يعرفوا إنّا منوقف صفوف"),
    (114.0, "من غزة لميناب، نفس الحرب ونفس الألم"),
    (117.0, "نفس الدموع، نفس الأطفال، ونفس الظلم"),

    # [Hook 2] — 8 lines, ~119s to ~144s
    (119.0, ""),
    (120.0, "مية وجه، مية صوت — إحنا لسّه هون"),
    (123.5, "مية قلب تحت الرُكام، لسّه كلّه حنون"),
    (127.0, "مية حلم ضاع بنُصّه — لا تنساهم"),
    (130.5, "طفل بيقولّك: مش هتحارب عشاني?"),
    (134.0, ""),
    (135.0, "مية وجه، مية صوت — إحنا لسّه هون"),
    (138.5, "مية قلب تحت الرُكام، لسّه كلّه حنون"),
    (142.0, "مية حلم ضاع بنُصّه — لا تنساهم"),
    (145.0, "طفل بيقولّك: مش هتحارب عشاني?"),

    # [Bridge] — 3 lines, ~147s to ~158s (slower, emotional — energy dips at 136-155s)
    (147.0, ""),
    (148.0, "مشاركة وحدة موجة صغيرة، مية مشاركة تسونامي"),
    (152.0, "صوت واحد بالصمت ممكن يكون اللي ينقذهم"),
    (156.0, "بُصّ في عيونهم — دول بيتطلّعوا عليك"),

    # [Final Section] — ~159s to ~200s
    (159.0, ""),
    (160.0, "مية وجه... مية حلم..."),
    (163.0, "شعوب من أجل السلام — هاد معناها"),
    (166.0, "شو رح تعمل إنت?"),
    (169.0, ""),
    (170.0, "من غزة لميناب، مش رح نسكت أبداً"),
    (173.0, "كل. طفل. يستاهل. أكتر."),

    (176.0, "مية وجه، مية صوت — إحنا لسّه هون"),
    (179.0, "مية قلب تحت الرُكام، لسّه كلّه حنون"),
    (182.0, "مية حلم ضاع بنُصّه — لا تنساهم"),
    (185.0, "طفل بيقولّك: مش هتحارب عشاني?"),

    (188.0, "كل. طفل. يستاهل. أكتر."),

    (191.0, "مية وجه، مية صوت — إحنا لسّه هون"),
    (194.0, "مية قلب تحت الرُكام، لسّه كلّه حنون"),
    (197.0, "طفل بيقولّك: مش هتحارب عشاني?"),

    # Fade
    (200.0, ""),
]


def parse_memorial_data() -> list[dict]:
    """Parse memorial-data.js to get verified children."""
    text = MEMORIAL_DATA_JS.read_text(encoding="utf-8")
    children: list[dict] = []
    for match in re.finditer(
        r'\{\s*id:\s*"([^"]+)".*?name:\s*"([^"]+)".*?'
        r'nameFa:\s*"([^"]+)".*?'
        r'photoGrid:\s*"(r\d+_c\d+)"',
        text,
        re.DOTALL,
    ):
        child_id, name_en, name_fa, grid = match.groups()
        photo_file = f"child_{grid}.jpg"
        children.append({
            "id": child_id,
            "name_en": name_en,
            "name_fa": name_fa,
            "photo": photo_file,
            "grid": grid,
        })
    children.sort(
        key=lambda c: (int(c["grid"].split("_")[0][1:]), int(c["grid"].split("_")[1][1:]))
    )
    return children


def load_photos(photo_dir: Path) -> tuple[list[Image.Image], list[str | None]]:
    """Load child photos with Arabic-script names."""
    memorial_children = parse_memorial_data()
    print(f"  Memorial data: {len(memorial_children)} children with photos")

    cell_w = (VIDEO_SIZE[0] - 2 * GRID_PADDING - (GRID_COLS - 1) * GRID_GAP) // GRID_COLS
    cell_h = (
        VIDEO_SIZE[1] - TOP_AREA - BOTTOM_AREA - 2 * GRID_PADDING - (GRID_ROWS - 1) * GRID_GAP
    ) // GRID_ROWS

    photos: list[Image.Image] = []
    names: list[str | None] = []
    for child in memorial_children:
        photo_path = photo_dir / child["photo"]
        if not photo_path.exists():
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
            names.append(child["name_fa"])
        except Exception as exc:
            print(f"  ⚠ Error loading {child['photo']}: {exc}")

    print(f"  Named: {sum(1 for n in names if n)} / {len(photos)}")
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


def draw_rtl_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
    anchor: str = "lt",
) -> None:
    """Draw RTL (Arabic) text with proper shaping via raqm engine."""
    if not text:
        return
    draw.text(xy, text, font=font, fill=fill, anchor=anchor, direction="rtl", language="ar")


def get_rtl_text_width(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
) -> int:
    """Get the width of RTL text."""
    bbox = draw.textbbox((0, 0), text, font=font, direction="rtl", language="ar")
    return bbox[2] - bbox[0]


def create_frame(
    photos: list[Image.Image],
    names: list[str | None],
    frame_time: float,
    cell_w: int,
    cell_h: int,
    font_latin_small: ImageFont.FreeTypeFont,
    font_ar_title: ImageFont.FreeTypeFont,
    font_ar_lyrics: ImageFont.FreeTypeFont,
    font_ar_name: ImageFont.FreeTypeFont,
    font_ar_small: ImageFont.FreeTypeFont,
) -> Image.Image:
    """Create a single polished video frame with Arabic text."""
    frame = Image.new("RGB", VIDEO_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(frame)

    beat_frac = (frame_time / BEAT_DURATION) % 1.0
    current_beat_in_bar = int((frame_time / BEAT_DURATION) % 4)

    change_index = int(frame_time / CHANGE_INTERVAL_SEC)
    transition_time = frame_time % CHANGE_INTERVAL_SEC
    transition_progress = min(1.0, transition_time / 0.2)

    # --- Title (Arabic) ---
    title_alpha_mult = 0.85 + 0.15 * math.sin(frame_time * 1.5)
    title = "مئة وجه للسلام"
    title_w = get_rtl_text_width(draw, title, font_ar_title)
    title_color = tuple(int(c * title_alpha_mult) for c in GOLD)
    draw_rtl_text(
        draw,
        ((VIDEO_SIZE[0] + title_w) // 2, 18),
        title,
        font_ar_title,
        title_color,
        anchor="rt",
    )

    draw.line([(40, TOP_AREA - 6), (VIDEO_SIZE[0] - 40, TOP_AREA - 6)], fill=GOLD_DIM, width=1)

    # --- 3×3 Grid ---
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            idx = row * GRID_COLS + col
            x = GRID_PADDING + col * (cell_w + GRID_GAP)
            y = TOP_AREA + GRID_PADDING + row * (cell_h + GRID_GAP)

            photo_idx = (change_index * 9 + idx) % len(photos)
            photo = photos[photo_idx]

            if transition_progress < 1.0:
                prev_idx = ((change_index - 1) * 9 + idx) % len(photos)
                prev_photo = photos[prev_idx]
                blended = Image.blend(prev_photo, photo, transition_progress)
                frame.paste(blended, (x, y))
            else:
                frame.paste(photo, (x, y))

            # --- Name overlay ---
            child_name = names[photo_idx]
            if child_name:
                strip_h = 30
                strip_y = y + cell_h - strip_h
                overlay = Image.new("RGBA", (cell_w, strip_h), (0, 0, 0, 0))
                ov_draw = ImageDraw.Draw(overlay)
                for gy in range(strip_h):
                    alpha = int(190 * (gy / strip_h))
                    ov_draw.line([(0, gy), (cell_w, gy)], fill=(0, 0, 0, alpha))
                frame.paste(overlay, (x, strip_y), overlay)

                first_name = child_name.split()[0]
                name_w = get_rtl_text_width(draw, first_name, font_ar_name)
                draw_rtl_text(
                    draw,
                    (x + (cell_w + name_w) // 2, strip_y + strip_h - 22),
                    first_name,
                    font_ar_name,
                    (255, 255, 255, 230),
                    anchor="rt",
                )

            # Beat pulse border
            if beat_frac < 0.08:
                intensity = int(200 * (1 - beat_frac / 0.08))
                if current_beat_in_bar < 3:
                    border_color = (intensity // 2, intensity // 2, intensity // 2)
                else:
                    border_color = (intensity, int(intensity * 0.75), int(intensity * 0.3))
                draw.rectangle(
                    [(x - 1, y - 1), (x + cell_w, y + cell_h)],
                    outline=border_color, width=2,
                )

    # --- Bottom area: Lyrics + beat viz + progress ---
    bottom_y = VIDEO_SIZE[1] - BOTTOM_AREA
    draw.rectangle([(0, bottom_y), (VIDEO_SIZE[0], VIDEO_SIZE[1])], fill=LYRIC_BG)
    draw.line([(30, bottom_y + 4), (VIDEO_SIZE[0] - 30, bottom_y + 4)], fill=GOLD_DIM, width=1)

    # Current lyric (Arabic — RTL)
    lyric = get_current_lyric(frame_time)
    if lyric:
        lyric_w = get_rtl_text_width(draw, lyric, font_ar_lyrics)
        lyric_x = (VIDEO_SIZE[0] + lyric_w) // 2
        draw_rtl_text(draw, (lyric_x, bottom_y + 14), lyric, font_ar_lyrics, WHITE, anchor="rt")

    # --- Beat visualizer ---
    viz_y = bottom_y + 55
    viz_width = VIDEO_SIZE[0] - 80
    viz_x = 40
    beat_block_w = viz_width // 4 - 4
    for b in range(4):
        bx = viz_x + b * (beat_block_w + 4)
        is_active = current_beat_in_bar == b and beat_frac < 0.15
        color = (GOLD if b < 3 else (255, 120, 80)) if is_active else (30, 30, 40)
        draw.rounded_rectangle([(bx, viz_y), (bx + beat_block_w, viz_y + 8)], radius=4, fill=color)

    # --- Progress bar ---
    prog_y = VIDEO_SIZE[1] - 22
    progress = frame_time / TOTAL_DURATION
    prog_w = VIDEO_SIZE[0] - 80
    draw.rounded_rectangle([(40, prog_y), (40 + prog_w, prog_y + 4)], radius=2, fill=(25, 25, 35))
    filled_w = int(prog_w * progress)
    if filled_w > 0:
        draw.rounded_rectangle([(40, prog_y), (40 + filled_w, prog_y + 4)], radius=2, fill=GOLD)

    # Time display (Latin font)
    minutes = int(frame_time // 60)
    seconds = int(frame_time % 60)
    total_min = int(TOTAL_DURATION // 60)
    total_sec = int(TOTAL_DURATION % 60)
    time_str = f"{minutes}:{seconds:02d} / {total_min}:{total_sec:02d}"
    time_bbox = draw.textbbox((0, 0), time_str, font=font_latin_small)
    draw.text(
        (VIDEO_SIZE[0] - (time_bbox[2] - time_bbox[0]) - 40, prog_y - 16),
        time_str, font=font_latin_small, fill=DIM,
    )

    # Branding (Arabic)
    brand = "شعوب من أجل السلام"
    draw_rtl_text(draw, (40, prog_y - 18), brand, font_ar_small, DIM)

    return frame


def main() -> None:
    """Generate the Arabic version of the video."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("🎬 بناء الفيديو العربي — مئة وجه للسلام...")
    print(f"   Duration: {TOTAL_DURATION:.1f}s ({TOTAL_DURATION / 60:.1f} min)")
    print(f"   Frames: {TOTAL_FRAMES}")
    print(f"   Resolution: {VIDEO_SIZE[0]}×{VIDEO_SIZE[1]}")
    print()

    try:
        font_latin_small = ImageFont.truetype(FONT_LATIN_REG, 14)
        font_ar_title = ImageFont.truetype(FONT_ARABIC, 30)
        font_ar_lyrics = ImageFont.truetype(FONT_ARABIC, 20)
        font_ar_name = ImageFont.truetype(FONT_ARABIC, 15)
        font_ar_small = ImageFont.truetype(FONT_ARABIC, 14)
    except OSError as exc:
        print(f"⚠ Font error: {exc}")
        return

    print("Loading photos...")
    photos, names = load_photos(PHOTO_DIR)
    print(f"  Loaded {len(photos)} photos")

    cell_w = (VIDEO_SIZE[0] - 2 * GRID_PADDING - (GRID_COLS - 1) * GRID_GAP) // GRID_COLS
    cell_h = (
        VIDEO_SIZE[1] - TOP_AREA - BOTTOM_AREA - 2 * GRID_PADDING - (GRID_ROWS - 1) * GRID_GAP
    ) // GRID_ROWS

    # --- Step 1: Mix audio ---
    print("\nStep 1: Mixing audio tracks...")
    mixed_audio = OUTPUT_DIR / "_mixed_temp_ar.wav"
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", str(VOCAL_FILE), "-i", str(BEAT_FILE),
        "-filter_complex",
        "[0:a]volume=1.0,aformat=sample_rates=44100:channel_layouts=stereo[vocals];"
        "[1:a]volume=0.15,aformat=sample_rates=44100:channel_layouts=stereo[beat];"
        "[vocals][beat]amix=inputs=2:duration=first:normalize=0[out]",
        "-map", "[out]", "-ac", "2", "-ar", "44100",
        str(mixed_audio),
    ]
    result = subprocess.run(mix_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ⚠ Beat mix failed, using vocals only")
        mixed_audio = VOCAL_FILE
    else:
        print("  ✅ Audio mixed")

    # --- Step 2: Generate video ---
    output_path = OUTPUT_DIR / "100_faces_ARABIC_V1.mp4"
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{VIDEO_SIZE[0]}x{VIDEO_SIZE[1]}",
        "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-i", str(mixed_audio),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path),
    ]

    print(f"\nStep 2: Encoding video ({TOTAL_FRAMES} frames)...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    for frame_num in range(TOTAL_FRAMES):
        frame_time = frame_num / FPS
        frame = create_frame(
            photos, names, frame_time, cell_w, cell_h,
            font_latin_small, font_ar_title, font_ar_lyrics,
            font_ar_name, font_ar_small,
        )
        proc.stdin.write(frame.tobytes())
        if (frame_num + 1) % (FPS * 15) == 0:
            elapsed_s = (frame_num + 1) / FPS
            pct = (frame_num + 1) / TOTAL_FRAMES * 100
            print(f"  → {elapsed_s:.0f}s / {TOTAL_DURATION:.0f}s ({pct:.0f}%)")

    proc.stdin.close()
    stderr = proc.communicate()[1]

    temp_audio = OUTPUT_DIR / "_mixed_temp_ar.wav"
    if temp_audio.exists():
        temp_audio.unlink()

    if proc.returncode != 0:
        print(f"❌ ffmpeg error:\n{stderr.decode()[-500:]}")
    else:
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\n🎉 الفيديو العربي: {output_path}")
        print(f"   Size: {file_size_mb:.1f} MB")
        print(f"   Duration: {TOTAL_DURATION:.1f}s ({TOTAL_DURATION / 60:.1f} min)")
        print(f"   Lyrics: Synced to actual Suno track")
        print(f"\n   !جاهز للرفع 🚀")


if __name__ == "__main__":
    main()

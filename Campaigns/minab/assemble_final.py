#!/usr/bin/env python3
"""
Final Assembly Script — merges vocal recording with beat and video.

Usage:
    python3 assemble_final.py path/to/vocals.wav

The vocals WAV will be mixed with the beat and synced to the grid video.
Output: music/100_faces_FINAL.mp4
"""

import sys
import subprocess
from pathlib import Path

MUSIC_DIR = Path(__file__).parent / "music"
BEAT_FILE = MUSIC_DIR / "100_faces_beat.wav"
VIDEO_FILE = MUSIC_DIR / "100_faces_grid_video.mp4"
OUTPUT_FILE = MUSIC_DIR / "100_faces_FINAL.mp4"


def main() -> None:
    """Assemble the final video."""
    if len(sys.argv) < 2:
        print("Usage: python3 assemble_final.py <vocals.wav>")
        print()
        print("This script mixes your vocal recording with the beat")
        print("and syncs it to the grid video to produce the final MP4.")
        sys.exit(1)

    vocals_path = Path(sys.argv[1])
    if not vocals_path.exists():
        print(f"❌ Vocal file not found: {vocals_path}")
        sys.exit(1)

    if not BEAT_FILE.exists():
        print(f"❌ Beat file not found: {BEAT_FILE}")
        print("   Run generate_beat.py first.")
        sys.exit(1)

    if not VIDEO_FILE.exists():
        print(f"❌ Video file not found: {VIDEO_FILE}")
        print("   Run generate_grid_video.py first.")
        sys.exit(1)

    print("🎬 Assembling final video...")
    print(f"   Beat:   {BEAT_FILE}")
    print(f"   Vocals: {vocals_path}")
    print(f"   Video:  {VIDEO_FILE}")
    print()

    # Step 1: Mix vocals + beat into a single audio track
    mixed_audio = MUSIC_DIR / "mixed_audio.wav"
    print("Step 1: Mixing vocals + beat...")
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", str(BEAT_FILE),
        "-i", str(vocals_path),
        "-filter_complex",
        # Beat at 70% volume, vocals at full volume
        "[0:a]volume=0.7[beat];[1:a]volume=1.0[vocals];[beat][vocals]amix=inputs=2:duration=longest",
        "-ac", "2",
        str(mixed_audio),
    ]
    result = subprocess.run(mix_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Audio mix failed:\n{result.stderr}")
        sys.exit(1)
    print("   ✅ Audio mixed")

    # Step 2: Merge mixed audio with video
    print("Step 2: Merging audio with video...")
    merge_cmd = [
        "ffmpeg", "-y",
        "-i", str(VIDEO_FILE),
        "-i", str(mixed_audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        str(OUTPUT_FILE),
    ]
    result = subprocess.run(merge_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Video merge failed:\n{result.stderr}")
        sys.exit(1)
    print("   ✅ Video merged")

    # Cleanup
    mixed_audio.unlink(missing_ok=True)

    file_size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\n🎉 FINAL VIDEO: {OUTPUT_FILE}")
    print(f"   Size: {file_size_mb:.1f} MB")
    print(f"\n   Upload to Twitter/Instagram and share! 🚀")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Beat Generator for "100 Faces of Peace" rap track.
Pattern: dub dub dub dish · dish (kick kick kick snare · snare)
BPM: 85 · Key: Em

Generates a complete instrumental WAV file with:
- Kick drum (synthesized sine wave with pitch drop)
- Snare (noise burst with bandpass)
- Hi-hat (high-freq noise, short decay)
- Sub-bass line (low sine, follows chord progression)
- Atmospheric pad (ambient texture)
"""

import struct
import wave
import math
import random
from pathlib import Path

import numpy as np

# --- Configuration ---
OUTPUT_DIR = Path(__file__).parent / "music"
SAMPLE_RATE = 44100
BPM = 85
BEAT_DURATION = 60.0 / BPM  # seconds per beat (~0.706s)
BAR_DURATION = BEAT_DURATION * 4  # seconds per bar (~2.824s)
TOTAL_BARS = 48  # ~2:15 total (with some extra room)
TOTAL_SAMPLES = int(TOTAL_BARS * BAR_DURATION * SAMPLE_RATE)

# --- Sound Synthesis Functions ---

def generate_kick(duration: float = 0.25, volume: float = 0.8) -> np.ndarray:
    """Synthesize a punchy kick drum — sine wave with pitch drop."""
    num_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # Pitch envelope: starts at 160Hz, drops to 45Hz
    freq_start = 160
    freq_end = 45
    decay_rate = 20
    freq = freq_end + (freq_start - freq_end) * np.exp(-decay_rate * t)

    # Phase accumulation for frequency sweep
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE

    # Amplitude envelope
    amp = np.exp(-5 * t) * volume

    # Add slight distortion for punch
    signal = np.sin(phase) * amp
    signal = np.tanh(signal * 2.5) * 0.7

    return signal


def generate_snare(duration: float = 0.2, volume: float = 0.55) -> np.ndarray:
    """Synthesize a snare — noise burst + body tone."""
    num_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # Noise component
    noise = np.random.uniform(-1, 1, num_samples)
    noise_env = np.exp(-12 * t)
    noise_part = noise * noise_env * 0.7

    # Body tone (200Hz sine)
    body = np.sin(2 * np.pi * 200 * t) * np.exp(-20 * t) * 0.4

    signal = (noise_part + body) * volume
    return signal


def generate_hihat(duration: float = 0.06, volume: float = 0.25) -> np.ndarray:
    """Synthesize a hi-hat — short high-freq noise."""
    num_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    noise = np.random.uniform(-1, 1, num_samples)
    # High-pass effect: differentiate
    noise_hp = np.diff(noise, prepend=0)
    env = np.exp(-40 * t)

    signal = noise_hp * env * volume
    return signal


def generate_open_hihat(duration: float = 0.2, volume: float = 0.2) -> np.ndarray:
    """Synthesize an open hi-hat — longer decay."""
    num_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    noise = np.random.uniform(-1, 1, num_samples)
    noise_hp = np.diff(noise, prepend=0)
    env = np.exp(-8 * t)

    signal = noise_hp * env * volume
    return signal


def generate_sub_bass(
    freq: float, duration: float, volume: float = 0.35
) -> np.ndarray:
    """Synthesize a sub-bass tone."""
    num_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # Smooth sine with slight saturation
    signal = np.sin(2 * np.pi * freq * t)
    # Soft envelope
    attack = np.minimum(t * 20, 1.0)
    release_start = duration - 0.05
    release = np.where(t > release_start, (duration - t) / 0.05, 1.0)
    env = attack * release

    signal = np.tanh(signal * 1.3) * env * volume
    return signal


def generate_pad(
    freq: float, duration: float, volume: float = 0.08
) -> np.ndarray:
    """Synthesize an atmospheric pad — detuned sines for warmth."""
    num_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # Three detuned oscillators
    sig1 = np.sin(2 * np.pi * freq * t)
    sig2 = np.sin(2 * np.pi * freq * 1.003 * t)
    sig3 = np.sin(2 * np.pi * freq * 0.997 * t)

    # Slow amplitude modulation (tremolo)
    tremolo = 0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t)

    # Soft attack/release
    attack = np.minimum(t * 2, 1.0)
    release_start = duration - 0.3
    release = np.where(t > release_start, (duration - t) / 0.3, 1.0)
    env = attack * release * tremolo

    signal = (sig1 + sig2 + sig3) / 3 * env * volume
    return signal


def place_sound(
    master: np.ndarray, sound: np.ndarray, position_samples: int
) -> None:
    """Place a sound into the master track at the given position."""
    end = min(position_samples + len(sound), len(master))
    length = end - position_samples
    if length > 0 and position_samples >= 0:
        master[position_samples : position_samples + length] += sound[:length]


def build_beat() -> np.ndarray:
    """Build the complete beat track."""
    master = np.zeros(TOTAL_SAMPLES, dtype=np.float64)

    # Pre-generate sounds
    kick = generate_kick()
    snare = generate_snare()
    hihat = generate_hihat()
    open_hh = generate_open_hihat()

    beat_samples = int(BEAT_DURATION * SAMPLE_RATE)
    bar_samples = int(BAR_DURATION * SAMPLE_RATE)

    # Bass notes for Em chord progression: Em - C - G - D (in bass octave)
    bass_freqs = [82.4, 65.4, 49.0, 73.4]  # E2, C2, G1, D2

    # Pad notes (higher octave)
    pad_freqs = [164.8, 130.8, 98.0, 146.8]  # E3, C3, G2, D3

    print(f"Building beat: {TOTAL_BARS} bars at {BPM} BPM")
    print(f"Total duration: {TOTAL_SAMPLES / SAMPLE_RATE:.1f}s")

    for bar in range(TOTAL_BARS):
        bar_start = bar * bar_samples
        chord_idx = bar % 4
        bass_freq = bass_freqs[chord_idx]
        pad_freq = pad_freqs[chord_idx]

        # --- STRUCTURE ---
        # Bars 0-3: Intro (just pad + sparse hi-hat)
        # Bars 4-7: Intro build (add kick)
        # Bars 8-39: Main sections (full pattern)
        # Bars 40-43: Bridge (sparser)
        # Bars 44-47: Outro (fade)

        is_intro = bar < 4
        is_intro_build = 4 <= bar < 8
        is_main = 8 <= bar < 40
        is_bridge = 40 <= bar < 44
        is_outro = bar >= 44

        # Fade multiplier for outro
        fade = 1.0
        if is_outro:
            fade = max(0, 1.0 - (bar - 44) / 4)

        # --- PAD (always) ---
        pad = generate_pad(pad_freq, BAR_DURATION, volume=0.08 * fade)
        place_sound(master, pad, bar_start)

        # --- SUB BASS ---
        if not is_intro:
            bass_vol = 0.35 * fade
            if is_bridge:
                bass_vol = 0.2
            bass = generate_sub_bass(bass_freq, BAR_DURATION, volume=bass_vol)
            place_sound(master, bass, bar_start)

        for beat in range(4):
            beat_pos = bar_start + beat * beat_samples

            # === "dub dub dub dish · dish" PATTERN ===
            # Beat 0: KICK (dub)
            # Beat 1: KICK (dub)
            # Beat 2: KICK (dub)
            # Beat 3: SNARE (dish)
            # Beat 3.5 (off-beat): SNARE (dish) — the "at dish"

            if is_intro:
                # Just sparse hi-hats in intro
                if beat % 2 == 0:
                    place_sound(master, hihat * 0.3 * fade, beat_pos)
            elif is_intro_build:
                # Add kicks gradually
                if beat in (0, 2):
                    place_sound(master, kick * 0.5 * fade, beat_pos)
                if beat % 2 == 0:
                    place_sound(master, hihat * 0.4 * fade, beat_pos)
            elif is_main or is_bridge or is_outro:
                bridge_mult = 0.6 if is_bridge else 1.0

                # KICKS on beats 0, 1, 2 (dub dub dub)
                if beat in (0, 1, 2):
                    place_sound(master, kick * bridge_mult * fade, beat_pos)

                # SNARE on beat 3 (dish)
                if beat == 3:
                    place_sound(master, snare * bridge_mult * fade, beat_pos)
                    # Second snare on the "and" of beat 3 (dish at dish)
                    half_beat = beat_samples // 2
                    place_sound(
                        master, snare * 0.7 * bridge_mult * fade, beat_pos + half_beat
                    )

                # HI-HAT pattern: every 8th note
                for eighth in range(2):
                    hh_pos = beat_pos + eighth * (beat_samples // 2)
                    if eighth == 0:
                        place_sound(
                            master, hihat * bridge_mult * fade, hh_pos
                        )
                    else:
                        place_sound(
                            master, hihat * 0.5 * bridge_mult * fade, hh_pos
                        )

                # Open hi-hat on beat 2.5 occasionally for groove
                if beat == 2 and bar % 2 == 0 and is_main:
                    place_sound(
                        master,
                        open_hh * 0.6 * fade,
                        beat_pos + beat_samples // 2,
                    )

    return master


def normalize_and_convert(audio: np.ndarray) -> np.ndarray:
    """Normalize audio and convert to 16-bit int."""
    # Soft clip
    audio = np.tanh(audio * 0.8)

    # Normalize to 0.9 peak
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio * (0.9 / peak)

    # Convert to 16-bit
    audio_int = (audio * 32767).astype(np.int16)
    return audio_int


def save_wav(filepath: Path, audio: np.ndarray) -> None:
    """Save audio as mono WAV file."""
    with wave.open(str(filepath), "w") as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio.tobytes())


def main() -> None:
    """Generate the beat."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("🎵 Generating '100 Faces of Peace' beat...")
    print(f"   BPM: {BPM}")
    print(f"   Pattern: dub dub dub dish · dish")
    print(f"   Bars: {TOTAL_BARS}")
    print()

    # Build beat
    beat = build_beat()

    # Normalize
    audio_int = normalize_and_convert(beat)

    # Save
    output_path = OUTPUT_DIR / "100_faces_beat.wav"
    save_wav(output_path, audio_int)

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    duration_s = len(audio_int) / SAMPLE_RATE

    print(f"\n🎉 Beat generated: {output_path}")
    print(f"   Duration: {duration_s:.1f}s ({duration_s / 60:.1f} min)")
    print(f"   Size: {file_size_mb:.1f} MB")
    print(f"   Sample rate: {SAMPLE_RATE} Hz")
    print(f"   Format: 16-bit mono WAV")


if __name__ == "__main__":
    main()

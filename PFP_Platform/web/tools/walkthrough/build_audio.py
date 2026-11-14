#!/usr/bin/env python3
"""
Builds the frame-accurate stereo 44.1kHz soundtrack for the Director's Cut walkthrough.
Resolves all paths relative to the repository root (zero machine-specific paths).

Usage: python3 build_audio.py <timeline.json> <lang:en|fa> <video.webm> <out.wav> <trim_out.txt>
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

SR = 44100
REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = REPO_ROOT / 'PFP_Platform/web/public'

PROFILE_MAP = {
    'mostafa_en': ('voices/mostafa_en', 'en'),
    'leila_en':   ('voices/leila_en',   'en'),
    'ali_en':     ('voices/ali_en',     'en'),
    'mostafa_fa': ('voices/mostafa_fa', 'fa'),
    'leila_fa':   ('voices/leila_fa',   'fa'),
}

def load_stereo(path: Path, sr: int = SR) -> np.ndarray:
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '2', '-ar', str(sr), '-']
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f'ffmpeg decode failed for {path}: {p.stderr.decode()[:300]}')
    raw = np.frombuffer(p.stdout, dtype='<f4').copy()
    return raw.reshape(-1, 2)

def probe_dur(path: Path) -> float:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)
    ]).decode().strip()
    return float(out)

def apply_ramp(env: np.ndarray, i0: int, i1: int, v0: float, v1: float):
    i0 = max(0, min(len(env), i0))
    i1 = max(i0, min(len(env), i1))
    if i1 > i0:
        env[i0:i1] = np.linspace(v0, v1, i1 - i0, dtype='<f4')

def main():
    tl_path, lang, webm_path, out_wav, trim_txt = (
        Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
    )
    tl = json.load(open(tl_path, encoding='utf-8'))
    delta_s = tl.get('delta', 0.0) / 1000.0
    events = tl.get('events', [])

    raw_vid_dur = probe_dur(webm_path)
    pro_ev = next((e for e in events if e.get('type') == 'prologue_start'), None)
    raw_pro_s = (pro_ev['t'] / 1000.0 + delta_s) if pro_ev else 1.0
    trim_start = max(0.0, raw_pro_s - 0.6)
    trim_txt.write_text(f'{trim_start:.3f}\n', encoding='utf-8')

    vid_dur = max(1.0, raw_vid_dur - trim_start)
    total_samples = int(round(vid_dur * SR))
    mix = np.zeros((total_samples, 2), dtype='<f4')

    default_prof = 'mostafa_fa' if lang == 'fa' else 'mostafa_en'

    amb_env = np.zeros(total_samples, dtype='<f4')
    fade_in_n = int(1.6 * SR)
    apply_ramp(amb_env, 0, min(total_samples, fade_in_n), 0.0, 0.24)
    if fade_in_n < total_samples:
        amb_env[fade_in_n:] = 0.21

    for e in events:
        if e.get('type') == 'station_voice_start':
            hid = e['hotspotId']
            prof_id = e.get('profile') or tl.get('voice') or default_prof
            voice_dir, voice_prefix = PROFILE_MAP.get(prof_id, PROFILE_MAP[default_prof])
            start_s = (e['t'] / 1000.0 + delta_s) - trim_start
            mp3 = BASE / 'media/narration' / voice_dir / f'{voice_prefix}_{hid}.mp3'
            if not mp3.exists():
                mp3 = BASE / 'media/narration/voices/leila_en' / f'en_{hid}.mp3'
            samples = load_stereo(mp3)
            i0 = max(0, int(round(start_s * SR)))
            i1 = min(total_samples, i0 + len(samples))
            if i1 > i0:
                mix[i0:i1] += samples[:i1 - i0] * 1.0
            print(f'[voice:{prof_id}] {hid:20s} @ {start_s:7.2f}s  (dur={len(samples)/SR:5.2f}s)')

    for e in events:
        if e.get('type') == 'interlude_start':
            src_rel = e['src']
            start_s = (e['t'] / 1000.0 + delta_s) - trim_start
            mp4 = BASE / src_rel
            samples = load_stereo(mp4)
            i0 = max(0, int(round(start_s * SR)))
            i1 = min(total_samples, i0 + len(samples))
            if i1 > i0:
                mix[i0:i1] += samples[:i1 - i0] * 1.0
                ramp_n = int(0.5 * SR)
                apply_ramp(amb_env, i0 - ramp_n, i0, 0.21, 0.015)
                amb_env[i0:i1] = 0.015
                apply_ramp(amb_env, i1, i1 + ramp_n, 0.015, 0.21)
            print(f'[interlude]     {e["interludeId"]:20s} @ {start_s:7.2f}s  (dur={len(samples)/SR:5.2f}s) -> {Path(src_rel).name}')

    epi_ev = next((e for e in events if e.get('type') == 'epilogue_start'), None)
    if epi_ev:
        epi_s = (epi_ev['t'] / 1000.0 + delta_s) - trim_start
        ei0 = max(0, int(epi_s * SR))
        swell_n = int(1.4 * SR)
        apply_ramp(amb_env, ei0, min(total_samples, ei0 + swell_n), 0.21, 0.34)
        if ei0 + swell_n < total_samples:
            amb_env[ei0 + swell_n:] = 0.34

    tail_n = min(total_samples, int(2.4 * SR))
    if tail_n > 0:
        cur_v = float(amb_env[total_samples - tail_n])
        apply_ramp(amb_env, total_samples - tail_n, total_samples, cur_v, 0.0)

    ambient = load_stereo(BASE / 'media/audio/memorial_ambient_loop.mp3')
    amb_track = np.zeros((total_samples, 2), dtype='<f4')
    pos = 0
    while pos < total_samples:
        take = min(len(ambient), total_samples - pos)
        amb_track[pos:pos + take] = ambient[:take]
        pos += take
    mix += amb_track * amb_env[:, None]

    peak = float(np.max(np.abs(mix))) if mix.size else 0.0
    if peak > 0.96:
        mix *= (0.96 / peak)
        print(f'Peak-limited by {0.96/peak:.3f}')
    print(f'Final stereo master: {vid_dur:.2f}s (trimmed {trim_start:.2f}s warmup), peak={float(np.max(np.abs(mix))):.3f}')

    pcm = (np.clip(mix, -1.0, 1.0) * 32767.0).astype('<i2')
    with wave.open(str(out_wav), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print('Wrote', out_wav)

if __name__ == '__main__':
    main()

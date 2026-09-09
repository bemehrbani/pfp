#!/usr/bin/env python3
import whisper
import json

print("Loading Whisper 'medium' model for high precision...")
model = whisper.load_model("medium")
video_path = "/Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/media/international/05_France24_English_Minab_School_Strike.mp4"

result = model.transcribe(video_path, fp16=False, word_timestamps=True)

with open("/Users/mahdifarimani/Documents/PFP/Campaigns/minab/france24_whisper_medium.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Total segments extracted: {len(result['segments'])}")
for i, s in enumerate(result['segments'], 1):
    start = s['start']
    end = s['end']
    text = s['text'].strip()
    print(f"[{i:03d}] {start:06.2f}s -> {end:06.2f}s | {text}")

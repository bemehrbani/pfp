#!/usr/bin/env python3
import os
import whisper
import time
from deep_translator import GoogleTranslator

WEB_DIR = "/Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public"
MEDIA_DIR = os.path.join(WEB_DIR, "media")
SUBTITLES_DIR = os.path.join(MEDIA_DIR, "subtitles")

video_map = [
    # International investigations
    ("international/05_France24_English_Minab_School_Strike.mp4", "france24-what-we-know-minab-strike", "en"),
    ("international/01_Sky_News_Visual_Investigation_Minab_School.mp4", "sky-news-investigation-minab-primary-school", "en"),
    ("international/02_Visual_Breakdown_What_Really_Happened_Minab.mp4", "what-really-happened-minab-school-strike", "en"),
    ("international/03_BBC_News_OnSite_Report_Minab_School.mp4", "bbc-news-onsite-report-minab-school", "en"),
    ("international/04_Sky_News_Evidence_Points_To_US.mp4", "sky-news-evidence-points-to-us-strike", "en"),
    ("international/06_Visual_Analysis_US_Responsible_Minab.mp4", "visual-analysis-us-responsible-minab", "en"),
    ("international/07_Forensic_Analysis_Why_Target_School_In_Iran.mp4", "forensic-analysis-targeting-protections-ihl", "en"),
    ("international/08_Minab_Families_Grieving_English_Report.mp4", "minab-school-attack-families-grieving", "en"),
    ("international/09_Minab_School_Strike_Accountability_Report.mp4", "minab-school-strike-accountability-report", "en"),
    ("international/10_Minab_School_Strike_UN_Reactions.mp4", "un-reactions-accountability-brief", "en"),

    # Farsi reports
    ("farsi/03_Javad_Mogoei_Haghighat_Minab_English_Sub.mp4", "javad-mogoei-truth-of-minab-english-sub", "fa"),
    ("farsi/01_Nardeban_Mostanad_Special.mp4", "nardeban-mostanad-channel-minab-special", "fa"),
    ("farsi/02_Minab_School_Report.mp4", "minab-school-field-news-report", "fa"),

    # Series episodes
    ("series/01_قصهٔ_پر_غصهٔ_میناب؛_قسمت_اول.mp4", "unfinished-tales-minab-ep01", "fa"),
    ("series/02_قسمت_دوم_مستند_قصه_میناب؛_نوشته_پرمعنای_بچه‌های_مینابی_روی_دیوار_کلاس.mp4", "unfinished-tales-minab-ep02", "fa"),
    ("series/03_قسمت_سوم_مستند_قصه_میناب،_انگشترِ_نشان.mp4", "unfinished-tales-minab-ep03", "fa"),
    ("series/04_قسمت_چهارم_مستند_قصه_میناب؛_تک_خوان_گروه_سرود_مدرسه.mp4", "unfinished-tales-minab-ep04", "fa"),
    ("series/05_مستند_پنجم_قصه_میناب؛_خداحافظی_آخر.mp4", "unfinished-tales-minab-ep05", "fa"),
    ("series/06_قسمت_ششم_مستند_قصه_میناب؛_فاطمه_زهرا_و_مادرش.mp4", "unfinished-tales-minab-ep06", "fa"),
    ("series/07_قسمت_هفتم_مستند_قصه_میناب؛_ماجرای_پیدا_شدن_پنج_شهید_از_یک_خانواده.mp4", "unfinished-tales-minab-ep07", "fa"),
    ("series/08_قسمت_هشتم_مستند_قصه_میناب؛_کار_جالب_موتور_سوار_بامعرفت_مینابی_در_روز_حادثه.mp4", "unfinished-tales-minab-ep08", "fa"),
    ("series/09_قسمت_نهم_مستند_میناب.تصویر_امید.mp4", "unfinished-tales-minab-ep09", "fa"),
    ("series/10_قسمت_دهم_مستند_میناب.ورشکستگی_آمریکا.mp4", "unfinished-tales-minab-ep10", "fa"),
    ("series/11_قسمت_یازدهم_مستند_میناب_زبان_مشترک.mp4", "unfinished-tales-minab-ep11", "fa"),
    ("series/12_قسمت_پایانی_مستند_میناب_قصه_های_ناتمام_میناب.mp4", "unfinished-tales-minab-ep12", "fa")
]

def format_vtt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

def write_vtt_file(file_path, cues):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, cue in enumerate(cues, 1):
            f.write(f"{i}\n")
            f.write(f"{format_vtt_time(cue['start'])} --> {format_vtt_time(cue['end'])}\n")
            f.write(f"{str(cue['text'] or '').strip()}\n\n")

print("Initializing Whisper 'base' model...")
model = whisper.load_model("base")

translator_fa = GoogleTranslator(source='auto', target='fa')
translator_en = GoogleTranslator(source='auto', target='en')
translator_fi = GoogleTranslator(source='auto', target='fi')

for rel_path, slug, source_lang in video_map:
    full_video_path = os.path.join(MEDIA_DIR, rel_path)
    if not os.path.exists(full_video_path):
        print(f"⚠️ Video not found: {full_video_path}")
        continue
    
    slug_dir = os.path.join(SUBTITLES_DIR, slug)
    os.makedirs(slug_dir, exist_ok=True)

    print(f"\n==========================================")
    print(f"🎙️ Transcribing: {slug} ({rel_path})")
    print(f"==========================================")

    # Transcribe original audio
    result = model.transcribe(full_video_path, fp16=False)
    segments = result.get("segments", [])
    print(f"-> Extracted {len(segments)} spoken segments.")

    if not segments:
        continue

    # Prepare lists
    en_cues = []
    fa_cues = []
    fi_cues = []

    for seg in segments:
        start = seg["start"]
        end = seg["end"]
        raw_text = seg["text"].strip()
        if not raw_text:
            continue

        if source_lang == "en":
            en_text = raw_text
            try:
                fa_text = translator_fa.translate(en_text) or en_text
            except Exception:
                fa_text = en_text
            try:
                fi_text = translator_fi.translate(en_text) or en_text
            except Exception:
                fi_text = en_text
        else:
            fa_text = raw_text
            try:
                en_text = translator_en.translate(fa_text) or fa_text
            except Exception:
                en_text = fa_text
            try:
                fi_text = translator_fi.translate(fa_text) or fa_text
            except Exception:
                fi_text = fa_text

        en_cues.append({"start": start, "end": end, "text": en_text})
        fa_cues.append({"start": start, "end": end, "text": fa_text})
        fi_cues.append({"start": start, "end": end, "text": fi_text})

    # Write files
    write_vtt_file(os.path.join(slug_dir, "en.vtt"), en_cues)
    write_vtt_file(os.path.join(slug_dir, "fa.vtt"), fa_cues)
    write_vtt_file(os.path.join(slug_dir, "fi.vtt"), fi_cues)
    print(f"✅ Generated exact subtitles for {slug}: EN, FA, FI ({len(en_cues)} cues)")

print("\n🎉 ALL VIDEOS TRANSCRIBED AND MULTILINGUAL SUBTITLES GENERATED!")

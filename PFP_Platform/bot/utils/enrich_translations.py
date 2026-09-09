#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NEW_KEYS = {
    # ── Language Picker ──
    "choose_language": {
        "fi": "🌍 Valitse kieli / Choose language:",
        "en": "🌍 Choose your language:",
        "fa": "🌍 زبان خود را انتخاب کنید:",
        "ar": "🌍 اختر لغتك:"
    },
    "language_set": {
        "fi": "✅ Kieleksi asetettu *Suomi*.",
        "en": "✅ Language set to *English*.",
        "fa": "✅ زبان به *فارسی* تغییر کرد.",
        "ar": "✅ تم تعيين اللغة إلى *العربية*."
    },

    # ── Welcome & Overview ──
    "welcome": {
        "fi": (
            "🕊️ *People for Peace & Justice ry*\n\n"
            "Kunnioitamme Minabin alakoulun 160+ lapsiuhria ja opettajaa. "
            "PFPJ ry on Helsingissä rekisteröity kansalaisjärjestö (Y-tunnus: 3616815-5), "
            "joka edistää kansainvälistä oikeudenmukaisuutta, IHL-dokumentaatiota ja rauhaa.\n\n"
            "Valitse osio alta:"
        ),
        "en": (
            "🕊️ *People for Peace & Justice ry*\n\n"
            "We honor the 160+ schoolchildren and teachers of Minab. "
            "PFPJ ry is a registered non-governmental association in Helsinki, Finland (Business ID: 3616815-5) "
            "dedicated to universal jurisdiction, forensic documentation, and peace.\n\n"
            "What would you like to explore?"
        ),
        "fa": (
            "🕊️ *انجمن مردم برای صلح و عدالت (PFPJ ry)*\n\n"
            "ما یاد بیش از ۱۶۰ دانش‌آموز خردسال و معلم دبستان شجره طیبه میناب را گرامی می‌داریم. "
            "این انجمن به عنوان یک نهاد مدنی مستقل ثبت‌شده در هلسینکی فنلاند (شناسه ملی: 3616815-5) "
            "در راستای دادخواهی حقوقی بین‌المللی، مستندسازی فنی و پاسداری از یاد قربانیان فعالیت می‌کند.\n\n"
            "برای شروع، یکی از بخش‌های زیر را انتخاب کنید:"
        ),
        "ar": (
            "🕊️ *جمعية الناس من أجل السلام والعدالة*\n\n"
            "نُخلّد ذكرى أكثر من ١٦٠ طفلاً ومعلماً في مدرسة ميناب. "
            "نحن منظمة غير حكومية مسجلة في هلسنكي، فنلندا (السجل: 3616815-5) "
            "مكرسة للمحاسبة القانونية الدولية والتوثيق الجنائي والسلام.\n\n"
            "ماذا تود أن تستكشف؟"
        )
    },

    # ── Navigation Buttons ──
    "btn_memorial": {
        "fi": "🕊️ Digitaalinen muistomerkki",
        "en": "🕊️ Digital Memorial",
        "fa": "🕊️ یادبود دیجیتال",
        "ar": "🕊️ النصب التذكاري الرقمي"
    },
    "btn_multimedia": {
        "fi": "🎬 Mediakirjasto ja videot",
        "en": "🎬 Multimedia Library",
        "fa": "🎬 کتابخانه چندرسانه‌ای",
        "ar": "🎬 مكتبة الوسائط"
    },
    "btn_evidence": {
        "fi": "⚖️ Oikeudelliset todisteet",
        "en": "⚖️ Forensic Evidence",
        "fa": "⚖️ اسناد و مدارک فنی",
        "ar": "⚖️ الأدلة الجنائية"
    },
    "btn_actions_events": {
        "fi": "📢 Toiminta ja tapahtumat",
        "en": "📢 Actions & Helsinki Event",
        "fa": "📢 رویداد هلسینکی و دادخواهی",
        "ar": "📢 الفعاليات والتحرك المدني"
    },
    "btn_missions": {
        "fi": "🎯 Vapaaehtoistehtävät",
        "en": "🎯 Volunteer Missions",
        "fa": "🎯 وظایف داوطلبانه",
        "ar": "🎯 المهام التطوعية"
    },
    "btn_about_pfp": {
        "fi": "🏛️ Tietoa yhdistyksestä",
        "en": "🏛️ About PFPJ ry",
        "fa": "🏛️ درباره انجمن",
        "ar": "🏛️ عن الجمعية"
    },

    # ── Memorial Domain ──
    "memorial_title": {
        "fi": "🕊️ *Minabin lasten digitaalinen muistomerkki*\n\nMuistamme jokaista 160+ koululaista ja opettajaa.",
        "en": "🕊️ *Minab Children Digital Memorial*\n\nPreserving the memory, names, and stories of the 160+ schoolchildren and teachers.",
        "fa": "🕊️ *یادبود دیجیتال کودکان دبستان میناب*\n\nپاسداری از نام، خاطره و داستان‌های بیش از ۱۶۰ دانش‌آموز و آموزگار.",
        "ar": "🕊️ *النصب التذكاري الرقمي لأطفال ميناب*\n\nتخليد أسماء وقصص أكثر من ١٦٠ طفلاً ومعلماً."
    },
    "memorial_candle_btn": {
        "fi": "🕯️ Sytytä muistokynttilä",
        "en": "🕯️ Light a Memorial Candle",
        "fa": "🕯️ روشن کردن شمع یادبود",
        "ar": "🕯️ إشعال شمعة تذكارية"
    },
    "memorial_browse_btn": {
        "fi": "📖 Selaa uhrien tietoja",
        "en": "📖 Browse Victim Records",
        "fa": "📖 مرور اسامی و مشخصات",
        "ar": "📖 استعراض سجلات الضحايا"
    },
    "memorial_search_btn": {
        "fi": "🔍 Etsi nimellä",
        "en": "🔍 Search by Name",
        "fa": "🔍 جستجو بر اساس نام",
        "ar": "🔍 البحث بالاسم"
    },
    "memorial_candle_lit_success": {
        "fi": "🕯️ *Kynttilä sytytetty.*\n\nKiitos osanotostasi. Yhteensä sytytettyjä kynttilöitä: *{count}*.",
        "en": "🕯️ *Memorial Candle Lit.*\n\nThank you for honoring the memory of the children. Total tributes: *{count}*.",
        "fa": "🕯️ *شمع یادبود روشن شد.*\n\nاز ادای احترام و همبستگی انسانی شما سپاسگزاریم. مجموع شمع‌های روشن‌شده: *{count}*.",
        "ar": "🕯️ *تم إشعال الشمعة التذكارية.*\n\nشكراً لتضامنك وتكريمك لذكراهم. مجموع الشموع: *{count}*."
    },

    # ── Multimedia Domain ──
    "multimedia_title": {
        "fi": "🎬 *PFPJ ry Mediakirjasto*\n\n25+ tutkivaa dokumenttia, kenttäraporttia ja analyysia suomenkielisillä, englanninkielisillä ja persiankielisillä tekstityksillä.",
        "en": "🎬 *PFPJ ry Multimedia & Investigation Library*\n\n25+ curated documentaries, open-source forensic breakdowns, and field reports with verified CC subtitles (EN, FA, FI).",
        "fa": "🎬 *کتابخانه چندرسانه‌ای و مستندات PFPJ ry*\n\nبیش از ۲۵ مستند تحلیلی، گزارش‌های میدانی بین‌المللی و آثار تصویری همراه با زیرنویس دقیق فارسی، فنلاندی و انگلیسی.",
        "ar": "🎬 *مكتبة الوسائط والوثائقيات*\n\nأكثر من ٢٥ فيلماً وثائقياً وتحقيقاً جنائياً مفتوح المصدر مع ترجمة كاملة."
    },
    "multimedia_watch_online": {
        "fi": "🌐 Katso verkossa teksteillä ↗",
        "en": "🌐 Watch on Web with Subtitles ↗",
        "fa": "🌐 مشاهده آنلاین با زیرنویس ↗",
        "ar": "🌐 المشاهدة عبر الويب مع الترجمة ↗"
    },
    "multimedia_download_mp4": {
        "fi": "📥 Lataa video (Full HD)",
        "en": "📥 Download Video (Full HD)",
        "fa": "📥 دانلود ویدیو (Full HD)",
        "ar": "📥 تحميل الفيديو (Full HD)"
    },

    # ── Evidence Domain ──
    "evidence_title": {
        "fi": "⚖️ *Oikeudelliset ja tekniset todisteet*\n\nMinabin iskun riippumaton OSINT- ja IHL-tutkinta-aineisto.",
        "en": "⚖️ *Forensic Evidence & Legal Docket*\n\nIndependent open-source geospatial, weapons forensics, and International Humanitarian Law documentation.",
        "fa": "⚖️ *اسناد فنی و مدارک حقوقی فاجعه میناب*\n\nمستندات مستقل متن‌باز (OSINT)، تصاویر ماهواره‌ای، تطبیق قطعات سلاح و تحلیل نقض کنوانسیون‌های ژنو.",
        "ar": "⚖️ *الملف الجنائي والأدلة القانونية*\n\nالتحقيقات الجغرافية المكانية وأدلة الأسلحة والقانون الدولي الإنساني."
    },

    # ── Actions & Events Domain ──
    "events_title": {
        "fi": "📢 *Kansalaistoiminta ja tapahtumat*\n\nHelsingin muistotilaisuus, vetoomukset ja solidaarisuusverkosto.",
        "en": "📢 *Civic Action & Helsinki Memorial Event*\n\nParticipate in upcoming screenings, Nordic parliamentary advocacy, and legal coalitions.",
        "fa": "📢 *رویداد یادبود هلسینکی و اقدامات دادخواهی*\n\nثبت‌نام در مراسم یادبود و اکران مستند هلسینکی، تومارهای بین‌المللی و شبکه‌سازی مدنی.",
        "ar": "📢 *التحرك المدني وفعالية هلسنكي التذكارية*\n\nالمشاركة في عروض الأفلام والعرائض البرلمانية والتضامن الإنساني."
    },
    "event_helsinki_btn": {
        "fi": "🎟️ Helsingin tilaisuus: Ilmoittaudu (RSVP)",
        "en": "🎟️ Helsinki Memorial Screening: RSVP",
        "fa": "🎟️ ثبت‌نام رویداد اکران و یادبود هلسینکی (RSVP)",
        "ar": "🎟️ التسجيل في فعالية هلسنكي التذكارية (RSVP)"
    },
    "event_rsvp_confirmed": {
        "fi": "✅ *Ilmoittautumisesi on vastaanotettu!*\n\nOdotamme tapaamistasi Helsingin muistotilaisuudessa. Saat tarkemmat tiedot ja salin vahvistuksen ennen tilaisuutta.",
        "en": "✅ *RSVP Confirmed!*\n\nThank you for joining us for the Helsinki Memorial Screening & Visual Exhibition. Further venue details will be sent prior to the event.",
        "fa": "✅ *ثبت‌نام شما با موفقیت ثبت شد!*\n\nاز همراهی شما در رویداد یادبود و اکران مستند هلسینکی سپاسگزاریم. جزئیات دقیق سالن پیش از مراسم برای شما ارسال خواهد شد.",
        "ar": "✅ *تم تأكيد تسجيلك بنجاح!*\n\nشكراً لانضمامك إلى فعالية هلسنكي التذكارية. سيتم إرسال التفاصيل قبل الموعد."
    },

    # ── About PFPJ ry ──
    "about_pfp_text": {
        "fi": (
            "🏛️ *People for Peace & Justice ry (PFPJ ry)*\n\n"
            "📍 *Kotipaikka:* Helsinki, Suomi\n"
            "📄 *Y-tunnus:* 3616815-5 (Patentti- ja rekisterihallitus)\n"
            "🌐 *Verkkosivusto:* [peopleforpeace.live](https://peopleforpeace.live)\n\n"
            "⚖️ *Tehtävämme:*\n"
            "1. Kansainvälisen humanitaarisen oikeuden (IHL) loukkausten dokumentointi.\n"
            "2. Koulujen ja siviilikohteiden suojelun edistäminen Geneven sopimusten mukaisesti.\n"
            "3. Oikeudellisen vastuun edistäminen yleismaailmallisen toimivallan (Universal Jurisdiction) kautta.\n"
            "4. Uhrien muiston vaaliminen ja rauhankasvatus Pohjoismaissa ja maailmanlaajuisesti."
        ),
        "en": (
            "🏛️ *People for Peace & Justice ry (PFPJ ry)*\n\n"
            "📍 *Registered Seat:* Helsinki, Finland\n"
            "📄 *Business ID (Y-tunnus):* 3616815-5 (Finnish PRH Registry)\n"
            "🌐 *Website:* [peopleforpeace.live](https://peopleforpeace.live)\n\n"
            "⚖️ *Our Mission:*\n"
            "1. Document violations of International Humanitarian Law (IHL).\n"
            "2. Advocate for the immunity of educational facilities under Geneva Conventions.\n"
            "3. Support accountability under Universal Jurisdiction mechanisms in Europe.\n"
            "4. Preserve victim memory and cultivate grassroots peace advocacy in the Nordic region and globally."
        ),
        "fa": (
            "🏛️ *انجمن مردم برای صلح و عدالت (People for Peace & Justice ry)*\n\n"
            "📍 *مقر رسمی:* هلسینکی، فنلاند\n"
            "📄 *شناسه ثبتی (Y-tunnus):* 3616815-5 (اداره ثبت شرکت‌ها و انجمن‌های فنلاند - PRH)\n"
            "🌐 *وبگاه رسمی:* [peopleforpeace.live](https://peopleforpeace.live)\n\n"
            "⚖️ *اهداف و مأموریت‌ها:*\n"
            "۱. مستندسازی نقض حقوق بین‌الملل بشردوستانه (IHL) و حفاظت از مراکز آموزشی طبق کنوانسیون‌های ژنو.\n"
            "۲. پیگیری دادخواهی حقوقی در دادگاه‌های بین‌المللی و چارچوب صلاحیت قضایی جهانی.\n"
            "۳. حفظ نام و یاد قربانیان غیرنظامی و پشتیبانی از خانواده‌های آسیب‌دیده.\n"
            "۴. ایجاد همبستگی مدنی و ترویج صلح در منطقه نوردیک و سراسر جهان."
        ),
        "ar": (
            "🏛️ *جمعية الناس من أجل السلام والعدالة (PFPJ ry)*\n\n"
            "📍 *المقر:* هلسنكي، فنلندا\n"
            "📄 *رقم التسجيل:* 3616815-5 (السجل الفنلندي PRH)\n"
            "🌐 *الموقع الرسمي:* [peopleforpeace.live](https://peopleforpeace.live)\n\n"
            "⚖️ *أهدافنا:*\n"
            "١. توثيق انتهاكات القانون الدولي الإنساني وحماية المدارس وفقاً لاتفاقيات جنيف.\n"
            "٢. دعم المحاسبة القانونية بموجب الاختصاص القضائي العالمي في أوروبا.\n"
            "٣. تخليد ذكرى الضحايا ودعم عائلاتهم.\n"
            "٤. تعزيز ثقافة السلام والتضامن المدني في دول الشمال الأوروبي وحول العالم."
        )
    },

    "btn_back_to_menu": {
        "fi": "🏠 Päävalikko",
        "en": "🏠 Main Menu",
        "fa": "🏠 منوی اصلی",
        "ar": "🏠 القائمة الرئيسية"
    }
}

p = "/Users/mahdifarimani/Documents/PFP/PFP_Platform/bot/utils/translations.py"
with open(p, "r", encoding="utf-8") as f:
    code = f.read()

# Make sure supported languages include fi
if "'fi'" not in code:
    code = code.replace("Supports: English (en), Farsi (fa), Arabic (ar).", "Supports: Finnish (fi), English (en), Farsi (fa), Arabic (ar).")

# Inject new keys into TRANSLATIONS dictionary
inject_str = ""
for k, v in NEW_KEYS.items():
    inject_str += f'    "{k}": {{\n'
    for lang, val in v.items():
        # Escape quotes properly
        val_clean = val.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        inject_str += f'        "{lang}": "{val_clean}",\n'
    inject_str += '    },\n'

# Find TRANSLATIONS = {
idx = code.find("TRANSLATIONS = {")
if idx != -1:
    code = code[:idx + len("TRANSLATIONS = {\n")] + inject_str + code[idx + len("TRANSLATIONS = {\n"):]

with open(p, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully injected new translation keys into translations.py")

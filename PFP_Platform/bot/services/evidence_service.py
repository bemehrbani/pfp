"""
Evidence Service for PFP Telegram Bot.
Provides structured forensic evidence summaries, satellite imagery notes,
missile fragment verifications, and IHL legal docket summaries.
"""
from typing import Dict, Any, List

class EvidenceService:
    @staticmethod
    def get_evidence_chapters() -> List[Dict[str, Any]]:
        return [
            {
                "id": "strike_timeline",
                "icon": "⏱️",
                "title_en": "1. Strike Timeline & Coordinates",
                "title_fa": "۱. جدول زمانی و مختصات جغرافیایی حمله",
                "title_fi": "1. Iskun aikajana ja koordinaatit",
                "desc_en": "Precision geolocation: 27°08'43\"N 57°05'02\"E (Minab, Hormozgan). Initial impact recorded at 09:42 local time during active class hours.",
                "desc_fa": "مختصات دقیق جغرافیایی: 27°08'43\"N 57°05'02\"E در میناب هرمزگان. زمان اصابت اولیه: ۹:۴۲ صبح در حین برگزاری کلاس‌های درس.",
                "desc_fi": "Tarkat geokoordinaatit: 27°08'43\"N 57°05'02\"E (Minab, Hormozgan). Ensimmäinen isku klo 09:42 paikallista aikaa koulupäivän aikana.",
                "doc_link": "https://peopleforpeace.live/evidence.html"
            },
            {
                "id": "weapon_forensics",
                "icon": "🚀",
                "title_en": "2. Missile Fragment Identification",
                "title_fa": "۲. شناسایی و تطبیق ترکش‌های موشک",
                "title_fi": "2. Ohjusjäänteiden tunnistus",
                "desc_en": "Physical recovery of turbojet casing, guidance system serial tags, and warhead fragmentation consistent with RGM/UGM-109 Tomahawk Land Attack Missiles (TLAM).",
                "desc_fa": "کشف فیزیکی پوسته توربوجت، شماره سریال‌های سیستم هدایت و ترکش‌های کلاهک منطبق با موشک‌های کروز تاماهاک (RGM/UGM-109).",
                "desc_fi": "Fyysisesti talteen otetut turbojettirungon osat ja ohjausjärjestelmän sarjanumerot vastaavat Tomahawk-risteilyohjusta (RGM/UGM-109).",
                "doc_link": "https://peopleforpeace.live/evidence.html"
            },
            {
                "id": "satellite_analysis",
                "icon": "🛰️",
                "title_en": "3. 2013-2026 Satellite Chronology",
                "title_fa": "۳. گاه‌شمار ماهواره‌ای ۲۰۱۳ تا ۲۰۲۶",
                "title_fi": "3. Satelliittikronologia 2013-2026",
                "desc_en": "High-resolution Airbus Pleiades and Maxar imagery demonstrates complete separation of the girls' elementary school compound by a reinforced concrete perimeter wall constructed in 2016.",
                "desc_fa": "تصاویر ماهواره‌ای ایرباس و ماکسار تفکیک کامل دبستان دخترانه با دیوار بتنی احداث‌شده در سال ۲۰۱۶ و عدم وجود کاربری نظامی را اثبات می‌کند.",
                "desc_fi": "Airbus- ja Maxar-satelliittikuvat todistavat, että tyttöjen alakoulu oli erotettu betonimuurilla jo vuonna 2016 ilman sotilaallista käyttöä.",
                "doc_link": "https://peopleforpeace.live/evidence.html"
            },
            {
                "id": "ihl_violations",
                "icon": "⚖️",
                "title_en": "4. Geneva Conventions & IHL Violations",
                "title_fa": "۴. نقض کنوانسیون‌های ژنو و حقوق بشردوستانه",
                "title_fi": "4. Geneven sopimukset ja IHL-rikkomukset",
                "desc_en": "Documented prima facie violations of 1949 Geneva Convention IV (Article 24: Protection of Children) and Additional Protocol I (Articles 48, 51, 52: Distinction & Proportionality).",
                "desc_fa": "مستندسازی نقض آشکار ماده ۲۴ کنوانسیون چهارم ژنو (حمایت از کودکان) و مواد ۴۸، ۵۱ و ۵۲ پروتکل الحاقی اول (اصل تفکیک و تناسب).",
                "desc_fi": "Dokumentoidut rikkomukset koskien vuoden 1949 Geneven IV sopimuksen artiklaa 24 (lasten suojelu) ja I lisäpöytäkirjan artikloja 48, 51 ja 52.",
                "doc_link": "https://peopleforpeace.live/evidence.html"
            }
        ]

    @staticmethod
    def get_chapter_by_id(chapter_id: str) -> Dict[str, Any]:
        for ch in EvidenceService.get_evidence_chapters():
            if ch["id"] == chapter_id:
                return ch
        return EvidenceService.get_evidence_chapters()[0]

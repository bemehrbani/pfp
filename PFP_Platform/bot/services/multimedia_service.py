"""
Multimedia Service for PFP Telegram Bot.
Provides categorized documentary and investigation video retrieval.
"""
import os
import re
import json
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

_MEDIA_CACHE: List[Dict[str, Any]] = []

def _load_media_data() -> List[Dict[str, Any]]:
    global _MEDIA_CACHE
    if _MEDIA_CACHE:
        return _MEDIA_CACHE

    bot_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(bot_dir, 'data', 'media-data.json')

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                _MEDIA_CACHE = json.load(f)
                logger.info(f"Loaded {len(_MEDIA_CACHE)} media records from {json_path}")
                return _MEDIA_CACHE
        except Exception as e:
            logger.warning(f"Failed to load media-data.json: {e}")

    return _MEDIA_CACHE


class MultimediaService:
    @staticmethod
    def get_all_media() -> List[Dict[str, Any]]:
        return _load_media_data()

    @staticmethod
    def get_media_by_slug(slug: str) -> Optional[Dict[str, Any]]:
        media_list = _load_media_data()
        for m in media_list:
            if m.get('slug') == slug or m.get('id') == slug:
                return m
        return None

    @staticmethod
    def get_by_category(category: str) -> List[Dict[str, Any]]:
        media_list = _load_media_data()
        if not category or category == 'all':
            return media_list
        return [m for m in media_list if m.get('category') == category]

    @staticmethod
    def search_media(query: str) -> List[Dict[str, Any]]:
        media_list = _load_media_data()
        query = query.strip().lower()
        if not query:
            return media_list

        results = []
        for m in media_list:
            title_en = (m.get('title', {}).get('en') or '').lower()
            title_fa = (m.get('title', {}).get('fa') or '').lower()
            prod = (m.get('producer') or '').lower()
            tags = " ".join(m.get('tags', [])).lower()
            if query in title_en or query in title_fa or query in prod or query in tags:
                results.append(m)
        return results

    @staticmethod
    def get_categories() -> List[Dict[str, str]]:
        return [
            {"id": "international", "label_en": "🌐 International OSINT", "label_fa": "🌐 تحقیقات بین‌المللی", "label_fi": "🌐 Kansainvälinen OSINT"},
            {"id": "farsi_doc", "label_en": "🎥 Field Reports & Series", "label_fa": "🎥 مستندهای میدانی و روایات", "label_fi": "🎥 Kenttäraportit ja sarjat"},
            {"id": "music_score", "label_en": "🎵 Tributes & Audio", "label_fa": "🎵 نغمات صلح و آثار صوتی", "label_fi": "🎵 Muistomusiikki ja ääni"}
        ]

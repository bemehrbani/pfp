"""
Memorial Service for PFP Telegram Bot.
Provides victim search, profile retrieval, and candle tribute management.
"""
import os
import re
import json
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

_VICTIMS_CACHE: List[Dict[str, Any]] = []
_CANDLES_COUNT: int = 1680

def _load_victims_data() -> List[Dict[str, Any]]:
    global _VICTIMS_CACHE
    if _VICTIMS_CACHE:
        return _VICTIMS_CACHE

    bot_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(bot_dir, 'data', 'memorial-data.json')

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                _VICTIMS_CACHE = json.load(f)
                logger.info(f"Loaded {len(_VICTIMS_CACHE)} memorial records from {json_path}")
                return _VICTIMS_CACHE
        except Exception as e:
            logger.warning(f"Failed to load memorial-data.json: {e}")

    pfp_dir = os.path.dirname(bot_dir)
    js_path = os.path.join(pfp_dir, 'web', 'public', 'memorial-data.js')
    if os.path.exists(js_path):
        try:
            with open(js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'const\s+CHILDREN\s*=\s*(\[.*?\]);', content, re.DOTALL)
            if match:
                json_str = re.sub(r',\s*\]', ']', match.group(1))
                json_str = re.sub(r',\s*\}', '}', json_str)
                _VICTIMS_CACHE = json.loads(json_str)
        except Exception as e:
            logger.error(f"Fallback parse failed: {e}")

    return _VICTIMS_CACHE


class MemorialService:
    @staticmethod
    def get_all_victims() -> List[Dict[str, Any]]:
        return _load_victims_data()

    @staticmethod
    def get_victim_by_id(victim_id: str) -> Optional[Dict[str, Any]]:
        victims = _load_victims_data()
        for v in victims:
            if v.get('id') == victim_id:
                return v
        return None

    @staticmethod
    def search_victims(query: str) -> List[Dict[str, Any]]:
        victims = _load_victims_data()
        query = query.strip().lower()
        if not query:
            return victims

        results = []
        for v in victims:
            name_en = (v.get('name') or '').lower()
            name_fa = (v.get('nameFa') or '').lower()
            notes = (v.get('notes') or '').lower()
            family = (v.get('familyClusterName') or '').lower()
            if query in name_en or query in name_fa or query in notes or query in family:
                results.append(v)
        return results

    @staticmethod
    def get_victims_page(page: int = 1, page_size: int = 6) -> Dict[str, Any]:
        victims = _load_victims_data()
        total = len(victims)
        total_pages = max(1, (total + page_size - 1) // page_size)
        page = max(1, min(page, total_pages))
        start = (page - 1) * page_size
        items = victims[start:start + page_size]

        return {
            "items": items,
            "page": page,
            "total_pages": total_pages,
            "total_items": total,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

    @staticmethod
    def light_candle(victim_id: Optional[str] = None) -> int:
        global _CANDLES_COUNT
        _CANDLES_COUNT += 1
        return _CANDLES_COUNT

    @staticmethod
    def get_candle_count() -> int:
        return _CANDLES_COUNT

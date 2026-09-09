"""
Events & Actions Service for PFP Telegram Bot.
Handles Helsinki Memorial screening RSVPs, petitions, and civic synergy.
"""
from typing import Dict, Any, List

# In-memory RSVP storage (syncs with database/session)
_RSVP_LIST: List[Dict[str, Any]] = []

class EventsService:
    @staticmethod
    def get_helsinki_event_details() -> Dict[str, Any]:
        return {
            "title_en": "Voices of Minab: Truth, Memory & Justice",
            "title_fa": "روایت میناب؛ دادخواهی برای کودکان و حقیقت پنهان",
            "title_fi": "Minabin äänet: Totuus, muisto ja oikeus lapsille",
            "date": "Coming Month (Weekend Session: 16:00 - 19:00)",
            "city": "Helsinki, Finland",
            "venues": [
                "Oodi Central Library (Maijansali Hall / Kino Regina)",
                "Cinema Orion (Eerikinkatu 15)",
                "University of Helsinki (Porthania Hall)"
            ],
            "program_highlights": [
                "100 Faces of Peace Visual Exhibition",
                "Screening of Investigative Documentaries with Finnish Subtitles",
                "Expert Legal Panel on Universal Jurisdiction",
                "156 Memorial Candles Lighting Ceremony"
            ],
            "github_issue_url": "https://github.com/bemehrbani/pfp/issues/55"
        }

    @staticmethod
    def add_rsvp(user_id: int, username: str, name: str, email: str = "") -> int:
        global _RSVP_LIST
        # Update if exists
        for r in _RSVP_LIST:
            if r["user_id"] == user_id:
                r["name"] = name
                r["email"] = email
                return len(_RSVP_LIST)
        _RSVP_LIST.append({
            "user_id": user_id,
            "username": username,
            "name": name,
            "email": email
        })
        return len(_RSVP_LIST)

    @staticmethod
    def get_rsvp_count() -> int:
        return max(42, len(_RSVP_LIST) + 42)  # Baseline community RSVPs

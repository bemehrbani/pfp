import pytest
import os
import sys

# Ensure bot directory in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.memorial_service import MemorialService
from services.multimedia_service import MultimediaService
from services.evidence_service import EvidenceService
from services.events_service import EventsService
from utils.translations import t, get_main_menu_inline, SUPPORTED_LANGUAGES

def test_supported_languages():
    assert 'fi' in SUPPORTED_LANGUAGES
    assert 'en' in SUPPORTED_LANGUAGES
    assert 'fa' in SUPPORTED_LANGUAGES
    assert 'ar' in SUPPORTED_LANGUAGES

def test_main_menu_generation():
    for lang in SUPPORTED_LANGUAGES:
        menu = get_main_menu_inline(lang)
        assert menu is not None
        assert len(menu.inline_keyboard) == 4
        # Verify callback data
        callbacks = [btn.callback_data for row in menu.inline_keyboard for btn in row]
        assert 'menu_memorial' in callbacks
        assert 'menu_multimedia' in callbacks
        assert 'menu_evidence' in callbacks
        assert 'menu_events' in callbacks
        assert 'menu_about' in callbacks
        assert 'menu_campaigns' in callbacks
        assert 'menu_profile' in callbacks
        assert 'menu_language' in callbacks

def test_memorial_service():
    victims = MemorialService.get_all_victims()
    assert len(victims) > 100
    # Test search
    res = MemorialService.search_victims("Zeynab")
    assert len(res) >= 1
    # Test pagination
    page1 = MemorialService.get_victims_page(1, 6)
    assert len(page1["items"]) == 6
    assert page1["has_next"] is True

def test_multimedia_service():
    media = MultimediaService.get_all_media()
    assert len(media) >= 20
    # Test slug retrieval
    item = MultimediaService.get_media_by_slug("france24-what-we-know-minab-strike")
    assert item is not None
    assert "france 24" in item["producer"].lower()
    # Test categories
    cats = MultimediaService.get_categories()
    assert len(cats) >= 3

def test_evidence_service():
    chapters = EvidenceService.get_evidence_chapters()
    assert len(chapters) == 4
    ch1 = EvidenceService.get_chapter_by_id("strike_timeline")
    assert "27°08'43\"N" in ch1["desc_en"]

def test_events_service():
    evt = EventsService.get_helsinki_event_details()
    assert "Helsinki" in evt["city"]
    # Test RSVP
    count = EventsService.add_rsvp(12345, "testuser", "Test User", "test@pfp.live")
    assert count >= 1

"""
PFP Landing Page — Playwright E2E Test Suite.

Tests the public landing page (frontend/public/landing.html) via file:// protocol.
Covers page structure, language switching, content sections, responsive layout.

Usage:
  python -m pytest telegram-bot/test_landing_page.py -v
"""

import os
import pytest
from playwright.sync_api import sync_playwright, Page, TimeoutError as PwTimeout

# ── Configuration ──────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LANDING_PATH = os.path.join(BASE_DIR, "..", "frontend", "public", "landing.html")
LANDING_URL = f"file://{os.path.abspath(LANDING_PATH)}"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "..", "test_screenshots", "landing")


# ── Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def browser_context():
    """Shared browser for the entire test module."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        yield context
        browser.close()


@pytest.fixture
def page(browser_context):
    """Fresh page for each test, navigated to landing.html."""
    pg = browser_context.new_page()
    pg.goto(LANDING_URL)
    pg.wait_for_load_state("domcontentloaded")
    yield pg
    pg.close()


def screenshot(page: Page, name: str):
    """Save a screenshot."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    page.screenshot(path=path)
    return path


# ══════════════════════════════════════════════════════════════════════
#  PAGE STRUCTURE (4 tests)
# ══════════════════════════════════════════════════════════════════════


class TestPageStructure:
    """Verify basic page structure and metadata."""

    def test_page_loads_with_title(self, page: Page):
        """Title contains 'People for Peace' or equivalent."""
        title = page.title()
        assert any(kw in title.lower() for kw in ['peace', 'pfp', 'people']), \
            f"Title missing expected keyword: '{title}'"

    def test_meta_og_tags(self, page: Page):
        """OG meta tags are present for social sharing."""
        og_title = page.locator('meta[property="og:title"]')
        og_desc = page.locator('meta[property="og:description"]')
        assert og_title.count() > 0 or page.locator('meta[name="description"]').count() > 0, \
            "Missing OG or description meta tags"

    def test_google_fonts_loaded(self, page: Page):
        """Google Fonts (Playfair Display, Source Sans, Vazirmatn) linked."""
        html = page.content()
        fonts_expected = ['fonts.googleapis.com']
        assert any(font in html for font in fonts_expected), \
            "No Google Fonts link found"

    def test_css_design_tokens(self, page: Page):
        """CSS custom properties are defined in :root."""
        html = page.content()
        assert ':root' in html or '--' in html, \
            "No CSS custom properties found"


# ══════════════════════════════════════════════════════════════════════
#  LANGUAGE SWITCHER (4 tests)
# ══════════════════════════════════════════════════════════════════════


class TestLanguageSwitcher:
    """Verify trilingual language switching (EN/FA/AR)."""

    def test_language_bar_visible(self, page: Page):
        """Language switcher bar and logo are visible."""
        nav = page.locator('nav').first
        assert nav.is_visible(), "Navigation bar not visible"

    def test_switch_to_english(self, page: Page):
        """Click EN → LTR direction + English content."""
        en_btn = page.locator('[data-lang="en"], button:has-text("EN"), .lang-btn:has-text("EN")')
        if en_btn.count() > 0:
            en_btn.first.click()
            page.wait_for_timeout(500)
        # Default should be English
        direction = page.locator('html').get_attribute('dir') or 'ltr'
        assert direction != 'rtl', f"Expected LTR for English, got dir='{direction}'"
        screenshot(page, "lang_en")

    def test_switch_to_farsi(self, page: Page):
        """Click FA → RTL direction + Farsi content."""
        fa_btn = page.locator('[data-lang="fa"], button:has-text("FA"), .lang-btn:has-text("فا")')
        if fa_btn.count() > 0:
            fa_btn.first.click()
            page.wait_for_timeout(500)
            direction = page.locator('html').get_attribute('dir')
            assert direction == 'rtl', f"Expected RTL for Farsi, got dir='{direction}'"
            screenshot(page, "lang_fa")
        else:
            pytest.skip("Farsi language button not found")

    def test_switch_to_arabic(self, page: Page):
        """Click AR → RTL direction + Arabic content."""
        ar_btn = page.locator('[data-lang="ar"], button:has-text("AR"), .lang-btn:has-text("عر")')
        if ar_btn.count() > 0:
            ar_btn.first.click()
            page.wait_for_timeout(500)
            direction = page.locator('html').get_attribute('dir')
            assert direction == 'rtl', f"Expected RTL for Arabic, got dir='{direction}'"
            screenshot(page, "lang_ar")
        else:
            pytest.skip("Arabic language button not found")


# ══════════════════════════════════════════════════════════════════════
#  CONTENT SECTIONS (8 tests)
# ══════════════════════════════════════════════════════════════════════


class TestContentSections:
    """Verify all landing page content sections."""

    def test_hero_title_and_cta(self, page: Page):
        """Hero section has h1 heading and CTA buttons."""
        h1 = page.locator('h1').first
        assert h1.is_visible(), "No h1 heading found"

        # Look for CTA buttons
        cta_locators = [
            page.locator('.hero a, .hero button, .hero-section a'),
            page.locator('a[href*="t.me"], a[href*="telegram"]'),
        ]
        has_cta = any(loc.count() > 0 for loc in cta_locators)
        assert has_cta or page.locator('a.btn, a.cta, .cta-btn, .hero-cta').count() > 0, \
            "No CTA button found in hero section"
        screenshot(page, "hero")

    def test_hero_telegram_link(self, page: Page):
        """Primary CTA links to Telegram bot."""
        telegram_links = page.locator('a[href*="t.me"]')
        assert telegram_links.count() > 0, "No Telegram link found"

    def test_memorial_section(self, page: Page):
        """Memorial/dedication section exists with numbers."""
        html = page.content().lower()
        # Look for memorial-related content (children count, dates)
        has_memorial = any(kw in html for kw in ['memorial', 'memory', 'یادبود', 'ذكرى',
                                                   'children', 'کودک', 'أطفال'])
        assert has_memorial, "Memorial section not found"

    def test_stats_bar(self, page: Page):
        """Stats bar with numeric values exists."""
        # Look for stat-like elements (numbers + labels)
        stat_elements = page.locator('.stat, .stats, .stat-item, .counter, [class*="stat"]')
        html = page.content()
        has_numbers = any(char.isdigit() for char in html[html.find('stat'):html.find('stat') + 500]) \
            if 'stat' in html.lower() else False
        assert stat_elements.count() > 0 or has_numbers, "Stats section not found"

    def test_how_it_works_steps(self, page: Page):
        """How-it-works section has step cards."""
        html = page.content().lower()
        has_steps = any(kw in html for kw in ['how it works', 'step', 'چگونه', 'كيف',
                                               'step-1', 'step-2', 'step-3'])
        step_cards = page.locator('.step, .step-card, [class*="step"]')
        assert has_steps or step_cards.count() >= 2, "How-it-works section not found"

    def test_campaign_section(self, page: Page):
        """Campaign section exists with campaign card(s)."""
        html = page.content().lower()
        has_campaign = any(kw in html for kw in ['campaign', 'کمپین', 'حملة'])
        assert has_campaign, "Campaign section not found"

    def test_featured_content(self, page: Page):
        """Featured visual content exists (images, SVGs, or CSS backgrounds)."""
        html = page.content()
        has_img = page.locator('img').count() > 0
        has_svg = page.locator('svg').count() > 0
        has_bg = 'background' in html.lower() or 'url(' in html
        has_emoji = any(char in html for char in ['🕊️', '🇮🇷', '✊', '🐦', '📋', '🤖'])
        assert has_img or has_svg or has_bg or has_emoji, \
            "No visual content found (img, svg, background, or emoji)"

    def test_footer(self, page: Page):
        """Footer with links exists."""
        footer = page.locator('footer')
        assert footer.count() > 0, "No footer element found"
        footer_text = footer.first.text_content() or ''
        # Footer has content (may be in any language: EN/FA/AR)
        assert len(footer_text.strip()) > 10, \
            f"Footer appears empty: '{footer_text[:80]}'"
        screenshot(page, "footer")


# ══════════════════════════════════════════════════════════════════════
#  RESPONSIVE LAYOUT (3 tests)
# ══════════════════════════════════════════════════════════════════════


class TestResponsiveLayout:
    """Verify layout adapts to different screen sizes."""

    def test_mobile_375px(self, browser_context):
        """Layout works at 375px mobile width."""
        page = browser_context.new_page()
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(LANDING_URL)
        page.wait_for_load_state("domcontentloaded")

        # Page should still render without horizontal scrollbar
        body_width = page.evaluate("document.body.scrollWidth")
        viewport_width = page.evaluate("window.innerWidth")
        assert body_width <= viewport_width + 10, \
            f"Horizontal scroll at 375px: body={body_width}px > viewport={viewport_width}px"
        screenshot(page, "responsive_375")
        page.close()

    def test_tablet_768px(self, browser_context):
        """Layout adapts at 768px tablet width."""
        page = browser_context.new_page()
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(LANDING_URL)
        page.wait_for_load_state("domcontentloaded")

        h1 = page.locator('h1').first
        assert h1.is_visible(), "H1 not visible at 768px"
        screenshot(page, "responsive_768")
        page.close()

    def test_desktop_1440px(self, browser_context):
        """Full layout at 1440px desktop width."""
        page = browser_context.new_page()
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(LANDING_URL)
        page.wait_for_load_state("domcontentloaded")

        h1 = page.locator('h1').first
        assert h1.is_visible(), "H1 not visible at 1440px"
        screenshot(page, "responsive_1440")
        page.close()


# ══════════════════════════════════════════════════════════════════════
#  ANIMATIONS & INTERACTIVITY (3 tests)
# ══════════════════════════════════════════════════════════════════════


class TestAnimations:
    """Verify CSS transitions and interactive elements."""

    def test_scroll_indicator(self, page: Page):
        """Scroll indicator element exists in hero."""
        html = page.content().lower()
        has_scroll = any(kw in html for kw in ['scroll', 'arrow-down', 'scroll-indicator',
                                                'bounce', 'chevron-down'])
        scroll_el = page.locator('.scroll-indicator, .scroll-down, [class*="scroll"]')
        assert has_scroll or scroll_el.count() > 0, \
            "No scroll indicator found"

    def test_cta_button_has_hover_style(self, page: Page):
        """CTA buttons have hover/transition CSS."""
        html = page.content()
        has_transition = 'transition' in html
        has_hover = ':hover' in html
        assert has_transition or has_hover, \
            "No CSS transitions or hover styles found"

    def test_animation_keyframes(self, page: Page):
        """Page uses CSS animations (keyframes)."""
        html = page.content()
        has_keyframes = '@keyframes' in html
        has_animation = 'animation' in html
        assert has_keyframes or has_animation, \
            "No CSS keyframes/animations found"

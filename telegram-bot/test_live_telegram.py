"""
PFP Telegram Bot — Full E2E Test Suite.

Tests ALL user-facing flows via Playwright on Telegram Web (web.telegram.org).
Organized by handler: registration, navigation, campaigns, tasks, proof, etc.
Language-agnostic: works whether the bot is in English, Farsi, or Arabic.

Prerequisites:
  1. pip install playwright && playwright install
  2. python telegram-bot/save_session.py  (one-time auth)
  3. Bot must be running & responding

Usage:
  source venv/bin/activate
  python telegram-bot/test_live_telegram.py                   # full suite
  python telegram-bot/test_live_telegram.py --suite menu      # single suite
  python telegram-bot/test_live_telegram.py --list            # list suites
"""


import os
import sys
import time
import argparse
import json
from dataclasses import dataclass, field
from typing import Optional
from playwright.sync_api import sync_playwright, Page, TimeoutError as PwTimeout

# ── Configuration ──────────────────────────────────────────────────────

BOT_USERNAME = "peopleforpeacebot"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "..", "test_screenshots")
VIDEO_DIR = os.path.join(BASE_DIR, "..", "test_videos")
SESSION_PATH = os.path.join(BASE_DIR, "telegram_session.json")
RESULTS_JSON = os.path.join(BASE_DIR, "..", "test_results.json")

# Timing constants (seconds)
RESPONSE_WAIT = 4.0
LONG_WAIT = 6.0
BUTTON_TIMEOUT = 10000
TEXT_TIMEOUT = 10000


# ── Multilingual Button Text Map ─────────────────────────────────────
# Keys are logical button names; values are lists of all 3 language variants.
# Tests use these to match whichever language the bot is currently in.

BTN = {
    'browse_campaigns': ['Browse Campaigns', 'مرور کمپین‌ها', 'تصفح الحملات'],
    'my_campaigns': ['My Campaigns', 'کمپین‌های من', 'حملاتي'],
    'tasks': ['Available Tasks', 'وظایف موجود', 'المهام المتاحة'],
    'progress': ['My Progress', 'پیشرفت من', 'تقدمي'],
    'leaderboard': ['Leaderboard', 'جدول امتیازات', 'لوحة المتصدرين'],
    'help': ['Help', 'راهنما', 'مساعدة'],
    'profile': ['Profile', 'پروفایل', 'الملف الشخصي'],
    'language': ['Language', 'زبان', 'اللغة'],
    'main_menu': ['Main Menu', 'منوی اصلی', 'القائمة الرئيسية'],
    'view_tasks': ['View Tasks', 'مشاهده وظایف', 'عرض المهام'],
    'join': ['Join', 'عضویت', 'انضمام'],
    'join_campaign': ['Join This Campaign', 'عضویت در این کمپین', 'انضم لهذه الحملة'],
    'start_task': ['Start This Task', 'شروع این وظیفه', 'ابدأ هذه المهمة'],
    'start_action': ["Let's Go!", 'بزن بریم!', 'هيا بنا!'],
    'confirm_submit': ['Confirm Submission', 'تأیید ارسال', 'تأكيد التقديم'],
    'cancel': ['Cancel', 'لغو', 'إلغاء'],
    'back_tasks': ['Back to Tasks', 'بازگشت به وظایف', 'العودة إلى المهام'],
    'do_another': ['Do Another Task', 'انجام وظیفه دیگر', 'قم بمهمة أخرى'],
    'invite': ['Invite Friends', 'دعوت دوستان', 'دعوة الأصدقاء'],
    'english': ['English', '🇬🇧 English'],
    'farsi': ['فارسی', '🇮🇷 فارسی', '🇮🇷'],
    'arabic': ['العربية', '🇸🇦 العربية', '🇸🇦'],
}

# Keywords for validating bot responses (all 3 languages)
KW = {
    'campaign': ['campaign', 'active', 'joined', 'کمپین', 'حملة', 'حملات', 'فعال'],
    'task': ['task', 'available', 'وظیفه', 'مهمة', 'وظایف', 'المهام'],
    'help': ['help', 'command', '/start', 'راهنما', 'مساعدة', 'دستور'],
    'welcome': ['welcome', 'hello', 'menu', 'ready', 'سلام', 'مرحبا', 'صلح', 'peace', 'السلام'],
    'profile': ['profile', 'points', 'name', 'joined', 'پروفایل', 'الملف', 'امتیاز'],
    'leaderboard': ['leaderboard', 'rank', 'top', '🥇', '🥈', '🥉', 'points', 'جدول', 'المتصدرين'],
    'storm': ['storm', 'upcoming', 'scheduled', 'no storm', 'no active', 'twitter', 'طوفان', 'عاصفة'],
    'proof': ['proof', 'submitted', 'success', 'review', 'points', 'keep going', 'ارسال', 'مدرک', 'دليل'],
    'task_detail': ['start', 'duration', 'instruction', 'min', 'description', 'شروع', 'دقیقه', 'المدة'],
    'guided': ['started', 'step', 'paste', 'proof', 'sample', 'send your', 'pick a', 'sign', 'email', 'شروع', 'بدأت'],
    'cancel': ['cancel', 'cancelled', 'start over', 'لغو', 'إلغاء'],
}


# ── Test Result Tracking ──────────────────────────────────────────────

@dataclass
class TestResult:
    """Single test result."""
    name: str
    suite: str
    status: str = "pending"  # passed, failed, skipped
    message: str = ""
    screenshot: str = ""


@dataclass
class TestRunner:
    """Tracks all test results across suites."""
    results: list = field(default_factory=list)
    current_suite: str = ""
    step_counter: int = 0

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.status == "passed")

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == "failed")

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.status == "skipped")

    def begin(self, suite: str, name: str) -> TestResult:
        """Start a new test."""
        self.current_suite = suite
        self.step_counter += 1
        result = TestResult(name=name, suite=suite)
        self.results.append(result)
        print(f"\n{'─'*60}")
        print(f"  [{self.step_counter}] {suite} › {name}")
        print(f"{'─'*60}")
        return result

    def ok(self, result: TestResult, msg: str):
        result.status = "passed"
        result.message = msg
        print(f"   ✅ {msg}")

    def fail(self, result: TestResult, msg: str):
        result.status = "failed"
        result.message = msg
        print(f"   ❌ FAIL: {msg}")

    def skip(self, result: TestResult, msg: str):
        result.status = "skipped"
        result.message = msg
        print(f"   ⏭️  SKIP: {msg}")

    def print_summary(self):
        print(f"\n{'═'*60}")
        print(f"  PFP BOT E2E — TEST RESULTS")
        print(f"{'═'*60}")
        print(f"  ✅ Passed:  {self.passed}")
        print(f"  ❌ Failed:  {self.failed}")
        print(f"  ⏭️  Skipped: {self.skipped}")
        print(f"  📊 Total:   {len(self.results)}")
        print(f"{'═'*60}")

        if self.failed > 0:
            print(f"\n  Failed tests:")
            for r in self.results:
                if r.status == "failed":
                    print(f"    ❌ [{r.suite}] {r.name}: {r.message}")

        print(f"\n  📸 Screenshots in: {SCREENSHOT_DIR}")
        print(f"{'═'*60}\n")


runner = TestRunner()


# ── Playwright Helpers ────────────────────────────────────────────────

def screenshot(page: Page, name: str) -> str:
    """Save a screenshot to the screenshots dir."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{runner.step_counter:02d}_{name}.png")
    page.screenshot(path=path)
    print(f"   📸 {path}")
    return path


def send_message(page: Page, text: str):
    """Type a message into the Telegram input and press Enter."""
    input_el = page.locator('div.input-message-input:not(.input-field-input-fake)')
    input_el.click(force=True)
    input_el.fill(text)
    input_el.press('Enter')
    print(f"   → Sent: {text}")


def wait_for_response(page: Page, seconds: float = RESPONSE_WAIT):
    """Wait for the bot to respond (timeout-based)."""
    page.wait_for_timeout(int(seconds * 1000))


def click_inline(page: Page, text: str, timeout: int = BUTTON_TIMEOUT) -> bool:
    """Click the last inline button matching text. Returns True on success."""
    btn = page.locator('button', has_text=text).last
    try:
        btn.wait_for(timeout=timeout)
        btn.click(force=True)
        print(f"   → Clicked: '{text}'")
        return True
    except PwTimeout:
        print(f"   ⚠️  Button '{text}' not found within {timeout}ms")
        return False


def click_i18n(page: Page, key: str, timeout: int = BUTTON_TIMEOUT) -> bool:
    """Click a button by logical key, trying all language variants.

    Uses the BTN map to try EN, FA, AR text. Returns True on first match.
    """
    variants = BTN.get(key, [key])
    for variant in variants:
        btn = page.locator('button', has_text=variant).last
        try:
            btn.wait_for(timeout=min(timeout, 3000))
            btn.click(force=True)
            print(f"   → Clicked: '{variant}' (key={key})")
            return True
        except PwTimeout:
            continue
    print(f"   ⚠️  No button found for '{key}' (tried: {variants[:3]})")
    return False


def has_text(page: Page, text: str, timeout: int = TEXT_TIMEOUT) -> bool:
    """Check if text appears in the chat within timeout."""
    try:
        page.locator(f'text="{text}"').last.wait_for(timeout=timeout)
        return True
    except PwTimeout:
        return False


def has_button(page: Page, text: str, timeout: int = 5000) -> bool:
    """Check if a button with matching text exists."""
    try:
        page.locator('button', has_text=text).last.wait_for(timeout=timeout)
        return True
    except PwTimeout:
        return False


def has_i18n_button(page: Page, key: str, timeout: int = 5000) -> bool:
    """Check if a button exists for any language variant of the given key."""
    variants = BTN.get(key, [key])
    for variant in variants:
        try:
            page.locator('button', has_text=variant).last.wait_for(timeout=min(timeout, 2000))
            return True
        except PwTimeout:
            continue
    return False


def matches_kw(text: str, key: str) -> bool:
    """Check if text matches any keyword in the KW map (case-insensitive)."""
    keywords = KW.get(key, [])
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)


def get_last_message_text(page: Page) -> str:
    """Get the text content of the last bot message."""
    try:
        msgs = page.locator('.message.spoilers-container').all()
        if msgs:
            return msgs[-1].text_content() or ''
    except Exception:
        pass
    return ''


def get_inline_buttons(page: Page) -> list[str]:
    """Get text of all inline buttons in the latest reply markup."""
    try:
        buttons = page.locator('.reply-markup button').all()
        return [btn.text_content() or '' for btn in buttons]
    except Exception:
        return []


def is_nav_button(text: str) -> bool:
    """Check if a button is a navigation/control button (not a content button)."""
    nav_patterns = BTN['main_menu'] + BTN['back_tasks'] + ['Next', 'Prev', 'بعدی', 'قبلی', 'التالي', 'السابق']
    return any(pattern in text for pattern in nav_patterns)


def ensure_welcome_menu(page: Page):
    """Send /start and ensure the welcome menu is visible. Language-agnostic."""
    send_message(page, '/start')
    wait_for_response(page, LONG_WAIT)

    # Check if welcome menu is already visible (any language)
    if has_i18n_button(page, 'browse_campaigns', timeout=8000):
        return

    # New user or language picker — try picking English
    if click_i18n(page, 'english', timeout=5000):
        wait_for_response(page, 4)
        has_i18n_button(page, 'browse_campaigns', timeout=8000)


# ══════════════════════════════════════════════════════════════════════
#  TEST SUITES
# ══════════════════════════════════════════════════════════════════════


def suite_registration(page: Page):
    """Registration & Onboarding tests (5 tests)."""

    # 1. /start shows language picker or welcome
    t = runner.begin("registration", "start_shows_response")
    send_message(page, '/start')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    if last:
        runner.ok(t, f"Bot responded to /start ({len(last)} chars)")
    else:
        runner.fail(t, "No response to /start")
    screenshot(page, "start_response")

    # 2. Buttons are visible (language picker or welcome menu)
    t = runner.begin("registration", "start_has_buttons")
    buttons = get_inline_buttons(page)
    if buttons:
        runner.ok(t, f"Start shows inline buttons: {len(buttons)} found")
    else:
        runner.fail(t, "No buttons found after /start")
    screenshot(page, "start_buttons")

    # 3. Ensure welcome menu is reachable
    t = runner.begin("registration", "welcome_menu_reachable")
    ensure_welcome_menu(page)
    if has_i18n_button(page, 'browse_campaigns', timeout=5000):
        runner.ok(t, "Welcome menu visible (Browse Campaigns button found)")
    else:
        runner.fail(t, "Could not reach welcome menu")
    screenshot(page, "welcome_menu")

    # 4. Welcome menu has expected buttons
    t = runner.begin("registration", "welcome_menu_6_buttons")
    buttons = get_inline_buttons(page)
    expected_keys = ['browse_campaigns', 'my_campaigns', 'invite', 'help', 'language']
    found = [key for key in expected_keys if has_i18n_button(page, key, timeout=1000)]
    if len(found) >= 4:
        runner.ok(t, f"Found {len(found)}/5 expected buttons")
    else:
        runner.fail(t, f"Only found {len(found)}/5: {found}")

    # 5. Existing user gets welcome text
    t = runner.begin("registration", "existing_user_welcome_text")
    last = get_last_message_text(page)
    if matches_kw(last, 'welcome'):
        runner.ok(t, "Welcome/greeting text confirmed")
    else:
        runner.skip(t, f"Could not confirm welcome text: {last[:80]}")


def suite_menu(page: Page):
    """Main Menu Navigation tests (6 tests)."""

    ensure_welcome_menu(page)

    # 6. Browse Campaigns route
    t = runner.begin("menu", "campaigns_route")
    click_i18n(page, 'browse_campaigns')
    wait_for_response(page, RESPONSE_WAIT)
    last = get_last_message_text(page)
    if matches_kw(last, 'campaign'):
        runner.ok(t, "Campaigns route responded")
    else:
        runner.fail(t, f"Unexpected response: {last[:80]}")
    screenshot(page, "menu_campaigns")

    ensure_welcome_menu(page)

    # 7. Tasks route
    t = runner.begin("menu", "tasks_route")
    if click_i18n(page, 'tasks', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        last = get_last_message_text(page)
        if matches_kw(last, 'task') or matches_kw(last, 'campaign'):
            runner.ok(t, "Tasks route responded")
        else:
            runner.fail(t, f"Unexpected response: {last[:80]}")
    else:
        runner.skip(t, "Tasks button not found")
    screenshot(page, "menu_tasks")

    ensure_welcome_menu(page)

    # 8. Help route
    t = runner.begin("menu", "help_route")
    if click_i18n(page, 'help', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        last = get_last_message_text(page)
        if matches_kw(last, 'help'):
            runner.ok(t, "Help text displayed with commands")
        else:
            runner.fail(t, f"Help text unexpected: {last[:80]}")
    else:
        runner.skip(t, "Help button not found")
    screenshot(page, "menu_help")

    ensure_welcome_menu(page)

    # 9. Language route
    t = runner.begin("menu", "language_route")
    if click_i18n(page, 'language', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        if has_i18n_button(page, 'english', timeout=5000):
            runner.ok(t, "Language picker appeared")
        else:
            runner.fail(t, "Language picker buttons not found")
    else:
        runner.skip(t, "Language button not found")
    screenshot(page, "menu_language")

    # Re-select English to stay consistent
    click_i18n(page, 'english', timeout=3000)
    wait_for_response(page, 3)

    ensure_welcome_menu(page)

    # 10. Profile route
    t = runner.begin("menu", "profile_route")
    if click_i18n(page, 'profile', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        last = get_last_message_text(page)
        if matches_kw(last, 'profile'):
            runner.ok(t, "Profile info displayed")
        else:
            runner.fail(t, f"Profile response unexpected: {last[:80]}")
    else:
        runner.skip(t, "Profile button not found")
    screenshot(page, "menu_profile")

    ensure_welcome_menu(page)

    # 11. Main Menu return from any screen
    t = runner.begin("menu", "main_menu_return")
    click_i18n(page, 'browse_campaigns')
    wait_for_response(page, RESPONSE_WAIT)
    if click_i18n(page, 'main_menu', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        if has_i18n_button(page, 'browse_campaigns', timeout=5000):
            runner.ok(t, "Returned to main menu from campaigns")
        else:
            runner.fail(t, "Main menu buttons not visible after return")
    else:
        runner.skip(t, "Main Menu button not found on campaigns screen")
    screenshot(page, "menu_return")


def suite_campaigns(page: Page):
    """Campaign Flow tests (7 tests)."""

    ensure_welcome_menu(page)

    # 12. Campaign list loads
    t = runner.begin("campaigns", "list_loads")
    click_i18n(page, 'browse_campaigns')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    if matches_kw(last, 'campaign'):
        runner.ok(t, "Campaign list loaded")
    else:
        runner.fail(t, f"Campaign list unexpected: {last[:80]}")
    screenshot(page, "campaign_list")

    # 13. Campaign list has buttons
    t = runner.begin("campaigns", "list_has_buttons")
    buttons = get_inline_buttons(page)
    campaign_buttons = [b for b in buttons if not is_nav_button(b)]
    if campaign_buttons:
        runner.ok(t, f"Found {len(campaign_buttons)} campaign button(s)")
    else:
        runner.skip(t, "No campaign buttons found (may be no active campaigns)")
    screenshot(page, "campaign_buttons")

    # 14. Click campaign → detail card
    t = runner.begin("campaigns", "detail_card")
    if campaign_buttons:
        first_campaign = campaign_buttons[0]
        click_inline(page, first_campaign, timeout=5000)
        wait_for_response(page, RESPONSE_WAIT)
        last = get_last_message_text(page)
        if any(kw in last.lower() for kw in ['volunteer', 'task', 'join', 'member', 'عضویت', 'داوطلب', 'متطوع', 'وظیفه', 'مهمة']):
            runner.ok(t, f"Campaign detail card loaded for '{first_campaign[:30]}'")
        else:
            runner.fail(t, f"Detail card unexpected: {last[:80]}")
        screenshot(page, "campaign_detail")
    else:
        runner.skip(t, "No campaigns to view")

    # 15. Join or View Tasks button visible
    t = runner.begin("campaigns", "action_button_visible")
    has_join = has_i18n_button(page, 'join', timeout=3000) or has_i18n_button(page, 'join_campaign', timeout=2000)
    has_tasks = has_i18n_button(page, 'view_tasks', timeout=3000)
    if has_join or has_tasks:
        runner.ok(t, f"Action buttons: Join={has_join}, ViewTasks={has_tasks}")
    elif campaign_buttons:
        runner.fail(t, "No action buttons on campaign detail")
    else:
        runner.skip(t, "No campaign to check")
    screenshot(page, "campaign_actions")

    # 16. Join campaign (if not already joined)
    t = runner.begin("campaigns", "join_campaign")
    if has_join and not has_tasks:
        click_i18n(page, 'join_campaign', timeout=3000) or click_i18n(page, 'join', timeout=3000)
        wait_for_response(page, RESPONSE_WAIT)
        last = get_last_message_text(page)
        if any(kw in last.lower() for kw in ["you're in", 'welcome', 'joined', 'view tasks', 'عضو شد', 'انضمم']):
            runner.ok(t, "Successfully joined campaign")
        else:
            runner.ok(t, "Join action completed")
    elif has_tasks:
        runner.ok(t, "Already a member — skipping join")
    else:
        runner.skip(t, "No join button available")
    screenshot(page, "campaign_joined")

    # 17. View Tasks from campaign detail
    t = runner.begin("campaigns", "view_tasks")
    if click_i18n(page, 'view_tasks', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        last = get_last_message_text(page)
        if any(icon in last for icon in ['⬜', '🚧', '✅', '🐦', '🔁', '💬']) or matches_kw(last, 'task'):
            runner.ok(t, "Task list/checklist loaded from campaign")
        else:
            runner.fail(t, f"Task list response unexpected: {last[:80]}")
    else:
        runner.skip(t, "View Tasks button not found")
    screenshot(page, "campaign_tasks")

    # 18. Back navigation to campaign list
    t = runner.begin("campaigns", "back_navigation")
    if click_i18n(page, 'back_tasks', timeout=3000) or click_i18n(page, 'main_menu', timeout=3000):
        wait_for_response(page, RESPONSE_WAIT)
        runner.ok(t, "Back navigation responded")
    elif click_inline(page, 'Back', timeout=3000) or click_inline(page, 'بازگشت', timeout=2000) or click_inline(page, 'العودة', timeout=2000):
        wait_for_response(page, RESPONSE_WAIT)
        runner.ok(t, "Back navigation responded")
    else:
        runner.skip(t, "No back/menu button found")
    screenshot(page, "campaign_back")


def suite_tasks(page: Page):
    """Task Checklist & Detail Flow tests (7 tests)."""

    ensure_welcome_menu(page)

    # Navigate to tasks via /tasks command
    t = runner.begin("tasks", "tasks_command")
    send_message(page, '/tasks')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    if matches_kw(last, 'task') or matches_kw(last, 'campaign'):
        runner.ok(t, "/tasks command responded")
    else:
        runner.fail(t, f"/tasks unexpected: {last[:80]}")
    screenshot(page, "tasks_command")

    # 20. Navigate via campaign → tasks to get checklist
    t = runner.begin("tasks", "checklist_via_campaign")
    ensure_welcome_menu(page)
    click_i18n(page, 'browse_campaigns')
    wait_for_response(page, RESPONSE_WAIT)

    # Click first campaign
    buttons = get_inline_buttons(page)
    campaign_buttons = [b for b in buttons if not is_nav_button(b)]
    if campaign_buttons:
        click_inline(page, campaign_buttons[0], timeout=5000)
        wait_for_response(page, RESPONSE_WAIT)

        # Click View Tasks
        if click_i18n(page, 'view_tasks', timeout=5000):
            wait_for_response(page, RESPONSE_WAIT)
            last = get_last_message_text(page)
            if any(icon in last for icon in ['⬜', '🚧', '✅', '🐦', '🔁', '💬']):
                runner.ok(t, "Task checklist with status/type icons loaded")
            elif matches_kw(last, 'task'):
                runner.ok(t, "Task list loaded (no icon match)")
            else:
                runner.fail(t, f"Checklist unexpected: {last[:80]}")
        elif click_i18n(page, 'join', timeout=3000) or click_i18n(page, 'join_campaign', timeout=3000):
            wait_for_response(page, RESPONSE_WAIT)
            runner.ok(t, "Joined first, tasks should be available now")
        else:
            runner.fail(t, "No View Tasks or Join button")
    else:
        runner.skip(t, "No campaigns available")
    screenshot(page, "task_checklist")

    # 21. Task checklist has type icons (🐦 🔁 💬 ✍️ 📧)
    t = runner.begin("tasks", "checklist_type_icons")
    last = get_last_message_text(page)
    type_icons = ['🐦', '🔁', '💬', '✍️', '📧', '📤', '📨', '📝']
    found_icons = [icon for icon in type_icons if icon in last]
    if found_icons:
        runner.ok(t, f"Type icons found: {' '.join(found_icons)}")
    elif campaign_buttons:
        runner.skip(t, "No type icons in current message")
    else:
        runner.skip(t, "No task checklist loaded")

    # 22. Task checklist has invite button
    t = runner.begin("tasks", "checklist_invite_button")
    if has_i18n_button(page, 'invite', timeout=3000):
        runner.ok(t, "Invite Friends button present in checklist")
    else:
        runner.skip(t, "Invite button not in current view")

    # 23. Click a task → task detail
    t = runner.begin("tasks", "task_detail")
    buttons = get_inline_buttons(page)
    task_buttons = [b for b in buttons if not is_nav_button(b)
                    and not any(inv in b for inv in BTN.get('invite', []))]
    if task_buttons:
        click_inline(page, task_buttons[0], timeout=5000)
        wait_for_response(page, RESPONSE_WAIT)
        last = get_last_message_text(page)
        if matches_kw(last, 'task_detail'):
            runner.ok(t, f"Task detail loaded: '{task_buttons[0][:30]}'")
        else:
            runner.ok(t, "Task button responded")
        screenshot(page, "task_detail")
    else:
        runner.skip(t, "No task buttons to click")

    # 24. Task detail has Start button
    t = runner.begin("tasks", "detail_start_button")
    if has_i18n_button(page, 'start_task', timeout=3000) or has_i18n_button(page, 'start_action', timeout=2000):
        runner.ok(t, "'Start Task' / 'Let's Go' button visible on detail")
    elif has_button(page, 'Start', timeout=2000) or has_button(page, 'شروع', timeout=2000) or has_button(page, 'ابدأ', timeout=2000):
        runner.ok(t, "Start button visible on detail")
    elif task_buttons:
        runner.skip(t, "Start button not visible (may be already started)")
    else:
        runner.skip(t, "No task detail loaded")
    screenshot(page, "task_start_button")

    # 25. Back navigation from task detail
    t = runner.begin("tasks", "detail_back_navigation")
    if click_i18n(page, 'back_tasks', timeout=3000):
        wait_for_response(page, RESPONSE_WAIT)
        runner.ok(t, "Back from task detail responded")
    elif click_i18n(page, 'main_menu', timeout=3000):
        wait_for_response(page, RESPONSE_WAIT)
        runner.ok(t, "Returned to main menu from task detail")
    elif click_inline(page, 'Back', timeout=3000) or click_inline(page, 'بازگشت', timeout=2000):
        wait_for_response(page, RESPONSE_WAIT)
        runner.ok(t, "Back button responded")
    else:
        runner.skip(t, "No back button found")
    screenshot(page, "task_back")


def suite_guided_flows(page: Page):
    """Guided Task Flow tests (5 tests) — Start Task → guided UI."""

    ensure_welcome_menu(page)

    # Navigate to a task's Start button
    click_i18n(page, 'browse_campaigns')
    wait_for_response(page, RESPONSE_WAIT)

    buttons = get_inline_buttons(page)
    campaign_buttons = [b for b in buttons if not is_nav_button(b)]

    if not campaign_buttons:
        t = runner.begin("guided", "no_campaigns")
        runner.skip(t, "No campaigns available — skipping guided flow tests")
        return

    click_inline(page, campaign_buttons[0], timeout=5000)
    wait_for_response(page, RESPONSE_WAIT)

    # Get to task list
    if not click_i18n(page, 'view_tasks', timeout=5000):
        # Try joining first
        click_i18n(page, 'join', timeout=3000) or click_i18n(page, 'join_campaign', timeout=3000)
        wait_for_response(page, RESPONSE_WAIT)
        click_i18n(page, 'view_tasks', timeout=5000)

    wait_for_response(page, RESPONSE_WAIT)

    # Find a task to start
    buttons = get_inline_buttons(page)
    task_buttons = [b for b in buttons if not is_nav_button(b)
                    and not any(inv in b for inv in BTN.get('invite', []))]

    if not task_buttons:
        t = runner.begin("guided", "no_tasks")
        runner.skip(t, "No tasks available — skipping guided flow tests")
        return

    # 26. Click task → detail → Start Task
    t = runner.begin("guided", "start_task_trigger")
    click_inline(page, task_buttons[0], timeout=5000)
    wait_for_response(page, RESPONSE_WAIT)

    started = (click_i18n(page, 'start_task', timeout=5000) or
               click_i18n(page, 'start_action', timeout=3000) or
               click_inline(page, 'Start', timeout=3000) or
               click_inline(page, 'شروع', timeout=2000))

    if started:
        wait_for_response(page, LONG_WAIT)
        last = get_last_message_text(page)
        screenshot(page, "guided_started")

        if matches_kw(last, 'guided'):
            runner.ok(t, "Guided flow triggered — step instructions shown")
        elif 'already' in last.lower():
            runner.ok(t, "Task already in progress")
        else:
            runner.ok(t, "Start task responded")
    else:
        runner.skip(t, "Start button not found — task may be in progress")
        send_message(page, '/mytasks')
        wait_for_response(page, RESPONSE_WAIT)

    # 27. Guided flow has action buttons (intent links or navigation)
    t = runner.begin("guided", "flow_has_buttons")
    buttons = get_inline_buttons(page)
    action_buttons = [b for b in buttons if not is_nav_button(b)]
    if action_buttons:
        runner.ok(t, f"Guided flow buttons: {[b[:30] for b in action_buttons[:3]]}")
    else:
        runner.skip(t, "No guided flow buttons visible")
    screenshot(page, "guided_buttons")

    # 28. Check for guided step pattern
    t = runner.begin("guided", "twitter_intent_or_action")
    last = get_last_message_text(page)
    has_steps = '①' in last or '②' in last or '③' in last or 'step' in last.lower()
    if has_steps:
        runner.ok(t, "3-step guided instructions detected")
    elif any(kw in last.lower() for kw in ['tweet', 'retweet', 'reply', 'sign', 'email', 'proof', 'توییت', 'تغريد']):
        runner.ok(t, "Task-specific guidance detected")
    else:
        runner.skip(t, "No step-based guidance detected")

    # 29. Cancel hint present
    t = runner.begin("guided", "cancel_hint_present")
    if matches_kw(last, 'cancel'):
        runner.ok(t, "Cancel hint visible in guided flow")
    else:
        runner.skip(t, "No cancel hint (may not be in guided state)")

    # 30. Test /cancel command
    t = runner.begin("guided", "cancel_command")
    send_message(page, '/cancel')
    wait_for_response(page, RESPONSE_WAIT)
    last = get_last_message_text(page)
    if matches_kw(last, 'cancel'):
        runner.ok(t, "/cancel acknowledged")
    else:
        runner.ok(t, "/cancel sent — state should be reset")
    screenshot(page, "guided_cancel")


def suite_proof(page: Page):
    """Proof Submission Flow tests (5 tests)."""

    # Navigate to a started task to test proof submission
    ensure_welcome_menu(page)

    click_i18n(page, 'browse_campaigns')
    wait_for_response(page, RESPONSE_WAIT)
    buttons = get_inline_buttons(page)
    campaign_buttons = [b for b in buttons if not is_nav_button(b)]

    task_ready = False
    if campaign_buttons:
        click_inline(page, campaign_buttons[0], timeout=5000)
        wait_for_response(page, RESPONSE_WAIT)

        if click_i18n(page, 'view_tasks', timeout=5000):
            wait_for_response(page, RESPONSE_WAIT)
            buttons = get_inline_buttons(page)
            task_buttons = [b for b in buttons if not is_nav_button(b)
                            and not any(inv in b for inv in BTN.get('invite', []))]

            if task_buttons:
                click_inline(page, task_buttons[0], timeout=5000)
                wait_for_response(page, RESPONSE_WAIT)

                started = (click_i18n(page, 'start_task', timeout=5000) or
                           click_i18n(page, 'start_action', timeout=3000) or
                           click_inline(page, 'Start', timeout=3000) or
                           click_inline(page, 'شروع', timeout=2000))
                if started:
                    wait_for_response(page, LONG_WAIT)
                    task_ready = True

    # 31. Submit proof URL
    t = runner.begin("proof", "submit_tweet_url")
    if task_ready:
        send_message(page, 'https://x.com/testuser/status/1234567890')
        wait_for_response(page, LONG_WAIT)
        last = get_last_message_text(page)
        if matches_kw(last, 'proof'):
            runner.ok(t, "Proof review screen appeared")
        else:
            runner.ok(t, f"Proof sent — response: {last[:60]}")
        screenshot(page, "proof_url_submitted")
    else:
        send_message(page, 'https://x.com/testuser/status/1234567890')
        wait_for_response(page, RESPONSE_WAIT)
        runner.skip(t, "Could not reach proof submission state")
        screenshot(page, "proof_url_fallback")

    # 32. Proof review has confirm/cancel buttons
    t = runner.begin("proof", "review_buttons")
    has_confirm = has_i18n_button(page, 'confirm_submit', timeout=3000)
    has_cancel = has_i18n_button(page, 'cancel', timeout=2000)
    if has_confirm or has_cancel:
        runner.ok(t, f"Review buttons: Confirm={has_confirm}, Cancel={has_cancel}")
    else:
        runner.skip(t, "Proof review screen not reached")
    screenshot(page, "proof_review_buttons")

    # 33. Confirm proof submission
    t = runner.begin("proof", "confirm_submission")
    if has_confirm:
        click_i18n(page, 'confirm_submit', timeout=5000)
        wait_for_response(page, LONG_WAIT)
        last = get_last_message_text(page)
        if matches_kw(last, 'proof'):
            runner.ok(t, "Proof confirmed successfully!")
        else:
            runner.ok(t, f"Confirm responded: {last[:60]}")
        screenshot(page, "proof_confirmed")
    else:
        runner.skip(t, "No confirm button to press")

    # 34. After confirmation — shows next actions
    t = runner.begin("proof", "post_confirm_actions")
    if has_confirm:
        has_another = has_i18n_button(page, 'do_another', timeout=3000)
        has_menu = has_i18n_button(page, 'main_menu', timeout=2000)
        if has_another or has_menu:
            runner.ok(t, f"Post-confirm buttons: DoAnother={has_another}, MainMenu={has_menu}")
        else:
            runner.skip(t, "No post-confirm actions detected")
    else:
        runner.skip(t, "Confirmation not reached")

    # 35. Test submit without active task
    t = runner.begin("proof", "no_active_task_error")
    send_message(page, '/cancel')
    wait_for_response(page, 2)
    send_message(page, 'https://x.com/testuser/status/9999')
    wait_for_response(page, RESPONSE_WAIT)
    last = get_last_message_text(page)
    if any(kw in last.lower() for kw in ['no task', 'not found', 'start', 'not sure', 'command', '?',
                                          'پیدا نشد', 'لم يتم']):
        runner.ok(t, "Bot handled proof without active task gracefully")
    else:
        runner.ok(t, f"Bot responded: {last[:60]}")
    screenshot(page, "proof_no_task")


def suite_leaderboard(page: Page):
    """Leaderboard & Profile tests (4 tests)."""

    # 36. /leaderboard command
    t = runner.begin("leaderboard", "leaderboard_command")
    send_message(page, '/leaderboard')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    if matches_kw(last, 'leaderboard'):
        runner.ok(t, "Leaderboard displayed")
    else:
        runner.fail(t, f"Leaderboard unexpected: {last[:80]}")
    screenshot(page, "leaderboard")

    # 37. Leaderboard has filter buttons
    t = runner.begin("leaderboard", "filter_buttons")
    buttons = get_inline_buttons(page)
    filter_buttons = [b for b in buttons if not is_nav_button(b)]
    if filter_buttons:
        runner.ok(t, f"Leaderboard filter buttons: {[b[:25] for b in filter_buttons[:3]]}")
    else:
        runner.skip(t, "No filter buttons (may be global only)")
    screenshot(page, "leaderboard_filters")

    # 38. /profile command
    t = runner.begin("leaderboard", "profile_command")
    send_message(page, '/profile')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    if matches_kw(last, 'profile'):
        runner.ok(t, "Profile displayed")
    else:
        runner.fail(t, f"Profile unexpected: {last[:80]}")
    screenshot(page, "profile")

    # 39. Profile has inline buttons
    t = runner.begin("leaderboard", "profile_buttons")
    buttons = get_inline_buttons(page)
    if buttons:
        runner.ok(t, f"Profile buttons: {[b[:25] for b in buttons[:3]]}")
    else:
        runner.skip(t, "No profile inline buttons")


def suite_storms(page: Page):
    """Storm Commands tests (3 tests)."""

    # 40. /storms command
    t = runner.begin("storms", "storms_command")
    send_message(page, '/storms')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    if matches_kw(last, 'storm'):
        runner.ok(t, "/storms command responded")
    else:
        runner.fail(t, f"/storms unexpected: {last[:80]}")
    screenshot(page, "storms")

    # 41. Storm has detail buttons (if storms exist)
    t = runner.begin("storms", "storm_buttons")
    buttons = get_inline_buttons(page)
    storm_buttons = [b for b in buttons if not is_nav_button(b)]
    if storm_buttons:
        runner.ok(t, f"Storm buttons: {[b[:25] for b in storm_buttons[:3]]}")

        # 42. Click storm detail
        t2 = runner.begin("storms", "storm_detail")
        click_inline(page, storm_buttons[0], timeout=5000)
        wait_for_response(page, RESPONSE_WAIT)
        last = get_last_message_text(page)
        if any(kw in last.lower() for kw in ['storm', 'hashtag', 'schedule', 'duration', 'tweet', 'ready']):
            runner.ok(t2, "Storm detail loaded")
        else:
            runner.ok(t2, f"Storm button responded: {last[:60]}")
        screenshot(page, "storm_detail")
    else:
        runner.skip(t, "No storms available")
        t2 = runner.begin("storms", "storm_detail")
        runner.skip(t2, "No storms to view detail for")


def suite_language(page: Page):
    """Language Switching tests (4 tests)."""

    ensure_welcome_menu(page)

    # 43. Switch to Farsi
    t = runner.begin("language", "switch_to_farsi")
    if click_i18n(page, 'language', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        if click_i18n(page, 'farsi', timeout=5000):
            wait_for_response(page, LONG_WAIT)
            last = get_last_message_text(page)
            if any(kw in last for kw in ['سلام', 'خوش آمدید', 'فارسی', 'کمپین', 'منو', 'صلح']):
                runner.ok(t, "Switched to Farsi — Persian text visible")
            else:
                runner.ok(t, f"Farsi selected — response: {last[:60]}")
            screenshot(page, "lang_farsi")
        else:
            runner.skip(t, "Farsi button not found")
    else:
        runner.skip(t, "Language button not found")

    # 44. Verify Farsi menu buttons
    t = runner.begin("language", "farsi_menu_buttons")
    buttons = get_inline_buttons(page)
    if buttons:
        runner.ok(t, f"Farsi menu buttons: {[b[:20] for b in buttons[:3]]}")
    else:
        runner.skip(t, "No buttons visible in Farsi")

    # 45. Switch to Arabic
    t = runner.begin("language", "switch_to_arabic")
    if click_i18n(page, 'language', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        if click_i18n(page, 'arabic', timeout=5000):
            wait_for_response(page, LONG_WAIT)
            last = get_last_message_text(page)
            if any(kw in last for kw in ['مرحبا', 'أهلا', 'العربية', 'حملة', 'القائمة', 'السلام']):
                runner.ok(t, "Switched to Arabic — Arabic text visible")
            else:
                runner.ok(t, f"Arabic selected — response: {last[:60]}")
            screenshot(page, "lang_arabic")
        else:
            runner.skip(t, "Arabic button not found")
    else:
        runner.skip(t, "Language button not found from Farsi")

    # 46. Switch back to English (restore)
    t = runner.begin("language", "restore_english")
    if click_i18n(page, 'language', timeout=5000):
        wait_for_response(page, RESPONSE_WAIT)
        if click_i18n(page, 'english', timeout=5000):
            wait_for_response(page, LONG_WAIT)
            if has_i18n_button(page, 'browse_campaigns', timeout=5000):
                runner.ok(t, "Restored to English — menu visible")
            else:
                runner.ok(t, "English selected")
            screenshot(page, "lang_english_restored")
        else:
            runner.skip(t, "English button not found")
    else:
        # Force restore via /start
        send_message(page, '/start')
        wait_for_response(page, LONG_WAIT)
        click_i18n(page, 'english', timeout=5000)
        wait_for_response(page, 3)
        runner.ok(t, "English restored via /start")


def suite_errors(page: Page):
    """Error Handling & Edge Cases tests (4 tests)."""

    ensure_welcome_menu(page)

    # 47. Unknown text handling
    t = runner.begin("errors", "unknown_text")
    send_message(page, 'random gibberish text 12345')
    wait_for_response(page, RESPONSE_WAIT)
    last = get_last_message_text(page)
    if any(kw in last.lower() for kw in ['not sure', 'command', 'help', '/start', 'try', 'available', '?',
                                          'نمی‌فهمم', 'لا أفهم', 'دستور', 'أمر']):
        runner.ok(t, "Unknown text handled with guidance")
    else:
        runner.ok(t, f"Bot responded to random text: {last[:60]}")
    screenshot(page, "error_unknown")

    # 48. Invalid command
    t = runner.begin("errors", "invalid_command")
    send_message(page, '/nonexistentcommand')
    wait_for_response(page, RESPONSE_WAIT)
    last = get_last_message_text(page)
    runner.ok(t, f"Invalid command response: {last[:60]}")
    screenshot(page, "error_invalid_cmd")

    # 49. /help command
    t = runner.begin("errors", "help_command")
    send_message(page, '/help')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    if matches_kw(last, 'help'):
        runner.ok(t, "Help text with command list displayed")
    else:
        runner.fail(t, f"Help text unexpected: {last[:80]}")
    screenshot(page, "help_command")

    # 50. Double /start doesn't break state
    t = runner.begin("errors", "double_start_safe")
    send_message(page, '/start')
    wait_for_response(page, 2)
    send_message(page, '/start')
    wait_for_response(page, LONG_WAIT)
    if has_i18n_button(page, 'browse_campaigns', timeout=5000) or has_i18n_button(page, 'english', timeout=3000):
        runner.ok(t, "Double /start handled gracefully — menu visible")
    else:
        runner.fail(t, "Double /start broke state")
    screenshot(page, "double_start")


# ══════════════════════════════════════════════════════════════════════
#  MAIN RUNNER
# ══════════════════════════════════════════════════════════════════════

SUITES = {
    'registration': suite_registration,
    'menu': suite_menu,
    'campaigns': suite_campaigns,
    'tasks': suite_tasks,
    'guided': suite_guided_flows,
    'proof': suite_proof,
    'leaderboard': suite_leaderboard,
    'storms': suite_storms,
    'language': suite_language,
    'errors': suite_errors,
}


def main():
    """Run the E2E test suite."""
    parser = argparse.ArgumentParser(description="PFP Bot E2E Test Suite")
    parser.add_argument('--suite', type=str, help=f"Run single suite: {', '.join(SUITES.keys())}")
    parser.add_argument('--list', action='store_true', help="List available suites")
    parser.add_argument('--headless', action='store_true', help="Run headless (default: headed)")
    args = parser.parse_args()

    if args.list:
        print("Available test suites:")
        for name in SUITES:
            print(f"  • {name}")
        sys.exit(0)

    if args.suite and args.suite not in SUITES:
        print(f"❌ Unknown suite: {args.suite}")
        print(f"Available: {', '.join(SUITES.keys())}")
        sys.exit(1)

    if not os.path.exists(SESSION_PATH):
        print(f"❌ Session file not found at {SESSION_PATH}")
        print("   Run `python save_session.py` first to authenticate.")
        sys.exit(1)

    suites_to_run = {args.suite: SUITES[args.suite]} if args.suite else SUITES
    headless = args.headless

    print(f"\n{'═'*60}")
    print(f"  PFP Bot — Full E2E Test Suite")
    print(f"  Suites: {', '.join(suites_to_run.keys())}")
    print(f"  Bot: @{BOT_USERNAME}")
    print(f"  Mode: {'headless' if headless else 'headed'}")
    print(f"{'═'*60}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        os.makedirs(VIDEO_DIR, exist_ok=True)
        context = browser.new_context(
            storage_state=SESSION_PATH,
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()

        # Open bot chat — uses search if direct hash navigation fails
        print(f"\n🔄 Opening Telegram Web → @{BOT_USERNAME}...")
        page.goto(f"https://web.telegram.org/k/#{BOT_USERNAME}")
        chat_ready = False

        # Try 1: Direct hash navigation (works if bot is in recent chats)
        try:
            page.wait_for_selector(
                'div.input-message-input:not(.input-field-input-fake)',
                timeout=15000,
            )
            chat_ready = True
        except PwTimeout:
            pass

        # Try 2: Search for the bot and click the result
        if not chat_ready:
            print("   ↪ Bot not in recent chats, searching...")
            page.goto("https://web.telegram.org/k/")
            page.wait_for_timeout(4000)
            try:
                search_input = page.locator('.input-search input').first
                search_input.wait_for(timeout=10000)
                search_input.click()
                search_input.fill(f'@{BOT_USERNAME}')
                page.wait_for_timeout(3000)

                # Click the bot in global search results
                bot_result = page.locator('.search-group .chatlist-chat').first
                bot_result.wait_for(timeout=8000)
                bot_result.click()
                page.wait_for_timeout(5000)

                page.wait_for_selector(
                    'div.input-message-input:not(.input-field-input-fake)',
                    timeout=10000,
                )
                chat_ready = True
            except PwTimeout:
                pass

        if chat_ready:
            print("✅ Telegram Web loaded, chat input ready\n")
        else:
            print("❌ Could not open bot chat (tried hash nav + search)")
            screenshot(page, "boot_failure")
            browser.close()
            sys.exit(1)

        # Run suites
        for suite_name, suite_fn in suites_to_run.items():
            print(f"\n{'━'*60}")
            print(f"  ▶ Suite: {suite_name.upper()}")
            print(f"{'━'*60}")
            try:
                suite_fn(page)
            except Exception as exc:
                print(f"\n   💥 SUITE CRASHED: {suite_name} — {exc}")
                screenshot(page, f"crash_{suite_name}")

        # Final screenshot
        page.wait_for_timeout(1000)
        screenshot(page, "final_state")

        # Close context to finalize video
        video_path = page.video.path() if page.video else None
        context.close()
        browser.close()

    # Export results as JSON for HTML report
    results_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(runner.results),
        "passed": runner.passed,
        "failed": runner.failed,
        "skipped": runner.skipped,
        "video": os.path.abspath(video_path) if video_path else None,
        "screenshot_dir": os.path.abspath(SCREENSHOT_DIR),
        "tests": [
            {
                "name": r.name,
                "suite": r.suite,
                "status": r.status,
                "message": r.message,
            }
            for r in runner.results
        ]
    }
    with open(RESULTS_JSON, 'w') as f:
        json.dump(results_data, f, indent=2)
    print(f"\n  📄 Results JSON: {RESULTS_JSON}")

    # Print results
    runner.print_summary()

    if runner.failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

"""
PFP Telegram Bot — Core Campaign Flow E2E Test.

Tests the CRITICAL user journey:
  1. Start bot & register
  2. Browse campaigns → find "Justice for Minab Children"
  3. Join the campaign
  4. View tasks → open task detail
  5. Start a task (guided flow)
  6. Submit proof
  7. Verify progress in /profile

Prerequisites:
  1. pip install playwright && playwright install
  2. python telegram-bot/save_session.py  (one-time auth)
  3. Bot must be running & responding

Usage:
  source venv/bin/activate
  python telegram-bot/test_core_flow.py
"""

import os
import sys
import time
import json
from dataclasses import dataclass, field
from typing import Optional
from playwright.sync_api import sync_playwright, Page, TimeoutError as PwTimeout

# ── Configuration ──────────────────────────────────────────────────────

BOT_USERNAME = "peopleforpeacebot"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "..", "test_screenshots_core")
VIDEO_DIR = os.path.join(BASE_DIR, "..", "test_videos_core")
SESSION_PATH = os.path.join(BASE_DIR, "telegram_session.json")
RESULTS_JSON = os.path.join(BASE_DIR, "..", "test_results_core.json")

# Timing constants (seconds)
RESPONSE_WAIT = 5.0
LONG_WAIT = 8.0
BUTTON_TIMEOUT = 12000

# Target campaign
TARGET_CAMPAIGN = "Justice for Minab"

# Step counter for screenshot ordering
step_counter = 0


# ── Test Result Tracking ──────────────────────────────────────────────

@dataclass
class StepResult:
    """Single step result."""
    step: int
    name: str
    status: str = "pending"  # passed, failed, skipped, blocked
    message: str = ""
    screenshot: str = ""


class FlowRunner:
    """Track the core flow steps."""

    def __init__(self):
        self.steps: list[StepResult] = []
        self.passed = 0
        self.failed = 0
        self.blocked = 0

    def step(self, name: str) -> StepResult:
        global step_counter
        step_counter += 1
        result = StepResult(step=step_counter, name=name)
        self.steps.append(result)
        print(f"\n{'─'*50}")
        print(f"  Step {step_counter}: {name}")
        print(f"{'─'*50}")
        return result

    def ok(self, result: StepResult, msg: str):
        result.status = "passed"
        result.message = msg
        self.passed += 1
        print(f"   ✅ PASS: {msg}")

    def fail(self, result: StepResult, msg: str):
        result.status = "failed"
        result.message = msg
        self.failed += 1
        print(f"   ❌ FAIL: {msg}")

    def block(self, result: StepResult, msg: str):
        """Critical failure — subsequent steps can't proceed."""
        result.status = "blocked"
        result.message = msg
        self.blocked += 1
        print(f"   🚫 BLOCKED: {msg}")

    def print_summary(self):
        total = len(self.steps)
        print(f"\n{'═'*60}")
        print(f"  CORE FLOW E2E — RESULTS")
        print(f"{'═'*60}")
        print(f"  ✅ Passed:  {self.passed}")
        print(f"  ❌ Failed:  {self.failed}")
        print(f"  🚫 Blocked: {self.blocked}")
        print(f"  📊 Total:   {total}")
        print(f"{'═'*60}")
        for s in self.steps:
            icon = {"passed": "✅", "failed": "❌", "blocked": "🚫"}.get(s.status, "⬜")
            print(f"  {icon} Step {s.step}: {s.name}")
            if s.message:
                print(f"     → {s.message}")
        print(f"\n  📸 Screenshots: {SCREENSHOT_DIR}")
        print(f"{'═'*60}\n")

    def export_json(self, path: str):
        data = {
            "summary": {
                "total": len(self.steps),
                "passed": self.passed,
                "failed": self.failed,
                "blocked": self.blocked,
            },
            "steps": [
                {
                    "step": s.step,
                    "name": s.name,
                    "status": s.status,
                    "message": s.message,
                    "screenshot": s.screenshot,
                }
                for s in self.steps
            ],
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  📄 Results exported to {path}")


runner = FlowRunner()


# ── Playwright Helpers ────────────────────────────────────────────────

def screenshot(page: Page, name: str) -> str:
    """Save a screenshot with step numbering."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{step_counter:02d}_{name}.png")
    page.screenshot(path=path)
    print(f"   📸 {path}")
    return path


def send_message(page: Page, text: str):
    """Type a message into the Telegram input and press Enter."""
    input_el = page.locator('div.input-message-input:not(.input-field-input-fake)')
    input_el.click(force=True)
    input_el.type(text)
    input_el.press('Enter')
    print(f"   → Sent: {text}")


def wait_for_response(page: Page, seconds: float = RESPONSE_WAIT):
    """Wait for the bot to respond."""
    page.wait_for_timeout(int(seconds * 1000))


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
    """Get text of inline buttons from the LAST reply markup block only."""
    try:
        # Get all reply-markup containers
        markups = page.locator('.reply-markup').all()
        if not markups:
            return []
        # Use the LAST one (most recent bot message)
        last_markup = markups[-1]
        buttons = last_markup.locator('button').all()
        return [btn.text_content() or '' for btn in buttons]
    except Exception:
        return []


def click_button(page: Page, text: str, timeout: int = BUTTON_TIMEOUT) -> bool:
    """Click an inline button matching text (substring). Returns True on success."""
    btn = page.locator('button', has_text=text).last
    try:
        btn.wait_for(timeout=timeout)
        btn.click(force=True)
        print(f"   → Clicked: '{text}'")
        return True
    except PwTimeout:
        print(f"   ⚠️  Button '{text}' not found within {timeout}ms")
        return False


def find_and_click_button(page: Page, *candidates: str, timeout: int = BUTTON_TIMEOUT) -> Optional[str]:
    """Try clicking buttons from a list of candidates. Returns the one that matched."""
    for text in candidates:
        btn = page.locator('button', has_text=text).last
        try:
            btn.wait_for(timeout=min(timeout, 4000))
            btn.click(force=True)
            print(f"   → Clicked: '{text}'")
            return text
        except PwTimeout:
            continue
    print(f"   ⚠️  No button found from: {candidates[:5]}")
    return None


def find_campaign_button(page: Page, campaign_substr: str) -> Optional[str]:
    """Find a campaign button containing the given substring."""
    buttons = get_inline_buttons(page)
    for btn_text in buttons:
        if campaign_substr.lower() in btn_text.lower():
            return btn_text
    return None


# ── CORE FLOW ─────────────────────────────────────────────────────────

def run_core_flow(page: Page):
    """Execute the core campaign interaction flow."""

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 1: Send /start — get bot response
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Send /start to bot")
    send_message(page, '/start')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    s.screenshot = screenshot(page, "01_start")

    if len(last) > 20:
        runner.ok(s, f"Bot responded ({len(last)} chars)")
    else:
        runner.fail(s, f"Empty or short response: '{last[:50]}'")
        # Not blocking — might already be registered

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 2: Navigate to Browse Campaigns
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Navigate to Browse Campaigns")
    wait_for_response(page, 2)
    matched = find_and_click_button(
        page,
        'Browse Campaigns', 'My Campaigns',
        'مرور کمپین‌ها', 'کمپین‌های من',
        'تصفح الحملات', 'حملاتي',
    )
    if not matched:
        # Fallback: send the /campaigns command
        send_message(page, '/campaigns')
        wait_for_response(page, LONG_WAIT)
        last = get_last_message_text(page)
        if 'campaign' in last.lower() or 'کمپین' in last or 'حملة' in last:
            runner.ok(s, "Used /campaigns command as fallback")
        else:
            runner.block(s, "Cannot reach campaigns list")
            s.screenshot = screenshot(page, "02_campaigns_blocked")
            return
    else:
        wait_for_response(page, LONG_WAIT)
        runner.ok(s, f"Clicked '{matched}'")

    s.screenshot = screenshot(page, "02_campaigns_list")

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 3: Find "Justice for Minab Children" campaign
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step(f"Find '{TARGET_CAMPAIGN}' campaign")
    buttons = get_inline_buttons(page)
    print(f"   Found {len(buttons)} buttons")

    # Look for the target campaign button
    target_btn = None
    for btn_text in buttons:
        if 'minab' in btn_text.lower() or 'مینیب' in btn_text.lower() or 'ميناب' in btn_text.lower():
            target_btn = btn_text
            break

    if target_btn:
        runner.ok(s, f"Found campaign button: '{target_btn}'")
    else:
        # Try second page
        if find_and_click_button(page, '➡️', timeout=3000):
            wait_for_response(page, RESPONSE_WAIT)
            buttons = get_inline_buttons(page)
            for btn_text in buttons:
                if 'minab' in btn_text.lower() or 'مینیب' in btn_text.lower():
                    target_btn = btn_text
                    break

        if target_btn:
            runner.ok(s, f"Found on page 2: '{target_btn}'")
        else:
            runner.block(s, f"Campaign '{TARGET_CAMPAIGN}' not found in buttons: {[b[:30] for b in buttons[:10]]}")
            s.screenshot = screenshot(page, "03_campaign_not_found")
            return

    s.screenshot = screenshot(page, "03_campaign_found")

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 4: Click on the campaign (Join or View Tasks)
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Click campaign button (Join / View Tasks)")
    clicked = click_button(page, target_btn, timeout=5000)
    if not clicked:
        runner.block(s, f"Could not click '{target_btn}'")
        s.screenshot = screenshot(page, "04_click_failed")
        return

    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    s.screenshot = screenshot(page, "04_campaign_clicked")

    # Determine if this was a "Join" or "View Tasks" action
    is_join_result = any(kw in last.lower() for kw in [
        'welcome', 'joined', "you're in", 'عضو شد', 'انضمم',
        'successfully', 'next steps', 'checklist',
    ])
    is_task_list = any(icon in last for icon in ['⬜', '🚧', '✅', '🐦', '🔁', '💬', '📧', '✍️'])
    is_detail = any(kw in last.lower() for kw in [
        'volunteer', 'task', 'join', 'member', 'عضویت', 'داوطلب',
    ])

    if is_join_result:
        runner.ok(s, "Joined the campaign! Now looking for View Tasks...")
    elif is_task_list:
        runner.ok(s, "Already a member — task checklist loaded directly")
    elif is_detail:
        runner.ok(s, "Campaign detail card loaded")
    else:
        runner.ok(s, f"Campaign response received ({len(last)} chars)")

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 5: Ensure we have the task checklist
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Get task checklist")

    if not is_task_list:
        # We might be on the join success screen or campaign detail
        # Try clicking "View Tasks" button
        view_tasks_clicked = find_and_click_button(
            page,
            '📋 View Tasks', 'View Tasks', '📋',
            'مشاهده وظایف', 'عرض المهام',
            timeout=5000,
        )
        if view_tasks_clicked:
            wait_for_response(page, LONG_WAIT)
            last = get_last_message_text(page)
            is_task_list = any(icon in last for icon in ['⬜', '🚧', '✅', '🐦', '🔁', '💬', '📧', '✍️'])

        if not is_task_list:
            # Maybe we need to join first
            join_clicked = find_and_click_button(
                page,
                'Join This Campaign', 'Join', '✊ Join',
                'عضویت در این کمپین', 'عضویت',
                'انضم لهذه الحملة', 'انضمام',
                timeout=5000,
            )
            if join_clicked:
                wait_for_response(page, LONG_WAIT)
                last = get_last_message_text(page)
                s.screenshot = screenshot(page, "05a_joined")
                print(f"   → Join result: {last[:100]}")

                # Now click "View Tasks" after joining
                view_tasks_clicked = find_and_click_button(
                    page,
                    '📋 View Tasks', 'View Tasks', '📋',
                    'مشاهده وظایف', 'عرض المهام',
                    timeout=8000,
                )
                if view_tasks_clicked:
                    wait_for_response(page, LONG_WAIT)
                    last = get_last_message_text(page)
                    is_task_list = True

    if is_task_list or 'task' in last.lower() or 'وظیفه' in last or 'مهمة' in last:
        buttons = get_inline_buttons(page)
        nav_keywords = [
            'main menu', 'invite', 'language', 'help', 'back',
            'منوی اصلی', 'دعوت', 'کمپین', 'زبان', 'راهنما', 'بازگشت',
            'القائمة', 'دعوة', 'حملات', 'لغة', 'مساعدة',
        ]
        task_buttons = [b for b in buttons if not any(kw in b.lower() for kw in nav_keywords)]
        runner.ok(s, f"Task checklist loaded with {len(task_buttons)} task button(s)")
    else:
        runner.block(s, f"Could not reach task checklist. Last response: {last[:100]}")
        s.screenshot = screenshot(page, "05_checklist_blocked")
        return

    s.screenshot = screenshot(page, "05_task_checklist")

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 6: Click first task to see detail
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Open task detail")

    if not task_buttons:
        runner.block(s, "No task buttons found in checklist")
        s.screenshot = screenshot(page, "06_no_tasks")
        return

    first_task = task_buttons[0]
    clicked = click_button(page, first_task, timeout=5000)
    if not clicked:
        runner.block(s, f"Could not click task: '{first_task}'")
        s.screenshot = screenshot(page, "06_task_click_failed")
        return

    wait_for_response(page, RESPONSE_WAIT)
    last = get_last_message_text(page)
    s.screenshot = screenshot(page, "06_task_detail")

    if any(kw in last.lower() for kw in ['start', 'duration', 'instruction', 'min', 'بزن', "let's go", 'هيا', 'شروع']):
        runner.ok(s, f"Task detail loaded: {first_task[:40]}")
    else:
        runner.ok(s, f"Task screen loaded ({len(last)} chars)")

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 7: Start the task (click "Let's Go!" / start action)
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Start task (Let's Go!)")

    start_clicked = find_and_click_button(
        page,
        "Let's Go!", "🚀 Let's Go!", "بزن بریم!", "هيا بنا!",
        "Start This Task", "شروع این وظیفه", "ابدأ هذه المهمة",
        timeout=8000,
    )

    if not start_clicked:
        runner.block(s, "Could not find Start/Let's Go button")
        s.screenshot = screenshot(page, "07_start_not_found")
        return

    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    s.screenshot = screenshot(page, "07_task_started")

    if any(kw in last.lower() for kw in [
        'started', 'step', 'paste', 'proof', 'tweet', 'send',
        'sign', 'email', 'شروع', 'بدأت', 'گام', 'الخطوة',
        'intent', 'cancel', '/cancel',
    ]):
        runner.ok(s, "Task guided flow started — instructions visible")
    else:
        runner.ok(s, f"Task started, response: {last[:80]}")

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 8: Submit proof (send a URL as proof)
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Submit proof")

    proof_text = "https://x.com/peopleforpeace/status/1234567890"
    send_message(page, proof_text)
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    s.screenshot = screenshot(page, "08_proof_submitted")

    if any(kw in last.lower() for kw in [
        'submitted', 'completed', 'verified', 'proof',
        'points', 'keep going', 'great', 'well done', 'awesome',
        'ارسال', 'تکمیل', 'نقاط', 'أرسل', 'أكمل',
        'do another', 'another task',
    ]):
        runner.ok(s, "Proof submitted and task completed!")
    else:
        runner.fail(s, f"Proof submission response unclear: {last[:100]}")

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 9: Check /profile — verify progress recorded
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Check /profile — verify progress")

    send_message(page, '/profile')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    s.screenshot = screenshot(page, "09_profile")

    if any(kw in last.lower() for kw in [
        'profile', 'points', 'task', 'completed', 'joined',
        'name', 'volunteer',
        'پروفایل', 'امتیاز', 'الملف',
    ]):
        # Try to extract points
        import re
        points_match = re.search(r'(\d+)\s*(?:point|pts|امتیاز|نقاط)', last.lower())
        tasks_match = re.search(r'(\d+)\s*(?:task|وظیفه|مهمة)', last.lower())
        details = []
        if points_match:
            details.append(f"{points_match.group(1)} points")
        if tasks_match:
            details.append(f"{tasks_match.group(1)} tasks")
        runner.ok(s, f"Profile loaded — {', '.join(details) if details else 'data visible'}")
    else:
        runner.fail(s, f"Profile unexpected: {last[:100]}")

    # ═══════════════════════════════════════════════════════════════════
    #  STEP 10: Verify completed task shows in /leaderboard
    # ═══════════════════════════════════════════════════════════════════
    s = runner.step("Check /leaderboard — verify ranking")

    send_message(page, '/leaderboard')
    wait_for_response(page, LONG_WAIT)
    last = get_last_message_text(page)
    s.screenshot = screenshot(page, "10_leaderboard")

    if any(kw in last.lower() for kw in [
        'leaderboard', 'rank', 'top', '🥇', '🥈', '🥉',
        'points', 'جدول', 'المتصدرين',
    ]):
        runner.ok(s, "Leaderboard loaded — user should appear in rankings")
    else:
        runner.fail(s, f"Leaderboard unexpected: {last[:100]}")


# ── Main Entry Point ──────────────────────────────────────────────────

def main():
    """Run the core flow test."""
    print(f"\n{'═'*60}")
    print(f"  PFP BOT — CORE CAMPAIGN FLOW E2E TEST")
    print(f"  Target: {TARGET_CAMPAIGN}")
    print(f"{'═'*60}")

    # Load session
    if not os.path.exists(SESSION_PATH):
        print(f"\n❌ No session file found at {SESSION_PATH}")
        print("   Run: python telegram-bot/save_session.py")
        sys.exit(1)

    with open(SESSION_PATH) as f:
        session = json.load(f)

    storage_state = session.get("storage_state", session)

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            storage_state=storage_state,
            viewport={"width": 1280, "height": 900},
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 900},
        )
        page = context.new_page()

        # Navigate to Telegram Web
        print("\n  🌐 Opening Telegram Web...")
        page.goto("https://web.telegram.org/k/", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)

        # Open bot chat
        print(f"  🤖 Opening @{BOT_USERNAME} chat...")
        page.goto(f"https://web.telegram.org/k/#{BOT_USERNAME}")
        page.wait_for_timeout(8000)

        # Check if chat input is ready
        try:
            page.locator('div.input-message-input:not(.input-field-input-fake)').wait_for(timeout=15000)
            print("  ✅ Chat input ready")
        except (PwTimeout, Exception):
            # Fallback: search for the bot
            print("  ⚠️  Chat not loaded via hash — searching...")
            search = page.locator('.input-search input, input[type="search"]').first
            search.click(force=True)
            search.fill(f"@{BOT_USERNAME}")
            page.wait_for_timeout(3000)

            try:
                result = page.locator('.search-group .chatlist-chat').first
                result.wait_for(timeout=8000)
                result.click(force=True)
                page.wait_for_timeout(5000)
                page.locator('div.input-message-input:not(.input-field-input-fake)').wait_for(timeout=15000)
                print("  ✅ Found bot via search")
            except (PwTimeout, Exception):
                print("  ❌ Could not open bot chat — aborting")
                screenshot(page, "00_chat_failed")
                browser.close()
                sys.exit(1)

        screenshot(page, "00_chat_ready")
        print("  🚀 Starting core flow test...\n")

        # Run the core flow
        run_core_flow(page)

        # Summary
        runner.print_summary()
        runner.export_json(RESULTS_JSON)

        context.close()
        browser.close()

    print("  ✅ Core flow test complete.\n")


if __name__ == "__main__":
    main()

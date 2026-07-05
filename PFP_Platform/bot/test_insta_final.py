import os
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "telegram_session.json")

def get_buttons(page):
    try:
        page.wait_for_selector('.reply-markup button', timeout=5000)
        buttons = page.locator('.reply-markup button').all()
        return [(i, b.text_content() or "") for i, b in enumerate(buttons)]
    except Exception:
        return []

def click_matching_btn(page, keywords):
    for i in range(5): # retry logic
        buttons = get_buttons(page)
        print(f"   Visible buttons: {[b[1] for b in buttons]}")
        for idx, text in buttons:
            text_lower = text.lower()
            if any(kw.lower() in text_lower for kw in keywords):
                print(f"   👉 Clicking: {text}")
                try:
                    page.locator('.reply-markup button').nth(idx).click(force=True)
                    time.sleep(4)
                    return True
                except Exception as e:
                    print(f"   ❌ Error clicking button: {e}")
        time.sleep(2)
    return False

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--window-size=1200,800'])
        context = browser.new_context(storage_state=SESSION_PATH, viewport={'width': 1200, 'height': 800})
        page = context.new_page()

        print("\n🤖 Initiating Final E2E Test against @fatemesbati_bot")
        page.goto('https://web.telegram.org/k/#@fatemesbati_bot')
        
        try:
            page.wait_for_selector('div.input-message-input:not(.input-field-input-fake)', timeout=15000)
            print("✅ Chat interface loaded.")
        except Exception:
            print("❌ Failed to load chat.")
            return
            
        input_el = page.locator('div.input-message-input:not(.input-field-input-fake)')
        
        print("🔄 Resetting bot state (/cancel + /start)...")
        input_el.click(force=True); input_el.fill('/cancel'); input_el.press('Enter')
        time.sleep(2)
        input_el.click(force=True); input_el.fill('/start'); input_el.press('Enter')
        time.sleep(4)
        
        # In case language selector opens, just pick anything or try to find Browse
        # Browse Campaigns
        print("\n▶️ Navigating to Browse Campaigns...")
        if not click_matching_btn(page, ['click here to open', 'campaigns', 'مرور', 'تصفح']):
            print("Trying to bypass language picker...")
            click_matching_btn(page, ['english', 'فارسی', 'العربية'])
            time.sleep(3)
            click_matching_btn(page, ['campaigns', 'مرور', 'تصفح'])
            
        print("\n▶️ Clicking a Campaign...")
        # A campaign is usually any button that's not 'Back' or 'Menu'
        # Get all buttons, pick the first one that doesn't match standard nav
        buttons = get_buttons(page)
        nav_kws = ['back', 'menu', 'بازگشت', 'العودة', 'منو', 'next', 'prev']
        tgt_idx = -1
        for idx, text in buttons:
            if not any(n in text.lower() for n in nav_kws):
                tgt_idx = idx
                break
        if tgt_idx >= 0:
            print(f"   👉 Clicking campaign: {buttons[tgt_idx][1]}")
            page.locator('.reply-markup button').nth(tgt_idx).click(force=True)
            time.sleep(4)
            
        print("\n▶️ Accessing Tasks...")
        click_matching_btn(page, ['view tasks', 'مشاهده', 'عرض المهام', 'join', 'عضویت', 'انضمام'])
        # If it was 'Join', we might need to click View Tasks next
        buttons = get_buttons(page)
        if any('task' in b[1].lower() or 'مشاهده' in b[1] for b in buttons):
            click_matching_btn(page, ['view tasks', 'مشاهده', 'عرض المهام'])
            
        print("\n▶️ Selecting a Task...")
        buttons = get_buttons(page)
        tgt_idx = -1
        for idx, text in buttons:
            if not any(n in text.lower() for n in nav_kws + ['invite', 'دعوت']):
                tgt_idx = idx
                break
        if tgt_idx >= 0:
            print(f"   👉 Clicking task: {buttons[tgt_idx][1]}")
            page.locator('.reply-markup button').nth(tgt_idx).click(force=True)
            time.sleep(4)
            
        print("\n▶️ Starting Task...")
        click_matching_btn(page, ['start', 'شروع', 'ابدأ', "let's", 'بزن'])
        
        print("\n▶️ Selecting Instagram...")
        click_matching_btn(page, ['instagram', 'اینستاگرام', 'انستغرام'])
        
        print("\n🔍 EVALUATING NEW FEATURE BUTTONS...")
        buttons = get_buttons(page)
        texts = [b[1] for b in buttons]
        print(f"Available Options: {texts}")
        
        support_ok = any('support' in t.lower() or 'حمایت' in t or 'دعم' in t for t in texts)
        child_ok = any("child" in t.lower() or 'کودک' in t or 'طفل' in t for t in texts)
        
        page.screenshot(path="test_proof_insta.png")
        print("📸 Captured proof screenshot (test_proof_insta.png)")
        
        if support_ok and child_ok:
            print("\n✅ MISSION ACCOMPLISHED: The Instagram flow correctly split into Support and Child Story options!")
        else:
            print(f"\n❌ FAILED. Expected Support/Child buttons, but got: {texts}")
            
        browser.close()

if __name__ == "__main__":
    run_test()

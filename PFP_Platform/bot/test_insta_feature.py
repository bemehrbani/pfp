import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "telegram_session.json")

def wait_for_response(page, seconds=4):
    page.wait_for_timeout(int(seconds * 1000))

def has_button(page, text, timeout=5000):
    try:
        page.locator('button', has_text=text).last.wait_for(timeout=timeout)
        return True
    except Exception:
        return False

def click_button(page, text, timeout=5000):
    try:
        btn = page.locator('button', has_text=text).last
        btn.wait_for(timeout=timeout)
        btn.click(force=True)
        print(f"Clicked: {text}")
        return True
    except Exception as e:
        print(f"Failed to click {text}: {e}")
        return False

def run_test():
    with sync_playwright() as p:
        if not os.path.exists(SESSION_PATH):
            print("Session not found. Please authenticate first.")
            return

        browser = p.chromium.launch(headless=True, args=['--window-size=1200,800'])
        context = browser.new_context(storage_state=SESSION_PATH, viewport={'width': 1200, 'height': 800})
        page = context.new_page()

        print("Navigating to Telegram Web...")
        page.goto('https://web.telegram.org/k/#@fatemesbati_bot')
        page.wait_for_selector('div.input-message-input:not(.input-field-input-fake)', timeout=30000)

        # Clear state
        print("Sending /start...")
        input_el = page.locator('div.input-message-input:not(.input-field-input-fake)')
        input_el.click(force=True)
        input_el.fill('/start')
        input_el.press('Enter')
        wait_for_response(page, 5)

        print("Navigating to Browse Campaigns...")
        if not click_button(page, 'Browse Campaigns'):
            click_button(page, 'English')
            wait_for_response(page, 3)
            click_button(page, 'Browse Campaigns')

        wait_for_response(page, 5)
        
        # Click the first campaign
        buttons = page.locator('.reply-markup button').all()
        if not buttons:
            print("No campaign buttons found.")
            return
            
        print("Clicking a campaign...")
        buttons[0].click(force=True)
        wait_for_response(page, 4)

        print("Clicking View Tasks or Join...")
        if not click_button(page, "View Tasks"):
            click_button(page, "Join This Campaign")
            wait_for_response(page, 4)
            click_button(page, "View Tasks")
            
        wait_for_response(page, 5)

        print("Clicking a Task (Instagram related)...")
        # Try to find a task button
        buttons = page.locator('.reply-markup button').all()
        for btn in buttons:
            text = btn.text_content()
            if text and not any(nav in text for nav in ['Back', 'Main', 'Menu']):
                print(f"Clicking task: {text}")
                btn.click(force=True)
                break
        
        wait_for_response(page, 4)
        
        print("Clicking Start Task...")
        click_button(page, "Start This Task")
        wait_for_response(page, 4)
        
        print("Clicking Instagram platform...")
        click_button(page, "Instagram")
        wait_for_response(page, 4)
        
        # Now verify the two buttons
        if has_button(page, "Support Posts"):
            print("✅ 'Support Posts and Activists' button found!")
        else:
            print("❌ 'Support Posts and Activists' button missing!")
            
        if has_button(page, "Share a Child's Story"):
            print("✅ 'Share a Child's Story' button found!")
        else:
            print("❌ 'Share a Child's Story' button missing!")
            
        print("Test complete.")
        browser.close()

if __name__ == "__main__":
    run_test()

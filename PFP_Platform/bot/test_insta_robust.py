import os
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "telegram_session.json")

def click_btn(page, text, exact=False):
    print(f"  -> Attempting to click: {text}")
    try:
        # Give it some time to appear
        page.wait_for_selector(f'button:has-text("{text}")', timeout=8000)
        # Find all buttons with this text
        locs = page.locator(f'button:has-text("{text}")').all()
        if not locs:
            print(f"     ❌ Button '{text}' not found!")
            return False
        # Click the last one (most recent message)
        locs[-1].click(force=True)
        print(f"     ✅ Clicked: {text}")
        return True
    except Exception as e:
        print(f"     ❌ Error clicking '{text}': {e}")
        return False

def verify_btn(page, text):
    try:
        page.wait_for_selector(f'button:has-text("{text}")', timeout=5000)
        locs = page.locator(f'button:has-text("{text}")').all()
        if locs:
            print(f"     ✅ Verified button exists: {text}")
            return True
    except Exception:
        pass
    print(f"     ❌ Button MISSING: {text}")
    return False

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--window-size=1200,800'])
        context = browser.new_context(storage_state=SESSION_PATH, viewport={'width': 1200, 'height': 800})
        page = context.new_page()

        print("\n🚀 Starting Robust Telegram E2E Test for Instagram Feature")
        print("1. Loading Telegram Web...")
        page.goto('https://web.telegram.org/k/#@fatemesbati_bot')
        
        # Wait for chat input to be ready
        try:
            page.wait_for_selector('div.input-message-input:not(.input-field-input-fake)', timeout=15000)
            print("   ✅ Chat loaded")
        except Exception as e:
            print("   ❌ Failed to load chat. Taking screenshot...")
            page.screenshot(path="test_error_chat_load.png")
            return
            
        print("2. Sending /start command...")
        input_el = page.locator('div.input-message-input:not(.input-field-input-fake)')
        input_el.click(force=True)
        input_el.fill('/start')
        input_el.press('Enter')
        time.sleep(3)
        
        # English language standardizes text
        print("3. Ensuring Language is English")
        click_btn(page, 'English')
        time.sleep(2)
        
        print("4. Accessing Menu")
        if not click_btn(page, 'Browse Campaigns'):
            input_el.fill('/start')
            input_el.press('Enter')
            time.sleep(3)
            click_btn(page, 'Browse Campaigns')
            
        time.sleep(3)
        
        print("5. Selecting first campaign")
        # Click the last keyboard button that isn't a nav button
        try:
            buttons = page.locator('.reply-markup button').all()
            for b in buttons:
                txt = b.text_content() or ""
                if "Back" not in txt and "Menu" not in txt and "Browse" not in txt:
                    b.click(force=True)
                    print(f"   ✅ Clicked campaign: {txt}")
                    break
        except Exception as e:
            print("   ❌ Error clicking campaign", e)
            
        time.sleep(3)
        
        print("6. Going to Tasks")
        if not click_btn(page, 'View Tasks'):
            click_btn(page, 'Join This Campaign')
            time.sleep(2)
            click_btn(page, 'View Tasks')
            
        time.sleep(3)
        
        print("7. Selecting a specific task")
        try:
            buttons = page.locator('.reply-markup button').all()
            clicked = False
            for b in buttons:
                txt = b.text_content() or ""
                if "Back" not in txt and "Menu" not in txt and "Invite" not in txt:
                    b.click(force=True)
                    print(f"   ✅ Clicked task: {txt}")
                    clicked = True
                    break
        except Exception:
            pass
            
        time.sleep(3)
        
        print("8. Starting the task")
        if not click_btn(page, 'Start This Task'):
            click_btn(page, "Let's Go!")
            
        time.sleep(3)
        
        print("9. Selecting Instagram platform")
        click_btn(page, 'Instagram')
        time.sleep(3)
        
        print("\n🔍 VERIFICATION RESULTS:")
        success_1 = verify_btn(page, 'Support Posts and Activists')
        success_2 = verify_btn(page, "Share a Child’s Story")
        
        # Also check fallback text if translation is different
        if not success_2:
            success_2 = verify_btn(page, "Share a Child")
            
        page.screenshot(path="test_final_result.png")
        print(f"📸 Final screenshot saved as test_final_result.png")
        
        if success_1 and success_2:
            print("\n🎉 TEST PASSED! Both new Instagram buttons are present and working.")
        else:
            print("\n🚨 TEST FAILED! Buttons missing.")
        
        browser.close()

if __name__ == "__main__":
    run_test()

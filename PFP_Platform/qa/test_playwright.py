import sys
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Navigating to https://peopleforpeace.live/dashboard")
        response = page.goto('https://peopleforpeace.live/dashboard')
        print(f"Status: {response.status}")
        page.wait_for_load_state('networkidle')
        page.screenshot(path='/tmp/pfp_home.png')
        print("Screenshot saved to /tmp/pfp_home.png")
        print("Title:", page.title())
        browser.close()

if __name__ == "__main__":
    main()

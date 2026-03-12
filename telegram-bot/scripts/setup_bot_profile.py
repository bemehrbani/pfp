#!/usr/bin/env python3
"""
One-time script to set up the PFP bot profile on Telegram.

Sets:
  - Bot profile photo (avatar)
  - Bot description (en/fa/ar)
  - Bot short description (en/fa/ar)

Usage:
  BOT_TOKEN=<token> python setup_bot_profile.py
"""

import asyncio
import os
import sys
from pathlib import Path


async def main():
    token = os.environ.get('BOT_TOKEN')
    if not token:
        print("Error: BOT_TOKEN environment variable is required")
        sys.exit(1)

    # Import here to avoid early import issues
    from telegram import Bot

    bot = Bot(token=token)

    # Add parent to path for brand_constants
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from utils.brand_constants import BOT_DESCRIPTIONS, BOT_SHORT_DESCRIPTIONS

    # ── Set Bot Profile Photo ─────────────────────────────────
    avatar_path = Path(__file__).parent.parent / 'assets' / 'bot_avatar.png'
    if avatar_path.exists():
        print(f"Setting bot profile photo from {avatar_path}...")
        with open(avatar_path, 'rb') as photo:
            await bot.set_chat_photo(
                chat_id=(await bot.get_me()).id,
                photo=photo
            )
        print("  ✅ Profile photo set!")
    else:
        print(f"  ⚠️ Avatar not found at {avatar_path}, skipping profile photo")

    # ── Set Bot Description (per language) ────────────────────
    for lang_code, description in BOT_DESCRIPTIONS.items():
        print(f"Setting description ({lang_code})...")
        await bot.set_my_description(
            description=description,
            language_code=lang_code if lang_code != 'en' else None
        )
        print(f"  ✅ Description ({lang_code}) set!")

    # ── Set Bot Short Description (per language) ──────────────
    for lang_code, short_desc in BOT_SHORT_DESCRIPTIONS.items():
        print(f"Setting short description ({lang_code})...")
        await bot.set_my_short_description(
            short_description=short_desc,
            language_code=lang_code if lang_code != 'en' else None
        )
        print(f"  ✅ Short description ({lang_code}) set!")

    print("\n🕊️ Bot profile setup complete!")


if __name__ == '__main__':
    asyncio.run(main())

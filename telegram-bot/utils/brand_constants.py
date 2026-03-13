"""
Brand constants for PFP Telegram Bot.
Central source of truth for all branding across bot, channel, and group.
"""

# ── Identity ──────────────────────────────────────────────────
BRAND_NAME = "People for Peace"
BRAND_EMOJI = "🕊️"
BRAND_TAGLINE = "Together for Justice, Together for Peace"
BOT_USERNAME = "peopleforpeacebot"
CHANNEL_USERNAME = "people4peace"
BRAND_URL = "https://peopleforpeace.live"

# ── Message Templates ─────────────────────────────────────────
BRAND_FOOTER = f"🕊️ {BRAND_NAME} · {BRAND_URL}"
BRAND_FOOTER_HTML = f'🕊️ <b>{BRAND_NAME}</b> · <a href="{BRAND_URL}">peopleforpeace.live</a>'
BRAND_SEPARATOR = "━━━━━━━━━━━━━━━━━━━"
BRAND_HEADER_HTML = f'🕊️ <b>{BRAND_NAME}</b>'
BRAND_CTA_HTML = f'✊ Join: @{BOT_USERNAME}'

# ── Visual Identity (for generated images) ────────────────────
COLOR_NAVY = "#1a2332"
COLOR_GOLD = "#d4a853"
COLOR_WHITE = "#f5f5f5"

# ── Bot Profile Descriptions ─────────────────────────────────
BOT_DESCRIPTIONS = {
    "en": (
        "People for Peace — Campaign Manager\n\n"
        "Join peace-building campaigns, complete tasks, "
        "and amplify voices for justice.\n\n"
        "🕊️ Together for Justice, Together for Peace"
    ),
    "fa": (
        "مردم برای صلح — مدیریت کمپین\n\n"
        "به کمپین‌های صلح‌سازی بپیوندید، وظایف را انجام دهید "
        "و صدای عدالت را تقویت کنید.\n\n"
        "🕊️ با هم برای عدالت، با هم برای صلح"
    ),
    "ar": (
        "الناس من أجل السلام — مدير الحملات\n\n"
        "انضم إلى حملات بناء السلام، أكمل المهام، "
        "وضخّم الأصوات من أجل العدالة.\n\n"
        "🕊️ معاً من أجل العدالة، معاً من أجل السلام"
    ),
}

BOT_SHORT_DESCRIPTIONS = {
    "en": "Join peace campaigns & complete tasks for justice 🕊️",
    "fa": "به کمپین‌های صلح بپیوندید و وظایف را انجام دهید 🕊️",
    "ar": "انضم لحملات السلام وأكمل المهام من أجل العدالة 🕊️",
}

# ── Channel / Group Descriptions ──────────────────────────────
CHANNEL_DESCRIPTION = (
    "People for Peace — Official Updates\n\n"
    "Real-time campaign progress, volunteer milestones, "
    "and daily digests from the movement.\n\n"
    "🤖 Join via bot: @peopleforpeacebot\n"
    "🌐 Website: peopleforpeace.live"
)

GROUP_DESCRIPTION = (
    "P4P Internal — Volunteer Coordination\n\n"
    "Private group for active PFP volunteers who have "
    "completed at least one campaign task.\n\n"
    "📢 Channel: @people4peace\n"
    "🤖 Bot: @peopleforpeacebot"
)

"""
Brand constants for PFP Telegram Bot.
Central source of truth for all branding across bot, channel, and group.
"""

# ── Identity ──────────────────────────────────────────────────
BRAND_NAME = "People for Peace & Justice ry"
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
COLOR_NAVY = "#0b1220"
COLOR_GOLD = "#e5b95f"
COLOR_WHITE = "#f5f3ef"

# ── Bot Profile Descriptions ─────────────────────────────────
BOT_DESCRIPTIONS = {
    "en": (
        "People for Peace & Justice ry (PFPJ ry) — Campaign Manager\n\n"
        "Join peace-building and legal accountability campaigns, complete tasks, "
        "and amplify voices for justice.\n\n"
        "🕊️ Together for Justice, Together for Peace"
    ),
    "fa": (
        "انجمن مردم برای صلح و عدالت (PFPJ ry) — مدیریت کمپین\n\n"
        "به کمپین‌های صلح‌سازی و دادخواهی حقوقی بپیوندید، وظایف را انجام دهید "
        "و صدای عدالت را تقویت کنید.\n\n"
        "🕊️ با هم برای عدالت، با هم برای صلح"
    ),
    "ar": (
        "منظمة الناس من أجل السلام والعدالة (PFPJ ry) — مدير الحملات\n\n"
        "انضم إلى حملات بناء السلام والمساءلة القانونية، أكمل المهام، "
        "وضخّم الأصوات من أجل العدالة.\n\n"
        "🕊️ معاً من أجل العدالة، معاً من أجل السلام"
    ),
}

BOT_SHORT_DESCRIPTIONS = {
    "en": "People for Peace & Justice ry — Peace & accountability campaigns 🕊️",
    "fa": "انجمن مردم برای صلح و عدالت (PFPJ ry) — کمپین‌های صلح و دادخواهی 🕊️",
    "ar": "الناس من أجل السلام والعدالة (PFPJ ry) — حملات السلام والعدالة 🕊️",
}

# ── Channel / Group Descriptions ──────────────────────────────
CHANNEL_DESCRIPTION = (
    "People for Peace & Justice ry (PFPJ ry) — Official Updates\n\n"
    "Real-time campaign progress, forensic documentation updates, "
    "and daily digests from Helsinki (PRH ID: 3616815-5).\n\n"
    "🤖 Join via bot: @peopleforpeacebot\n"
    "🌐 Website: peopleforpeace.live"
)

GROUP_DESCRIPTION = (
    "PFPJ Internal — Volunteer Coordination\n\n"
    "Private group for active PFPJ ry volunteers who have "
    "completed at least one campaign task.\n\n"
    "📢 Channel: @people4peace\n"
    "🤖 Bot: @peopleforpeacebot"
)

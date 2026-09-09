"""
Actions & Events handlers for PFP Telegram Bot.
Handles Helsinki Memorial Screening RSVPs, petitions, and About PFPJ ry overview.
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.translations import t, get_back_to_menu_inline
from utils.state_management import state_manager
from services.events_service import EventsService

logger = logging.getLogger(__name__)


async def events_menu_handler(update: Update, context: CallbackContext):
    """Show the Actions & Events main menu."""
    query = update.callback_query
    if query:
        await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'
    rsvps = EventsService.get_rsvp_count()

    text = (
        f"{t('events_title', lang)}\n\n"
        f"🏛️ *Upcoming Flagship Event:* Helsinki Memorial Screening & Visual Exhibition\n"
        f"👥 *Confirmed Community RSVPs:* {rsvps}\n\n"
        f"Select an option to participate:"
    )

    keyboard = [
        [
            InlineKeyboardButton(t('event_helsinki_btn', lang), callback_data='event_helsinki_detail'),
        ],
        [
            InlineKeyboardButton("🗳️ View Community Proposal on GitHub ↗", url="https://github.com/bemehrbani/pfp/issues/55"),
        ],
        [
            InlineKeyboardButton("🤝 Global Initiatives Directory ↗", url="https://peopleforpeace.live/initiatives.html"),
        ],
        [
            InlineKeyboardButton(t('btn_back_to_menu', lang), callback_data='menu_main'),
        ]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    if query and query.message:
        await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
    elif update.message:
        await update.message.reply_text(text=text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)


async def event_detail_handler(update: Update, context: CallbackContext):
    """Show Helsinki Event detailed program and RSVP button."""
    query = update.callback_query
    await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'
    evt = EventsService.get_helsinki_event_details()

    title = evt.get(f'title_{lang}', evt['title_en'])

    text = (
        f"🎟️ *{title}*\n\n"
        f"📍 *Location:* Helsinki, Finland\n"
        f"🏢 *Candidate Venues:* Oodi Central Library (Maijansali/Kino Regina) / Cinema Orion\n"
        f"📅 *Schedule:* {evt['date']}\n\n"
        f"🌟 *Program Highlights:*\n"
        f"• 100 Faces of Peace Visual Memorial Exhibition\n"
        f"• Documentary Screening with Finnish Subtitles (France 24, Sky News, Minab Field Tales)\n"
        f"• Expert Panel on Universal Jurisdiction & IHL Protections\n"
        f"• 156 Memorial Candles Lighting Ceremony (Honoring each certified martyr)\n"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Click here to Confirm My RSVP (Free)", callback_data='event_do_rsvp'),
        ],
        [
            InlineKeyboardButton("📋 Discuss on GitHub Issue #55 ↗", url=evt['github_issue_url']),
        ],
        [
            InlineKeyboardButton("⬅️ Back to Events", callback_data='menu_events'),
            InlineKeyboardButton("🏠 Main Menu", callback_data='menu_main'),
        ]
    ]

    await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)


async def event_do_rsvp_handler(update: Update, context: CallbackContext):
    """Confirm user RSVP for the Helsinki event."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    EventsService.add_rsvp(
        user_id=user.id,
        username=user.username or "",
        name=user.full_name or user.first_name
    )

    msg = t('event_rsvp_confirmed', lang)

    keyboard = [
        [InlineKeyboardButton("🕊️ Explore Digital Memorial", callback_data='menu_memorial')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='menu_main')]
    ]

    await query.edit_message_text(text=msg, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def about_pfp_handler(update: Update, context: CallbackContext):
    """Show official PFPJ ry NGO information and legal registration."""
    query = update.callback_query
    if query:
        await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    text = t('about_pfp_text', lang)

    keyboard = [
        [
            InlineKeyboardButton("🌐 Official Website ↗", url="https://peopleforpeace.live"),
            InlineKeyboardButton("⚖️ Legal Documents Portal ↗", url="https://peopleforpeace.live/legal/jfmc-2026/index.html"),
        ],
        [
            InlineKeyboardButton(t('btn_back_to_menu', lang), callback_data='menu_main')
        ]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    if query and query.message:
        await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
    elif update.message:
        await update.message.reply_text(text=text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)

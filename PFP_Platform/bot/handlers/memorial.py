"""
Memorial handlers for PFP Telegram Bot.
Handles victim browsing, search, tributes, and virtual candle lighting.
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.translations import t, get_back_to_menu_inline
from utils.state_management import state_manager
from services.memorial_service import MemorialService

logger = logging.getLogger(__name__)


async def memorial_menu_handler(update: Update, context: CallbackContext):
    """Show the Memorial main menu."""
    query = update.callback_query
    if query:
        await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'
    candles = MemorialService.get_candle_count()

    text = (
        f"{t('memorial_title', lang)}\n\n"
        f"🕯️ *Tributes Lit:* {candles:,}\n"
        f"📍 *Location:* Shajareh Tayyebeh Primary School, Minab\n"
        f"🕊️ *Casualties:* 156 certified martyrs (120 students, 26 teachers & staff) | 95+ injured"
    )

    keyboard = [
        [
            InlineKeyboardButton(t('memorial_candle_btn', lang), callback_data='memorial_candle'),
        ],
        [
            InlineKeyboardButton(t('memorial_browse_btn', lang), callback_data='memorial_page_1'),
            InlineKeyboardButton(t('memorial_search_btn', lang), callback_data='memorial_search'),
        ],
        [
            InlineKeyboardButton("🌐 Digital Memorial Online ↗", url="https://peopleforpeace.live/memorial.html"),
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


async def memorial_candle_handler(update: Update, context: CallbackContext):
    """Handle lighting a memorial candle."""
    query = update.callback_query
    await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    count = MemorialService.light_candle()
    success_msg = t('memorial_candle_lit_success', lang).format(count=f"{count:,}")

    keyboard = [
        [InlineKeyboardButton("🕊️ Browse Memorial Records", callback_data='memorial_page_1')],
        [InlineKeyboardButton(t('btn_back_to_menu', lang), callback_data='menu_main')]
    ]
    await query.edit_message_text(text=success_msg, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def memorial_pagination_handler(update: Update, context: CallbackContext):
    """Handle browsing victim records with pagination."""
    query = update.callback_query
    await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    # Extract page number
    try:
        page = int(query.data.replace('memorial_page_', ''))
    except ValueError:
        page = 1

    data = MemorialService.get_victims_page(page=page, page_size=6)
    items = data["items"]
    page = data["page"]
    total_pages = data["total_pages"]

    text = (
        f"🕊️ *Minab Children Memorial Archive* (Page {page}/{total_pages})\n"
        f"Select a child's name to view their profile and memory:"
    )

    keyboard = []
    for victim in items:
        name = victim.get('nameFa' if lang == 'fa' else 'name', 'Unknown')
        age_str = f" ({victim['age']} yrs)" if victim.get('age') else ""
        keyboard.append([
            InlineKeyboardButton(f"🌸 {name}{age_str}", callback_data=f"victim_{victim['id']}")
        ])

    # Nav buttons
    nav_row = []
    if data["has_prev"]:
        nav_row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"memorial_page_{page - 1}"))
    nav_row.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="noop"))
    if data["has_next"]:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"memorial_page_{page + 1}"))

    keyboard.append(nav_row)
    keyboard.append([
        InlineKeyboardButton("🕯️ Light a Candle", callback_data="memorial_candle"),
        InlineKeyboardButton("⬅️ Memorial Menu", callback_data="menu_memorial")
    ])

    await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def victim_detail_handler(update: Update, context: CallbackContext):
    """Display individual victim detail card."""
    query = update.callback_query
    await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    victim_id = query.data.replace('victim_', '')
    v = MemorialService.get_victim_by_id(victim_id)

    if not v:
        await query.edit_message_text("Victim record not found.", reply_markup=get_back_to_menu_inline(lang))
        return

    name = v.get('nameFa' if lang == 'fa' else 'name', 'Unknown')
    age = f"{v['age']} years old" if v.get('age') else "Primary school student"
    father = v.get('father') or "Not recorded"
    mother = v.get('motherNameFa' if lang == 'fa' else 'motherName') or "Not recorded"
    notes = v.get('notes') or "Elementary school student at Shajareh Tayyebeh Primary School, Minab."

    text = (
        f"🌸 *In Memoriam: {name}*\n\n"
        f"🎂 *Age / Status:* {age}\n"
        f"👨‍👩‍👧 *Family:* Father: {father} | Mother: {mother}\n"
        f"📝 *Biographical Notes:* {notes}\n\n"
        f"🕯️ *Rest in peace and dignity.*"
    )

    share_url = f"https://peopleforpeace.live/memorial.html?id={victim_id}"

    keyboard = [
        [
            InlineKeyboardButton("🕯️ Light Candle for Her", callback_data="memorial_candle"),
            InlineKeyboardButton("🌐 Memorial Profile ↗", url=share_url)
        ],
        [
            InlineKeyboardButton("⬅️ Back to List", callback_data="memorial_page_1"),
            InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")
        ]
    ]

    await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

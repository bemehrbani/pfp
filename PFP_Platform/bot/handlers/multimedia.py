"""
Multimedia handlers for PFP Telegram Bot.
Handles browsing investigative video reports, documentaries, and audio tributes.
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.translations import t, get_back_to_menu_inline
from utils.state_management import state_manager
from services.multimedia_service import MultimediaService

logger = logging.getLogger(__name__)


async def multimedia_menu_handler(update: Update, context: CallbackContext):
    """Show the Multimedia main menu."""
    query = update.callback_query
    if query:
        await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    text = (
        f"{t('multimedia_title', lang)}\n\n"
        f"Select a category below to stream investigative reports and field documentaries:"
    )

    categories = MultimediaService.get_categories()
    keyboard = []
    for cat in categories:
        label = cat.get(f'label_{lang}', cat['label_en'])
        keyboard.append([
            InlineKeyboardButton(label, callback_data=f"media_cat_{cat['id']}")
        ])

    keyboard.append([
        InlineKeyboardButton("🌐 Open Web Multimedia Portal ↗", url="https://peopleforpeace.live/multimedia.html")
    ])
    keyboard.append([
        InlineKeyboardButton(t('btn_back_to_menu', lang), callback_data='menu_main')
    ])

    markup = InlineKeyboardMarkup(keyboard)

    if query and query.message:
        await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
    elif update.message:
        await update.message.reply_text(text=text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)


async def multimedia_category_handler(update: Update, context: CallbackContext):
    """Show media items under a specific category."""
    query = update.callback_query
    await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    cat_id = query.data.replace('media_cat_', '')
    items = MultimediaService.get_by_category(cat_id)

    cat_labels = {
        'international': '🌐 International Investigations',
        'farsi_doc': '🎥 Field Reports & Series',
        'music_score': '🎵 Tributes & Audio'
    }

    text = f"🎬 *{cat_labels.get(cat_id, 'Documentaries')}* ({len(items)} items)\n\nSelect a report to inspect details and stream:"

    keyboard = []
    for m in items[:8]:  # Top items
        title = m.get('title', {}).get(lang if lang in ('fa', 'en') else 'en', m.get('id', 'Video'))
        dur = m.get('runtime', '')
        dur_str = f" [{dur}]" if dur else ""
        keyboard.append([
            InlineKeyboardButton(f"▶️ {title[:32]}{dur_str}", callback_data=f"media_item_{m['slug']}")
        ])

    keyboard.append([
        InlineKeyboardButton("⬅️ Back to Categories", callback_data="menu_multimedia"),
        InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")
    ])

    await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def media_detail_handler(update: Update, context: CallbackContext):
    """Display detailed media report card."""
    query = update.callback_query
    await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    slug = query.data.replace('media_item_', '')
    item = MultimediaService.get_media_by_slug(slug)

    if not item:
        await query.edit_message_text("Media asset not found.", reply_markup=get_back_to_menu_inline(lang))
        return

    title = item.get('title', {}).get(lang if lang in ('fa', 'en') else 'en', item.get('id'))
    desc = item.get('description', {}).get(lang if lang in ('fa', 'en') else 'en', '')
    producer = item.get('producer', 'PFPJ ry')
    runtime = item.get('runtime', '')
    res = item.get('resolution', '1080p HD')
    web_url = f"https://peopleforpeace.live/media-item.html?v={item['slug']}"

    text = (
        f"🎬 *{title}*\n\n"
        f"🏢 *Creator/Broadcaster:* {producer}\n"
        f"⏱️ *Runtime:* {runtime} | 🖥️ *Resolution:* {res}\n"
        f"🗣️ *Subtitles:* English, فارسی, Suomi [CC WebVTT]\n\n"
        f"📖 *Synopsis:*\n{desc}\n"
    )

    keyboard = [
        [
            InlineKeyboardButton(t('multimedia_watch_online', lang), url=web_url),
        ]
    ]

    if item.get('sourceUrl'):
        keyboard.append([
            InlineKeyboardButton("🔗 Original Broadcaster Source ↗", url=item['sourceUrl'])
        ])

    keyboard.append([
        InlineKeyboardButton("⬅️ Back to Media", callback_data="menu_multimedia"),
        InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")
    ])

    await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

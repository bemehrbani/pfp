"""
Evidence handlers for PFP Telegram Bot.
Provides interactive forensic evidence summaries, missile components, and IHL dossiers.
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.translations import t, get_back_to_menu_inline
from utils.state_management import state_manager
from services.evidence_service import EvidenceService

logger = logging.getLogger(__name__)


async def evidence_menu_handler(update: Update, context: CallbackContext):
    """Show the Evidence & Forensics main menu."""
    query = update.callback_query
    if query:
        await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    text = (
        f"{t('evidence_title', lang)}\n\n"
        f"Select an investigation chapter below to review verified open-source and physical evidence:"
    )

    chapters = EvidenceService.get_evidence_chapters()
    keyboard = []
    for ch in chapters:
        title = ch.get(f'title_{lang}', ch['title_en'])
        keyboard.append([
            InlineKeyboardButton(f"{ch['icon']} {title}", callback_data=f"ev_ch_{ch['id']}")
        ])

    keyboard.append([
        InlineKeyboardButton("🌐 Open Public Evidence Docket ↗", url="https://peopleforpeace.live/evidence.html")
    ])
    keyboard.append([
        InlineKeyboardButton(t('btn_back_to_menu', lang), callback_data='menu_main')
    ])

    markup = InlineKeyboardMarkup(keyboard)

    if query and query.message:
        await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
    elif update.message:
        await update.message.reply_text(text=text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)


async def evidence_chapter_handler(update: Update, context: CallbackContext):
    """Display individual evidence chapter."""
    query = update.callback_query
    await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = session.language or 'en'

    chapter_id = query.data.replace('ev_ch_', '')
    ch = EvidenceService.get_chapter_by_id(chapter_id)

    title = ch.get(f'title_{lang}', ch['title_en'])
    desc = ch.get(f'desc_{lang}', ch['desc_en'])

    text = (
        f"⚖️ *{title}*\n\n"
        f"📋 *Verified Finding:*\n{desc}\n\n"
        f"📁 *Archived under:* Universal Jurisdiction Evidence Docket (PFPJ ry, Helsinki)"
    )

    keyboard = [
        [
            InlineKeyboardButton("🌐 Full Technical Analysis on Web ↗", url=ch['doc_link'])
        ],
        [
            InlineKeyboardButton("⬅️ Back to Evidence Chapters", callback_data="menu_evidence"),
            InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")
        ]
    ]

    await query.edit_message_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

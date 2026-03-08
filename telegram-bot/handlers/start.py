"""
Start command handler for Telegram bot.
"""
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from asgiref.sync import sync_to_async
from .db import get_user_by_telegram_id
from utils.state_management import state_manager
from utils.translations import t, get_keyboard_buttons

logger = logging.getLogger(__name__)


@sync_to_async
def _db_get_session_language(session):
    """Get language from session (sync ORM access)."""
    session.refresh_from_db(fields=['language'])
    return session.language


@sync_to_async
def _db_set_session_language(session, language):
    """Set language on session (sync ORM access)."""
    session.language = language
    session.save(update_fields=['language', 'updated_at'])


async def start_command(update: Update, context: CallbackContext):
    """Handle /start command."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Start command from user {user.id} (@{user.username})")

    # Get or create session
    session, created = await state_manager.get_or_create_session(update, context)

    if created:
        # New user — show language picker first
        await _show_language_picker(update, context)
    else:
        # Existing user — use their language preference
        lang = await _db_get_session_language(session)
        await _send_welcome(update, context, session, lang)


async def _show_language_picker(update: Update, context: CallbackContext, message_text: str = None):
    """Show language selection buttons."""
    text = message_text or "🌍 Choose your language / زبان خود را انتخاب کنید / اختر لغتك:"

    keyboard = [[
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
        InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
    )


async def language_command(update: Update, context: CallbackContext):
    """Handle /language command — show language picker."""
    await _show_language_picker(update, context)


async def language_callback_handler(update: Update, context: CallbackContext):
    """Handle language selection callback."""
    query = update.callback_query
    await query.answer()

    lang_code = query.data.split('_')[1]  # lang_en → en, lang_fa → fa, lang_ar → ar
    if lang_code not in ('en', 'fa', 'ar'):
        lang_code = 'en'

    # Save language preference
    session, _ = await state_manager.get_or_create_session(update, context)
    await _db_set_session_language(session, lang_code)

    # Confirm language choice
    await query.edit_message_text(t('language_set', lang_code), parse_mode='Markdown')

    # Send welcome with keyboard in chosen language
    await _send_welcome(update, context, session, lang_code)


async def _send_welcome(update: Update, context: CallbackContext, session, lang: str):
    """Send welcome message and keyboard in the user's language."""
    chat_id = update.effective_chat.id

    # Create keyboard in user's language
    keyboard = get_keyboard_buttons(lang)
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text=t('welcome', lang),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    # Check if user needs registration
    user = update.effective_user
    db_user = await get_user_by_telegram_id(user.id)
    if db_user:
        logger.info(f"Existing user {db_user.username} started bot (lang={lang})")
    else:
        # Start registration
        from apps.telegram.models import TelegramSession
        await state_manager.update_state(session, TelegramSession.State.AWAITING_EMAIL)

        await context.bot.send_message(
            chat_id=chat_id,
            text=t('register_new_user', lang)
        )
        logger.info(f"New user {user.id} started registration (lang={lang})")


async def help_command(update: Update, context: CallbackContext):
    """Handle /help command."""
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = await _db_get_session_language(session)

    await update.message.reply_text(
        t('help_text', lang),
        parse_mode='Markdown'
    )
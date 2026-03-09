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


@sync_to_async
def _db_store_deeplink(session, campaign_id):
    """Store deep-link campaign ID in session temp_data for post-registration auto-join."""
    session.temp_data = session.temp_data or {}
    session.temp_data['deeplink_campaign_id'] = campaign_id
    session.save(update_fields=['temp_data', 'updated_at'])


@sync_to_async
def _db_get_campaign_name(campaign_id):
    """Get campaign name by ID (for personalized registration prompt)."""
    from apps.campaigns.models import Campaign
    try:
        return Campaign.objects.get(id=campaign_id, status=Campaign.Status.ACTIVE).name
    except Campaign.DoesNotExist:
        return None


async def start_command(update: Update, context: CallbackContext):
    """Handle /start command with optional deep-link parameter."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Start command from user {user.id} (@{user.username})")

    # Parse deep-link parameter (e.g. campaign_16 → campaign_id=16)
    deeplink_campaign_id = None
    if context.args:
        arg = context.args[0]
        if arg.startswith('campaign_'):
            try:
                deeplink_campaign_id = int(arg.split('_', 1)[1])
                logger.info(f"Deep-link campaign ID: {deeplink_campaign_id}")
            except (ValueError, IndexError):
                logger.warning(f"Invalid deep-link arg: {arg}")

    # Get or create session
    session, created = await state_manager.get_or_create_session(update, context)

    # Store deep-link campaign ID in session for post-registration use
    if deeplink_campaign_id:
        await _db_store_deeplink(session, deeplink_campaign_id)

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
        # Existing user with deep-link → auto-join the campaign
        await _handle_deeplink_for_existing_user(context, session, db_user, lang, chat_id)
    else:
        # Start registration — skip email, go straight to name
        from apps.telegram.models import TelegramSession
        await state_manager.update_state(session, TelegramSession.State.AWAITING_NAME)

        # Personalized prompt if coming from deep-link
        deeplink_campaign_id = await _db_get_deeplink_campaign_id(session)
        if deeplink_campaign_id:
            campaign_name = await _db_get_campaign_name(deeplink_campaign_id)
            if campaign_name:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=t('register_for_campaign', lang).format(name=campaign_name),
                    parse_mode='Markdown'
                )
                logger.info(f"New user {user.id} registering for campaign {deeplink_campaign_id} (lang={lang})")
                return

        # Generic registration prompt (no deep-link)
        await context.bot.send_message(
            chat_id=chat_id,
            text=t('register_new_user', lang)
        )
        logger.info(f"New user {user.id} started registration (lang={lang})")


@sync_to_async
def _db_get_deeplink_campaign_id(session):
    """Read deep-link campaign ID from session temp_data."""
    session.refresh_from_db(fields=['temp_data'])
    return (session.temp_data or {}).get('deeplink_campaign_id')


async def _handle_deeplink_for_existing_user(context, session, db_user, lang, chat_id):
    """Auto-join campaign from deep-link for already-registered users."""
    deeplink_campaign_id = await _db_get_deeplink_campaign_id(session)
    if not deeplink_campaign_id:
        return

    from handlers.campaigns import (
        _get_campaign, _is_volunteer, _join_campaign,
        _get_task_count, handle_campaign_view_tasks
    )

    campaign = await _get_campaign(deeplink_campaign_id)
    if not campaign:
        return

    already_joined = await _is_volunteer(campaign, db_user)
    if already_joined:
        # Already a member — just show tasks
        await context.bot.send_message(
            chat_id=chat_id,
            text=t('campaign_joined_success', lang).format(name=campaign.name),
            parse_mode='Markdown'
        )
    else:
        # Join and show tasks
        member_count = await _join_campaign(campaign, db_user)
        task_count = await _get_task_count(campaign)
        await context.bot.send_message(
            chat_id=chat_id,
            text=t('auto_joined_campaign', lang).format(
                name=campaign.name,
                description=campaign.short_description,
                members=member_count,
                target=campaign.target_members,
                tasks=task_count,
            ),
            parse_mode='Markdown'
        )

    # Clear the deep-link from temp_data
    await _db_clear_deeplink(session)


@sync_to_async
def _db_clear_deeplink(session):
    """Remove deep-link data from session."""
    if session.temp_data and 'deeplink_campaign_id' in session.temp_data:
        del session.temp_data['deeplink_campaign_id']
        session.save(update_fields=['temp_data', 'updated_at'])


async def help_command(update: Update, context: CallbackContext):
    """Handle /help command."""
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = await _db_get_session_language(session)

    await update.message.reply_text(
        t('help_text', lang),
        parse_mode='Markdown'
    )
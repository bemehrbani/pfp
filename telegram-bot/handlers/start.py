"""
Start command handler for Telegram bot.
"""
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from asgiref.sync import sync_to_async
from .db import get_user_by_telegram_id
from utils.state_management import state_manager
from utils.translations import t, get_keyboard_buttons, get_main_menu_inline

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
def _db_store_deeplink(session, campaign_id, referrer_id=None):
    """Store deep-link campaign ID and optional referrer in session temp_data."""
    session.temp_data = session.temp_data or {}
    session.temp_data['deeplink_campaign_id'] = campaign_id
    if referrer_id:
        session.temp_data['deeplink_referrer_id'] = referrer_id
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

    # Parse deep-link parameter (e.g. campaign_16 or campaign_16_ref_42)
    deeplink_campaign_id = None
    deeplink_referrer_id = None
    if context.args:
        arg = context.args[0]
        if arg.startswith('campaign_'):
            try:
                # Handle campaign_16_ref_42 format
                if '_ref_' in arg:
                    parts = arg.split('_ref_')
                    deeplink_campaign_id = int(parts[0].split('_', 1)[1])
                    deeplink_referrer_id = int(parts[1])
                    logger.info(f"Deep-link campaign={deeplink_campaign_id} referrer={deeplink_referrer_id}")
                else:
                    deeplink_campaign_id = int(arg.split('_', 1)[1])
                    logger.info(f"Deep-link campaign ID: {deeplink_campaign_id}")
            except (ValueError, IndexError):
                logger.warning(f"Invalid deep-link arg: {arg}")

    # Get or create session
    session, created = await state_manager.get_or_create_session(update, context)

    # Store deep-link campaign ID + referrer in session for post-registration use
    if deeplink_campaign_id:
        await _db_store_deeplink(session, deeplink_campaign_id, deeplink_referrer_id)

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
    """Send welcome message with inline menu buttons."""
    chat_id = update.effective_chat.id

    # Remove any old persistent keyboard, then send inline menu
    await context.bot.send_message(
        chat_id=chat_id,
        text=t('welcome', lang),
        reply_markup=get_main_menu_inline(lang),
        parse_mode='Markdown'
    )

    # Check if user needs registration
    user = update.effective_user
    db_user = await get_user_by_telegram_id(user.id)
    if db_user:
        logger.info(f"Existing user {db_user.username} started bot (lang={lang})")
        # Existing user with deep-link → auto-join the campaign
        await _handle_deeplink_for_existing_user(context, session, db_user, lang, chat_id)
        # Show joined campaigns task-first (skip if deep-link already handled it)
        deeplink_campaign_id = await _db_get_deeplink_campaign_id(session)
        if not deeplink_campaign_id:
            from handlers.campaigns import show_my_campaigns
            # Create a lightweight query-like object for show_my_campaigns
            await _show_campaigns_after_welcome(context, session, chat_id, lang)
    else:
        # Start registration — immediately create the user!
        logger.info(f"New user {user.id} auto-registering (lang={lang})")
        
        # Personalized prompt if coming from deep-link just to mention the campaign
        deeplink_campaign_id = await _db_get_deeplink_campaign_id(session)
        if deeplink_campaign_id:
            campaign_name = await _db_get_campaign_name(deeplink_campaign_id)
            if campaign_name:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=t('register_for_campaign', lang).format(name=campaign_name),
                    parse_mode='Markdown'
                )
        
        # Complete automatic registration
        await state_manager.register_user_automatically(update, context, session, lang)


async def _show_campaigns_after_welcome(context, session, chat_id, lang):
    """Show joined campaigns as a follow-up message after welcome.

    This is a lightweight wrapper that uses show_my_campaigns logic
    but sends via context.bot.send_message (not inline edit).
    """
    from asgiref.sync import sync_to_async
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    if not session.user:
        return

    @sync_to_async
    def _get_joined(user):
        from apps.campaigns.models import CampaignVolunteer
        cvs = (
            CampaignVolunteer.objects
            .filter(volunteer=user, status='active')
            .select_related('campaign')
            .order_by('-joined_at')
        )
        return [
            (cv.campaign.id, cv.campaign.name, cv.campaign.tasks.filter(is_active=True).count())
            for cv in cvs
        ]

    joined = await _get_joined(session.user)

    if len(joined) == 0:
        # No campaigns — nothing to show, menu is enough
        return

    if len(joined) == 1:
        # Single campaign — show task checklist
        campaign_id, campaign_name, _ = joined[0]
        from handlers.campaigns import _get_campaign
        campaign = await _get_campaign(campaign_id)
        if not campaign:
            return

        # We need to create a pseudo-query for handle_campaign_view_tasks
        # Instead, just send a redirect message
        from handlers.campaigns import handle_campaign_view_tasks
        from handlers.tasks import _db_get_user_task_status_map

        @sync_to_async
        def _get_tasks(cid):
            from apps.tasks.models import Task
            return list(Task.objects.filter(
                campaign_id=cid, is_active=True,
                task_type__in=[
                    'twitter_post', 'twitter_retweet', 'twitter_comment',
                    'petition', 'mass_email',
                ]
            ).order_by('-points')[:10])

        tasks = await _get_tasks(campaign_id)
        if not tasks:
            return

        status_map = await _db_get_user_task_status_map(session.user, campaign_id)

        type_icons = {
            'twitter_post': '🐦', 'twitter_retweet': '🔁', 'twitter_comment': '💬',
            'twitter_like': '❤️', 'telegram_share': '📢', 'telegram_invite': '👥',
            'content_creation': '✍️', 'research': '🔍', 'other': '📌',
            'petition': '✍️', 'mass_email': '📧',
        }

        message = t('checklist_title', lang).format(name=campaign_name) + "\n\n"
        keyboard = []

        for task in tasks:
            icon = type_icons.get(task.task_type, '📌')
            user_status = status_map.get(task.id)

            if user_status in ('completed', 'verified'):
                check = '✅'
                label = f"✅ {task.title[:28]}"
            elif user_status in ('assigned', 'in_progress'):
                check = '🚧'
                label = f"🚧 {task.title[:28]}"
            else:
                check = '⬜'
                label = f"{icon} {task.title[:28]}"

            message += f"{check} {icon} {task.title}  (+{task.points} {t('task_pts', lang)})\n"
            keyboard.append([
                InlineKeyboardButton(label, callback_data=f"task_claim_{task.id}")
            ])

        message += "\n" + t('checklist_tap_start', lang)

        keyboard.append([
            InlineKeyboardButton(
                t('btn_invite_friends', lang),
                callback_data=f"campaign_invite_{campaign_id}"
            )
        ])
        keyboard.append([
            InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")
        ])

        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        return

    # 2+ campaigns — show picker
    text = t('my_campaigns_title', lang) + "\n\n"
    keyboard = []

    for campaign_id, campaign_name, task_count in joined:
        text += f"✊ *{campaign_name}*  —  {task_count} {t('campaigns_tasks_label', lang)}\n"
        keyboard.append([
            InlineKeyboardButton(
                f"✊ {campaign_name}",
                callback_data=f"campaign_tasks_{campaign_id}"
            )
        ])

    text += "\n" + t('my_campaigns_tap', lang)
    keyboard.append([
        InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")
    ])

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


@sync_to_async
def _db_get_deeplink_campaign_id(session):
    """Read deep-link campaign ID from session temp_data."""
    session.refresh_from_db(fields=['temp_data'])
    return (session.temp_data or {}).get('deeplink_campaign_id')


@sync_to_async
def _db_get_deeplink_referrer_id(session):
    """Read referrer user ID from session temp_data."""
    session.refresh_from_db(fields=['temp_data'])
    return (session.temp_data or {}).get('deeplink_referrer_id')


async def _handle_deeplink_for_existing_user(context, session, db_user, lang, chat_id):
    """Auto-join campaign from deep-link for already-registered users."""
    deeplink_campaign_id = await _db_get_deeplink_campaign_id(session)
    if not deeplink_campaign_id:
        return

    referrer_id = await _db_get_deeplink_referrer_id(session)

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
        # Join and show tasks — pass referrer for credit
        member_count = await _join_campaign(campaign, db_user, referrer_id=referrer_id)
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

        # Notify inviter
        if referrer_id:
            await _notify_referrer(context, referrer_id, db_user, campaign, lang)

    # Clear the deep-link from temp_data
    await _db_clear_deeplink(session)


@sync_to_async
def _db_clear_deeplink(session):
    """Remove deep-link data from session."""
    if session.temp_data:
        session.temp_data.pop('deeplink_campaign_id', None)
        session.temp_data.pop('deeplink_referrer_id', None)
        session.save(update_fields=['temp_data', 'updated_at'])


async def _notify_referrer(context, referrer_id, new_user, campaign, lang):
    """Send notification to the referrer that someone joined via their link."""
    from apps.telegram.models import TelegramSession

    @sync_to_async
    def _get_referrer_chat_id(rid):
        try:
            return TelegramSession.objects.get(user_id=rid).telegram_chat_id
        except TelegramSession.DoesNotExist:
            return None

    chat_id = await _get_referrer_chat_id(referrer_id)
    if chat_id:
        name = new_user.first_name or new_user.username or 'Someone'
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=t('referral_credited', lang).format(
                    name=name, campaign=campaign.name
                ),
                parse_mode='Markdown'
            )
        except Exception:
            logger.warning(f"Could not notify referrer {referrer_id}")


async def help_command(update: Update, context: CallbackContext):
    """Handle /help command."""
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = await _db_get_session_language(session)

    await update.message.reply_text(
        t('help_text', lang),
        parse_mode='Markdown'
    )
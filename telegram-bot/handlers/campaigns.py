"""
Campaign command handlers for Telegram bot.
"""
import logging
from typing import List, Tuple
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from asgiref.sync import sync_to_async
from utils.translations import t

logger = logging.getLogger(__name__)


@sync_to_async
def _get_or_create_session(telegram_id, telegram_username, chat_id):
    """Get or create TelegramSession (sync, wrapped for async)."""
    from django.contrib.auth import get_user_model
    from apps.telegram.models import TelegramSession
    User = get_user_model()

    try:
        session = TelegramSession.objects.select_related('user').get(telegram_id=telegram_id)
        session.telegram_username = telegram_username
        session.telegram_chat_id = chat_id
        update_fields = ['telegram_username', 'telegram_chat_id', 'updated_at']

        # Auto-repair: link orphaned session to existing user
        if not session.user:
            try:
                db_user = User.objects.get(telegram_id=telegram_id)
                session.user = db_user
                update_fields.append('user')
            except User.DoesNotExist:
                pass

        session.save(update_fields=update_fields)
        return session, False
    except TelegramSession.DoesNotExist:
        db_user = None
        try:
            db_user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            pass

        session = TelegramSession.objects.create(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            telegram_chat_id=chat_id,
            user=db_user
        )
        return session, True


@sync_to_async
def _get_active_campaigns(exclude_user=None):
    """Get active campaigns, optionally excluding those the user joined."""
    from apps.campaigns.models import Campaign
    qs = Campaign.objects.filter(status=Campaign.Status.ACTIVE)
    if exclude_user:
        qs = qs.exclude(volunteers=exclude_user)
    return list(qs.order_by('-created_at')[:10])


@sync_to_async
def _get_joined_campaign_ids(user):
    """Get the set of campaign IDs that a user has joined."""
    from apps.campaigns.models import CampaignVolunteer
    return set(
        CampaignVolunteer.objects.filter(
            volunteer=user, status='active'
        ).values_list('campaign_id', flat=True)
    )

@sync_to_async
def _get_campaign(campaign_id):
    """Get a campaign by ID."""
    from apps.campaigns.models import Campaign
    try:
        return Campaign.objects.get(id=campaign_id, status=Campaign.Status.ACTIVE)
    except Campaign.DoesNotExist:
        return None


@sync_to_async
def _is_volunteer(campaign, user):
    """Check if user is a volunteer for campaign."""
    from apps.campaigns.models import CampaignVolunteer
    return CampaignVolunteer.objects.filter(campaign=campaign, volunteer=user).exists()


@sync_to_async
def _join_campaign(campaign, user):
    """Join a campaign."""
    from apps.campaigns.models import CampaignVolunteer
    CampaignVolunteer.objects.create(
        campaign=campaign,
        volunteer=user,
        status='active'
    )
    campaign.current_members = campaign.volunteers.count()
    campaign.save(update_fields=['current_members'])
    return campaign.current_members


@sync_to_async
def _get_task_count(campaign):
    """Get task count for a campaign."""
    return campaign.tasks.count()


@sync_to_async
def _record_command(session, command):
    """Record a command."""
    session.record_command(command)


async def campaigns_command(update: Update, context: CallbackContext):
    """Handle /campaigns command - list available campaigns with pagination."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Campaigns command from user {user.id} (@{user.username})")

    session, created = await _get_or_create_session(user.id, user.username, chat_id)
    await _record_command(session, 'campaigns')

    # Get language
    lang = getattr(session, 'language', 'en') or 'en'

    if not session.user:
        await update.message.reply_text(
            t('register_need_first', lang),
            parse_mode='Markdown'
        )
        return

    # Show ALL active campaigns, not just unjoined ones
    campaigns = await _get_active_campaigns()

    if not campaigns:
        await update.message.reply_text(
            t('campaigns_none', lang),
            parse_mode='Markdown'
        )
        return

    # Check which campaigns user already joined
    joined_ids = await _get_joined_campaign_ids(session.user)

    message = t('campaigns_title', lang) + "\n\n"
    keyboard = []

    for i, campaign in enumerate(campaigns, 1):
        task_count = await _get_task_count(campaign)
        is_joined = campaign.id in joined_ids
        status_icon = "✅" if is_joined else "🔹"

        message += f"*{i}. {status_icon} {campaign.name}*\n"
        message += f"   {campaign.short_description}\n"
        message += f"   {t('campaigns_members', lang)}: {campaign.current_members}/{campaign.target_members}\n"
        message += f"   {t('campaigns_tasks_available', lang)}: {task_count} {t('campaigns_available', lang)}\n\n"

        if is_joined:
            keyboard.append([
                InlineKeyboardButton(
                    f"{t('btn_view_tasks', lang)}: {campaign.name[:20]}...",
                    callback_data=f"campaign_tasks_{campaign.id}"
                )
            ])
        else:
            keyboard.append([
                InlineKeyboardButton(
                    f"{t('btn_join', lang)}: {campaign.name[:20]}...",
                    callback_data=f"campaign_join_{campaign.id}"
                )
            ])

    if len(campaigns) == 10:
        keyboard.append([
            InlineKeyboardButton("⬅️", callback_data="campaigns_page_0"),
            InlineKeyboardButton("➡️", callback_data="campaigns_page_2")
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def joincampaign_command(update: Update, context: CallbackContext):
    """Handle /joincampaign <id> command - join a specific campaign."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Join campaign command from user {user.id} (@{user.username})")

    session, created = await _get_or_create_session(user.id, user.username, chat_id)
    await _record_command(session, 'joincampaign')

    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a campaign ID.\n"
            "Usage: `/joincampaign <campaign_id>`\n\n"
            "Use `/campaigns` to see available campaigns with their IDs.",
            parse_mode='Markdown'
        )
        return

    try:
        campaign_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid campaign ID.", parse_mode='Markdown')
        return

    campaign = await _get_campaign(campaign_id)
    if not campaign:
        await update.message.reply_text(
            "❌ Invalid campaign ID or campaign is not active.\n"
            "Use `/campaigns` to see available campaigns.",
            parse_mode='Markdown'
        )
        return

    already_joined = await _is_volunteer(campaign, session.user)
    if already_joined:
        await update.message.reply_text(
            f"✅ You're already a member of *{campaign.name}*!",
            parse_mode='Markdown'
        )
        return

    member_count = await _join_campaign(campaign, session.user)

    await update.message.reply_text(
        f"🎉 *Welcome to {campaign.name}!*\n\n"
        f"You've successfully joined the campaign.\n\n"
        f"*Next steps:*\n"
        f"1. Use `/tasks` to see available tasks\n"
        f"2. Claim tasks with `/claimtask <task_id>`\n"
        f"3. Complete tasks and earn points!\n\n"
        f"Check `/help` for more commands.",
        parse_mode='Markdown'
    )


async def campaign_callback_handler(update: Update, context: CallbackContext):
    """Handle callback queries for campaign actions."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    chat_id = update.effective_chat.id

    session, created = await _get_or_create_session(user.id, user.username, chat_id)

    callback_data = query.data

    if callback_data.startswith('campaign_join_'):
        campaign_id = int(callback_data.split('_')[-1])
        await handle_campaign_join(query, session, campaign_id)

    elif callback_data.startswith('campaign_tasks_'):
        campaign_id = int(callback_data.split('_')[-1])
        await handle_campaign_view_tasks(query, session, campaign_id)

    elif callback_data.startswith('campaigns_page_'):
        page = int(callback_data.split('_')[-1])
        await handle_campaigns_pagination(query, session, page)


async def handle_campaign_join(query, session, campaign_id):
    """Handle campaign join from inline button."""
    campaign = await _get_campaign(campaign_id)
    if not campaign:
        await query.edit_message_text(
            "❌ This campaign is no longer available.",
            parse_mode='Markdown'
        )
        return

    already_joined = await _is_volunteer(campaign, session.user)
    if already_joined:
        await query.edit_message_text(
            f"✅ You're already a member of *{campaign.name}*!",
            parse_mode='Markdown'
        )
        return

    member_count = await _join_campaign(campaign, session.user)
    task_count = await _get_task_count(campaign)

    await query.edit_message_text(
        f"🎉 *Welcome to {campaign.name}!*\n\n"
        f"You've successfully joined the campaign.\n\n"
        f"*Campaign Details:*\n"
        f"• {campaign.short_description}\n"
        f"• 👥 Members: {member_count}/{campaign.target_members}\n"
        f"• 🎯 Tasks: {task_count} available\n\n"
        f"*Next steps:*\n"
        f"1. Use `/tasks` to see available tasks\n"
        f"2. Claim tasks with `/claimtask <task_id>`\n"
        f"3. Complete tasks and earn points!",
        parse_mode='Markdown'
    )


async def handle_campaign_view_tasks(query, session, campaign_id):
    """Handle View Tasks button for a joined campaign."""
    lang = getattr(session, 'language', 'en') or 'en'

    campaign = await _get_campaign(campaign_id)
    if not campaign:
        await query.edit_message_text(
            t('campaign_not_available', lang),
            parse_mode='Markdown'
        )
        return

    @sync_to_async
    def _get_campaign_tasks(cid):
        from apps.tasks.models import Task
        return list(Task.objects.filter(
            campaign_id=cid, is_active=True
        ).order_by('-points')[:10])

    tasks = await _get_campaign_tasks(campaign_id)

    if not tasks:
        await query.edit_message_text(
            t('tasks_none', lang).format(name=campaign.name),
            parse_mode='Markdown'
        )
        return

    # Task type icons
    type_icons = {
        'twitter_post': '🐦', 'twitter_retweet': '🔁', 'twitter_like': '❤️',
        'telegram_share': '📢', 'telegram_invite': '👥',
        'content_creation': '✍️', 'research': '🔍', 'other': '📌',
    }

    message = t('tasks_title', lang).format(name=campaign.name) + "\n\n"
    keyboard = []

    for i, task in enumerate(tasks, 1):
        icon = type_icons.get(task.task_type, '📌')
        message += f"*{i}. {icon} {task.title}*\n"
        message += f"   🏆 {task.points} {t('task_pts', lang)}  ⏱ {task.estimated_time} {t('task_min', lang)}\n\n"

        keyboard.append([
            InlineKeyboardButton(
                f"{icon} {task.title[:30]}",
                callback_data=f"task_claim_{task.id}"
            )
        ])

    message += t('tasks_tap_to_start', lang)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def handle_campaigns_pagination(query, session, page):
    """Handle pagination for campaigns list."""
    @sync_to_async
    def _get_page(user, offset):
        from apps.campaigns.models import Campaign
        return list(Campaign.objects.filter(
            status=Campaign.Status.ACTIVE
        ).order_by('-created_at')[offset:offset+10])

    offset = page * 10
    campaigns = await _get_page(session.user, offset)

    if not campaigns:
        await query.edit_message_text(
            "📭 No more campaigns available.",
            parse_mode='Markdown'
        )
        return

    message = f"📋 *Available Campaigns* (Page {page + 1})\n\n"
    keyboard = []

    for i, campaign in enumerate(campaigns, 1):
        task_count = await _get_task_count(campaign)
        message += f"*{i}. {campaign.name}*\n"
        message += f"   {campaign.short_description}\n"
        message += f"   👥 Members: {campaign.current_members}/{campaign.target_members}\n"
        message += f"   🎯 Tasks: {task_count} available\n\n"

        keyboard.append([
            InlineKeyboardButton(
                f"Join: {campaign.name[:20]}...",
                callback_data=f"campaign_join_{campaign.id}"
            )
        ])

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton("⬅️ Previous", callback_data=f"campaigns_page_{page-1}")
        )
    if len(campaigns) == 10:
        pagination_buttons.append(
            InlineKeyboardButton("Next ➡️", callback_data=f"campaigns_page_{page+1}")
        )

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# Exported session helper for other handlers
get_or_create_session = _get_or_create_session


# Handler registration
campaign_handlers = [
    CallbackQueryHandler(campaign_callback_handler, pattern='^campaign_')
]
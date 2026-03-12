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
def _join_campaign(campaign, user, referrer_id=None):
    """Join a campaign, optionally crediting a referrer."""
    from apps.campaigns.models import CampaignVolunteer
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Resolve referrer
    invited_by = None
    if referrer_id:
        try:
            invited_by = User.objects.get(id=referrer_id)
        except User.DoesNotExist:
            pass

    CampaignVolunteer.objects.create(
        campaign=campaign,
        volunteer=user,
        invited_by=invited_by,
        status='active'
    )
    campaign.current_members = campaign.volunteers.count()
    campaign.save(update_fields=['current_members'])

    # Award bonus points to inviter
    if invited_by:
        invited_by.points += 10
        invited_by.save(update_fields=['points'])

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

        message += f"*{i}. {status_icon} {campaign.localized_name(lang)}*\n"
        message += f"   {campaign.localized_short_description(lang)}\n"
        message += f"   {t('campaigns_members', lang)}: {campaign.current_members}/{campaign.target_members}\n"
        message += f"   {t('campaigns_tasks_available', lang)}: {task_count} {t('campaigns_available', lang)}\n\n"

        if is_joined:
            keyboard.append([
                InlineKeyboardButton(
                    f"{t('btn_view_tasks', lang)}: {campaign.localized_name(lang)[:20]}...",
                    callback_data=f"campaign_tasks_{campaign.id}"
                )
            ])
        else:
            keyboard.append([
                InlineKeyboardButton(
                    f"{t('btn_join', lang)}: {campaign.localized_name(lang)[:20]}...",
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
            f"✅ You're already a member of *{campaign.localized_name(lang)}*!",
            parse_mode='Markdown'
        )
        return

    member_count = await _join_campaign(campaign, session.user)

    await update.message.reply_text(
        f"🎉 *Welcome to {campaign.localized_name(lang)}!*\n\n"
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

    elif callback_data.startswith('campaign_invite_'):
        campaign_id = int(callback_data.split('_')[-1])
        await handle_invite_link(query, session, campaign_id)

    elif callback_data.startswith('invite_style_'):
        # invite_style_{campaign_id}_{lang}
        parts = callback_data.split('_')
        campaign_id = int(parts[2])
        invite_lang = parts[3]
        await handle_invite_style_picker(query, session, campaign_id, invite_lang)

    elif callback_data.startswith('invite_send_'):
        # invite_send_{campaign_id}_{lang}_{style}
        parts = callback_data.split('_')
        campaign_id = int(parts[2])
        invite_lang = parts[3]
        style = parts[4]
        await handle_invite_send(query, session, campaign_id, invite_lang, style)

    elif callback_data.startswith('campaigns_page_'):
        page = int(callback_data.split('_')[-1])
        await handle_campaigns_pagination(query, session, page)

    else:
        # Handle campaign_{id} — campaign detail view from menu
        parts = callback_data.split('_')
        if len(parts) == 2 and parts[0] == 'campaign' and parts[1].isdigit():
            campaign_id = int(parts[1])
            await handle_campaign_detail(query, session, campaign_id)


async def handle_campaign_detail(query, session, campaign_id):
    """Show campaign detail card with Join or View Tasks button."""
    lang = getattr(session, 'language', 'en') or 'en'
    campaign = await _get_campaign(campaign_id)
    if not campaign:
        await query.edit_message_text(
            t('campaign_not_available', lang),
            parse_mode='Markdown'
        )
        return

    is_member = await _is_volunteer(campaign, session.user) if session.user else False
    task_count = await _get_task_count(campaign)

    msg = f"📢 *{campaign.localized_name(lang)}*\n\n"
    msg += f"{campaign.localized_short_description(lang)}\n\n"
    msg += t('campaign_detail_volunteers', lang).format(
        current=campaign.current_members, target=campaign.target_members
    ) + "\n"
    msg += t('campaign_detail_tasks', lang).format(count=task_count) + "\n"

    keyboard = []
    if is_member:
        msg += f"\n{t('campaign_already_in', lang)}\n"
        msg += t('campaign_tap_tasks', lang) + "\n"
        keyboard.append([
            InlineKeyboardButton(
                t('btn_view_tasks_icon', lang),
                callback_data=f"campaign_tasks_{campaign_id}"
            )
        ])
    else:
        msg += f"\n{t('campaign_ready_join', lang)}\n"
        keyboard.append([
            InlineKeyboardButton(
                t('btn_join_campaign', lang),
                callback_data=f"campaign_join_{campaign_id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")
    ])

    await query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def handle_campaign_join(query, session, campaign_id):
    """Handle campaign join from inline button."""
    lang = getattr(session, 'language', 'en') or 'en'
    campaign = await _get_campaign(campaign_id)
    if not campaign:
        await query.edit_message_text(
            t('campaign_not_available', lang),
            parse_mode='Markdown'
        )
        return

    already_joined = await _is_volunteer(campaign, session.user)
    if already_joined:
        # Show tasks directly if already joined
        await handle_campaign_view_tasks(query, session, campaign_id)
        return

    member_count = await _join_campaign(campaign, session.user)
    task_count = await _get_task_count(campaign)

    # ── Channel Broadcast (fire-and-forget) ──
    from handlers.tasks import _broadcast_volunteer_joined
    await _broadcast_volunteer_joined(
        bot=query._bot,
        campaign_id=campaign_id,
        member_count=member_count
    )

    keyboard = [[
        InlineKeyboardButton(
            t('btn_view_tasks_icon', lang),
            callback_data=f"campaign_tasks_{campaign_id}"
        )
    ], [
        InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")
    ]]

    await query.edit_message_text(
        t('campaign_join_welcome', lang).format(
            name=campaign.localized_name(lang), count=member_count, tasks=task_count
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def handle_campaign_view_tasks(query, session, campaign_id):
    """Handle View Tasks — checklist-style with ✅/⬜ status and community pulse."""
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
            campaign_id=cid, is_active=True,
            task_type__in=[
                'twitter_post', 'twitter_retweet', 'twitter_comment',
                'petition', 'mass_email',
            ]
        ).order_by('-points')[:10])

    tasks = await _get_campaign_tasks(campaign_id)

    if not tasks:
        await query.edit_message_text(
            t('tasks_none', lang).format(name=campaign.localized_name(lang)),
            parse_mode='Markdown'
        )
        return

    # Get user's completion status for each task
    from handlers.tasks import (
        _db_get_user_task_status_map, _db_get_campaign_pulse, get_level_title
    )
    status_map = {}
    if session.user:
        status_map = await _db_get_user_task_status_map(session.user, campaign_id)

    # Task type icons
    type_icons = {
        'twitter_post': '🐦', 'twitter_retweet': '🔁', 'twitter_comment': '💬',
        'twitter_like': '❤️', 'telegram_share': '📢', 'telegram_invite': '👥',
        'content_creation': '✍️', 'research': '🔍', 'other': '📌',
    }

    # Count done/total
    done_count = sum(
        1 for task in tasks
        if status_map.get(task.id) in ('completed', 'verified')
    )
    total_count = len(tasks)
    user_points = sum(
        task.points for task in tasks
        if status_map.get(task.id) in ('completed', 'verified')
    )

    message = t('checklist_title', lang).format(name=campaign.localized_name(lang)) + "\n\n"
    keyboard = []

    for task in tasks:
        icon = type_icons.get(task.task_type, '📌')
        user_status = status_map.get(task.id)

        # Status checkbox
        if user_status in ('completed', 'verified'):
            check = '✅'
            label = f"✅ {task.localized_title(lang)[:28]}"
        elif user_status in ('assigned', 'in_progress'):
            check = '🚧'
            label = f"🚧 {task.localized_title(lang)[:28]}"
        else:
            check = '⬜'
            label = f"{icon} {task.localized_title(lang)[:28]}"

        message += f"{check} {icon} {task.localized_title(lang)}  (+{task.points} {t('task_pts', lang)})\n"

        keyboard.append([
            InlineKeyboardButton(
                label,
                callback_data=f"task_claim_{task.id}"
            )
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
        message += f"*{i}. {campaign.localized_name(lang)}*\n"
        message += f"   {campaign.localized_short_description(lang)}\n"
        message += f"   👥 Members: {campaign.current_members}/{campaign.target_members}\n"
        message += f"   🎯 Tasks: {task_count} available\n\n"

        keyboard.append([
            InlineKeyboardButton(
                f"Join: {campaign.localized_name(lang)[:20]}...",
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


async def handle_invite_link(query, session, campaign_id):
    """Legacy entry point — redirect to language picker."""
    await handle_invite_language_picker(query, session, campaign_id)


async def handle_invite_language_picker(query, session, campaign_id):
    """Step 1: Let the volunteer choose the language for their invite message."""
    lang = getattr(session, 'language', 'en') or 'en'

    campaign = await _get_campaign(campaign_id)
    if not campaign:
        await query.edit_message_text(
            t('campaign_not_available', lang),
            parse_mode='Markdown'
        )
        return

    keyboard = [
        [InlineKeyboardButton(
            "🇬🇧 English",
            callback_data=f"invite_style_{campaign_id}_en"
        )],
        [InlineKeyboardButton(
            "🇮🇷 فارسی",
            callback_data=f"invite_style_{campaign_id}_fa"
        )],
        [InlineKeyboardButton(
            "🇸🇦 العربية",
            callback_data=f"invite_style_{campaign_id}_ar"
        )],
        [InlineKeyboardButton(
            t('btn_back_to_tasks', lang),
            callback_data=f"campaign_tasks_{campaign_id}"
        )],
        [InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")]
    ]

    await query.edit_message_text(
        t('invite_pick_language', lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def handle_invite_style_picker(query, session, campaign_id, invite_lang):
    """Step 2: Let the volunteer choose memorial (photo) or campaign (text) style."""
    lang = getattr(session, 'language', 'en') or 'en'

    keyboard = [
        [InlineKeyboardButton(
            t('btn_memorial_style', lang),
            callback_data=f"invite_send_{campaign_id}_{invite_lang}_memorial"
        )],
        [InlineKeyboardButton(
            t('btn_campaign_style', lang),
            callback_data=f"invite_send_{campaign_id}_{invite_lang}_campaign"
        )],
        [InlineKeyboardButton(
            t('btn_change_language', lang),
            callback_data=f"campaign_invite_{campaign_id}"
        )],
        [InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")]
    ]

    await query.edit_message_text(
        t('invite_pick_style', lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def handle_invite_send(query, session, campaign_id, invite_lang, style):
    """Step 3: Send the invite — photo for memorial, share-link for campaign."""
    lang = getattr(session, 'language', 'en') or 'en'

    campaign = await _get_campaign(campaign_id)
    if not campaign:
        await query.edit_message_text(
            t('campaign_not_available', lang),
            parse_mode='Markdown'
        )
        return

    # Build personalized deep-link with referral
    user_id = session.user.id if session.user else 0
    invite_link = f"https://t.me/peopleforpeacebot?start=campaign_{campaign_id}_ref_{user_id}"

    if style == 'memorial':
        # Send photo with emotional caption — volunteer then forwards it
        caption = t('invite_memorial_caption', invite_lang).format(link=invite_link)
        photo_url = "https://peopleforpeace.live/images/og-share-card.png"

        # Delete the inline message first, then send photo as new message
        try:
            await query.delete_message()
        except Exception:
            pass

        await query.get_bot().send_photo(
            chat_id=query.message.chat_id,
            photo=photo_url,
            caption=caption,
            parse_mode='Markdown'
        )

        # Follow up with instruction + back buttons
        keyboard = [
            [InlineKeyboardButton(
                t('btn_back_to_tasks', lang),
                callback_data=f"campaign_tasks_{campaign_id}"
            )],
            [InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")]
        ]

        await query.get_bot().send_message(
            chat_id=query.message.chat_id,
            text=t('invite_memorial_sent', lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    else:
        # Campaign style: open Telegram's share dialog with text
        from urllib.parse import quote
        share_text = t('invite_campaign_text', invite_lang).format(
            name=campaign.localized_name(invite_lang), link=invite_link
        )
        share_url = f"https://t.me/share/url?url={quote(invite_link)}&text={quote(share_text)}"

        keyboard = [
            [InlineKeyboardButton(
                t('btn_share_link', lang),
                url=share_url
            )],
            [InlineKeyboardButton(
                t('btn_change_language', lang),
                callback_data=f"campaign_invite_{campaign_id}"
            )],
            [InlineKeyboardButton(
                t('btn_back_to_tasks', lang),
                callback_data=f"campaign_tasks_{campaign_id}"
            )],
            [InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")]
        ]

        await query.edit_message_text(
            t('invite_message', lang).format(
                name=campaign.localized_name(lang), link=invite_link
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown',
            disable_web_page_preview=True
        )


# Exported session helper for other handlers
get_or_create_session = _get_or_create_session


async def show_my_campaigns(query, session, lang: str):
    """Show user's joined campaigns. Task-first flow.

    - 0 joined → fall through to browse all campaigns
    - 1 joined → show that campaign's task checklist directly
    - 2+ joined → show campaign picker with task counts
    """
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    if not session.user:
        from utils.translations import get_back_to_menu_inline
        await query.message.reply_text(
            t('register_need_first', lang),
            reply_markup=get_back_to_menu_inline(lang),
            parse_mode='Markdown',
        )
        return

    @sync_to_async
    def _get_joined_campaigns(user):
        from apps.campaigns.models import CampaignVolunteer
        cvs = (
            CampaignVolunteer.objects
            .filter(volunteer=user, status='active')
            .select_related('campaign')
            .order_by('-joined_at')
        )
        return [(cv.campaign, cv.campaign.tasks.filter(is_active=True).count()) for cv in cvs]

    joined = await _get_joined_campaigns(session.user)

    if len(joined) == 0:
        # No campaigns joined — show browse list (existing behavior)
        await _handle_browse_campaigns(query, session, lang)
        return

    if len(joined) == 1:
        # Single campaign — go straight to task checklist
        campaign, _ = joined[0]
        await handle_campaign_view_tasks(query, session, campaign.id)
        return

    # 2+ campaigns — show picker
    text = t('my_campaigns_title', lang) + "\n\n"
    keyboard = []

    for campaign, task_count in joined:
        text += f"✊ *{campaign.localized_name(lang)}*  —  {task_count} {t('campaigns_tasks_label', lang)}\n"
        keyboard.append([
            InlineKeyboardButton(
                f"✊ {campaign.localized_name(lang)}",
                callback_data=f"campaign_tasks_{campaign.id}"
            )
        ])

    text += "\n" + t('my_campaigns_tap', lang)

    from utils.translations import get_back_to_menu_inline
    keyboard.append([
        InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")
    ])

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown',
    )


async def _handle_browse_campaigns(query, session, lang: str):
    """Show all active campaigns for users who haven't joined any yet."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    campaigns = await _get_active_campaigns()

    if not campaigns:
        from utils.translations import get_back_to_menu_inline
        await query.message.reply_text(
            t('campaigns_none', lang),
            reply_markup=get_back_to_menu_inline(lang),
            parse_mode='Markdown',
        )
        return

    text = t('campaigns_title', lang) + "\n\n"
    keyboard = []

    for campaign in campaigns:
        task_count = await _get_task_count(campaign)
        desc = campaign.localized_short_description(lang)
        if desc:
            desc = desc[:60] + ('...' if len(desc) > 60 else '')
        text += f"✊ *{campaign.localized_name(lang)}*\n"
        if desc:
            text += f"  {desc}\n"
        text += f"  👥 {campaign.current_members} volunteers • {task_count} tasks\n\n"
        keyboard.append([
            InlineKeyboardButton(
                f"✊ {t('btn_join', lang)}: {campaign.localized_name(lang)[:20]}",
                callback_data=f"campaign_join_{campaign.id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")
    ])

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown',
    )


# Handler registration
campaign_handlers = [
    CallbackQueryHandler(campaign_callback_handler, pattern='^(campaign_|invite_style_|invite_send_)')
]
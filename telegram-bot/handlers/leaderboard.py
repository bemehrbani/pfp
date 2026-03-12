"""
Leaderboard command handlers for Telegram bot.
"""
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from asgiref.sync import sync_to_async

from utils.error_handling import error_handler, require_registration
from utils.state_management import state_manager

logger = logging.getLogger(__name__)


@sync_to_async
def _get_leaderboard_data(campaign_filter=None, current_user=None):
    """Get leaderboard data from database (sync, wrapped for async)."""
    from django.contrib.auth import get_user_model
    from django.db.models import Sum, Count, Q
    from apps.campaigns.models import CampaignVolunteer

    User = get_user_model()
    users = User.objects.filter(role='volunteer', is_active=True)

    if campaign_filter:
        campaign_user_ids = CampaignVolunteer.objects.filter(
            campaign=campaign_filter
        ).values_list('volunteer_id', flat=True)
        users = users.filter(id__in=campaign_user_ids)

    users = users.order_by('-total_points', 'date_joined')
    top_users = list(users[:10])
    total_users = users.count()

    current_user_rank = None
    if current_user and current_user.id not in [u.id for u in top_users]:
        current_user_rank = users.filter(total_points__gt=(current_user.total_points or 0)).count() + 1

    return {
        'top_users': top_users,
        'current_user_rank': current_user_rank,
        'total_users': total_users,
        'campaign_filter': campaign_filter
    }


@sync_to_async
def _get_campaign_for_filter(campaign_id):
    """Get campaign by ID."""
    from apps.campaigns.models import Campaign
    try:
        return Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return None


@sync_to_async
def _get_user_by_telegram_id(telegram_id):
    """Get user by telegram ID."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None


@sync_to_async
def _get_user_campaigns(telegram_id):
    """Get user's campaigns for filter."""
    from apps.campaigns.models import CampaignVolunteer
    return list(
        CampaignVolunteer.objects.filter(
            volunteer__telegram_id=telegram_id,
            status='active'
        ).select_related('campaign').order_by('campaign__name')
    )


@error_handler
@require_registration
async def leaderboard_command(update: Update, context: CallbackContext):
    """Handle /leaderboard command - show top volunteers."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Leaderboard command from user {user.id} (@{user.username})")

    session, created = await state_manager.get_or_create_session(update, context)
    await state_manager.record_command(session, 'leaderboard')

    db_user = context.user_data['db_user']

    campaign_filter = None
    if context.args:
        try:
            campaign_id = int(context.args[0])
            campaign_filter = await _get_campaign_for_filter(campaign_id)
            if not campaign_filter:
                await update.message.reply_text(
                    "❌ Invalid campaign ID.\n"
                    "Use `/campaigns` to see available campaigns.",
                    parse_mode='Markdown'
                )
                return
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid campaign ID.", parse_mode='Markdown'
            )
            return

    data = await _get_leaderboard_data(campaign_filter, db_user)

    message = create_leaderboard_message(data, campaign_filter, db_user)
    keyboard = create_leaderboard_keyboard(campaign_filter)

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


def create_leaderboard_message(data, campaign_filter, current_user):
    """Create leaderboard message from data (pure formatting, no DB)."""
    top_users = data['top_users']
    current_user_rank = data['current_user_rank']
    total_users = data['total_users']

    if campaign_filter:
        message = f"🏆 *Leaderboard - {campaign_filter.name}*\n\n"
    else:
        message = "🏆 *Global Leaderboard*\n\n"

    message += f"*Top Volunteers (out of {total_users} total)*\n\n"

    for i, user in enumerate(top_users, 1):
        medal = ""
        if i == 1:
            medal = "🥇 "
        elif i == 2:
            medal = "🥈 "
        elif i == 3:
            medal = "🥉 "

        points = getattr(user, 'total_points', 0) or 0

        if current_user and user.id == current_user.id:
            message += f"*{i}. {medal}YOU - {user.first_name}*\n"
        else:
            message += f"{i}. {medal}{user.first_name}\n"

        message += f"   📊 {points} points\n\n"

    if current_user_rank:
        message += f"*Your Rank:* #{current_user_rank}\n"
        message += f"*Your Points:* {getattr(current_user, 'total_points', 0) or 0}\n\n"

    message += "\n_Leaderboard updates in real-time._"

    return message


def create_leaderboard_keyboard(campaign_filter):
    """Create inline keyboard for leaderboard filters (pure, no DB)."""
    keyboard = []

    if campaign_filter:
        keyboard.append([
            InlineKeyboardButton("🌍 View Global Leaderboard", callback_data="leaderboard_global")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("📋 Filter by Campaign", callback_data="leaderboard_filter")
        ])

    keyboard.append([
        InlineKeyboardButton("🔄 Refresh", callback_data="leaderboard_refresh")
    ])

    return keyboard


async def leaderboard_callback_handler(update: Update, context: CallbackContext):
    """Handle callback queries for leaderboard actions."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    chat_id = update.effective_chat.id

    session, created = await state_manager.get_or_create_session(update, context)

    callback_data = query.data

    if callback_data == 'leaderboard_global':
        await show_global_leaderboard(query, session)
    elif callback_data == 'leaderboard_filter':
        await show_campaign_filter_options(query, session)
    elif callback_data == 'leaderboard_refresh':
        await refresh_leaderboard(query, session)
    elif callback_data.startswith('leaderboard_campaign_'):
        campaign_id = int(callback_data.split('_')[-1])
        await show_campaign_leaderboard(query, session, campaign_id)


async def show_global_leaderboard(query, session):
    """Show global leaderboard."""
    db_user = await _get_user_by_telegram_id(session.telegram_id)
    if not db_user:
        await query.edit_message_text("User not found. Please register first.")
        return

    data = await _get_leaderboard_data(None, db_user)
    message = create_leaderboard_message(data, None, db_user)
    keyboard = create_leaderboard_keyboard(None)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_campaign_filter_options(query, session):
    """Show campaign filter options."""
    user_campaigns = await _get_user_campaigns(session.telegram_id)

    if not user_campaigns:
        await query.edit_message_text(
            "📭 You haven't joined any campaigns yet.\n"
            "Use `/campaigns` to browse and join available campaigns.",
            parse_mode='Markdown'
        )
        return

    keyboard = []
    for cv in user_campaigns:
        keyboard.append([
            InlineKeyboardButton(
                f"📋 {cv.campaign.localized_name(lang)[:30]}",
                callback_data=f"leaderboard_campaign_{cv.campaign.id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅️ Back to Global", callback_data="leaderboard_global")
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "📋 *Select a Campaign*\n\n"
        "Choose a campaign to see its leaderboard:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_campaign_leaderboard(query, session, campaign_id):
    """Show leaderboard for a specific campaign."""
    db_user = await _get_user_by_telegram_id(session.telegram_id)
    if not db_user:
        await query.edit_message_text("User not found. Please register first.")
        return

    campaign = await _get_campaign_for_filter(campaign_id)
    if not campaign:
        await query.edit_message_text(
            "❌ Campaign not found or is no longer active.",
            parse_mode='Markdown'
        )
        return

    data = await _get_leaderboard_data(campaign, db_user)
    message = create_leaderboard_message(data, campaign, db_user)
    keyboard = create_leaderboard_keyboard(campaign)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def refresh_leaderboard(query, session):
    """Refresh the current leaderboard view."""
    await query.answer("Leaderboard refreshed! ✅")


# Handler registration
leaderboard_handlers = [
    CallbackQueryHandler(leaderboard_callback_handler, pattern='^leaderboard_')
]
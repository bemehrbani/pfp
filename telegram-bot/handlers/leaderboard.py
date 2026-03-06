"""
Leaderboard command handlers for Telegram bot.
"""
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count

from utils.error_handling import error_handler, require_registration
from utils.state_management import state_manager

logger = logging.getLogger(__name__)
User = get_user_model()


@error_handler
@require_registration
async def leaderboard_command(update: Update, context: CallbackContext):
    """Handle /leaderboard command - show top volunteers."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Leaderboard command from user {user.id} (@{user.username})")

    # Get or create session
    session, created = await state_manager.get_or_create_session(update, context)
    await state_manager.record_command(session, 'leaderboard')

    # Get user from context
    db_user = context.user_data['db_user']

    # Check if campaign filter was provided
    campaign_filter = None
    if context.args:
        try:
            from apps.campaigns.models import Campaign
            campaign_filter = Campaign.objects.get(id=int(context.args[0]))
        except (ValueError, Campaign.DoesNotExist):
            await update.message.reply_text(
                "❌ Invalid campaign ID.\n"
                "Use `/campaigns` to see available campaigns with their IDs.",
                parse_mode='Markdown'
            )
            return

    # Get leaderboard data
    leaderboard_data = await get_leaderboard_data(campaign_filter, db_user)

    # Create leaderboard message
    message = await create_leaderboard_message(leaderboard_data, campaign_filter, db_user)

    # Create inline keyboard for filters
    keyboard = await create_leaderboard_keyboard(campaign_filter)

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def get_leaderboard_data(campaign_filter=None, current_user=None):
    """
    Get leaderboard data from database.

    Args:
        campaign_filter: Optional campaign to filter by
        current_user: Current user to highlight in results

    Returns:
        Dictionary with leaderboard data
    """
    from apps.tasks.models import TaskAssignment
    from apps.campaigns.models import CampaignVolunteer

    # Base queryset for users
    users = User.objects.filter(role='volunteer', is_active=True)

    # Apply campaign filter if provided
    if campaign_filter:
        # Get users in this campaign
        campaign_user_ids = CampaignVolunteer.objects.filter(
            campaign=campaign_filter
        ).values_list('user_id', flat=True)
        users = users.filter(id__in=campaign_user_ids)

    # Annotate with statistics
    users = users.annotate(
        total_points=models.Sum('task_assignments__task__points',
                               filter=models.Q(task_assignments__status='completed')),
        completed_tasks=models.Count('task_assignments',
                                     filter=models.Q(task_assignments__status='completed')),
        active_campaigns=models.Count('campaign_volunteers',
                                      filter=models.Q(campaign_volunteers__campaign__status='active'))
    ).order_by('-total_points', '-completed_tasks', 'date_joined')

    # Get top 10 users
    top_users = list(users[:10])

    # Get current user's rank if not in top 10
    current_user_rank = None
    if current_user and current_user not in top_users:
        # Count users with more points
        users_with_more_points = users.filter(
            models.Q(total_points__gt=current_user.points) |
            models.Q(total_points=current_user.points, completed_tasks__gt=current_user.get_completed_task_count()) |
            models.Q(total_points=current_user.points, completed_tasks=current_user.get_completed_task_count(),
                     date_joined__lt=current_user.date_joined)
        ).count()
        current_user_rank = users_with_more_points + 1

    return {
        'top_users': top_users,
        'current_user_rank': current_user_rank,
        'total_users': users.count(),
        'campaign_filter': campaign_filter
    }


async def create_leaderboard_message(data, campaign_filter, current_user):
    """
    Create leaderboard message from data.

    Args:
        data: Leaderboard data dictionary
        campaign_filter: Campaign filter (if any)
        current_user: Current user object

    Returns:
        Formatted message string
    """
    top_users = data['top_users']
    current_user_rank = data['current_user_rank']
    total_users = data['total_users']

    # Create header
    if campaign_filter:
        message = f"🏆 *Leaderboard - {campaign_filter.name}*\n\n"
    else:
        message = "🏆 *Global Leaderboard*\n\n"

    message += f"*Top Volunteers (out of {total_users} total)*\n\n"

    # Add top users
    for i, user in enumerate(top_users, 1):
        medal = ""
        if i == 1:
            medal = "🥇 "
        elif i == 2:
            medal = "🥈 "
        elif i == 3:
            medal = "🥉 "

        points = user.total_points or 0
        tasks = user.completed_tasks or 0
        campaigns = user.active_campaigns or 0

        # Highlight current user
        if user.id == current_user.id:
            message += f"*{i}. {medal}YOU - {user.first_name}*\n"
        else:
            message += f"{i}. {medal}{user.first_name}\n"

        message += f"   📊 {points} points | ✅ {tasks} tasks | 📋 {campaigns} campaigns\n\n"

    # Add current user's rank if not in top 10
    if current_user_rank:
        user_points = current_user.points or 0
        user_tasks = current_user.get_completed_task_count()
        user_campaigns = current_user.get_active_campaign_count()

        message += f"*Your Rank:* #{current_user_rank}\n"
        message += f"*Your Stats:* {user_points} points | {user_tasks} tasks | {user_campaigns} campaigns\n\n"

        # Add motivational message
        if current_user_rank <= 10:
            message += "🌟 *You're in the top 10! Keep up the great work!*\n"
        elif current_user_rank <= 50:
            message += "🚀 *You're doing great! A few more tasks and you'll climb higher!*\n"
        else:
            message += "💪 *Keep participating! Every task brings you closer to the top!*\n"

    # Add time period note
    message += "\n_Leaderboard updates in real-time. Last updated: Now_"

    return message


async def create_leaderboard_keyboard(campaign_filter):
    """
    Create inline keyboard for leaderboard filters.

    Args:
        campaign_filter: Current campaign filter (if any)

    Returns:
        List of keyboard rows
    """
    keyboard = []

    # Global leaderboard button
    if campaign_filter:
        keyboard.append([
            InlineKeyboardButton("🌍 View Global Leaderboard", callback_data="leaderboard_global")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("📋 Filter by Campaign", callback_data="leaderboard_filter")
        ])

    # Refresh button
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

    # Get or create session
    session, created = await state_manager.get_or_create_session(update, context)

    callback_data = query.data

    if callback_data == 'leaderboard_global':
        # Show global leaderboard
        await show_global_leaderboard(query, session)

    elif callback_data == 'leaderboard_filter':
        # Show campaign filter options
        await show_campaign_filter_options(query, session)

    elif callback_data == 'leaderboard_refresh':
        # Refresh current leaderboard
        await refresh_leaderboard(query, session)

    elif callback_data.startswith('leaderboard_campaign_'):
        # Show leaderboard for specific campaign
        campaign_id = int(callback_data.split('_')[-1])
        await show_campaign_leaderboard(query, session, campaign_id)


async def show_global_leaderboard(query, session):
    """Show global leaderboard."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        db_user = User.objects.get(telegram_id=session.telegram_id)
    except User.DoesNotExist:
        await query.edit_message_text("User not found. Please register first.")
        return

    # Get leaderboard data
    leaderboard_data = await get_leaderboard_data(None, db_user)

    # Create message
    message = await create_leaderboard_message(leaderboard_data, None, db_user)

    # Create keyboard
    keyboard = await create_leaderboard_keyboard(None)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_campaign_filter_options(query, session):
    """Show campaign filter options."""
    from apps.campaigns.models import CampaignVolunteer, Campaign

    try:
        # Get user's campaigns
        user_campaigns = CampaignVolunteer.objects.filter(
            user__telegram_id=session.telegram_id,
            campaign__status='active'
        ).select_related('campaign').order_by('campaign__name')

        if not user_campaigns:
            await query.edit_message_text(
                "📭 You haven't joined any campaigns yet.\n"
                "Use `/campaigns` to browse and join available campaigns.",
                parse_mode='Markdown'
            )
            return

        # Create keyboard with campaign options
        keyboard = []
        for cv in user_campaigns:
            keyboard.append([
                InlineKeyboardButton(
                    f"📋 {cv.campaign.name[:30]}",
                    callback_data=f"leaderboard_campaign_{cv.campaign.id}"
                )
            ])

        # Add back button
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

    except Exception as e:
        logger.error(f"Failed to show campaign filter options: {e}")
        await query.edit_message_text(
            "❌ Failed to load campaign options. Please try again.",
            parse_mode='Markdown'
        )


async def show_campaign_leaderboard(query, session, campaign_id):
    """Show leaderboard for a specific campaign."""
    from django.contrib.auth import get_user_model
    from apps.campaigns.models import Campaign

    User = get_user_model()

    try:
        db_user = User.objects.get(telegram_id=session.telegram_id)
        campaign = Campaign.objects.get(id=campaign_id, status='active')

        # Get leaderboard data
        leaderboard_data = await get_leaderboard_data(campaign, db_user)

        # Create message
        message = await create_leaderboard_message(leaderboard_data, campaign, db_user)

        # Create keyboard
        keyboard = await create_leaderboard_keyboard(campaign)

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    except Campaign.DoesNotExist:
        await query.edit_message_text(
            "❌ Campaign not found or is no longer active.",
            parse_mode='Markdown'
        )
    except User.DoesNotExist:
        await query.edit_message_text("User not found. Please register first.")
    except Exception as e:
        logger.error(f"Failed to show campaign leaderboard: {e}")
        await query.edit_message_text(
            "❌ Failed to load leaderboard. Please try again.",
            parse_mode='Markdown'
        )


async def refresh_leaderboard(query, session):
    """Refresh the current leaderboard view."""
    # This would re-fetch and update the current view
    # For now, just show a message and keep the same view
    await query.answer("Leaderboard refreshed! ✅")


# Handler registration
leaderboard_handlers = [
    CallbackQueryHandler(leaderboard_callback_handler, pattern='^leaderboard_')
]
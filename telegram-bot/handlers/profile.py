"""
Profile command handlers for Telegram bot.
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count

from utils.error_handling import error_handler, require_registration
from utils.state_management import state_manager

logger = logging.getLogger(__name__)
User = get_user_model()


@error_handler
@require_registration
async def profile_command(update: Update, context: CallbackContext):
    """Handle /profile command - show user profile and statistics."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Profile command from user {user.id} (@{user.username})")

    # Get or create session
    session, created = await state_manager.get_or_create_session(update, context)
    await state_manager.record_command(session, 'profile')

    # Get user from context (added by require_registration decorator)
    db_user = context.user_data['db_user']

    # Calculate user statistics
    from apps.tasks.models import TaskAssignment
    from apps.campaigns.models import CampaignVolunteer

    # Get task statistics
    task_stats = TaskAssignment.objects.filter(user=db_user).aggregate(
        total_tasks=Count('id'),
        completed_tasks=Count('id', filter=models.Q(status='completed')),
        pending_tasks=Count('id', filter=models.Q(status='pending_review')),
        total_points=Sum('task__points', filter=models.Q(status='completed'))
    )

    # Get campaign statistics
    campaign_stats = CampaignVolunteer.objects.filter(user=db_user).aggregate(
        total_campaigns=Count('id'),
        active_campaigns=Count('id', filter=models.Q(campaign__status='active'))
    )

    # Create profile message
    profile_message = (
        f"👤 *Your Profile*\n\n"
        f"*Basic Information:*\n"
        f"• Name: {db_user.first_name} {db_user.last_name or ''}\n"
        f"• Email: {db_user.email}\n"
        f"• Telegram: @{db_user.telegram_username or 'Not set'}\n"
        f"• Role: {db_user.get_role_display()}\n"
        f"• Level: {db_user.level}\n\n"
    )

    # Add points information
    profile_message += (
        f"*Points & Progress:*\n"
        f"• Total Points: {db_user.points}\n"
        f"• Points to Next Level: {max(0, db_user.get_points_for_next_level() - db_user.points)}\n\n"
    )

    # Add task statistics
    profile_message += (
        f"*Task Statistics:*\n"
        f"• Total Tasks: {task_stats['total_tasks'] or 0}\n"
        f"• Completed: {task_stats['completed_tasks'] or 0}\n"
        f"• Pending Review: {task_stats['pending_tasks'] or 0}\n"
        f"• Points Earned: {task_stats['total_points'] or 0}\n\n"
    )

    # Add campaign statistics
    profile_message += (
        f"*Campaign Participation:*\n"
        f"• Total Campaigns: {campaign_stats['total_campaigns'] or 0}\n"
        f"• Active Campaigns: {campaign_stats['active_campaigns'] or 0}\n\n"
    )

    # Add registration date
    if db_user.date_joined:
        profile_message += (
            f"*Member Since:* {db_user.date_joined.strftime('%B %d, %Y')}\n\n"
        )

    # Add motivational message based on activity
    if task_stats['completed_tasks'] == 0:
        profile_message += "🌟 *Get started by joining a campaign with `/campaigns`!*"
    elif task_stats['completed_tasks'] < 5:
        profile_message += "🚀 *Great start! Keep going to earn more points!*"
    elif task_stats['completed_tasks'] < 20:
        profile_message += "🔥 *You're making great progress! Keep it up!*"
    else:
        profile_message += "🏆 *You're a top contributor! Thank you for your dedication!*"

    await update.message.reply_text(
        profile_message,
        parse_mode='Markdown'
    )


@error_handler
@require_registration
async def updateprofile_command(update: Update, context: CallbackContext):
    """Handle /updateprofile command - update user profile information."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Update profile command from user {user.id} (@{user.username})")

    # Get or create session
    session, created = await state_manager.get_or_create_session(update, context)
    await state_manager.record_command(session, 'updateprofile')

    # Get user from context
    db_user = context.user_data['db_user']

    # Check if arguments were provided
    if not context.args:
        await update.message.reply_text(
            "📝 *Update Your Profile*\n\n"
            "You can update the following information:\n\n"
            "• *Name:* `/updateprofile name <your name>`\n"
            "• *Email:* `/updateprofile email <new email>`\n\n"
            "Example: `/updateprofile name John Doe`\n\n"
            "Note: Some information like Telegram username is automatically updated.",
            parse_mode='Markdown'
        )
        return

    # Parse command arguments
    action = context.args[0].lower()
    value = ' '.join(context.args[1:]) if len(context.args) > 1 else None

    if not value:
        await update.message.reply_text(
            f"❌ Please provide a value for {action}.\n"
            f"Example: `/updateprofile {action} <value>`",
            parse_mode='Markdown'
        )
        return

    # Update based on action
    if action == 'name':
        # Split into first and last name
        name_parts = value.split(' ', 1)
        db_user.first_name = name_parts[0]
        db_user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        db_user.save(update_fields=['first_name', 'last_name'])

        await update.message.reply_text(
            f"✅ *Name updated successfully!*\n\n"
            f"Your name has been updated to: *{value}*",
            parse_mode='Markdown'
        )

    elif action == 'email':
        # Validate email
        if '@' not in value or '.' not in value.split('@')[-1]:
            await update.message.reply_text(
                "❌ Please enter a valid email address.\n"
                "Example: user@example.com"
            )
            return

        # Check if email already exists
        if User.objects.filter(email=value).exclude(id=db_user.id).exists():
            await update.message.reply_text(
                "❌ This email is already registered by another user."
            )
            return

        db_user.email = value
        db_user.save(update_fields=['email'])

        await update.message.reply_text(
            f"✅ *Email updated successfully!*\n\n"
            f"Your email has been updated to: *{value}*",
            parse_mode='Markdown'
        )

    else:
        await update.message.reply_text(
            f"❌ Unknown field: {action}\n\n"
            "Available fields: `name`, `email`\n"
            "Example: `/updateprofile name John Doe`",
            parse_mode='Markdown'
        )
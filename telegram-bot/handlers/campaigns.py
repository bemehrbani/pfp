"""
Campaign command handlers for Telegram bot.
"""
import logging
from typing import List, Tuple
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.campaigns.models import Campaign, CampaignVolunteer
from apps.telegram.models import TelegramSession, TelegramMessageLog

logger = logging.getLogger(__name__)
User = get_user_model()


async def campaigns_command(update: Update, context: CallbackContext):
    """Handle /campaigns command - list available campaigns with pagination."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Campaigns command from user {user.id} (@{user.username})")

    # Get or create Telegram session
    session, created = await get_or_create_session(user, chat_id)
    session.record_command('campaigns')

    # Check if user is registered
    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    # Get available campaigns (active, not joined by user)
    campaigns = Campaign.objects.filter(
        status=Campaign.Status.ACTIVE
    ).exclude(
        volunteers__user=session.user
    ).order_by('-created_at')[:10]  # Limit to 10 for pagination

    if not campaigns:
        await update.message.reply_text(
            "📭 No campaigns available at the moment.\n\n"
            "Check back later or contact your campaign manager for updates.",
            parse_mode='Markdown'
        )
        return

    # Create campaign list message
    message = "📋 *Available Campaigns*\n\n"
    keyboard = []

    for i, campaign in enumerate(campaigns, 1):
        message += f"*{i}. {campaign.name}*\n"
        message += f"   {campaign.short_description}\n"
        message += f"   👥 Members: {campaign.current_members}/{campaign.target_members}\n"
        message += f"   🎯 Tasks: {campaign.tasks.count()} available\n\n"

        # Create inline button for each campaign
        keyboard.append([
            InlineKeyboardButton(
                f"Join: {campaign.name[:20]}...",
                callback_data=f"campaign_join_{campaign.id}"
            )
        ])

    message += "Click a button below to join a campaign."

    # Add pagination buttons if needed
    if len(campaigns) == 10:
        keyboard.append([
            InlineKeyboardButton("⬅️ Previous", callback_data="campaigns_page_0"),
            InlineKeyboardButton("Next ➡️", callback_data="campaigns_page_2")
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

    # Get or create Telegram session
    session, created = await get_or_create_session(user, chat_id)
    session.record_command('joincampaign')

    # Check if user is registered
    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    # Check if campaign ID was provided
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
        campaign = Campaign.objects.get(id=campaign_id, status=Campaign.Status.ACTIVE)
    except (ValueError, Campaign.DoesNotExist):
        await update.message.reply_text(
            "❌ Invalid campaign ID or campaign is not active.\n"
            "Use `/campaigns` to see available campaigns.",
            parse_mode='Markdown'
        )
        return

    # Check if user already joined
    if CampaignVolunteer.objects.filter(campaign=campaign, user=session.user).exists():
        await update.message.reply_text(
            f"✅ You're already a member of *{campaign.name}*!",
            parse_mode='Markdown'
        )
        return

    # Join the campaign
    CampaignVolunteer.objects.create(
        campaign=campaign,
        user=session.user,
        role=CampaignVolunteer.Role.VOLUNTEER
    )

    # Update campaign member count
    campaign.current_members += 1
    campaign.save(update_fields=['current_members'])

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

    # Get or create Telegram session
    session, created = await get_or_create_session(user, chat_id)

    callback_data = query.data

    if callback_data.startswith('campaign_join_'):
        # Handle campaign join request
        campaign_id = int(callback_data.split('_')[-1])
        await handle_campaign_join(query, session, campaign_id)

    elif callback_data.startswith('campaigns_page_'):
        # Handle pagination
        page = int(callback_data.split('_')[-1])
        await handle_campaigns_pagination(query, session, page)


async def handle_campaign_join(query, session, campaign_id):
    """Handle campaign join from inline button."""
    try:
        campaign = Campaign.objects.get(id=campaign_id, status=Campaign.Status.ACTIVE)
    except Campaign.DoesNotExist:
        await query.edit_message_text(
            "❌ This campaign is no longer available.",
            parse_mode='Markdown'
        )
        return

    # Check if user already joined
    if CampaignVolunteer.objects.filter(campaign=campaign, user=session.user).exists():
        await query.edit_message_text(
            f"✅ You're already a member of *{campaign.name}*!",
            parse_mode='Markdown'
        )
        return

    # Join the campaign
    CampaignVolunteer.objects.create(
        campaign=campaign,
        user=session.user,
        role=CampaignVolunteer.Role.VOLUNTEER
    )

    # Update campaign member count
    campaign.current_members += 1
    campaign.save(update_fields=['current_members'])

    await query.edit_message_text(
        f"🎉 *Welcome to {campaign.name}!*\n\n"
        f"You've successfully joined the campaign.\n\n"
        f"*Campaign Details:*\n"
        f"• {campaign.short_description}\n"
        f"• 👥 Members: {campaign.current_members}/{campaign.target_members}\n"
        f"• 🎯 Tasks: {campaign.tasks.count()} available\n\n"
        f"*Next steps:*\n"
        f"1. Use `/tasks` to see available tasks\n"
        f"2. Claim tasks with `/claimtask <task_id>`\n"
        f"3. Complete tasks and earn points!",
        parse_mode='Markdown'
    )


async def handle_campaigns_pagination(query, session, page):
    """Handle pagination for campaigns list."""
    # Calculate offset based on page
    offset = page * 10
    campaigns = Campaign.objects.filter(
        status=Campaign.Status.ACTIVE
    ).exclude(
        volunteers__user=session.user
    ).order_by('-created_at')[offset:offset+10]

    if not campaigns:
        await query.edit_message_text(
            "📭 No more campaigns available.",
            parse_mode='Markdown'
        )
        return

    # Create updated message
    message = f"📋 *Available Campaigns* (Page {page + 1})\n\n"
    keyboard = []

    for i, campaign in enumerate(campaigns, 1):
        message += f"*{i}. {campaign.name}*\n"
        message += f"   {campaign.short_description}\n"
        message += f"   👥 Members: {campaign.current_members}/{campaign.target_members}\n"
        message += f"   🎯 Tasks: {campaign.tasks.count()} available\n\n"

        keyboard.append([
            InlineKeyboardButton(
                f"Join: {campaign.name[:20]}...",
                callback_data=f"campaign_join_{campaign.id}"
            )
        ])

    # Add pagination buttons
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


async def get_or_create_session(user, chat_id):
    """Get or create Telegram session for user."""
    try:
        session = TelegramSession.objects.get(telegram_id=user.id)
        session.telegram_username = user.username
        session.telegram_chat_id = chat_id
        session.save(update_fields=['telegram_username', 'telegram_chat_id', 'updated_at'])
        return session, False
    except TelegramSession.DoesNotExist:
        # Try to find existing user by Telegram ID
        try:
            db_user = User.objects.get(telegram_id=user.id)
        except User.DoesNotExist:
            db_user = None

        session = TelegramSession.objects.create(
            telegram_id=user.id,
            telegram_username=user.username,
            telegram_chat_id=chat_id,
            user=db_user
        )
        return session, True


# Handler registration
campaign_handlers = [
    CallbackQueryHandler(campaign_callback_handler, pattern='^campaign_')
]
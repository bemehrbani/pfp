"""
Start command handler for Telegram bot.
"""
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from .db import get_user_by_telegram_id
from utils.state_management import state_manager

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: CallbackContext):
    """Handle /start command."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Start command from user {user.id} (@{user.username})")

    welcome_message = (
        "👋 Welcome to *People for Peace Campaign Manager*!\n\n"
        "I'm your assistant for participating in peace campaigns. "
        "Here's what you can do:\n\n"
        "• 📋 Browse available campaigns\n"
        "• 🎯 Claim and complete tasks\n"
        "• 📊 Track your progress and points\n"
        "• 🤝 Collaborate with other volunteers\n\n"
        "Use the menu below to get started!"
    )

    # Create keyboard
    keyboard = [
        ["📋 Browse Campaigns", "🎯 Available Tasks"],
        ["📊 My Progress", "🏆 Leaderboard"],
        ["ℹ️ Help", "👤 Profile"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text=welcome_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    # Get or create session (async-safe)
    session, created = await state_manager.get_or_create_session(update, context)

    # Check if user exists in database
    db_user = await get_user_by_telegram_id(user.id)
    if db_user:
        logger.info(f"Existing user {db_user.username} started bot")
    else:
        # Start registration — set session state in DB to AWAITING_EMAIL
        from apps.telegram.models import TelegramSession
        await state_manager.update_state(session, TelegramSession.State.AWAITING_EMAIL)

        await context.bot.send_message(
            chat_id=chat_id,
            text="It looks like you're new here! Let's get you registered.\n\n"
                 "Please send me your email address to continue."
        )
        logger.info(f"New user {user.id} started registration — state set to AWAITING_EMAIL")


async def help_command(update: Update, context: CallbackContext):
    """Handle /help command."""
    help_text = (
        "*People for Peace Campaign Manager - Help*\n\n"
        "*Available Commands:*\n"
        "/start - Start the bot and show welcome message\n"
        "/help - Show this help message\n"
        "/campaigns - List available campaigns\n"
        "/tasks - Show available tasks\n"
        "/mytasks - Show your assigned tasks\n"
        "/profile - Show your profile and points\n"
        "/leaderboard - Show top volunteers\n"
        "/storms - Show upcoming Twitter storms\n\n"
        "*How to Participate:*\n"
        "1. Browse campaigns with /campaigns\n"
        "2. Join a campaign\n"
        "3. Claim tasks with /tasks\n"
        "4. Complete tasks and submit proof\n"
        "5. Earn points and climb the leaderboard!\n\n"
        "Need more help? Contact your campaign manager."
    )

    await update.message.reply_text(
        help_text,
        parse_mode='Markdown'
    )
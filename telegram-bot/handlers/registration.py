"""
Registration and text message handlers for Telegram bot.
Handles user registration flow and general text messages.
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler

from utils.error_handling import error_handler
from utils.state_management import state_manager

logger = logging.getLogger(__name__)


@error_handler
async def handle_text_message(update: Update, context: CallbackContext):
    """
    Handle general text messages (non-commands).
    Mainly used for registration flow.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Text message from user {user.id} (@{user.username})")

    # Get or create session
    session, created = await state_manager.get_or_create_session(update, context)

    # Check if user is in registration flow
    from apps.telegram.models import TelegramSession
    if session.state in [TelegramSession.State.AWAITING_EMAIL,
                         TelegramSession.State.AWAITING_NAME,
                         TelegramSession.State.AWAITING_CONFIRMATION]:
        # Handle registration flow
        registration_complete = await state_manager.handle_registration_flow(update, context, session)
        if registration_complete:
            return ConversationHandler.END
        return

    # If not in registration flow, check if user is registered
    if not session.user:
        # User is not registered, prompt for registration
        await update.message.reply_text(
            "👋 *Welcome to People for Peace!*\n\n"
            "It looks like you're not registered yet.\n"
            "Please use `/start` to begin registration and create your account.",
            parse_mode='Markdown'
        )
        return

    # User is registered but sent a regular text message
    # Provide helpful response
    await update.message.reply_text(
        "🤔 *Not sure what to do?*\n\n"
        "Here are some things you can try:\n\n"
        "• Use `/campaigns` to browse available campaigns\n"
        "• Use `/tasks` to see available tasks\n"
        "• Use `/mytasks` to view your assigned tasks\n"
        "• Use `/profile` to see your profile and points\n"
        "• Use `/leaderboard` to see top volunteers\n"
        "• Use `/help` for a full list of commands\n\n"
        "Or simply use the menu buttons if they're visible!",
        parse_mode='Markdown'
    )


@error_handler
async def handle_unknown_command(update: Update, context: CallbackContext):
    """Handle unknown commands."""
    await update.message.reply_text(
        "❓ *Unknown command.*\n\n"
        "Use `/help` to see all available commands.",
        parse_mode='Markdown'
    )


async def cancel_registration(update: Update, context: CallbackContext):
    """Cancel registration flow."""
    user = update.effective_user

    try:
        from apps.telegram.models import TelegramSession
        session = TelegramSession.objects.get(telegram_id=user.id)
        session.update_state(TelegramSession.State.IDLE)
        session.temp_data = {}
    except TelegramSession.DoesNotExist:
        pass

    # Clear context data
    context.user_data.clear()

    await update.message.reply_text(
        "❌ Registration cancelled.\n"
        "You can start over with `/start` when you're ready.",
        parse_mode='Markdown'
    )
    return ConversationHandler.END


# Conversation handler for registration
registration_conversation = ConversationHandler(
    entry_points=[],  # Started from start_command when user not found
    states={
        # States are handled by handle_text_message based on session state
    },
    fallbacks=[
        MessageHandler(filters.COMMAND, cancel_registration)
    ],
    allow_reentry=True
)

# Handler for general text messages
text_message_handler = MessageHandler(
    filters.TEXT & ~filters.COMMAND,
    handle_text_message
)

# Handler for unknown commands
unknown_command_handler = MessageHandler(
    filters.COMMAND,
    handle_unknown_command
)
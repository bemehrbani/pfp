"""
Menu callback handler for inline button navigation.
Routes `menu_*` callback queries to the appropriate command handlers.
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from utils.translations import get_main_menu_inline, t
from utils.state_management import state_manager

logger = logging.getLogger(__name__)


async def _get_user_lang(update: Update, context: CallbackContext) -> str:
    """Helper to get the current user's language from their session."""
    from asgiref.sync import sync_to_async

    session, _ = await state_manager.get_or_create_session(update, context)

    @sync_to_async
    def _read_lang(s):
        s.refresh_from_db(fields=['language'])
        return s.language or 'en'

    return await _read_lang(session)


async def menu_callback_handler(update: Update, context: CallbackContext):
    """Route inline menu button presses to the appropriate handlers."""
    query = update.callback_query
    await query.answer()

    action = query.data  # e.g. "menu_campaigns"

    if action == 'menu_main':
        # Re-send the main menu
        lang = await _get_user_lang(update, context)
        await query.message.reply_text(
            t('welcome', lang),
            reply_markup=get_main_menu_inline(lang),
            parse_mode='Markdown',
        )
        return

    if action == 'menu_campaigns':
        from handlers.campaigns import campaigns_command
        await campaigns_command(update, context)
    elif action == 'menu_tasks':
        from handlers.tasks import tasks_command
        await tasks_command(update, context)
    elif action == 'menu_profile':
        from handlers.profile import profile_command
        await profile_command(update, context)
    elif action == 'menu_leaderboard':
        from handlers.leaderboard import leaderboard_command
        await leaderboard_command(update, context)
    elif action == 'menu_help':
        from handlers.start import help_command
        await help_command(update, context)
    elif action == 'menu_language':
        from handlers.start import language_command
        await language_command(update, context)
    else:
        logger.warning(f"Unknown menu action: {action}")


# Export handler list for registration in bot.py
menu_handlers = [
    CallbackQueryHandler(menu_callback_handler, pattern=r"^menu_"),
]

"""
Menu callback handler for inline button navigation.
Routes `menu_*` callback queries to the appropriate command handlers.

Since callback queries don't have `update.message`, this handler
responds via `query.message.reply_text()` rather than calling command
handlers directly (which expect `update.message` to exist).
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from utils.translations import get_main_menu_inline, get_back_to_menu_inline, t
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


async def _handle_campaigns(query, lang: str):
    """Show available campaigns via the callback query message."""
    from asgiref.sync import sync_to_async
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    @sync_to_async
    def _fetch_campaigns():
        from apps.campaigns.models import Campaign
        return list(
            Campaign.objects.filter(status=Campaign.Status.ACTIVE)
            .select_related()
            .order_by('-created_at')[:10]
        )

    campaigns = await _fetch_campaigns()

    if not campaigns:
        await query.message.reply_text(
            t('campaigns_none', lang),
            reply_markup=get_back_to_menu_inline(lang),
            parse_mode='Markdown',
        )
        return

    text = t('campaigns_title', lang) + "\n\n"
    buttons = []

    for campaign in campaigns:
        text += f"• *{campaign.name}*\n"
        if campaign.description:
            desc = campaign.description[:80]
            text += f"  {desc}{'...' if len(campaign.description) > 80 else ''}\n"
        text += "\n"
        buttons.append([
            InlineKeyboardButton(
                f"📋 {campaign.name}",
                callback_data=f"campaign_{campaign.id}"
            )
        ])

    # Add back-to-menu button
    label = {'en': '🏠 Main Menu', 'fa': '🏠 منوی اصلی', 'ar': '🏠 القائمة الرئيسية'}
    buttons.append([
        InlineKeyboardButton(label.get(lang, label['en']), callback_data='menu_main')
    ])

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode='Markdown',
    )


async def _handle_tasks(query, lang: str):
    """Show available tasks."""
    from asgiref.sync import sync_to_async
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    @sync_to_async
    def _fetch_tasks():
        from apps.tasks.models import Task
        return list(
            Task.objects.filter(is_active=True, status='open')
            .select_related('campaign')
            .order_by('-created_at')[:10]
        )

    tasks = await _fetch_tasks()

    if not tasks:
        await query.message.reply_text(
            t('tasks_none', lang),
            reply_markup=get_back_to_menu_inline(lang),
            parse_mode='Markdown',
        )
        return

    text = "🎯 *Available Tasks*\n\n"
    for task in tasks:
        campaign_name = task.campaign.name if task.campaign else "General"
        text += f"• *{task.title}* ({campaign_name})\n"

    text += "\nUse /tasks for full details and to claim tasks."

    await query.message.reply_text(
        text,
        reply_markup=get_back_to_menu_inline(lang),
        parse_mode='Markdown',
    )


async def _handle_profile(query, update: Update, context: CallbackContext, lang: str):
    """Show user profile summary."""
    from asgiref.sync import sync_to_async

    session, _ = await state_manager.get_or_create_session(update, context)

    @sync_to_async
    def _read_profile(s):
        s.refresh_from_db()
        user = s.user
        if not user:
            return None
        return {
            'name': user.get_full_name() or user.username,
            'points': getattr(user, 'points', 0),
        }

    profile = await _read_profile(session)
    if not profile:
        await query.message.reply_text(
            "❌ Profile not found. Please /start to register.",
            reply_markup=get_back_to_menu_inline(lang),
        )
        return

    text = (
        f"👤 *Your Profile*\n\n"
        f"• Name: {profile['name']}\n"
        f"• Points: {profile['points']} ⭐\n\n"
        f"Use /profile for full details."
    )
    await query.message.reply_text(
        text,
        reply_markup=get_back_to_menu_inline(lang),
        parse_mode='Markdown',
    )


async def _handle_leaderboard(query, lang: str):
    """Show leaderboard summary."""
    import html as html_mod
    from asgiref.sync import sync_to_async

    @sync_to_async
    def _fetch_top_users():
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return list(
            User.objects.filter(is_active=True)
            .order_by('-total_points')[:5]
        )

    top_users = await _fetch_top_users()

    text = "🏆 <b>Leaderboard — Top 5</b>\n\n"
    medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']

    for idx, user in enumerate(top_users):
        name = html_mod.escape(user.get_full_name() or user.username)
        points = getattr(user, 'total_points', 0) or 0
        text += f"{medals[idx]} {name} — {points} pts\n"

    if not top_users:
        text += "No volunteers yet. Be the first!\n"

    text += "\nUse /leaderboard for the full ranking."

    await query.message.reply_text(
        text,
        reply_markup=get_back_to_menu_inline(lang),
        parse_mode='HTML',
    )


async def _handle_help(query, lang: str):
    """Show help text."""
    await query.message.reply_text(
        t('help', lang),
        reply_markup=get_back_to_menu_inline(lang),
        parse_mode='Markdown',
    )


async def menu_callback_handler(update: Update, context: CallbackContext):
    """Route inline menu button presses to the appropriate handlers."""
    query = update.callback_query
    await query.answer()

    action = query.data  # e.g. "menu_campaigns"
    lang = await _get_user_lang(update, context)

    if action == 'menu_main':
        await query.message.reply_text(
            t('welcome', lang),
            reply_markup=get_main_menu_inline(lang),
            parse_mode='Markdown',
        )
    elif action == 'menu_campaigns':
        await _handle_campaigns(query, lang)
    elif action == 'menu_tasks':
        await _handle_tasks(query, lang)
    elif action == 'menu_profile':
        await _handle_profile(query, update, context, lang)
    elif action == 'menu_leaderboard':
        await _handle_leaderboard(query, lang)
    elif action == 'menu_help':
        await _handle_help(query, lang)
    elif action == 'menu_language':
        # Re-use the existing language picker (it uses InlineKeyboardMarkup already)
        from handlers.start import language_command
        # language_command sends InlineKeyboard via context.bot, works with callback queries
        await query.message.reply_text(
            t('language_prompt', lang),
            reply_markup=_get_language_keyboard(),
            parse_mode='Markdown',
        )
    else:
        logger.warning(f"Unknown menu action: {action}")


def _get_language_keyboard():
    """Build the language selection inline keyboard."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
            InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
        ]
    ])


# Export handler list for registration in bot.py
menu_handlers = [
    CallbackQueryHandler(menu_callback_handler, pattern=r"^menu_"),
]

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

    text = "📋 *Active Campaigns*\n\n"
    text += "Choose a campaign to learn more and join:\n\n"
    buttons = []

    for campaign in campaigns:
        desc = campaign.localized_short_description(lang)
        if desc:
            desc = desc[:80] + ('...' if len(desc) > 80 else '')
        text += f"✊ *{campaign.localized_name(lang)}*\n"
        if desc:
            text += f"  {desc}\n"
        text += f"  👥 {campaign.current_members}/{campaign.target_members} volunteers\n\n"
        buttons.append([
            InlineKeyboardButton(
                f"✊ {campaign.localized_name(lang)}",
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
    """Show available tasks with clickable buttons."""
    from asgiref.sync import sync_to_async
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from handlers.tasks import _get_task_type_icon

    @sync_to_async
    def _fetch_tasks():
        from apps.tasks.models import Task
        return list(
            Task.objects.filter(is_active=True)
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

    text = t('checklist_title', lang).format(name='') + "\n\n"
    keyboard = []

    for task in tasks:
        type_icon = _get_task_type_icon(task.task_type)
        campaign_name = task.campaign.localized_name(lang) if task.campaign else ""
        text += f"• {type_icon} *{task.localized_title(lang)}* ({campaign_name}) — 🏆 {task.points} pts\n"
        keyboard.append([
            InlineKeyboardButton(
                f"{type_icon} {task.localized_title(lang)[:30]}",
                callback_data=f"task_claim_{task.id}"
            )
        ])

    text += "\n" + t('checklist_tap_start', lang)

    keyboard.append([
        InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")
    ])

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
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


async def _handle_invite(query, session, lang: str):
    """Show invite link for user's first joined campaign."""
    from asgiref.sync import sync_to_async

    @sync_to_async
    def _get_first_joined_campaign(user):
        from apps.campaigns.models import CampaignVolunteer
        cv = (
            CampaignVolunteer.objects
            .filter(volunteer=user, status='active')
            .select_related('campaign')
            .first()
        )
        return cv.campaign if cv else None

    if not session.user:
        await query.message.reply_text(
            t('register_need_first', lang),
            reply_markup=get_back_to_menu_inline(lang),
            parse_mode='Markdown',
        )
        return

    campaign = await _get_first_joined_campaign(session.user)
    if not campaign:
        await query.message.reply_text(
            t('campaigns_none', lang),
            reply_markup=get_back_to_menu_inline(lang),
            parse_mode='Markdown',
        )
        return

    # Delegate to existing invite handler
    from handlers.campaigns import handle_invite_link
    await handle_invite_link(query, session, campaign.id)


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
        # Show user's joined campaigns (task-first flow)
        session, _ = await state_manager.get_or_create_session(update, context)
        from handlers.campaigns import show_my_campaigns
        await show_my_campaigns(query, session, lang)
    elif action == 'menu_tasks':
        await _handle_tasks(query, lang)
    elif action == 'menu_invite':
        # Show invite for user's first joined campaign
        session, _ = await state_manager.get_or_create_session(update, context)
        await _handle_invite(query, session, lang)
    elif action == 'menu_help':
        await _handle_help(query, lang)
    elif action == 'menu_language':
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

"""
Twitter Storm command handlers for Telegram bot.

Provides /storms and /storminfo commands for volunteers to see
upcoming storms, countdown, and storm details.

All Django ORM calls wrapped with sync_to_async.
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from asgiref.sync import sync_to_async
from django.utils import timezone

logger = logging.getLogger(__name__)


# ── Async-safe DB helpers ──────────────────────────────────────────────

@sync_to_async
def _db_get_session(telegram_id):
    from apps.telegram.models import TelegramSession
    try:
        return TelegramSession.objects.select_related('user').get(telegram_id=telegram_id)
    except TelegramSession.DoesNotExist:
        return None


@sync_to_async
def _db_get_user_storms(user):
    from apps.campaigns.models import TwitterStorm, CampaignVolunteer

    campaign_ids = list(
        CampaignVolunteer.objects.filter(
            volunteer=user,
            status='active'
        ).values_list('campaign_id', flat=True)
    )

    storms = list(
        TwitterStorm.objects.filter(
            campaign_id__in=campaign_ids,
            status__in=['scheduled', 'countdown', 'active']
        ).order_by('scheduled_at')[:5]
    )
    return storms


@sync_to_async
def _db_get_storm(storm_id):
    from apps.campaigns.models import TwitterStorm
    try:
        return TwitterStorm.objects.get(id=storm_id)
    except TwitterStorm.DoesNotExist:
        return None


@sync_to_async
def _db_get_storm_participants_count(storm):
    return storm.participants.count()


@sync_to_async
def _db_mark_ready(storm_id, user):
    from apps.campaigns.models import StormParticipant
    StormParticipant.objects.update_or_create(
        storm_id=storm_id,
        volunteer=user,
        defaults={'status': 'ready'}
    )


# ── Formatting helpers ─────────────────────────────────────────────────

def _format_countdown(storm) -> str:
    """Format time remaining until storm."""
    now = timezone.now()
    delta = storm.scheduled_at - now

    if delta.total_seconds() <= 0:
        return '🔴 LIVE NOW'

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        return f'{days}d {hours}h'
    elif hours > 0:
        return f'{hours}h {minutes}m'
    else:
        return f'{minutes}m'


# ── Handlers ───────────────────────────────────────────────────────────

async def storms_command(update: Update, context: CallbackContext):
    """Handle /storms command — list upcoming storms for user's campaigns."""
    session = await _db_get_session(update.effective_user.id)
    if not session or not session.user:
        await update.message.reply_text('❌ Please register first with /start')
        return

    storms = await _db_get_user_storms(session.user)

    if not storms:
        await update.message.reply_text(
            '🌊 No upcoming storms.\n\n'
            'Your campaign managers will schedule storms — '
            'you\'ll get a notification when one is coming!'
        )
        return

    lines = ['🌊 <b>Upcoming Storms</b>\n']

    for storm in storms:
        countdown = _format_countdown(storm)
        status_emoji = {
            'scheduled': '⏳',
            'countdown': '🔥',
            'active': '🚀',
        }.get(storm.status, '📋')

        lines.append(
            f'{status_emoji} <b>{storm.title}</b>\n'
            f'   📅 {storm.scheduled_at:%b %d, %H:%M} UTC\n'
            f'   ⏱ {countdown}\n'
            f'   💬 {storm.get_hashtags()}\n'
        )

    keyboard = []
    for storm in storms:
        keyboard.append([
            InlineKeyboardButton(
                f'ℹ️ {storm.title}',
                callback_data=f'storm_info_{storm.id}'
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '\n'.join(lines),
        parse_mode='HTML',
        reply_markup=reply_markup
    )


async def storminfo_command(update: Update, context: CallbackContext):
    """Handle /storminfo <id> command — show detailed storm info."""
    if not context.args:
        await update.message.reply_text('Usage: /storminfo <storm_id>')
        return

    try:
        storm_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text('❌ Invalid storm ID.')
        return

    storm = await _db_get_storm(storm_id)
    if not storm:
        await update.message.reply_text('❌ Storm not found.')
        return

    countdown = _format_countdown(storm)
    participants = await _db_get_storm_participants_count(storm)
    templates = storm.tweet_templates or []
    sample_tweet = templates[0] if templates else 'No tweet template set yet.'

    text = (
        f'🌊 <b>{storm.title}</b>\n'
        f'━━━━━━━━━━━━━━━━━━━\n'
        f'📅 <b>Scheduled:</b> {storm.scheduled_at:%b %d, %Y at %H:%M} UTC\n'
        f'⏱ <b>Countdown:</b> {countdown}\n'
        f'⏳ <b>Duration:</b> {storm.duration_minutes} minutes\n'
        f'👥 <b>Participants:</b> {participants}\n'
        f'━━━━━━━━━━━━━━━━━━━\n\n'
        f'💬 <b>Hashtags:</b> {storm.get_hashtags()}\n'
        f'📢 <b>Mentions:</b> {storm.get_mentions() or "None"}\n\n'
        f'📝 <b>Sample Tweet:</b>\n'
        f'<code>{sample_tweet}</code>\n'
        f'━━━━━━━━━━━━━━━━━━━\n'
        f'🔔 You will receive countdown notifications before the storm!'
    )

    await update.message.reply_text(text, parse_mode='HTML')


async def storm_callback_handler(update: Update, context: CallbackContext):
    """Handle callback queries for storm actions."""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith('storm_info_'):
        storm_id = int(data.replace('storm_info_', ''))
        storm = await _db_get_storm(storm_id)
        if not storm:
            await query.edit_message_text('❌ Storm not found.')
            return

        countdown = _format_countdown(storm)
        templates = storm.tweet_templates or []
        sample_tweet = templates[0] if templates else 'No tweet template set yet.'

        text = (
            f'🌊 <b>{storm.title}</b>\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'📅 {storm.scheduled_at:%b %d, %Y at %H:%M} UTC\n'
            f'⏱ Countdown: {countdown}\n'
            f'⏳ Duration: {storm.duration_minutes} min\n'
            f'👥 Notified: {storm.participants_notified}\n'
            f'━━━━━━━━━━━━━━━━━━━\n\n'
            f'💬 {storm.get_hashtags()}\n\n'
            f'📝 <b>Sample Tweet:</b>\n'
            f'<code>{sample_tweet}</code>'
        )

        await query.edit_message_text(text, parse_mode='HTML')

    elif data.startswith('storm_ready_'):
        storm_id = int(data.replace('storm_ready_', ''))
        session = await _db_get_session(update.effective_user.id)

        if session and session.user:
            await _db_mark_ready(storm_id, session.user)
            await query.edit_message_text('✊ You\'re marked as READY! Stand by for the blast.')
        else:
            await query.edit_message_text('❌ Please register first with /start')


# Handler registration
storm_handlers = [
    CallbackQueryHandler(storm_callback_handler, pattern='^storm_')
]

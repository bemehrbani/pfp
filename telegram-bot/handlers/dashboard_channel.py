"""
Admin commands for the pinned campaign dashboard in the Telegram channel.

  /post_dashboard  — send + pin the dashboard message (first time)
  /refresh_dashboard — manually edit-in-place with fresh stats
"""
import logging
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import CallbackContext

from utils.dashboard import compose_dashboard_message

logger = logging.getLogger(__name__)


# ── DB helpers ─────────────────────────────────────────────────────────

@sync_to_async
def _is_admin(session) -> bool:
    """Check if the session user has admin or campaign_manager role."""
    if not session or not session.user:
        return False
    return session.user.role in ('admin', 'campaign_manager')


@sync_to_async
def _get_first_active_campaign():
    """Get the first active campaign (for single-campaign mode)."""
    from apps.campaigns.models import Campaign
    return Campaign.objects.filter(status=Campaign.Status.ACTIVE).first()


@sync_to_async
def _get_campaign_pulse(campaign_id: int) -> dict:
    """Get community pulse stats for a campaign (sync wrapper)."""
    from apps.tasks.models import TaskAssignment
    from apps.campaigns.models import CampaignVolunteer
    from django.utils import timezone
    from datetime import timedelta

    one_hour_ago = timezone.now() - timedelta(hours=1)

    total_completed = TaskAssignment.objects.filter(
        task__campaign_id=campaign_id,
        status__in=['completed', 'verified'],
    ).count()

    recent_active = TaskAssignment.objects.filter(
        task__campaign_id=campaign_id,
        status__in=['completed', 'verified'],
        completed_at__gte=one_hour_ago,
    ).values('volunteer').distinct().count()

    total_volunteers = CampaignVolunteer.objects.filter(
        campaign_id=campaign_id,
        status='active',
    ).count()

    return {
        'total_completed': total_completed,
        'recent_active': recent_active,
        'total_volunteers': total_volunteers,
    }


@sync_to_async
def _get_campaign_tasks(campaign_id: int) -> list:
    """Get active tasks for a campaign."""
    from apps.tasks.models import Task
    return list(Task.objects.filter(
        campaign_id=campaign_id,
        is_active=True,
        task_type__in=[
            'twitter_post', 'twitter_retweet', 'twitter_comment',
            'content_creation', 'petition', 'mass_email',
        ],
    ).order_by('estimated_time')[:10])


@sync_to_async
def _save_pinned_message_id(campaign, message_id: int):
    """Save the pinned dashboard message ID to the campaign."""
    campaign.pinned_dashboard_message_id = message_id
    campaign.save(update_fields=['pinned_dashboard_message_id'])


@sync_to_async
def _get_or_create_session(telegram_id, telegram_username, chat_id):
    """Get or create TelegramSession (sync, wrapped for async)."""
    from django.contrib.auth import get_user_model
    from apps.telegram.models import TelegramSession
    User = get_user_model()

    try:
        session = TelegramSession.objects.select_related('user').get(
            telegram_id=telegram_id
        )
        return session
    except TelegramSession.DoesNotExist:
        return None


# ── Commands ───────────────────────────────────────────────────────────

async def post_dashboard_command(update: Update, context: CallbackContext):
    """
    /post_dashboard — Send the campaign dashboard to the channel, pin it,
    and store the message ID for future edits.
    """
    user = update.effective_user
    session = await _get_or_create_session(
        user.id, user.username, update.effective_chat.id
    )

    if not await _is_admin(session):
        await update.message.reply_text('⛔ Admin only.')
        return

    campaign = await _get_first_active_campaign()
    if not campaign:
        await update.message.reply_text('❌ No active campaign found.')
        return

    if not campaign.telegram_channel_id:
        await update.message.reply_text(
            '❌ Campaign has no `telegram_channel_id` set.'
        )
        return

    pulse = await _get_campaign_pulse(campaign.id)
    tasks = await _get_campaign_tasks(campaign.id)
    html_text, keyboard = compose_dashboard_message(campaign, pulse, tasks)

    # Send to channel
    sent_msg = await context.bot.send_message(
        chat_id=campaign.telegram_channel_id,
        text=html_text,
        reply_markup=keyboard,
        parse_mode='HTML',
        disable_web_page_preview=True,
    )

    # Pin the message
    try:
        await context.bot.pin_chat_message(
            chat_id=campaign.telegram_channel_id,
            message_id=sent_msg.message_id,
            disable_notification=True,
        )
    except Exception as exc:
        logger.warning(f'Failed to pin dashboard: {exc}')

    # Persist the message ID
    await _save_pinned_message_id(campaign, sent_msg.message_id)

    await update.message.reply_text(
        f'✅ Dashboard posted and pinned (msg ID: {sent_msg.message_id}).'
    )
    logger.info(
        f'Dashboard posted to channel {campaign.telegram_channel_id}, '
        f'msg_id={sent_msg.message_id}'
    )


async def refresh_dashboard_command(update: Update, context: CallbackContext):
    """
    /refresh_dashboard — Edit the pinned dashboard message with fresh stats.
    """
    user = update.effective_user
    session = await _get_or_create_session(
        user.id, user.username, update.effective_chat.id
    )

    if not await _is_admin(session):
        await update.message.reply_text('⛔ Admin only.')
        return

    campaign = await _get_first_active_campaign()
    if not campaign:
        await update.message.reply_text('❌ No active campaign found.')
        return

    if not campaign.pinned_dashboard_message_id:
        await update.message.reply_text(
            '❌ No pinned dashboard yet. Use /post_dashboard first.'
        )
        return

    pulse = await _get_campaign_pulse(campaign.id)
    tasks = await _get_campaign_tasks(campaign.id)
    html_text, keyboard = compose_dashboard_message(campaign, pulse, tasks)

    try:
        await context.bot.edit_message_text(
            chat_id=campaign.telegram_channel_id,
            message_id=campaign.pinned_dashboard_message_id,
            text=html_text,
            reply_markup=keyboard,
            parse_mode='HTML',
            disable_web_page_preview=True,
        )
        await update.message.reply_text('✅ Dashboard refreshed.')
        logger.info(
            f'Dashboard refreshed for campaign {campaign.id}, '
            f'msg_id={campaign.pinned_dashboard_message_id}'
        )
    except Exception as exc:
        logger.error(f'Dashboard refresh failed: {exc}')
        await update.message.reply_text(f'❌ Refresh failed: {exc}')

"""
Celery tasks for the Twitter Storm countdown pipeline.

This module implements the core storm coordination:
- schedule_storm_notifications: Queues countdown tasks with ETA
- send_storm_countdown: Sends T-60m, T-15m, T-5m notifications
- send_storm_blast: The T-zero "POST NOW" message
- collect_storm_results: Post-storm statistics
"""
import logging
import random
from datetime import timedelta

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/sendMessage'


def _send_telegram_message(chat_id: int, text: str, parse_mode: str = 'HTML') -> bool:
    """Send a message via the Telegram Bot API."""
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    if not token:
        logger.error('TELEGRAM_BOT_TOKEN not configured')
        return False

    try:
        response = requests.post(
            TELEGRAM_API_URL.format(token=token),
            json={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': True,
            },
            timeout=10,
        )
        if response.status_code != 200:
            logger.warning(f'Telegram API error for chat {chat_id}: {response.text}')
            return False
        return True
    except requests.RequestException as exc:
        logger.error(f'Failed to send message to {chat_id}: {exc}')
        return False


@shared_task(name='campaigns.schedule_storm_notifications')
def schedule_storm_notifications(storm_id: int):
    """
    Queue countdown notification tasks for a storm.

    Called when a storm transitions to 'scheduled' status.
    Stores Celery task IDs on the storm for possible cancellation.
    """
    from apps.campaigns.models import TwitterStorm

    try:
        storm = TwitterStorm.objects.get(id=storm_id)
    except TwitterStorm.DoesNotExist:
        logger.error(f'Storm {storm_id} not found')
        return

    if storm.status not in ['draft', 'scheduled']:
        logger.warning(f'Storm {storm_id} is {storm.status}, skipping scheduling')
        return

    now = timezone.now()
    t_zero = storm.scheduled_at
    task_ids = []

    # Schedule countdown notifications
    if storm.notify_1h and t_zero - timedelta(hours=1) > now:
        result = send_storm_countdown.apply_async(
            args=[storm_id, '1_hour'],
            eta=t_zero - timedelta(hours=1),
        )
        task_ids.append(result.id)
        logger.info(f'Storm {storm_id}: T-60m notification queued')

    if storm.notify_15m and t_zero - timedelta(minutes=15) > now:
        result = send_storm_countdown.apply_async(
            args=[storm_id, '15_min'],
            eta=t_zero - timedelta(minutes=15),
        )
        task_ids.append(result.id)
        logger.info(f'Storm {storm_id}: T-15m notification queued')

    if storm.notify_5m and t_zero - timedelta(minutes=5) > now:
        result = send_storm_countdown.apply_async(
            args=[storm_id, '5_min'],
            eta=t_zero - timedelta(minutes=5),
        )
        task_ids.append(result.id)
        logger.info(f'Storm {storm_id}: T-5m notification queued')

    # Schedule the T-zero blast
    if t_zero > now:
        result = send_storm_blast.apply_async(
            args=[storm_id],
            eta=t_zero,
        )
        task_ids.append(result.id)
        logger.info(f'Storm {storm_id}: T-zero blast queued for {t_zero}')

    # Schedule post-storm stats collection
    result = collect_storm_results.apply_async(
        args=[storm_id],
        eta=t_zero + timedelta(minutes=storm.duration_minutes),
    )
    task_ids.append(result.id)

    # Save task IDs and update status
    storm.celery_task_ids = task_ids
    storm.status = TwitterStorm.Status.SCHEDULED
    storm.save(update_fields=['celery_task_ids', 'status', 'updated_at'])

    logger.info(f'Storm {storm_id}: {len(task_ids)} tasks scheduled')


@shared_task(name='campaigns.send_storm_countdown')
def send_storm_countdown(storm_id: int, countdown_type: str):
    """
    Send countdown notification to all campaign volunteers.

    countdown_type: '1_hour', '15_min', '5_min'
    """
    from apps.campaigns.models import TwitterStorm

    try:
        storm = TwitterStorm.objects.get(id=storm_id)
    except TwitterStorm.DoesNotExist:
        logger.error(f'Storm {storm_id} not found')
        return

    if storm.status == 'cancelled':
        logger.info(f'Storm {storm_id} cancelled, skipping countdown')
        return

    # Update status to countdown on first notification
    if storm.status == 'scheduled':
        storm.status = TwitterStorm.Status.COUNTDOWN
        storm.save(update_fields=['status', 'updated_at'])

    chat_ids = storm.get_volunteer_chat_ids()
    hashtags = storm.get_hashtags()
    time_left = storm.scheduled_at - timezone.now()
    minutes_left = max(1, int(time_left.total_seconds() / 60))

    # Build countdown message
    messages = {
        '1_hour': (
            f'⏰ <b>Storm Alert!</b>\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'🌊 <b>{storm.title}</b> starts in <b>1 HOUR</b>\n'
            f'📅 {storm.scheduled_at:%H:%M UTC}\n'
            f'💬 {hashtags}\n\n'
            f'Get your tweet ready! 📝'
        ),
        '15_min': (
            f'🔥 <b>15 MINUTES!</b>\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'🌊 <b>{storm.title}</b>\n'
            f'{len(chat_ids)} volunteers are standing by 🫡\n\n'
            f'💬 {hashtags}\n'
            f'📋 Prepare your tweet now!'
        ),
        '5_min': (
            f'⚡ <b>5 MINUTES! GET READY!</b>\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'🌊 <b>{storm.title}</b>\n\n'
            f'{len(chat_ids)} volunteers ready to post! 🫡\n\n'
            f'💬 {hashtags}\n'
            f'🐦 Open Twitter NOW and prepare to post!'
        ),
    }

    text = messages.get(countdown_type, f'Storm {storm.title} in {minutes_left} minutes!')

    sent_count = 0
    for chat_id in chat_ids:
        if _send_telegram_message(chat_id, text):
            sent_count += 1

    storm.participants_notified = max(storm.participants_notified, sent_count)
    storm.save(update_fields=['participants_notified', 'updated_at'])

    logger.info(f'Storm {storm_id}: {countdown_type} sent to {sent_count}/{len(chat_ids)} volunteers')


@shared_task(name='campaigns.send_storm_blast')
def send_storm_blast(storm_id: int):
    """
    Send the T-zero "POST NOW" blast to all campaign volunteers.

    Each volunteer gets a personalized tweet from the templates.
    """
    from apps.campaigns.models import TwitterStorm, StormParticipant

    try:
        storm = TwitterStorm.objects.get(id=storm_id)
    except TwitterStorm.DoesNotExist:
        logger.error(f'Storm {storm_id} not found')
        return

    if storm.status == 'cancelled':
        logger.info(f'Storm {storm_id} cancelled, skipping blast')
        return

    # Transition to active
    storm.status = TwitterStorm.Status.ACTIVE
    storm.activated_at = timezone.now()
    storm.save(update_fields=['status', 'activated_at', 'updated_at'])

    chat_ids = storm.get_volunteer_chat_ids()
    hashtags = storm.get_hashtags()
    mentions = storm.get_mentions()
    templates = storm.tweet_templates or []

    # Build the blast message with a random tweet template
    for chat_id in chat_ids:
        tweet = random.choice(templates) if templates else (
            f'We demand peace NOW! {hashtags} {mentions}'
        )

        text = (
            f'🚀 <b>POST NOW!</b> 🚀\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'🌊🌊🌊 THE STORM HAS BEGUN! 🌊🌊🌊\n\n'
            f'<b>Your tweet:</b>\n'
            f'<code>{tweet}</code>\n\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'📋 Copy the tweet above\n'
            f'🐦 Open Twitter → Post it NOW\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'{len(chat_ids)} people are posting <b>RIGHT NOW!</b>'
        )

        _send_telegram_message(chat_id, text)

    storm.participants_notified = len(chat_ids)
    storm.save(update_fields=['participants_notified', 'updated_at'])

    logger.info(f'Storm {storm_id}: BLAST sent to {len(chat_ids)} volunteers')


@shared_task(name='campaigns.collect_storm_results')
def collect_storm_results(storm_id: int):
    """
    Collect and finalize storm results after the storm window closes.
    """
    from apps.campaigns.models import TwitterStorm, StormParticipant

    try:
        storm = TwitterStorm.objects.get(id=storm_id)
    except TwitterStorm.DoesNotExist:
        logger.error(f'Storm {storm_id} not found')
        return

    if storm.status == 'cancelled':
        return

    # Count actual posts
    posted_count = StormParticipant.objects.filter(
        storm=storm,
        status__in=['posted', 'verified']
    ).count()

    storm.tweets_posted = posted_count
    storm.status = TwitterStorm.Status.COMPLETED
    storm.completed_at = timezone.now()
    storm.save(update_fields=['tweets_posted', 'status', 'completed_at', 'updated_at'])

    # Send results to volunteers
    chat_ids = storm.get_volunteer_chat_ids()
    text = (
        f'📊 <b>Storm Results!</b>\n'
        f'━━━━━━━━━━━━━━━━━━━\n'
        f'🌊 <b>{storm.title}</b>\n\n'
        f'👥 Volunteers notified: {storm.participants_notified}\n'
        f'🐦 Tweets posted: {storm.tweets_posted}\n'
        f'━━━━━━━━━━━━━━━━━━━\n'
        f'Thank you for standing for peace! ✊🏼'
    )

    for chat_id in chat_ids:
        _send_telegram_message(chat_id, text)

    logger.info(f'Storm {storm_id}: COMPLETED — {posted_count} tweets posted')

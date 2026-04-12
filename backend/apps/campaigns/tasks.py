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
from django.db import models
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


# ── Channel Broadcasting Tasks ────────────────────────────────────────

@shared_task(name='campaigns.broadcast_task_completion')
def broadcast_task_completion(campaign_id: int, task_title: str, task_type: str, points: int, proof_url: str = ''):
    """
    Broadcast an anonymized task completion to the campaign's Telegram channel.

    Posts: "A volunteer just tweeted for #IstandwithIran! 🐦"
    """
    from apps.campaigns.models import Campaign

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        logger.error(f'Campaign {campaign_id} not found for broadcast')
        return

    channel_id = campaign.telegram_channel_id
    if not channel_id:
        logger.warning(f'No telegram_channel_id set for campaign {campaign_id} — skipping task completion broadcast')
        return

    # Task type icons
    type_icons = {
        'twitter_post': '🐦', 'twitter_retweet': '🔁', 'twitter_comment': '💬',
        'twitter_like': '❤️', 'telegram_share': '📢', 'telegram_invite': '👥',
        'content_creation': '✍️', 'petition': '✍️', 'mass_email': '📧',
        'research': '🔍', 'other': '📌',
    }
    type_labels = {
        'twitter_post': 'tweeted', 'twitter_retweet': 'retweeted',
        'twitter_comment': 'commented on a tweet', 'twitter_like': 'liked a tweet',
        'telegram_share': 'shared on Telegram', 'telegram_invite': 'invited a friend',
        'content_creation': 'created content', 'petition': 'signed the petition',
        'mass_email': 'sent emails', 'research': 'submitted research',
        'other': 'completed a task',
    }

    icon = type_icons.get(task_type, '📌')
    action = type_labels.get(task_type, 'completed a task')

    # Campaign progress
    total_completed = campaign.completed_activities
    total_target = campaign.target_activities or '∞'
    hashtags = campaign.twitter_hashtags or ''

    text = (
        f'🕊️ <b>People for Peace</b>\n'
        f'━━━━━━━━━━━━━━━━━━━\n'
        f'{icon} <b>A volunteer just {action}!</b>\n'
    )

    if proof_url and proof_url.startswith('http'):
        text += f'🔗 <a href="{proof_url}">View</a>\n'

    text += f'🏆 +{points} points earned\n'
    text += f'📊 Progress: {total_completed}/{total_target} activities\n'

    if hashtags:
        text += f'💬 {hashtags}\n'

    text += f'\n✊ Join: @peopleforpeacebot'

    _send_telegram_message(channel_id, text)
    logger.info(f'Channel broadcast: task completion for campaign {campaign_id}')


@shared_task(name='campaigns.broadcast_volunteer_joined')
def broadcast_volunteer_joined(campaign_id: int):
    """
    Broadcast an anonymized volunteer join to the campaign's Telegram channel.
    """
    from apps.campaigns.models import Campaign

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        logger.error(f'Campaign {campaign_id} not found for broadcast')
        return

    channel_id = campaign.telegram_channel_id
    if not channel_id:
        logger.warning(f'No telegram_channel_id set for campaign {campaign_id} — skipping volunteer join broadcast')
        return

    count = campaign.current_members
    target = campaign.target_members or '∞'

    text = (
        f'🕊️ <b>People for Peace</b>\n'
        f'━━━━━━━━━━━━━━━━━━━\n'
        f'👋 <b>A new activist joined the movement!</b>\n'
        f'We are now <b>{count}</b> strong! (Target: {target})\n'
        f'\n✊ Join: @peopleforpeacebot'
    )

    _send_telegram_message(channel_id, text)
    logger.info(f'Channel broadcast: volunteer joined campaign {campaign_id} (now {count})')


@shared_task(name='campaigns.broadcast_campaign_update')
def broadcast_campaign_update(update_id: int):
    """
    Push a CampaignUpdate to the campaign's Telegram channel.
    Called from Django admin action.
    """
    from apps.campaigns.models import CampaignUpdate

    try:
        campaign_update = CampaignUpdate.objects.select_related('campaign').get(id=update_id)
    except CampaignUpdate.DoesNotExist:
        logger.error(f'CampaignUpdate {update_id} not found')
        return

    channel_id = campaign_update.campaign.telegram_channel_id
    if not channel_id:
        logger.warning(f'Campaign {campaign_update.campaign.id} has no channel_id')
        return

    text = (
        f'🕊️ <b>People for Peace</b>\n'
        f'━━━━━━━━━━━━━━━━━━━\n'
        f'📢 <b>{campaign_update.title}</b>\n\n'
        f'{campaign_update.content}\n'
        f'\n✊ Join: @peopleforpeacebot'
    )

    if _send_telegram_message(channel_id, text):
        campaign_update.sent_to_telegram = True
        campaign_update.save(update_fields=['sent_to_telegram'])

    logger.info(f'Channel broadcast: campaign update "{campaign_update.title}"')


@shared_task(name='campaigns.broadcast_milestone')
def broadcast_milestone(campaign_id: int, metric: str, current: int, target: int, percentage: int):
    """
    Broadcast a milestone achievement to the campaign's Telegram channel.

    metric: 'activities', 'members', 'twitter_posts'
    """
    from apps.campaigns.models import Campaign

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return

    channel_id = campaign.telegram_channel_id
    if not channel_id:
        logger.warning(f'No telegram_channel_id set for campaign {campaign_id} — skipping milestone broadcast')
        return

    metric_labels = {
        'activities': '🎯 activities',
        'members': '👥 volunteer',
        'twitter_posts': '🐦 tweet',
    }
    label = metric_labels.get(metric, metric)

    text = (
        f'🕊️ <b>People for Peace</b>\n'
        f'━━━━━━━━━━━━━━━━━━━\n'
        f'🎉 <b>MILESTONE REACHED!</b>\n\n'
        f'{percentage}% of our {label} goal!\n'
        f'<b>{current}/{target}</b>\n\n'
        f'Keep going! Every action counts! ✊\n'
        f'\n✊ Join: @peopleforpeacebot'
    )

    _send_telegram_message(channel_id, text)
    logger.info(f'Channel broadcast: milestone {percentage}% for {metric} in campaign {campaign_id}')


# ── Push Notifications for New Tasks ──────────────────────────────────

# Notification message templates per language (matches translations.py keys)
_NEW_TASK_TEMPLATES = {
    'en': (
        '📬 <b>New Task Available!</b>\n\n'
        '{icon} <b>{title}</b>\n'
        '⭐ {points} points · ⏱ {time} min\n\n'
        'Tap below to start 👇'
    ),
    'fa': (
        '📬 <b>تسک جدید موجود است!</b>\n\n'
        '{icon} <b>{title}</b>\n'
        '⭐ {points} امتیاز · ⏱ {time} دقیقه\n\n'
        'برای شروع دکمه زیر رو بزنید 👇'
    ),
    'ar': (
        '📬 <b>مهمة جديدة متاحة!</b>\n\n'
        '{icon} <b>{title}</b>\n'
        '⭐ {points} نقطة · ⏱ {time} دقيقة\n\n'
        'اضغط أدناه للبدء 👇'
    ),
}

_TASK_TYPE_ICONS = {
    'twitter_post': '🐦', 'twitter_retweet': '🔁',
    'twitter_comment': '💬', 'twitter_like': '❤️',
    'telegram_share': '📢', 'telegram_invite': '👥',
    'content_creation': '✍️', 'petition': '✍️',
    'mass_email': '📧', 'research': '🔍', 'other': '📌',
}


def _send_telegram_message_with_button(
    chat_id: int, text: str, button_text: str, button_url: str, parse_mode: str = 'HTML',
) -> bool:
    """Send a Telegram message with a single inline-keyboard button."""
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
                'reply_markup': {
                    'inline_keyboard': [[{
                        'text': button_text,
                        'url': button_url,
                    }]]
                },
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


@shared_task(name='campaigns.notify_new_task')
def notify_new_task(task_id: int):
    """
    Send push notification to all campaign volunteers about a new task.

    Each volunteer receives a localized message with a deep-link button
    to start the task directly in the bot.
    """
    from apps.tasks.models import Task
    from django.core.cache import cache

    # De-duplicate: prevent re-sends if the signal fires multiple times
    cache_key = f'new_task_notified_{task_id}'
    if cache.get(cache_key):
        logger.info(f'Task {task_id} already notified — skipping')
        return
    cache.set(cache_key, True, timeout=3600)

    try:
        task = Task.objects.select_related('campaign').get(id=task_id)
    except Task.DoesNotExist:
        logger.error(f'Task {task_id} not found for notification')
        return

    if not task.is_active:
        logger.info(f'Task {task_id} is inactive — no notification')
        return

    campaign = task.campaign
    sessions = campaign.get_volunteer_sessions()
    icon = _TASK_TYPE_ICONS.get(task.task_type, '📌')

    # Deep-link URL: opens bot → navigates to campaign tasks
    deep_link = f'https://t.me/peopleforpeacebot?start=campaign_{campaign.id}'

    # Button text per language
    button_labels = {
        'en': '▶️ Start Now',
        'fa': '▶️ شروع',
        'ar': '▶️ ابدأ الآن',
    }

    sent_count = 0
    for session in sessions:
        lang = session.get('language', 'en') or 'en'
        if lang not in _NEW_TASK_TEMPLATES:
            lang = 'en'

        title = task.localized_title(lang)
        template = _NEW_TASK_TEMPLATES[lang]
        text = template.format(
            icon=icon,
            title=title,
            points=task.points,
            time=task.estimated_time,
        )
        button_text = button_labels.get(lang, button_labels['en'])

        if _send_telegram_message_with_button(
            chat_id=session['telegram_chat_id'],
            text=text,
            button_text=button_text,
            button_url=deep_link,
        ):
            sent_count += 1

    logger.info(f'New task notification sent to {sent_count}/{len(sessions)} volunteers for task {task_id}')

    # Also broadcast to the campaign's Telegram channel
    channel_id = campaign.telegram_channel_id
    if channel_id:
        channel_text = (
            f'📬 New task: <b>{task.title}</b> '
            f'({task.points} pts · {task.estimated_time} min)\n\n'
            f'✊ Start → @peopleforpeacebot'
        )
        _send_telegram_message(channel_id, channel_text)
        logger.info(f'Channel broadcast: new task for campaign {campaign.id}')


def _store_channel_post(campaign_id: int, content_type: str, message_text: str, proof_url: str = ''):
    """Store a channel post record for recycling."""
    from apps.campaigns.models import ChannelPost
    ChannelPost.objects.create(
        campaign_id=campaign_id,
        content_type=content_type,
        message_text=message_text,
        proof_url=proof_url,
    )


@shared_task(name='campaigns.recycle_channel_content')
def recycle_channel_content():
    """
    Reshare older high-value channel posts every 8 hours.
    Picks a random task_completion post that hasn't been reposted in 48h.
    """
    from apps.campaigns.models import Campaign, ChannelPost

    cutoff = timezone.now() - timedelta(hours=48)

    active_campaigns = Campaign.objects.filter(
        status=Campaign.Status.ACTIVE
    ).exclude(telegram_channel_id='').exclude(telegram_channel_id__isnull=True)

    for campaign in active_campaigns:
        # Find posts eligible for recycling
        eligible_posts = ChannelPost.objects.filter(
            campaign=campaign,
            content_type='task_completion',
        ).filter(
            models.Q(last_reposted_at__isnull=True) | models.Q(last_reposted_at__lt=cutoff)
        ).order_by('?')[:1]

        post = eligible_posts.first()
        if not post:
            continue

        text = (
            f'🔄 <b>Flashback</b>\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'{post.message_text}\n'
            f'\n✊ <b>{campaign.name}</b>'
        )

        if _send_telegram_message(campaign.telegram_channel_id, text):
            post.repost_count += 1
            post.last_reposted_at = timezone.now()
            post.save(update_fields=['repost_count', 'last_reposted_at'])
            logger.info(f'Recycled post {post.id} for campaign {campaign.id}')


@shared_task(name='campaigns.send_daily_digest')
def send_daily_digest():
    """
    Post a daily campaign summary to each active campaign's Telegram channel.
    Runs at 21:00 UTC daily via Celery Beat.
    """
    from apps.campaigns.models import Campaign, CampaignVolunteer
    from apps.tasks.models import TaskAssignment

    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    active_campaigns = Campaign.objects.filter(
        status=Campaign.Status.ACTIVE
    ).exclude(telegram_channel_id='').exclude(telegram_channel_id__isnull=True)

    for campaign in active_campaigns:
        # Today's statistics
        today_completions = TaskAssignment.objects.filter(
            task__campaign=campaign,
            status__in=['completed', 'verified'],
            completed_at__gte=today_start
        ).count()

        today_new_volunteers = CampaignVolunteer.objects.filter(
            campaign=campaign,
            joined_at__gte=today_start
        ).count()

        total_volunteers = campaign.current_members
        total_completed = campaign.completed_activities
        total_target = campaign.target_activities or '∞'

        # Progress bar (10 segments)
        if campaign.target_activities and campaign.target_activities > 0:
            filled = min(10, int((total_completed / campaign.target_activities) * 10))
        else:
            filled = 0
        bar = '█' * filled + '░' * (10 - filled)

        text = (
            f'📊 <b>Daily Report</b>\n'
            f'━━━━━━━━━━━━━━━━━━━\n'
            f'🎯 Tasks completed today: <b>{today_completions}</b>\n'
            f'👋 New volunteers today: <b>{today_new_volunteers}</b>\n'
            f'👥 Total team: <b>{total_volunteers}</b>\n'
            f'\n'
            f'📈 Progress: [{bar}] {total_completed}/{total_target}\n'
            f'\n✊ <b>{campaign.name}</b>'
        )

        if _send_telegram_message(campaign.telegram_channel_id, text):
            _store_channel_post(campaign.id, 'digest', text)
            logger.info(f'Daily digest sent for campaign {campaign.id}')


# ── Pinned Dashboard Refresh Task ─────────────────────────────────────

@shared_task(name='campaigns.update_campaign_dashboards')
def update_campaign_dashboards():
    """
    Hourly task: edit the pinned campaign dashboard in-place with fresh stats.

    Uses the raw Telegram HTTP API (editMessageText) since Celery tasks
    don't have access to the python-telegram-bot Application instance.
    """
    from apps.campaigns.models import Campaign

    active_campaigns = Campaign.objects.filter(
        status=Campaign.Status.ACTIVE,
        pinned_dashboard_message_id__isnull=False,
    ).exclude(telegram_channel_id__isnull=True)

    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    if not token:
        logger.error('TELEGRAM_BOT_TOKEN not configured — cannot refresh dashboards')
        return

    for campaign in active_campaigns:
        try:
            _refresh_single_dashboard(campaign, token)
            logger.info(f'Dashboard refreshed for campaign {campaign.id}')
        except Exception as exc:
            logger.error(f'Dashboard refresh failed for campaign {campaign.id}: {exc}')


def _render_progress_bar_celery(current: int, target: int, width: int = 10) -> str:
    """Render a Unicode progress bar (Celery-side, no bot dependencies)."""
    if target <= 0:
        return '░' * width + f'  {current}/—'
    ratio = min(current / target, 1.0)
    filled = round(ratio * width)
    empty = width - filled
    return '█' * filled + '░' * empty + f'  {current}/{target}'


def _esc_html(text: str) -> str:
    """Escape HTML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _refresh_single_dashboard(campaign, token: str):
    """Compose and edit the pinned dashboard for one campaign."""
    from apps.tasks.models import Task, TaskAssignment
    from datetime import datetime, timezone as tz

    now = datetime.now(tz.utc)
    timestamp = now.strftime('%I:%M %p · %b %d, %Y')

    # ── Gather stats ──
    total_completed = TaskAssignment.objects.filter(
        task__campaign=campaign,
        status__in=['completed', 'verified'],
    ).count()

    tasks = list(Task.objects.filter(
        campaign=campaign, is_active=True,
        task_type__in=[
            'twitter_post', 'twitter_retweet', 'twitter_comment',
            'content_creation', 'petition', 'mass_email',
        ],
    ).order_by('estimated_time')[:10])

    type_icons = {
        'twitter_post': '🐦', 'twitter_retweet': '🔁',
        'twitter_comment': '💬', 'content_creation': '✍️',
        'petition': '✍️', 'mass_email': '📧',
        'research': '🔍', 'other': '📌',
    }

    # ── Compose HTML ──
    vbar = _render_progress_bar_celery(campaign.current_members, campaign.target_members)
    abar = _render_progress_bar_celery(total_completed, campaign.target_activities)
    tbar = _render_progress_bar_celery(campaign.completed_twitter_posts, campaign.target_twitter_posts)

    progress = campaign.progress_percentage()

    lines = [
        '🕊️ <b>People for Peace</b>',
        '━━━━━━━━━━━━━━━━━━━',
        '',
        f'📢 <b>{_esc_html(campaign.name)}</b>',
        '',
        _esc_html(campaign.short_description),
        '',
        '━━━━━━━━━━━━━━━━━━━',
        '📊 <b>Objectives &amp; Key Results</b>',
        '━━━━━━━━━━━━━━━━━━━',
        '',
        f'🎯 Volunteers:  <code>{vbar}</code>',
        f'📝 Actions:     <code>{abar}</code>',
        f'🐦 Tweets:      <code>{tbar}</code>',
        '',
        f'📈 Overall progress: <b>{progress:.0f}%</b>',
        '',
        '━━━━━━━━━━━━━━━━━━━',
        '🎯 <b>Available Tasks</b>',
        '━━━━━━━━━━━━━━━━━━━',
        '',
    ]

    for task in tasks:
        icon = type_icons.get(task.task_type, '📌')
        lines.append(f'{icon} {_esc_html(task.title)}  ({task.estimated_time} min)')

    lines.extend([
        '',
        '━━━━━━━━━━━━━━━━━━━',
        '🔗 <b>Resources</b>',
        '🕯 <a href="https://peopleforpeace.live">Memorial</a>'
        ' · 📄 <a href="https://peopleforpeace.live/evidence.html">Evidence</a>'
        ' · 📊 <a href="https://peopleforpeace.live/data.html">Data</a>',
        '',
        '🕊️ <b>People for Peace</b> · <a href="https://peopleforpeace.live">peopleforpeace.live</a>',
        f'🔄 Last updated: {timestamp}',
    ])

    html_text = '\n'.join(lines)

    # ── Edit via HTTP API ──
    deep_link = f'https://t.me/peopleforpeacebot?start=campaign_{campaign.id}'
    inline_keyboard = {
        'inline_keyboard': [[{
            'text': '➕ Join the Campaign',
            'url': deep_link,
        }]]
    }

    response = requests.post(
        f'https://api.telegram.org/bot{token}/editMessageText',
        json={
            'chat_id': campaign.telegram_channel_id,
            'message_id': campaign.pinned_dashboard_message_id,
            'text': html_text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True,
            'reply_markup': inline_keyboard,
        },
        timeout=15,
    )

    if response.status_code != 200:
        resp_data = {}
        try:
            resp_data = response.json()
        except Exception:
            pass
        # "message is not modified" is fine — nothing changed since last refresh
        if 'message is not modified' in resp_data.get('description', ''):
            logger.info(f'Dashboard for campaign {campaign.id}: no changes to update')
        else:
            logger.warning(f'editMessageText failed for campaign {campaign.id}: {response.text}')

@shared_task
def fetch_global_protests():
    """
    Task to fetch global protests from various scrapers and save them to the database.
    Runs periodically via Celery Beat.
    """
    from .scrapers.google_news_rss import GoogleNewsProtestScraper
    from .scrapers.world_beyond_war import WorldBeyondWarScraper
    
    logger.info("Starting global protest fetch...")
    
    scrapers = [
        GoogleNewsProtestScraper(),
        WorldBeyondWarScraper()
    ]
    
    total_new = 0
    total_updated = 0
    
    for scraper in scrapers:
        new_count, updated_count = scraper.fetch_and_save()
        total_new += new_count
        total_updated += updated_count
        
    logger.info(f"Finished global protest fetch. New: {total_new}, Updated: {total_updated}")
    return {"new": total_new, "updated": total_updated}

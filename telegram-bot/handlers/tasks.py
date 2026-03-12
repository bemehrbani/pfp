"""
Task command handlers for Telegram bot.
All Django ORM calls wrapped with sync_to_async.
"""
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, ConversationHandler,
    MessageHandler, filters, CommandHandler
)
from asgiref.sync import sync_to_async

from utils.state_management import state_manager
from utils.translations import t

logger = logging.getLogger(__name__)

# ── Level titles for gamification ──────────────────────────────────────
LEVEL_TITLES = {
    1: '🕊️ Peace Seeker',
    2: '✊ Voice of Justice',
    3: '📢 Movement Builder',
    4: '🔥 Campaign Warrior',
    5: '🌍 Peace Champion',
}


def get_level_title(level: int) -> str:
    """Return the activist rank name for a given level."""
    if level >= 5:
        return LEVEL_TITLES[5]
    return LEVEL_TITLES.get(level, LEVEL_TITLES[1])

# Conversation states for task completion
AWAITING_TASK_PROOF = 1
AWAITING_CONFIRMATION = 2


# ── Async-safe DB helpers ──────────────────────────────────────────────

@sync_to_async
def _db_get_or_create_session(telegram_id, telegram_username, telegram_chat_id):
    from apps.telegram.models import TelegramSession
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        session = TelegramSession.objects.select_related('user').get(telegram_id=telegram_id)
        session.telegram_username = telegram_username
        session.telegram_chat_id = telegram_chat_id
        update_fields = ['telegram_username', 'telegram_chat_id', 'updated_at']

        # Auto-repair: link orphaned session to existing user
        if not session.user:
            try:
                db_user = User.objects.get(telegram_id=telegram_id)
                session.user = db_user
                update_fields.append('user')
            except User.DoesNotExist:
                pass

        session.save(update_fields=update_fields)
        return session, False
    except TelegramSession.DoesNotExist:
        db_user = None
        try:
            db_user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            pass
        session = TelegramSession.objects.create(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            telegram_chat_id=telegram_chat_id,
            user=db_user
        )
        return session, True


@sync_to_async
def _db_record_command(session, cmd):
    session.record_command(cmd)


@sync_to_async
def _db_get_available_tasks(user):
    from apps.campaigns.models import Campaign, CampaignVolunteer
    from apps.tasks.models import Task
    from django.db.models import F

    campaign_ids = list(
        CampaignVolunteer.objects.filter(
            volunteer=user,
            campaign__status=Campaign.Status.ACTIVE
        ).values_list('campaign_id', flat=True)
    )
    if not campaign_ids:
        return [], False

    tasks = list(
        Task.objects.filter(
            campaign_id__in=campaign_ids,
        ).exclude(
            assignments__volunteer=user
        ).select_related('campaign').order_by('-points', 'created_at')[:10]
    )
    return tasks, True


@sync_to_async
def _db_get_user_task_status_map(user, campaign_id):
    """Get a dict of {task_id: status} for a user in a campaign."""
    from apps.tasks.models import TaskAssignment
    assignments = TaskAssignment.objects.filter(
        volunteer=user,
        task__campaign_id=campaign_id,
    ).values_list('task_id', 'status')
    return dict(assignments)


@sync_to_async
def _db_get_campaign_pulse(campaign_id):
    """Get community pulse stats for a campaign."""
    from apps.tasks.models import TaskAssignment
    from apps.campaigns.models import CampaignVolunteer
    from django.utils import timezone
    from datetime import timedelta

    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Total completed tasks (all time)
    total_completed = TaskAssignment.objects.filter(
        task__campaign_id=campaign_id,
        status__in=['completed', 'verified'],
    ).count()

    # Active in last hour
    recent_active = TaskAssignment.objects.filter(
        task__campaign_id=campaign_id,
        status__in=['completed', 'verified'],
        completed_at__gte=one_hour_ago,
    ).values('volunteer').distinct().count()

    # Total volunteers
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
def _db_get_user_rank(user, campaign_id):
    """Get user's rank percentile within a campaign."""
    from apps.campaigns.models import CampaignVolunteer

    volunteers = list(
        CampaignVolunteer.objects.filter(
            campaign_id=campaign_id,
            status='active',
        ).order_by('-points_earned').values_list('volunteer_id', 'points_earned')
    )
    if not volunteers:
        return None

    total = len(volunteers)
    rank = next(
        (i + 1 for i, (vid, _) in enumerate(volunteers) if vid == user.id),
        None
    )
    if rank is None:
        return None
    return max(1, int((1 - rank / total) * 100))


@sync_to_async
def _db_get_user_assignments(user):
    from apps.tasks.models import TaskAssignment
    return list(
        TaskAssignment.objects.filter(
            volunteer=user,
            status__in=['assigned', 'in_progress']
        ).select_related('task', 'task__campaign').order_by('created_at')
    )


@sync_to_async
def _db_get_task(task_id):
    from apps.tasks.models import Task
    try:
        return Task.objects.select_related('campaign').get(id=task_id)
    except Task.DoesNotExist:
        return None


@sync_to_async
def _db_validate_and_claim(user, task_id):
    """Validate, claim AND start task in one step. Returns (assignment, error_msg)."""
    from apps.tasks.models import Task, TaskAssignment
    from apps.campaigns.models import CampaignVolunteer

    try:
        task = Task.objects.select_related('campaign').get(id=task_id)
    except Task.DoesNotExist:
        return None, "❌ Task not found."

    if not CampaignVolunteer.objects.filter(campaign=task.campaign, volunteer=user).exists():
        return None, "❌ You need to join this campaign first to claim its tasks."

    existing = TaskAssignment.objects.filter(
        task=task, volunteer=user
    ).select_related('task', 'task__campaign').first()
    if existing:
        return existing, None  # Return existing assignment (already claimed)

    assignment = TaskAssignment.objects.create(
        task=task,
        campaign=task.campaign,
        volunteer=user,
        status='in_progress'  # Skip 'assigned', go straight to 'in_progress'
    )

    # Refetch with select_related so task FK is cached for async access
    assignment = TaskAssignment.objects.select_related(
        'task', 'task__campaign'
    ).get(id=assignment.id)

    return assignment, None


@sync_to_async
def _db_start_assignment(assignment_id, user):
    from apps.tasks.models import TaskAssignment
    try:
        assignment = TaskAssignment.objects.select_related('task').get(
            id=assignment_id,
            volunteer=user,
            status='assigned'
        )
        assignment.status = 'in_progress'
        assignment.save(update_fields=['status'])
        return assignment, None
    except TaskAssignment.DoesNotExist:
        return None, "❌ This task assignment is no longer available."


@sync_to_async
def _db_get_in_progress_assignment(assignment_id, user):
    from apps.tasks.models import TaskAssignment
    try:
        return TaskAssignment.objects.select_related('task').get(
            id=assignment_id,
            volunteer=user,
            status='in_progress'
        )
    except TaskAssignment.DoesNotExist:
        return None


@sync_to_async
def _db_get_session_by_telegram_id(telegram_id):
    from apps.telegram.models import TelegramSession
    try:
        return TelegramSession.objects.select_related('user').get(telegram_id=telegram_id)
    except TelegramSession.DoesNotExist:
        return None


@sync_to_async
def _db_update_session_state(session, state, data=None):
    session.update_state(state, data)


@sync_to_async
def _db_submit_proof(assignment_id, user, proof_type, proof_content):
    from apps.tasks.models import TaskAssignment
    try:
        assignment = TaskAssignment.objects.select_related('task').get(
            id=assignment_id,
            volunteer=user,
            status='in_progress'
        )
        assignment.status = 'completed'
        # Save proof based on type
        if proof_type == 'url':
            assignment.proof_url = proof_content
        elif proof_type == 'text':
            assignment.proof_text = proof_content
        update_fields = ['status', 'proof_url', 'proof_text', 'completed_at']
        from django.utils import timezone
        assignment.completed_at = timezone.now()
        assignment.save(update_fields=update_fields)
        return assignment, None
    except TaskAssignment.DoesNotExist:
        return None, "Task assignment not found or already completed."


@sync_to_async
def _db_get_campaign_channel_id(campaign_id):
    """Get the Telegram channel ID for a campaign."""
    from apps.campaigns.models import Campaign
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        return campaign.telegram_channel_id
    except Campaign.DoesNotExist:
        return None


@sync_to_async
def _db_get_campaign_group_id(campaign_id):
    """Get the Telegram group ID for a campaign."""
    from apps.campaigns.models import Campaign
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        return campaign.telegram_group_id
    except Campaign.DoesNotExist:
        return None


async def _broadcast_task_completion(bot, campaign_id, task_title, task_type, points, proof_url=''):
    """
    Broadcast an anonymized task completion to the campaign's Telegram channel.
    Fire-and-forget: errors are logged but never raised.
    """
    try:
        channel_id = await _db_get_campaign_channel_id(campaign_id)
        if not channel_id:
            return

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

        from utils.brand_constants import BRAND_HEADER_HTML, BRAND_SEPARATOR, BRAND_CTA_HTML

        text = f'{BRAND_HEADER_HTML}\n'
        text += f'{BRAND_SEPARATOR}\n'
        text += f'{icon} <b>A volunteer just {action}!</b>\n'

        if proof_url and proof_url.startswith('http'):
            text += f'🔗 <a href="{proof_url}">View</a>\n'

        text += f'🏆 +{points} points earned\n'
        text += f'\n{BRAND_CTA_HTML}'

        await bot.send_message(
            chat_id=channel_id,
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        logger.info(f'Channel broadcast: task completion for campaign {campaign_id}')
    except Exception as exc:
        logger.warning(f'Channel broadcast failed for campaign {campaign_id}: {exc}')


async def _broadcast_volunteer_joined(bot, campaign_id, member_count):
    """
    Broadcast an anonymized volunteer join to the campaign's Telegram channel.
    Fire-and-forget.
    """
    try:
        channel_id = await _db_get_campaign_channel_id(campaign_id)
        if not channel_id:
            return

        from utils.brand_constants import BRAND_HEADER_HTML, BRAND_SEPARATOR, BRAND_CTA_HTML

        text = (
            f'{BRAND_HEADER_HTML}\n'
            f'{BRAND_SEPARATOR}\n'
            f'👋 <b>A new activist joined the movement!</b>\n'
            f'We are now <b>{member_count}</b> strong! ✊\n'
            f'\n{BRAND_CTA_HTML}'
        )

        await bot.send_message(
            chat_id=channel_id,
            text=text,
            parse_mode='HTML'
        )
        logger.info(f'Channel broadcast: volunteer joined campaign {campaign_id}')
    except Exception as exc:
        logger.warning(f'Channel broadcast (join) failed for campaign {campaign_id}: {exc}')


@sync_to_async
def _db_check_first_completion(user, campaign_id):
    """Check if this is the user's first completed task AND group invite hasn't been sent."""
    from apps.campaigns.models import CampaignVolunteer
    from apps.tasks.models import TaskAssignment

    try:
        cv = CampaignVolunteer.objects.get(campaign_id=campaign_id, volunteer=user)
    except CampaignVolunteer.DoesNotExist:
        return False

    if cv.group_invite_sent:
        return False

    # Count completed/verified tasks for this user in this campaign
    completed_count = TaskAssignment.objects.filter(
        volunteer=user,
        task__campaign_id=campaign_id,
        status__in=['completed', 'verified'],
    ).count()

    # First completion = exactly 1 (the one just submitted)
    return completed_count == 1


@sync_to_async
def _db_mark_group_invite_sent(user, campaign_id):
    """Mark that the group invite has been sent for this volunteer."""
    from apps.campaigns.models import CampaignVolunteer
    CampaignVolunteer.objects.filter(
        campaign_id=campaign_id, volunteer=user
    ).update(group_invite_sent=True)


async def _send_gated_group_invite(bot, chat_id, campaign_id, user):
    """
    After first task completion, send a one-time invite link to the
    campaign's coordination group.
    """
    try:
        group_id = await _db_get_campaign_group_id(campaign_id)
        if not group_id:
            return

        is_first = await _db_check_first_completion(user, campaign_id)
        if not is_first:
            return

        # Create a one-time invite link
        invite_link = await bot.create_chat_invite_link(
            chat_id=group_id,
            member_limit=1,
            name=f'Volunteer invite',
        )

        text = (
            '🎉 <b>You\'ve earned access to the inner circle!</b>\n'
            '━━━━━━━━━━━━━━━━━━━\n'
            'Your first task is done — welcome to the\n'
            'coordination group! 🫡\n\n'
            f'🔗 <a href="{invite_link.invite_link}">Join Coordination Group</a>\n\n'
            '<i>This is a one-time invite link.</i>'
        )

        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True,
        )

        await _db_mark_group_invite_sent(user, campaign_id)
        logger.info(f'Gated group invite sent to user for campaign {campaign_id}')
    except Exception as exc:
        logger.warning(f'Gated group invite failed for campaign {campaign_id}: {exc}')


# ── Handlers ───────────────────────────────────────────────────────────

async def _get_session(user, chat_id):
    """Convenience wrapper."""
    return await _db_get_or_create_session(user.id, user.username, chat_id)


async def tasks_command(update: Update, context: CallbackContext):
    """Handle /tasks command - show available tasks for user's campaigns."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"Tasks command from user {user.id} (@{user.username})")

    session, created = await _get_session(user, chat_id)
    await _db_record_command(session, 'tasks')

    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    tasks, has_campaigns = await _db_get_available_tasks(session.user)

    if not has_campaigns:
        await update.message.reply_text(
            "📭 You haven't joined any campaigns yet.\n"
            "Use `/campaigns` to browse and join available campaigns.",
            parse_mode='Markdown'
        )
        return

    if not tasks:
        await update.message.reply_text(
            "📭 No tasks available in your campaigns at the moment.\n"
            "Check back later or join more campaigns with `/campaigns`.",
            parse_mode='Markdown'
        )
        return

    message = "🎯 *Available Tasks*\n\n"
    keyboard = []

    for i, task in enumerate(tasks, 1):
        type_icon = _get_task_type_icon(task.task_type)
        message += f"*{i}. {type_icon} {task.localized_title(lang)}*\n"
        message += f"   Campaign: {task.campaign.localized_name(lang)}\n"
        message += f"   🏆 {task.points} pts  ⏱ {task.estimated_time} min\n\n"

        keyboard.append([
            InlineKeyboardButton(
                f"{type_icon} {task.localized_title(lang)[:30]}",
                callback_data=f"task_claim_{task.id}"
            )
        ])

    message += "Tap a task to see details and start."

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')


async def mytasks_command(update: Update, context: CallbackContext):
    """Handle /mytasks command - show user's assigned tasks."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"My tasks command from user {user.id} (@{user.username})")

    session, created = await _get_session(user, chat_id)
    await _db_record_command(session, 'mytasks')

    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    assignments = await _db_get_user_assignments(session.user)

    if not assignments:
        await update.message.reply_text(
            "📭 You don't have any assigned tasks.\n"
            "Use `/tasks` to browse and claim available tasks.",
            parse_mode='Markdown'
        )
        return

    message = "📋 *Your Tasks*\n\n"
    keyboard = []

    for i, assignment in enumerate(assignments, 1):
        status_emoji = "⏳" if assignment.status == 'assigned' else "🚧"
        message += f"*{i}. {assignment.task.localized_title(lang)}*\n"
        message += f"   {status_emoji} Status: {assignment.status}\n"
        message += f"   Campaign: {assignment.task.campaign.localized_name(lang)}\n"
        message += f"   Points: {assignment.task.points}\n\n"

        if assignment.status == 'assigned':
            keyboard.append([
                InlineKeyboardButton(
                    f"Start: {assignment.task.localized_title(lang)[:15]}...",
                    callback_data=f"task_start_{assignment.id}"
                )
            ])
        elif assignment.status == 'in_progress':
            keyboard.append([
                InlineKeyboardButton(
                    f"Submit Proof: {assignment.task.localized_title(lang)[:15]}...",
                    callback_data=f"task_submit_{assignment.id}"
                )
            ])

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')


async def claimtask_command(update: Update, context: CallbackContext):
    """Handle /claimtask <id> command - claim a specific task."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"Claim task command from user {user.id} (@{user.username})")

    session, created = await _get_session(user, chat_id)
    await _db_record_command(session, 'claimtask')

    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a task ID.\n"
            "Usage: `/claimtask <task_id>`\n\n"
            "Use `/tasks` to see available tasks with their IDs.",
            parse_mode='Markdown'
        )
        return

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid task ID.", parse_mode='Markdown')
        return

    assignment, error = await _db_validate_and_claim(session.user, task_id)
    if error:
        await update.message.reply_text(error, parse_mode='Markdown')
        return

    task = assignment.task
    await update.message.reply_text(
        f"✅ *Task Claimed Successfully!*\n\n"
        f"*Task:* {task.localized_title(lang)}\n"
        f"*Campaign:* {task.campaign.localized_name(lang)}\n"
        f"*Points:* {task.points}\n\n"
        f"Use `/mytasks` to see your assigned tasks and start working on them.",
        parse_mode='Markdown'
    )


def _get_task_type_icon(task_type: str) -> str:
    """Get emoji icon for task type."""
    icons = {
        'twitter_post': '🐦',
        'twitter_retweet': '🔁',
        'twitter_comment': '💬',
        'twitter_like': '❤️',
        'telegram_share': '📢',
        'telegram_invite': '👥',
        'content_creation': '✍️',
        'petition': '✍️',
        'mass_email': '📧',
        'research': '🔍',
        'other': '📌',
    }
    return icons.get(task_type, '📌')


def _build_twitter_intent_url(tweet_text: str) -> str:
    """Build a Twitter intent URL that pre-fills the compose box."""
    from urllib.parse import quote
    return f"https://twitter.com/intent/tweet?text={quote(tweet_text)}"


def _build_twitter_reply_intent_url(tweet_url: str, reply_text: str) -> str:
    """Build a Twitter reply intent URL with pre-filled comment text.
    
    Uses twitter.com/intent/tweet?in_reply_to=TWEET_ID&text=COMMENT
    so the user taps and Twitter opens with the reply ready to post.
    """
    import re
    from urllib.parse import quote
    match = re.search(r'/status/(\d+)', tweet_url)
    if match:
        tweet_id = match.group(1)
        return f"https://twitter.com/intent/tweet?in_reply_to={tweet_id}&text={quote(reply_text)}"
    # Fallback: just open the tweet URL
    return tweet_url


def _build_twitter_retweet_url(tweet_url: str) -> str:
    """Build a Twitter retweet intent URL from a tweet URL."""
    # Extract tweet ID from URL like https://x.com/user/status/12345
    import re
    match = re.search(r'/status/(\d+)', tweet_url)
    if match:
        return f"https://twitter.com/intent/retweet?tweet_id={match.group(1)}"
    return tweet_url


def _get_sample_comments(task, author_handle: str = '') -> list[str]:
    """Get suggested comment texts for Twitter comment tasks.
    
    Returns list of comment strings, each including hashtags.
    """
    hashtags = task.hashtags.strip() if task.hashtags else '#StopTrumpMadness'

    comments = [
        f"This matters! The world must hold Trump accountable for the destruction in Iran. {hashtags}",
        f"Thank you for speaking truth. Innocent families are paying the price of Trump's madness. {hashtags}",
        f"The evidence is overwhelming. Trump's war on Iran has no justification. {hashtags}",
        f"We won't forget. Children, families, entire communities destroyed. {hashtags}",
        f"This is why we stand together for peace. Stop the war. {hashtags}",
    ]
    return comments


def _get_sample_tweets(task) -> list[dict]:
    """Get sample tweets for Twitter tasks.
    
    Returns list of dicts: [{'text': str, 'intent_url': str}]
    """
    hashtags = task.hashtags.strip() if task.hashtags else ''
    mentions = task.mentions.strip() if task.mentions else ''
    suffix_parts = []
    if mentions:
        suffix_parts.append(mentions)
    if hashtags:
        suffix_parts.append(hashtags)
    suffix = ' '.join(suffix_parts)

    if task.task_type == 'twitter_post':
        bases = [
            "Trump started this war with no justification. Iran demands accountability.",
            "Enough is enough. Trump's war on Iran is unlawful aggression. The world sees it.",
            "Iranian families deserve compensation for Trump's madness. Justice will prevail.",
            "No justification. No cause. Just destruction. Trump must pay for what he did to Iran.",
            "Civilians are dying because of one man's madness. Hold Trump accountable.",
        ]
        tweets = []
        for base in bases:
            full_text = f"{base} {suffix}".strip()
            tweets.append({
                'text': full_text,
                'intent_url': _build_twitter_intent_url(full_text),
            })
        return tweets
    elif task.task_type == 'twitter_retweet':
        return [{
            'text': f"Search for tweets with {hashtags} and retweet at least 3.",
            'intent_url': '',
        }]
    return []


async def task_callback_handler(update: Update, context: CallbackContext):
    """Handle callback queries for task actions.
    
    Note: task_claim_ and task_startclaim_ are now handled by the
    ConversationHandler (start_task_from_claim) so they never reach here.
    """
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    chat_id = update.effective_chat.id
    session, created = await _get_session(user, chat_id)

    callback_data = query.data

    if callback_data.startswith('task_start_'):
        assignment_id = int(callback_data.split('_')[-1])
        await handle_task_start(query, session, assignment_id)
    elif callback_data.startswith('task_submit_'):
        assignment_id = int(callback_data.split('_')[-1])
        await start_task_proof_submission(query, session, assignment_id, context)


async def handle_task_detail(query, session, task_id):
    """Show task details with a clear call-to-action and back navigation."""
    lang = getattr(session, 'language', 'en') or 'en'

    if not session.user:
        await query.edit_message_text(t('register_need_first', lang))
        return

    task = await _db_get_task(task_id)
    if not task:
        await query.edit_message_text(t('tasks_not_found', lang), parse_mode='Markdown')
        return

    type_icon = _get_task_type_icon(task.task_type)
    campaign_id = task.campaign_id if task.campaign else None

    # Build a concise, scannable detail message
    msg = f"{type_icon} *{task.localized_title(lang)}*\n\n"
    msg += f"{task.localized_description(lang)}\n\n"

    msg += f"🏆 *{task.points} points*  ·  ⏱ ~{task.estimated_time} min\n"
    slots = task.max_assignments - task.current_assignments
    if slots > 0:
        msg += t('task_spots_remaining', lang).format(n=slots) + "\n"
    msg += "\n"

    # For Twitter tasks, give a preview of what they'll do
    if task.task_type == 'twitter_post':
        msg += t('task_tweet_desc', lang) + "\n"
    elif task.task_type == 'twitter_retweet':
        msg += t('task_retweet_desc', lang) + "\n"
    elif task.task_type == 'twitter_comment':
        msg += t('task_comment_desc', lang) + "\n"

    msg += "\n" + t('btn_start_action', lang)

    keyboard = [[
        InlineKeyboardButton(
            t('btn_start_action', lang),
            callback_data=f"task_startclaim_{task.id}"
        )
    ]]

    # T5: Back navigation
    if campaign_id:
        keyboard.append([
            InlineKeyboardButton(
                t('btn_back_tasks', lang),
                callback_data=f"campaign_tasks_{campaign_id}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(msg, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_task_start_and_guide(query, session, task_id, context):
    """Claim + start task and show guided flow with 1-tap Twitter links."""
    lang = getattr(session, 'language', 'en') or 'en'

    if not session.user:
        await query.edit_message_text(t('register_need_first', lang))
        return

    assignment, error = await _db_validate_and_claim(session.user, task_id)
    if error:
        await query.edit_message_text(error, parse_mode='Markdown')
        return

    task = assignment.task
    type_icon = _get_task_type_icon(task.task_type)
    campaign_id = task.campaign_id if task.campaign else None

    # Set session state so we can receive proof as a plain message
    context.user_data['proof_submission'] = {
        'assignment_id': assignment.id,
        'task_title': task.localized_title(lang),
        'task_type': task.task_type,
        'campaign_id': campaign_id,
    }

    from apps.telegram.models import TelegramSession
    await _db_update_session_state(
        session,
        TelegramSession.State.AWAITING_TASK_PROOF,
        {'assignment_id': assignment.id}
    )

    keyboard = []

    # ── Twitter Post: Guided 3-step flow with intent links ──
    if task.task_type == 'twitter_post':
        samples = _get_sample_tweets(task)

        msg = t('task_started_title', lang) + "\n\n"
        msg += f"{type_icon} *{task.localized_title(lang)}*\n\n"
        msg += t('task_3_steps', lang) + "\n\n"
        msg += t('tweet_step1', lang) + "\n"
        msg += t('tweet_step2', lang) + "\n"
        msg += t('tweet_step3', lang) + "\n"
        msg += "\n───────────────────\n\n"

        for idx, sample in enumerate(samples, 1):
            num_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'][idx - 1] if idx <= 5 else f"{idx}."
            msg += f"{num_emoji} \"{sample['text'][:120]}{'...' if len(sample['text']) > 120 else ''}\"\n\n"
            keyboard.append([
                InlineKeyboardButton(
                    t('btn_post_tweet', lang).format(n=idx),
                    url=sample['intent_url']
                )
            ])

        msg += "───────────────────\n\n"
        msg += t('tweet_or_write_own', lang) + "\n\n"
        msg += t('tweet_paste_url_below', lang) + "\n"
        msg += t('cancel_hint', lang)

    # ── Twitter Retweet: Link to search ──
    elif task.task_type == 'twitter_retweet':
        hashtags = task.hashtags.strip() if task.hashtags else '#StopTrumpMadness'
        from urllib.parse import quote
        search_url = f"https://twitter.com/search?q={quote(hashtags)}&f=live"

        msg = t('task_started_title', lang) + "\n\n"
        msg += f"{type_icon} *{task.localized_title(lang)}*\n\n"
        msg += t('task_3_steps', lang) + "\n\n"
        msg += t('retweet_step1', lang).format(hashtags=hashtags) + "\n"
        msg += t('retweet_step2', lang) + "\n"
        msg += t('retweet_step3', lang) + "\n"

        keyboard.append([
            InlineKeyboardButton(
                t('btn_find_tweets', lang).format(hashtags=hashtags),
                url=search_url
            )
        ])

        msg += "\n" + t('retweet_paste_proof', lang) + "\n"
        msg += t('cancel_hint', lang)

    # ── Twitter Comment: Reply intents with suggested comments ──
    elif task.task_type == 'twitter_comment':
        msg = t('task_started_title', lang) + "\n\n"
        msg += f"{type_icon} *{task.localized_title(lang)}*\n\n"
        msg += t('task_3_steps', lang) + "\n\n"
        msg += t('comment_step1', lang) + "\n"
        msg += t('comment_step2', lang) + "\n"
        msg += t('comment_step3', lang) + "\n"

        # Fetch key tweets from DB
        key_tweets = await sync_to_async(
            lambda: list(task.key_tweets.filter(is_active=True).order_by('order'))
        )()

        sample_comments = _get_sample_comments(task)

        if key_tweets:
            msg += "\n───────────────────\n\n"
            msg += t('comment_pick_tweet', lang) + "\n\n"

            for idx, kt in enumerate(key_tweets, 1):
                # Rotate through sample comments per key tweet
                comment_text = sample_comments[(idx - 1) % len(sample_comments)]
                reply_url = _build_twitter_reply_intent_url(kt.tweet_url, comment_text)

                num_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'][idx - 1] if idx <= 5 else f"{idx}."
                msg += f"{num_emoji} *{kt.author_name}* ({kt.author_handle})\n"
                if kt.description:
                    msg += f"   _{kt.description}_\n"
                msg += f"   💬 _{comment_text[:80]}{'...' if len(comment_text) > 80 else ''}_\n\n"

                keyboard.append([
                    InlineKeyboardButton(
                        t('btn_reply_to', lang).format(handle=kt.author_handle),
                        url=reply_url
                    )
                ])

            msg += "───────────────────\n"
            msg += "\n" + t('comment_or_write_own', lang) + "\n"
        elif task.target_url:
            comment_text = sample_comments[0]
            reply_url = _build_twitter_reply_intent_url(task.target_url, comment_text)
            msg += f"\n🔗 {t('comment_target_tweet', lang)}\n"
            msg += f"💬 _{comment_text[:80]}_\n"
            keyboard.append([
                InlineKeyboardButton(
                    t('btn_reply_suggested', lang),
                    url=reply_url
                )
            ])

        msg += "\n" + t('comment_paste_reply', lang) + "\n"
        msg += t('cancel_hint', lang)

    # ── Telegram Share ──
    elif task.task_type == 'telegram_share':
        msg = t('task_started_title', lang) + "\n\n"
        msg += f"{type_icon} *{task.localized_title(lang)}*\n\n"
        msg += f"{task.instructions}\n\n"
        msg += t('share_send_proof', lang) + "\n"
        msg += t('cancel_hint', lang)

    # ── Telegram Invite ──
    elif task.task_type == 'telegram_invite':
        msg = t('task_started_title', lang) + "\n\n"
        msg += f"{type_icon} *{task.localized_title(lang)}*\n\n"
        msg += f"{task.instructions}\n\n"
        msg += t('invite_share_link', lang) + "\n\n"
        msg += t('invite_send_username', lang) + "\n"
        msg += t('cancel_hint', lang)

    # ── Petition: Guided sign flow ──
    elif task.task_type == 'petition':
        petition_url = task.target_url or task.instructions or ''
        msg = t('task_started_title', lang) + "\n\n"
        msg += f"{type_icon} *{task.localized_title(lang)}*\n\n"
        msg += t('task_3_steps', lang) + "\n\n"
        msg += t('task_petition_step1', lang) + "\n"
        msg += t('task_petition_step2', lang) + "\n"
        msg += t('task_petition_step3', lang) + "\n"

        if petition_url and petition_url.startswith('http'):
            keyboard.append([
                InlineKeyboardButton(
                    t('btn_open_petition', lang),
                    url=petition_url
                )
            ])

        msg += "\n" + t('generic_send_proof', lang) + "\n"
        msg += t('cancel_hint', lang)

    # ── Mass Email: Copy template + confirm ──
    elif task.task_type == 'mass_email':
        msg = t('task_started_title', lang) + "\n\n"
        msg += f"{type_icon} *{task.localized_title(lang)}*\n\n"
        msg += t('task_mass_email_step1', lang) + "\n\n"

        # Show email template from task instructions
        if task.instructions:
            msg += f"\n───────────────────\n"
            msg += f"`{task.instructions[:800]}`\n"
            msg += f"───────────────────\n\n"

        msg += t('task_mass_email_step2', lang) + "\n"
        msg += t('cancel_hint', lang)

    # ── Other task types ──
    else:
        msg = t('task_started_title', lang) + "\n\n"
        msg += f"{type_icon} *{task.localized_title(lang)}*\n\n"
        msg += f"{task.instructions}\n\n"
        msg += t('generic_send_proof', lang) + "\n"
        msg += t('cancel_hint', lang)

    # ── Back navigation on ALL task screens ──
    if campaign_id:
        keyboard.append([
            InlineKeyboardButton(
                t('btn_back_tasks', lang),
                callback_data=f"campaign_tasks_{campaign_id}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await query.edit_message_text(msg, reply_markup=reply_markup, parse_mode='Markdown')

    return AWAITING_TASK_PROOF


async def handle_task_start(query, session, assignment_id):
    """Handle task start from /mytasks inline button (legacy)."""
    if not session.user:
        await query.edit_message_text("You need to register first.")
        return

    assignment, error = await _db_start_assignment(assignment_id, session.user)
    if error:
        await query.edit_message_text(error, parse_mode='Markdown')
        return

    await query.edit_message_text(
        f"🚧 *Task Started!*\n\n"
        f"*Task:* {assignment.task.localized_title(lang)}\n"
        f"*Status:* In Progress\n\n"
        f"Once you complete the task, use `/mytasks` to submit proof.",
        parse_mode='Markdown'
    )


async def start_task_proof_submission(query, session, assignment_id, context):
    """Start the task proof submission conversation."""
    if not session.user:
        await query.edit_message_text("You need to register first.")
        return

    assignment = await _db_get_in_progress_assignment(assignment_id, session.user)
    if not assignment:
        await query.edit_message_text(
            "❌ This task is not in progress or no longer available.",
            parse_mode='Markdown'
        )
        return

    context.user_data['proof_submission'] = {
        'assignment_id': assignment_id,
        'task_title': assignment.task.localized_title(lang)
    }

    from apps.telegram.models import TelegramSession
    await _db_update_session_state(
        session,
        TelegramSession.State.AWAITING_TASK_PROOF,
        {'assignment_id': assignment_id}
    )

    await query.edit_message_text(
        f"📤 *Submit Task Proof*\n\n"
        f"*Task:* {assignment.task.localized_title(lang)}\n\n"
        f"Please provide proof of completion:\n"
        f"• Screenshot of your action\n"
        f"• Link to your content\n"
        f"• Summary of your work\n\n"
        f"*Send your proof as a photo, document, or text message.*\n"
        f"Type /cancel to cancel submission.",
        parse_mode='Markdown'
    )

    return AWAITING_TASK_PROOF


async def receive_task_proof(update: Update, context: CallbackContext):
    """Receive task proof from user."""
    user = update.effective_user

    session = await _db_get_session_by_telegram_id(user.id)
    if not session:
        await update.message.reply_text("Session not found. Please start over with /start.")
        return ConversationHandler.END

    proof_data = context.user_data.get('proof_submission')
    if not proof_data:
        await update.message.reply_text("No task found for proof submission. Please start over.")
        from apps.telegram.models import TelegramSession
        await _db_update_session_state(session, TelegramSession.State.IDLE)
        return ConversationHandler.END

    assignment_id = proof_data['assignment_id']
    task_title = proof_data['task_title']

    assignment = await _db_get_in_progress_assignment(assignment_id, session.user)
    if not assignment:
        await update.message.reply_text("Task assignment not found or already completed.")
        from apps.telegram.models import TelegramSession
        await _db_update_session_state(session, TelegramSession.State.IDLE)
        return ConversationHandler.END

    proof_content = ""
    if update.message.text:
        text = update.message.text.strip()
        # Check if it's a URL (Twitter/X proof)
        if any(domain in text.lower() for domain in ['twitter.com/', 'x.com/', 't.me/', 'https://']):
            proof_type = "url"
            proof_content = text
        else:
            proof_type = "text"
            proof_content = text
    elif update.message.photo:
        proof_content = "Photo proof submitted"
        proof_type = "photo"
    elif update.message.document:
        proof_content = f"Document: {update.message.document.file_name}"
        proof_type = "document"
    else:
        await update.message.reply_text("Please send proof as text, photo, or document.")
        return AWAITING_TASK_PROOF

    context.user_data['proof_details'] = {
        'content': proof_content,
        'type': proof_type,
        'assignment_id': assignment_id
    }

    from apps.telegram.models import TelegramSession
    await _db_update_session_state(
        session,
        TelegramSession.State.AWAITING_CONFIRMATION,
        {'proof_type': proof_type}
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm Submission", callback_data=f"proof_confirm_{assignment_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data="proof_cancel")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"📝 *Proof Submission Review*\n\n"
        f"*Task:* {task_title}\n"
        f"*Proof Type:* {proof_type}\n"
        f"*Proof Content:* {proof_content[:100]}...\n\n"
        f"Please confirm your submission:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    return AWAITING_CONFIRMATION


async def proof_callback_handler(update: Update, context: CallbackContext):
    """Handle proof submission callbacks."""
    query = update.callback_query
    await query.answer()
    user = update.effective_user

    session = await _db_get_session_by_telegram_id(user.id)
    if not session:
        await query.edit_message_text("Session not found.")
        return ConversationHandler.END

    callback_data = query.data

    if callback_data.startswith('proof_confirm_'):
        assignment_id = int(callback_data.split('_')[-1])
        await confirm_proof_submission(query, session, assignment_id, context)
        return ConversationHandler.END
    elif callback_data == 'proof_cancel':
        await cancel_proof_submission(query, session)
        return ConversationHandler.END


async def confirm_proof_submission(query, session, assignment_id, context):
    """Confirm and process proof submission with community pulse."""
    proof_details = context.user_data.get('proof_details', {})
    if not proof_details or proof_details.get('assignment_id') != assignment_id:
        await query.edit_message_text("Proof details not found. Please submit proof again.")
        from apps.telegram.models import TelegramSession
        await _db_update_session_state(session, TelegramSession.State.IDLE)
        return

    assignment, error = await _db_submit_proof(
        assignment_id, session.user,
        proof_details.get('type', 'text'),
        proof_details.get('content', '')
    )

    if error:
        await query.edit_message_text(error)
        from apps.telegram.models import TelegramSession
        await _db_update_session_state(session, TelegramSession.State.IDLE)
        return

    context.user_data.pop('proof_submission', None)
    context.user_data.pop('proof_details', None)

    from apps.telegram.models import TelegramSession
    await _db_update_session_state(session, TelegramSession.State.IDLE)

    # Get campaign context
    campaign_id = None
    if assignment.task.campaign:
        campaign_id = assignment.task.campaign_id

    # ── Channel Broadcast (fire-and-forget) ──
    if campaign_id:
        await _broadcast_task_completion(
            bot=query._bot,
            campaign_id=campaign_id,
            task_title=assignment.task.title,
            task_type=assignment.task.task_type,
            points=assignment.task.points,
            proof_url=proof_details.get('content', '') if proof_details.get('type') == 'url' else ''
        )

        # ── Gated Group Invite (first task only) ──
        await _send_gated_group_invite(
            bot=query._bot,
            chat_id=query.message.chat_id,
            campaign_id=campaign_id,
            user=session.user,
        )

    # ── Community Pulse (1C) ──────────────────────────────────
    pulse_msg = ""
    if campaign_id:
        pulse = await _db_get_campaign_pulse(campaign_id)
        rank = await _db_get_user_rank(session.user, campaign_id)

        pulse_msg += "\n───────────────────\n"
        if pulse['recent_active'] > 0:
            pulse_msg += t('pulse_active_hour', lang).format(count=pulse['recent_active']) + "\n"
        pulse_msg += t('pulse_total_actions', lang).format(count=pulse['total_completed']) + "\n"
        pulse_msg += t('pulse_volunteers', lang).format(count=pulse['total_volunteers']) + "\n"
        if rank is not None:
            pulse_msg += t('pulse_rank', lang).format(rank=rank) + "\n"
        pulse_msg += "───────────────────\n"

    next_keyboard = []
    if campaign_id:
        next_keyboard.append([
            InlineKeyboardButton(
                t('btn_do_another', lang),
                callback_data=f"campaign_tasks_{campaign_id}"
            )
        ])
    next_keyboard.append([
        InlineKeyboardButton(t('btn_main_menu', lang), callback_data="menu_main")
    ])

    await query.edit_message_text(
        t('proof_submitted_short', lang).format(points=assignment.task.points) + "\n\n"
        f"*{t('task_instructions', lang).replace('📝 ', '').replace('*', '')}* {assignment.task.localized_title(lang)}\n"
        + t('proof_under_review', lang) + "\n"
        f"{pulse_msg}\n"
        + t('proof_keep_going', lang),
        reply_markup=InlineKeyboardMarkup(next_keyboard),
        parse_mode='Markdown'
    )


async def cancel_proof_submission(query, session):
    """Cancel proof submission."""
    from apps.telegram.models import TelegramSession
    await _db_update_session_state(session, TelegramSession.State.IDLE)
    await query.edit_message_text(
        "❌ Proof submission cancelled.\n"
        "Use `/mytasks` to view your tasks and submit proof later.",
        parse_mode='Markdown'
    )


async def cancel_conversation(update: Update, context: CallbackContext):
    """Cancel any ongoing conversation."""
    user = update.effective_user

    session = await _db_get_session_by_telegram_id(user.id)
    if session:
        from apps.telegram.models import TelegramSession
        await _db_update_session_state(session, TelegramSession.State.IDLE)

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Operation cancelled.\n"
        "You can start over with any command.",
        parse_mode='Markdown'
    )
    return ConversationHandler.END


async def start_task_from_claim(update: Update, context: CallbackContext):
    """Entry point: user clicks a task from checklist → auto-claim + guided flow.
    
    Handles both task_claim_ (Phase 1: 2-click) and task_startclaim_ (legacy).
    """
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    chat_id = update.effective_chat.id
    session, created = await _get_session(user, chat_id)

    task_id = int(query.data.split('_')[-1])
    return await handle_task_start_and_guide(query, session, task_id, context)


# Conversation handler for task proof submission
task_proof_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_task_proof_submission, pattern='^task_submit_'),
        # 2-click flow: task_claim_ now enters ConversationHandler directly
        CallbackQueryHandler(start_task_from_claim, pattern='^task_claim_'),
        # Legacy entry point kept for compatibility
        CallbackQueryHandler(start_task_from_claim, pattern='^task_startclaim_'),
    ],
    states={
        AWAITING_TASK_PROOF: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task_proof),
            MessageHandler(filters.PHOTO, receive_task_proof),
            MessageHandler(filters.Document.ALL, receive_task_proof),
        ],
        AWAITING_CONFIRMATION: [
            CallbackQueryHandler(proof_callback_handler, pattern='^proof_')
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_conversation)
    ]
)

# Handler registration
# IMPORTANT: task_proof_conversation must come BEFORE task_callback_handler
# so that task_claim_ and task_startclaim_ are handled by ConversationHandler
task_handlers = [
    task_proof_conversation,
    CallbackQueryHandler(task_callback_handler, pattern='^task_'),
]
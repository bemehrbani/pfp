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

logger = logging.getLogger(__name__)

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

    existing = TaskAssignment.objects.filter(task=task, volunteer=user).first()
    if existing:
        return existing, None  # Return existing assignment (already claimed)

    assignment = TaskAssignment.objects.create(
        task=task,
        campaign=task.campaign,
        volunteer=user,
        status='in_progress'  # Skip 'assigned', go straight to 'in_progress'
    )

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
        message += f"*{i}. {type_icon} {task.title}*\n"
        message += f"   Campaign: {task.campaign.name}\n"
        message += f"   🏆 {task.points} pts  ⏱ {task.estimated_time} min\n\n"

        keyboard.append([
            InlineKeyboardButton(
                f"{type_icon} {task.title[:30]}",
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
        message += f"*{i}. {assignment.task.title}*\n"
        message += f"   {status_emoji} Status: {assignment.status}\n"
        message += f"   Campaign: {assignment.task.campaign.name}\n"
        message += f"   Points: {assignment.task.points}\n\n"

        if assignment.status == 'assigned':
            keyboard.append([
                InlineKeyboardButton(
                    f"Start: {assignment.task.title[:15]}...",
                    callback_data=f"task_start_{assignment.id}"
                )
            ])
        elif assignment.status == 'in_progress':
            keyboard.append([
                InlineKeyboardButton(
                    f"Submit Proof: {assignment.task.title[:15]}...",
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
        f"*Task:* {task.title}\n"
        f"*Campaign:* {task.campaign.name}\n"
        f"*Points:* {task.points}\n\n"
        f"Use `/mytasks` to see your assigned tasks and start working on them.",
        parse_mode='Markdown'
    )


def _get_task_type_icon(task_type: str) -> str:
    """Get emoji icon for task type."""
    icons = {
        'twitter_post': '🐦',
        'twitter_retweet': '🔁',
        'twitter_like': '❤️',
        'telegram_share': '📢',
        'telegram_invite': '👥',
        'content_creation': '✍️',
        'research': '🔍',
        'other': '📌',
    }
    return icons.get(task_type, '📌')


def _get_sample_tweets(task) -> list[str]:
    """Get sample tweets for Twitter tasks. Returns list of ready-to-post tweets."""
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
            "I stand for peace. Stop the war against Iran. Diplomacy over destruction.",
            "Enough is enough. The people of Iran deserve peace, not bombs.",
            "Peace is not weakness — it's strength. Stand with Iran.",
            "The world must choose diplomacy. War is never the answer. Protect innocent lives.",
            "Civilians are paying the price for political decisions. Demand a ceasefire now.",
        ]
        return [f"{b} {suffix}".strip() for b in bases]
    elif task.task_type == 'twitter_retweet':
        return [f"Search for tweets with {hashtags} and retweet at least 3."]
    return []


async def task_callback_handler(update: Update, context: CallbackContext):
    """Handle callback queries for task actions."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    chat_id = update.effective_chat.id
    session, created = await _get_session(user, chat_id)

    callback_data = query.data

    if callback_data.startswith('task_claim_'):
        task_id = int(callback_data.split('_')[-1])
        await handle_task_detail(query, session, task_id)
    elif callback_data.startswith('task_start_'):
        assignment_id = int(callback_data.split('_')[-1])
        await handle_task_start(query, session, assignment_id)
    elif callback_data.startswith('task_submit_'):
        assignment_id = int(callback_data.split('_')[-1])
        await start_task_proof_submission(query, session, assignment_id, context)


async def handle_task_detail(query, session, task_id):
    """Show full task details with description, instructions, and a Start button."""
    if not session.user:
        await query.edit_message_text("You need to register first. Use /start")
        return

    task = await _db_get_task(task_id)
    if not task:
        await query.edit_message_text("❌ Task not found.", parse_mode='Markdown')
        return

    type_icon = _get_task_type_icon(task.task_type)

    # Build the detail message
    msg = f"{type_icon} *{task.title}*\n\n"
    msg += f"{task.description}\n\n"
    msg += f"📝 *Instructions:*\n{task.instructions}\n\n"

    # Show hashtags/mentions for Twitter tasks
    if task.hashtags:
        msg += f"#️⃣ *Hashtags:* {task.hashtags}\n"
    if task.mentions:
        msg += f"@️ *Mentions:* {task.mentions}\n"
    if task.target_url:
        msg += f"🔗 *Link:* {task.target_url}\n"

    msg += f"\n🏆 *Points:* {task.points}  ⏱ *Est:* {task.estimated_time} min\n"
    msg += f"👥 *Slots:* {task.max_assignments - task.current_assignments} remaining\n"

    keyboard = [[
        InlineKeyboardButton(
            "✅ Start This Task",
            callback_data=f"task_startclaim_{task.id}"
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(msg, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_task_start_and_guide(query, session, task_id, context):
    """Claim + start task and show guidance (sample tweet for Twitter tasks)."""
    if not session.user:
        await query.edit_message_text("You need to register first. Use /start")
        return

    assignment, error = await _db_validate_and_claim(session.user, task_id)
    if error:
        await query.edit_message_text(error, parse_mode='Markdown')
        return

    task = assignment.task
    type_icon = _get_task_type_icon(task.task_type)

    # Set session state so we can receive proof as a plain message
    context.user_data['proof_submission'] = {
        'assignment_id': assignment.id,
        'task_title': task.title,
        'task_type': task.task_type
    }

    from apps.telegram.models import TelegramSession
    await _db_update_session_state(
        session,
        TelegramSession.State.AWAITING_TASK_PROOF,
        {'assignment_id': assignment.id}
    )

    # Build guidance message based on task type
    if task.task_type in ('twitter_post', 'twitter_retweet'):
        samples = _get_sample_tweets(task)
        msg = f"🚀 *Task Started!*\n\n"
        msg += f"{type_icon} *{task.title}*\n\n"

        if task.task_type == 'twitter_post':
            msg += f"📝 *Pick a tweet or write your own:*\n\n"
            for idx, tweet in enumerate(samples, 1):
                msg += f"*{idx}.* `{tweet}`\n\n"
            msg += f"👉 Copy one, customize it & post on Twitter/X\n\n"
        elif task.task_type == 'twitter_retweet':
            msg += f"📝 *What to do:*\n{samples[0]}\n\n"

        msg += f"✅ *When done, paste your tweet URL below*\n"
        msg += f"(e.g. https://x.com/yourname/status/123...)\n\n"
        msg += f"Type /cancel to cancel."

    elif task.task_type == 'telegram_share':
        msg = f"🚀 *Task Started!*\n\n"
        msg += f"{type_icon} *{task.title}*\n\n"
        msg += f"📝 *What to do:*\n{task.instructions}\n\n"
        msg += f"✅ *When done, paste the message link or send a screenshot*\n\n"
        msg += f"Type /cancel to cancel."

    elif task.task_type == 'telegram_invite':
        msg = f"🚀 *Task Started!*\n\n"
        msg += f"{type_icon} *{task.title}*\n\n"
        msg += f"📝 *What to do:*\n{task.instructions}\n\n"
        msg += f"👉 Share this link: https://t.me/peopleforpeacebot\n\n"
        msg += f"✅ *When done, send the username of the person you invited*\n\n"
        msg += f"Type /cancel to cancel."

    else:  # content_creation, research, other
        msg = f"🚀 *Task Started!*\n\n"
        msg += f"{type_icon} *{task.title}*\n\n"
        msg += f"📝 *What to do:*\n{task.instructions}\n\n"
        msg += f"✅ *When done, send your proof (text, link, or screenshot)*\n\n"
        msg += f"Type /cancel to cancel."

    await query.edit_message_text(msg, parse_mode='Markdown')

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
        f"*Task:* {assignment.task.title}\n"
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
        'task_title': assignment.task.title
    }

    from apps.telegram.models import TelegramSession
    await _db_update_session_state(
        session,
        TelegramSession.State.AWAITING_TASK_PROOF,
        {'assignment_id': assignment_id}
    )

    await query.edit_message_text(
        f"📤 *Submit Task Proof*\n\n"
        f"*Task:* {assignment.task.title}\n\n"
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
    """Confirm and process proof submission."""
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

    await query.edit_message_text(
        f"✅ *Proof Submitted Successfully!*\n\n"
        f"*Task:* {assignment.task.title}\n"
        f"*Status:* Pending Review\n"
        f"*Points:* {assignment.task.points} (pending verification)\n\n"
        f"Your proof has been submitted for review by the campaign manager.\n"
        f"You'll be notified once it's verified and points are awarded.",
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


async def start_task_from_detail(update: Update, context: CallbackContext):
    """Entry point wrapper for ConversationHandler when starting a task from detail view."""
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
        CallbackQueryHandler(start_task_from_detail, pattern='^task_startclaim_'),
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
# so that task_startclaim_ is handled by the ConversationHandler first
task_handlers = [
    task_proof_conversation,
    CallbackQueryHandler(task_callback_handler, pattern='^task_'),
]
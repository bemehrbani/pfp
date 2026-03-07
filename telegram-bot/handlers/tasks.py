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
        session.save(update_fields=['telegram_username', 'telegram_chat_id', 'updated_at'])
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
    """Validate and claim task in a single sync block. Returns (assignment, error_msg)."""
    from apps.tasks.models import Task, TaskAssignment
    from apps.campaigns.models import CampaignVolunteer

    try:
        task = Task.objects.select_related('campaign').get(id=task_id)
    except Task.DoesNotExist:
        return None, "❌ Task not found."

    if not CampaignVolunteer.objects.filter(campaign=task.campaign, volunteer=user).exists():
        return None, "❌ You need to join this campaign first to claim its tasks."

    if TaskAssignment.objects.filter(task=task, volunteer=user).exists():
        return None, f"✅ You've already claimed *{task.title}*!"

    assignment = TaskAssignment.objects.create(
        task=task,
        volunteer=user,
        status='assigned'
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
        assignment.status = 'submitted'
        assignment.save(update_fields=['status'])
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
        message += f"*{i}. {task.title}*\n"
        message += f"   Campaign: {task.campaign.name}\n"
        message += f"   Points: {task.points}\n\n"

        keyboard.append([
            InlineKeyboardButton(
                f"Claim: {task.title[:20]}...",
                callback_data=f"task_claim_{task.id}"
            )
        ])

    message += "Click a button below to claim a task."

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
        await handle_task_claim(query, session, task_id)
    elif callback_data.startswith('task_start_'):
        assignment_id = int(callback_data.split('_')[-1])
        await handle_task_start(query, session, assignment_id)
    elif callback_data.startswith('task_submit_'):
        assignment_id = int(callback_data.split('_')[-1])
        await start_task_proof_submission(query, session, assignment_id, context)


async def handle_task_claim(query, session, task_id):
    """Handle task claim from inline button."""
    if not session.user:
        await query.edit_message_text("You need to register first.")
        return

    assignment, error = await _db_validate_and_claim(session.user, task_id)
    if error:
        await query.edit_message_text(error, parse_mode='Markdown')
        return

    task = assignment.task
    await query.edit_message_text(
        f"✅ *Task Claimed Successfully!*\n\n"
        f"*Task:* {task.title}\n"
        f"*Campaign:* {task.campaign.name}\n"
        f"*Points:* {task.points}\n\n"
        f"Use `/mytasks` to start working on this task.",
        parse_mode='Markdown'
    )


async def handle_task_start(query, session, assignment_id):
    """Handle task start from inline button."""
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
        proof_content = update.message.text
        proof_type = "text"
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


# Conversation handler for task proof submission
task_proof_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_task_proof_submission, pattern='^task_submit_')],
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
task_handlers = [
    CallbackQueryHandler(task_callback_handler, pattern='^task_'),
    task_proof_conversation
]
"""
Task command handlers for Telegram bot.
"""
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, CommandHandler
from django.contrib.auth import get_user_model
from django.db.models import Q, F
from apps.campaigns.models import Campaign, CampaignVolunteer
from apps.tasks.models import Task, TaskAssignment
from apps.telegram.models import TelegramSession, TelegramMessageLog

logger = logging.getLogger(__name__)
User = get_user_model()

# Conversation states for task completion
AWAITING_TASK_PROOF = 1
AWAITING_CONFIRMATION = 2


async def tasks_command(update: Update, context: CallbackContext):
    """Handle /tasks command - show available tasks for user's campaigns."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Tasks command from user {user.id} (@{user.username})")

    # Get or create Telegram session
    session, created = await get_or_create_session(user, chat_id)
    session.record_command('tasks')

    # Check if user is registered
    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    # Get user's campaigns
    user_campaigns = CampaignVolunteer.objects.filter(
        user=session.user,
        campaign__status=Campaign.Status.ACTIVE
    ).values_list('campaign_id', flat=True)

    if not user_campaigns:
        await update.message.reply_text(
            "📭 You haven't joined any campaigns yet.\n"
            "Use `/campaigns` to browse and join available campaigns.",
            parse_mode='Markdown'
        )
        return

    # Get available tasks from user's campaigns
    tasks = Task.objects.filter(
        campaign_id__in=user_campaigns,
        current_assignments__lt=models.F('max_assignments')
    ).exclude(
        assignments__user=session.user
    ).order_by('-points', 'created_at')[:10]

    if not tasks:
        await update.message.reply_text(
            "📭 No tasks available in your campaigns at the moment.\n"
            "Check back later or join more campaigns with `/campaigns`.",
            parse_mode='Markdown'
        )
        return

    # Create tasks list message
    message = "🎯 *Available Tasks*\n\n"
    keyboard = []

    for i, task in enumerate(tasks, 1):
        message += f"*{i}. {task.title}*\n"
        message += f"   Campaign: {task.campaign.name}\n"
        message += f"   Points: {task.points} | Time: {task.estimated_time}min\n"
        message += f"   Slots: {task.current_assignments}/{task.max_assignments}\n\n"

        # Create inline button for each task
        keyboard.append([
            InlineKeyboardButton(
                f"Claim: {task.title[:20]}...",
                callback_data=f"task_claim_{task.id}"
            )
        ])

    message += "Click a button below to claim a task."

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def mytasks_command(update: Update, context: CallbackContext):
    """Handle /mytasks command - show user's assigned tasks."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"My tasks command from user {user.id} (@{user.username})")

    # Get or create Telegram session
    session, created = await get_or_create_session(user, chat_id)
    session.record_command('mytasks')

    # Check if user is registered
    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    # Get user's task assignments
    assignments = TaskAssignment.objects.filter(
        user=session.user,
        status__in=[TaskAssignment.Status.ASSIGNED, TaskAssignment.Status.IN_PROGRESS]
    ).select_related('task', 'task__campaign').order_by('deadline')

    if not assignments:
        await update.message.reply_text(
            "📭 You don't have any assigned tasks.\n"
            "Use `/tasks` to browse and claim available tasks.",
            parse_mode='Markdown'
        )
        return

    # Create tasks list message
    message = "📋 *Your Tasks*\n\n"
    keyboard = []

    for i, assignment in enumerate(assignments, 1):
        status_emoji = "⏳" if assignment.status == TaskAssignment.Status.ASSIGNED else "🚧"
        message += f"*{i}. {assignment.task.title}*\n"
        message += f"   {status_emoji} Status: {assignment.get_status_display()}\n"
        message += f"   Campaign: {assignment.task.campaign.name}\n"
        message += f"   Points: {assignment.task.points}\n"
        if assignment.deadline:
            message += f"   📅 Deadline: {assignment.deadline.strftime('%Y-%m-%d')}\n"
        message += "\n"

        # Create inline button for task actions
        if assignment.status == TaskAssignment.Status.ASSIGNED:
            keyboard.append([
                InlineKeyboardButton(
                    f"Start: {assignment.task.title[:15]}...",
                    callback_data=f"task_start_{assignment.id}"
                )
            ])
        elif assignment.status == TaskAssignment.Status.IN_PROGRESS:
            keyboard.append([
                InlineKeyboardButton(
                    f"Submit Proof: {assignment.task.title[:15]}...",
                    callback_data=f"task_submit_{assignment.id}"
                )
            ])

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def claimtask_command(update: Update, context: CallbackContext):
    """Handle /claimtask <id> command - claim a specific task."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"Claim task command from user {user.id} (@{user.username})")

    # Get or create Telegram session
    session, created = await get_or_create_session(user, chat_id)
    session.record_command('claimtask')

    # Check if user is registered
    if not session.user:
        await update.message.reply_text(
            "⚠️ You need to register first! Use /start to begin registration.",
            parse_mode='Markdown'
        )
        return

    # Check if task ID was provided
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
        task = Task.objects.get(id=task_id)
    except (ValueError, Task.DoesNotExist):
        await update.message.reply_text(
            "❌ Invalid task ID.\n"
            "Use `/tasks` to see available tasks.",
            parse_mode='Markdown'
        )
        return

    # Check if user can claim this task
    error = await validate_task_claim(session.user, task)
    if error:
        await update.message.reply_text(error, parse_mode='Markdown')
        return

    # Claim the task
    assignment = TaskAssignment.objects.create(
        task=task,
        user=session.user,
        status=TaskAssignment.Status.ASSIGNED
    )

    # Update task assignment count
    task.current_assignments += 1
    task.save(update_fields=['current_assignments'])

    await update.message.reply_text(
        f"✅ *Task Claimed Successfully!*\n\n"
        f"*Task:* {task.title}\n"
        f"*Campaign:* {task.campaign.name}\n"
        f"*Points:* {task.points}\n"
        f"*Estimated Time:* {task.estimated_time} minutes\n\n"
        f"*Instructions:*\n{task.instructions}\n\n"
        f"Use `/mytasks` to see your assigned tasks and start working on them.",
        parse_mode='Markdown'
    )


async def task_callback_handler(update: Update, context: CallbackContext):
    """Handle callback queries for task actions."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    chat_id = update.effective_chat.id

    # Get or create Telegram session
    session, created = await get_or_create_session(user, chat_id)

    callback_data = query.data

    if callback_data.startswith('task_claim_'):
        # Handle task claim request
        task_id = int(callback_data.split('_')[-1])
        await handle_task_claim(query, session, task_id)

    elif callback_data.startswith('task_start_'):
        # Handle task start
        assignment_id = int(callback_data.split('_')[-1])
        await handle_task_start(query, session, assignment_id)

    elif callback_data.startswith('task_submit_'):
        # Handle task proof submission start
        assignment_id = int(callback_data.split('_')[-1])
        await start_task_proof_submission(query, session, assignment_id, context)


async def handle_task_claim(query, session, task_id):
    """Handle task claim from inline button."""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        await query.edit_message_text(
            "❌ This task is no longer available.",
            parse_mode='Markdown'
        )
        return

    # Check if user can claim this task
    error = await validate_task_claim(session.user, task)
    if error:
        await query.edit_message_text(error, parse_mode='Markdown')
        return

    # Check if user already has this task
    if TaskAssignment.objects.filter(task=task, user=session.user).exists():
        await query.edit_message_text(
            f"✅ You've already claimed *{task.title}*!\n"
            f"Use `/mytasks` to see your assigned tasks.",
            parse_mode='Markdown'
        )
        return

    # Claim the task
    assignment = TaskAssignment.objects.create(
        task=task,
        user=session.user,
        status=TaskAssignment.Status.ASSIGNED
    )

    # Update task assignment count
    task.current_assignments += 1
    task.save(update_fields=['current_assignments'])

    await query.edit_message_text(
        f"✅ *Task Claimed Successfully!*\n\n"
        f"*Task:* {task.title}\n"
        f"*Campaign:* {task.campaign.name}\n"
        f"*Points:* {task.points}\n"
        f"*Estimated Time:* {task.estimated_time} minutes\n\n"
        f"*Instructions:*\n{task.instructions}\n\n"
        f"Use `/mytasks` to start working on this task.",
        parse_mode='Markdown'
    )


async def handle_task_start(query, session, assignment_id):
    """Handle task start from inline button."""
    try:
        assignment = TaskAssignment.objects.get(
            id=assignment_id,
            user=session.user,
            status=TaskAssignment.Status.ASSIGNED
        )
    except TaskAssignment.DoesNotExist:
        await query.edit_message_text(
            "❌ This task assignment is no longer available.",
            parse_mode='Markdown'
        )
        return

    # Update assignment status
    assignment.status = TaskAssignment.Status.IN_PROGRESS
    assignment.save(update_fields=['status'])

    await query.edit_message_text(
        f"🚧 *Task Started!*\n\n"
        f"*Task:* {assignment.task.title}\n"
        f"*Status:* In Progress\n\n"
        f"*Instructions:*\n{assignment.task.instructions}\n\n"
        f"*Target URL:* {assignment.task.target_url or 'N/A'}\n"
        f"*Hashtags:* {assignment.task.hashtags or 'N/A'}\n\n"
        f"Once you complete the task, use `/mytasks` to submit proof.",
        parse_mode='Markdown'
    )


async def start_task_proof_submission(query, session, assignment_id, context):
    """Start the task proof submission conversation."""
    try:
        assignment = TaskAssignment.objects.get(
            id=assignment_id,
            user=session.user,
            status=TaskAssignment.Status.IN_PROGRESS
        )
    except TaskAssignment.DoesNotExist:
        await query.edit_message_text(
            "❌ This task is not in progress or no longer available.",
            parse_mode='Markdown'
        )
        return

    # Store assignment ID in context for the conversation
    context.user_data['proof_submission'] = {
        'assignment_id': assignment_id,
        'task_title': assignment.task.title
    }

    # Update session state
    session.update_state(
        TelegramSession.State.AWAITING_TASK_PROOF,
        {'assignment_id': assignment_id}
    )

    await query.edit_message_text(
        f"📤 *Submit Task Proof*\n\n"
        f"*Task:* {assignment.task.title}\n\n"
        f"Please provide proof of completion:\n"
        f"• For Twitter tasks: Screenshot of your post/retweet/like\n"
        f"• For Telegram tasks: Screenshot of your share/invite\n"
        f"• For content creation: Link to your content\n"
        f"• For research: Summary of your findings\n\n"
        f"*Send your proof as a photo, document, or text message.*\n"
        f"Type /cancel to cancel submission.",
        parse_mode='Markdown'
    )

    return AWAITING_TASK_PROOF


async def receive_task_proof(update: Update, context: CallbackContext):
    """Receive task proof from user."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Get session
    try:
        session = TelegramSession.objects.get(telegram_id=user.id)
    except TelegramSession.DoesNotExist:
        await update.message.reply_text("Session not found. Please start over with /start.")
        return ConversationHandler.END

    # Get assignment from context
    proof_data = context.user_data.get('proof_submission')
    if not proof_data:
        await update.message.reply_text("No task found for proof submission. Please start over.")
        session.update_state(TelegramSession.State.IDLE)
        return ConversationHandler.END

    assignment_id = proof_data['assignment_id']
    task_title = proof_data['task_title']

    try:
        assignment = TaskAssignment.objects.get(
            id=assignment_id,
            user=session.user,
            status=TaskAssignment.Status.IN_PROGRESS
        )
    except TaskAssignment.DoesNotExist:
        await update.message.reply_text("Task assignment not found or already completed.")
        session.update_state(TelegramSession.State.IDLE)
        return ConversationHandler.END

    # Store proof in context
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

    # Store proof for confirmation
    context.user_data['proof_details'] = {
        'content': proof_content,
        'type': proof_type,
        'assignment_id': assignment_id
    }

    # Update session state
    session.update_state(
        TelegramSession.State.AWAITING_CONFIRMATION,
        {'proof_type': proof_type}
    )

    # Ask for confirmation
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
    chat_id = update.effective_chat.id

    # Get session
    try:
        session = TelegramSession.objects.get(telegram_id=user.id)
    except TelegramSession.DoesNotExist:
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
    try:
        assignment = TaskAssignment.objects.get(
            id=assignment_id,
            user=session.user,
            status=TaskAssignment.Status.IN_PROGRESS
        )
    except TaskAssignment.DoesNotExist:
        await query.edit_message_text("Task assignment not found.")
        session.update_state(TelegramSession.State.IDLE)
        return

    # Get proof details from context
    proof_details = context.user_data.get('proof_details', {})
    if not proof_details or proof_details.get('assignment_id') != assignment_id:
        await query.edit_message_text("Proof details not found. Please submit proof again.")
        session.update_state(TelegramSession.State.IDLE)
        return

    # Update assignment
    assignment.status = TaskAssignment.Status.PENDING_REVIEW
    assignment.proof_submitted = True
    assignment.proof_type = proof_details.get('type', 'text')
    assignment.proof_content = proof_details.get('content', '')
    assignment.save(update_fields=['status', 'proof_submitted', 'proof_type', 'proof_content'])

    # Update task completion count
    task = assignment.task
    task.completed_assignments += 1
    task.save(update_fields=['completed_assignments'])

    # Update user points (pending verification)
    # Points will be awarded after verification by campaign manager

    # Clear context data
    context.user_data.pop('proof_submission', None)
    context.user_data.pop('proof_details', None)

    # Update session state
    session.update_state(TelegramSession.State.IDLE)

    await query.edit_message_text(
        f"✅ *Proof Submitted Successfully!*\n\n"
        f"*Task:* {task.title}\n"
        f"*Status:* Pending Review\n"
        f"*Points:* {task.points} (pending verification)\n\n"
        f"Your proof has been submitted for review by the campaign manager.\n"
        f"You'll be notified once it's verified and points are awarded.",
        parse_mode='Markdown'
    )


async def cancel_proof_submission(query, session):
    """Cancel proof submission."""
    session.update_state(TelegramSession.State.IDLE)
    await query.edit_message_text(
        "❌ Proof submission cancelled.\n"
        "Use `/mytasks` to view your tasks and submit proof later.",
        parse_mode='Markdown'
    )


async def cancel_conversation(update: Update, context: CallbackContext):
    """Cancel any ongoing conversation."""
    user = update.effective_user

    try:
        session = TelegramSession.objects.get(telegram_id=user.id)
        session.update_state(TelegramSession.State.IDLE)
    except TelegramSession.DoesNotExist:
        pass

    # Clear context data
    context.user_data.clear()

    await update.message.reply_text(
        "❌ Operation cancelled.\n"
        "You can start over with any command.",
        parse_mode='Markdown'
    )
    return ConversationHandler.END


async def validate_task_claim(user, task):
    """Validate if user can claim a task."""
    # Check if task is from user's campaign
    if not CampaignVolunteer.objects.filter(campaign=task.campaign, user=user).exists():
        return "❌ You need to join this campaign first to claim its tasks."

    # Check if task has available slots
    if task.current_assignments >= task.max_assignments:
        return "❌ This task is already fully assigned."

    # Check if user already has this task
    if TaskAssignment.objects.filter(task=task, user=user).exists():
        return "❌ You've already claimed this task."

    return None


async def get_or_create_session(user, chat_id):
    """Get or create Telegram session for user."""
    try:
        session = TelegramSession.objects.get(telegram_id=user.id)
        session.telegram_username = user.username
        session.telegram_chat_id = chat_id
        session.save(update_fields=['telegram_username', 'telegram_chat_id', 'updated_at'])
        return session, False
    except TelegramSession.DoesNotExist:
        # Try to find existing user by Telegram ID
        try:
            db_user = User.objects.get(telegram_id=user.id)
        except User.DoesNotExist:
            db_user = None

        session = TelegramSession.objects.create(
            telegram_id=user.id,
            telegram_username=user.username,
            telegram_chat_id=chat_id,
            user=db_user
        )
        return session, True


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
"""
Telegram bot handlers package.
Exports all handler functions and handler lists.
"""

# Import handler functions
from .start import start_command, help_command, language_command, language_callback_handler
from .campaigns import campaigns_command, joincampaign_command, campaign_callback_handler, campaign_handlers
from .tasks import (
    tasks_command, mytasks_command, claimtask_command,
    task_callback_handler, task_proof_conversation, task_handlers
)
from .profile import profile_command, updateprofile_command
from .leaderboard import leaderboard_command, leaderboard_callback_handler, leaderboard_handlers
from .storms import storms_command, storminfo_command, storm_callback_handler, storm_handlers
from .registration import (
    handle_text_message, handle_unknown_command,
    cancel_registration, registration_conversation,
    text_message_handler, unknown_command_handler
)

# Export handler functions
__all__ = [
    # Command handlers
    'start_command',
    'help_command',
    'campaigns_command',
    'joincampaign_command',
    'tasks_command',
    'mytasks_command',
    'claimtask_command',
    'profile_command',
    'updateprofile_command',
    'leaderboard_command',
    'storms_command',
    'storminfo_command',

    # Callback handlers
    'campaign_callback_handler',
    'task_callback_handler',
    'leaderboard_callback_handler',
    'storm_callback_handler',
    'language_callback_handler',

    # Conversation handlers
    'task_proof_conversation',
    'registration_conversation',

    # Message handlers
    'handle_text_message',
    'handle_unknown_command',
    'cancel_registration',

    # Handler lists for registration
    'campaign_handlers',
    'task_handlers',
    'leaderboard_handlers',
    'storm_handlers',
    'text_message_handler',
    'unknown_command_handler',
]
"""
Telegram models for PFP Campaign Manager.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class TelegramSession(models.Model):
    """
    Manages Telegram bot conversation state for users.
    """
    class State(models.TextChoices):
        IDLE = 'idle', _('Idle')
        AWAITING_NAME = 'awaiting_name', _('Awaiting Name')
        AWAITING_EMAIL = 'awaiting_email', _('Awaiting Email')
        AWAITING_TASK_PROOF = 'awaiting_task_proof', _('Awaiting Task Proof')
        AWAITING_CAMPAIGN_CHOICE = 'awaiting_campaign_choice', _('Awaiting Campaign Choice')
        AWAITING_TASK_CHOICE = 'awaiting_task_choice', _('Awaiting Task Choice')
        AWAITING_CONFIRMATION = 'awaiting_confirmation', _('Awaiting Confirmation')

    # Telegram user information
    telegram_id = models.BigIntegerField(
        unique=True,
        help_text=_('Telegram user ID')
    )
    telegram_username = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text=_('Telegram username')
    )
    telegram_chat_id = models.BigIntegerField(
        help_text=_('Telegram chat ID for messaging')
    )

    # Linked Django user (if registered)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='telegram_sessions'
    )

    # Conversation state
    state = models.CharField(
        max_length=50,
        choices=State.choices,
        default=State.IDLE,
        help_text=_('Current conversation state')
    )
    state_data = models.JSONField(
        default=dict,
        help_text=_('Data associated with current state')
    )

    # Temporary data storage
    temp_data = models.JSONField(
        default=dict,
        help_text=_('Temporary data storage for conversation flow')
    )

    # Bot interaction tracking
    last_interaction = models.DateTimeField(
        auto_now=True,
        help_text=_('Last interaction with the bot')
    )
    total_messages = models.IntegerField(
        default=0,
        help_text=_('Total messages exchanged')
    )
    commands_used = models.JSONField(
        default=dict,
        help_text=_('Count of commands used by this user')
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Telegram Session')
        verbose_name_plural = _('Telegram Sessions')
        indexes = [
            models.Index(fields=['telegram_id']),
            models.Index(fields=['state']),
            models.Index(fields=['last_interaction']),
        ]

    def __str__(self):
        if self.user:
            return f'{self.user.username} ({self.telegram_id})'
        return f'Anonymous ({self.telegram_id})'

    def update_state(self, new_state, state_data=None):
        """Update conversation state."""
        self.state = new_state
        if state_data is not None:
            self.state_data = state_data
        self.save(update_fields=['state', 'state_data', 'updated_at'])

    def increment_message_count(self):
        """Increment total message count."""
        self.total_messages += 1
        self.save(update_fields=['total_messages', 'updated_at'])

    def record_command(self, command):
        """Record usage of a command."""
        if command not in self.commands_used:
            self.commands_used[command] = 0
        self.commands_used[command] += 1
        self.save(update_fields=['commands_used', 'updated_at'])


class TelegramMessageLog(models.Model):
    """
    Log of Telegram messages for auditing and analytics.
    """
    session = models.ForeignKey(
        TelegramSession,
        on_delete=models.CASCADE,
        related_name='message_logs'
    )
    message_id = models.BigIntegerField(
        help_text=_('Telegram message ID')
    )
    chat_id = models.BigIntegerField(
        help_text=_('Telegram chat ID')
    )
    from_user = models.JSONField(
        help_text=_('User information from Telegram')
    )
    message_type = models.CharField(
        max_length=20,
        choices=[
            ('text', _('Text')),
            ('command', _('Command')),
            ('callback_query', _('Callback Query')),
            ('photo', _('Photo')),
            ('document', _('Document')),
        ],
        help_text=_('Type of message')
    )
    content = models.TextField(
        help_text=_('Message content')
    )
    bot_response = models.TextField(
        null=True,
        blank=True,
        help_text=_('Bot response to this message')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Telegram Message Log')
        verbose_name_plural = _('Telegram Message Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Message {self.message_id} from {self.from_user.get("username", "unknown")}'
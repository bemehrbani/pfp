"""
User models for PFP Campaign Manager.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model with role-based permissions and Telegram integration.
    """
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        CAMPAIGN_MANAGER = 'campaign_manager', _('Campaign Manager')
        VOLUNTEER = 'volunteer', _('Volunteer')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VOLUNTEER,
        help_text=_('User role in the system')
    )

    # Telegram integration
    telegram_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        help_text=_('Telegram user ID for bot communication')
    )
    telegram_username = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text=_('Telegram username (without @)')
    )
    telegram_chat_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text=_('Telegram chat ID for direct messaging')
    )

    # Profile fields
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text=_('Phone number for SMS notifications')
    )
    email_verified = models.BooleanField(
        default=False,
        help_text=_('Whether the email address has been verified')
    )
    phone_verified = models.BooleanField(
        default=False,
        help_text=_('Whether the phone number has been verified')
    )

    # Points system for volunteers
    points = models.IntegerField(
        default=0,
        help_text=_('Points earned by completing tasks')
    )
    level = models.IntegerField(
        default=1,
        help_text=_('Volunteer level based on points')
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        indexes = [
            models.Index(fields=['telegram_id']),
            models.Index(fields=['role']),
            models.Index(fields=['points']),
        ]

    def __str__(self):
        return f'{self.username} ({self.role})'

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_campaign_manager(self):
        return self.role == self.Role.CAMPAIGN_MANAGER

    def is_volunteer(self):
        return self.role == self.Role.VOLUNTEER

    def update_level(self):
        """Update user level based on points."""
        # Simple level formula: level = floor(points / 100) + 1
        new_level = (self.points // 100) + 1
        if new_level != self.level:
            self.level = new_level
            self.save(update_fields=['level'])
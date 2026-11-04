"""
Analytics models for PFP Campaign Manager.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class ActivityLog(models.Model):
    """
    Log of user activities for analytics.
    """
    class ActionType(models.TextChoices):
        # User actions
        USER_LOGIN = 'user_login', _('User Login')
        USER_LOGOUT = 'user_logout', _('User Logout')
        USER_REGISTER = 'user_register', _('User Register')
        USER_UPDATE = 'user_update', _('User Update')
        TELEGRAM_LINK = 'telegram_link', _('Telegram Link')

        # Campaign actions
        CAMPAIGN_CREATE = 'campaign_create', _('Campaign Create')
        CAMPAIGN_UPDATE = 'campaign_update', _('Campaign Update')
        CAMPAIGN_JOIN = 'campaign_join', _('Campaign Join')
        CAMPAIGN_LEAVE = 'campaign_leave', _('Campaign Leave')

        # Task actions
        TASK_CREATE = 'task_create', _('Task Create')
        TASK_UPDATE = 'task_update', _('Task Update')
        TASK_ASSIGN = 'task_assign', _('Task Assign')
        TASK_COMPLETE = 'task_complete', _('Task Complete')
        TASK_VERIFY = 'task_verify', _('Task Verify')

        # Twitter actions
        TWITTER_POST = 'twitter_post', _('Twitter Post')
        TWITTER_RETWEET = 'twitter_retweet', _('Twitter Retweet')
        TWITTER_LIKE = 'twitter_like', _('Twitter Like')

        # Telegram actions
        TELEGRAM_MESSAGE = 'telegram_message', _('Telegram Message')
        TELEGRAM_COMMAND = 'telegram_command', _('Telegram Command')

    # User who performed the action
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        null=True,
        blank=True
    )

    # Action details
    action_type = models.CharField(
        max_length=50,
        choices=ActionType.choices,
        help_text=_('Type of action performed')
    )
    description = models.TextField(
        help_text=_('Human-readable description of the action')
    )

    # Generic foreign key to any related object
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Additional data as JSON
    metadata = models.JSONField(
        default=dict,
        help_text=_('Additional metadata about the action')
    )

    # IP and user agent for web actions
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['action_type']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.action_type} by {self.user} at {self.created_at}'


class AnalyticsSnapshot(models.Model):
    """
    Snapshot of analytics data for reporting.
    """
    snapshot_type = models.CharField(
        max_length=50,
        choices=[
            ('daily', _('Daily')),
            ('weekly', _('Weekly')),
            ('monthly', _('Monthly')),
        ],
        help_text=_('Type of snapshot')
    )
    snapshot_date = models.DateField(
        help_text=_('Date the snapshot represents')
    )

    # User metrics
    total_users = models.IntegerField(default=0)
    new_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)

    # Campaign metrics
    total_campaigns = models.IntegerField(default=0)
    active_campaigns = models.IntegerField(default=0)
    completed_campaigns = models.IntegerField(default=0)

    # Task metrics
    total_tasks = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)
    verification_rate = models.FloatField(default=0)

    # Engagement metrics
    total_points_awarded = models.IntegerField(default=0)
    avg_points_per_user = models.FloatField(default=0)
    avg_tasks_per_user = models.FloatField(default=0)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Analytics Snapshot')
        verbose_name_plural = _('Analytics Snapshots')
        unique_together = [('snapshot_type', 'snapshot_date')]
        ordering = ['-snapshot_date', 'snapshot_type']

    def __str__(self):
        return f'{self.snapshot_type} snapshot for {self.snapshot_date}'


class PageViewEvent(models.Model):
    """
    Lightweight, cookie-free first-party web analytics event.
    Stores salted daily visitor hash instead of raw visitor IP.
    """
    class EventType(models.TextChoices):
        PAGEVIEW = 'pageview', _('Pageview')
        PDF_DOWNLOAD = 'pdf_download', _('PDF Download')
        VOW_OPEN = 'vow_open', _('Accountability Vow Modal Opened')
        VOW_SIGNED = 'vow_signed', _('Accountability Vow Signed')

    path = models.CharField(
        max_length=255,
        help_text=_('Normalized page or document path')
    )
    event_type = models.CharField(
        max_length=32,
        choices=EventType.choices,
        default=EventType.PAGEVIEW,
        help_text=_('Type of web event')
    )
    referrer = models.CharField(
        max_length=500,
        blank=True,
        default='',
        help_text=_('HTTP referrer URL')
    )
    country = models.CharField(
        max_length=8,
        blank=True,
        default='',
        help_text=_('Two-letter country code from Cloudflare CF-IPCountry')
    )
    lang = models.CharField(
        max_length=16,
        blank=True,
        default='',
        help_text=_('Active UI or browser language')
    )
    screen_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_('Viewport width in pixels')
    )
    visitor_hash = models.CharField(
        max_length=32,
        blank=True,
        default='',
        help_text=_('Salted daily SHA-256 visitor hash (no raw IP stored)')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Page View Event')
        verbose_name_plural = _('Page View Events')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['path', 'created_at']),
            models.Index(fields=['visitor_hash']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.event_type} {self.path} ({self.country or "XX"}) at {self.created_at}'

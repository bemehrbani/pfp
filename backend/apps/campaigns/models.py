"""
Campaign models for PFP Campaign Manager.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Campaign(models.Model):
    """
    Campaign model representing a People for Peace campaign.
    """
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        ACTIVE = 'active', _('Active')
        PAUSED = 'paused', _('Paused')
        COMPLETED = 'completed', _('Completed')
        ARCHIVED = 'archived', _('Archived')

    class CampaignType(models.TextChoices):
        REGULAR = 'regular', _('Regular Campaign')
        TWITTER_STORM = 'twitter_storm', _('Twitter Storm')
        HYBRID = 'hybrid', _('Hybrid (Regular + Twitter Storm)')

    # Basic information
    name = models.CharField(
        max_length=200,
        help_text=_('Campaign name')
    )
    description = models.TextField(
        help_text=_('Detailed description of the campaign')
    )
    short_description = models.CharField(
        max_length=500,
        help_text=_('Short description for listings')
    )

    # Campaign type and status
    campaign_type = models.CharField(
        max_length=20,
        choices=CampaignType.choices,
        default=CampaignType.REGULAR,
        help_text=_('Type of campaign')
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text=_('Current status of the campaign')
    )

    # Goals
    target_members = models.IntegerField(
        default=0,
        help_text=_('Target number of core members')
    )
    target_activities = models.IntegerField(
        default=0,
        help_text=_('Target number of activities')
    )
    target_twitter_posts = models.IntegerField(
        default=0,
        help_text=_('Target number of Twitter posts (for Twitter storms)')
    )

    # Twitter storm specific fields
    twitter_hashtags = models.CharField(
        max_length=500,
        blank=True,
        help_text=_('Comma-separated list of hashtags for Twitter storm')
    )
    twitter_accounts = models.CharField(
        max_length=500,
        blank=True,
        help_text=_('Comma-separated list of Twitter accounts to mention')
    )
    twitter_storm_schedule = models.JSONField(
        null=True,
        blank=True,
        help_text=_('Schedule for Twitter storm activities')
    )

    # Telegram integration
    telegram_channel_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text=_('Telegram channel ID for campaign announcements')
    )
    telegram_group_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text=_('Telegram group ID for campaign coordination')
    )

    # Ownership and management
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_campaigns',
        help_text=_('User who created the campaign')
    )
    managers = models.ManyToManyField(
        User,
        related_name='managed_campaigns',
        blank=True,
        help_text=_('Campaign managers')
    )
    volunteers = models.ManyToManyField(
        User,
        related_name='volunteered_campaigns',
        through='CampaignVolunteer',
        blank=True,
        help_text=_('Volunteers participating in this campaign')
    )

    # Timelines
    start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Planned start date')
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Planned end date')
    )
    actual_start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Actual start date')
    )
    actual_end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Actual end date')
    )

    # Statistics (denormalized for performance)
    current_members = models.IntegerField(
        default=0,
        help_text=_('Current number of core members')
    )
    completed_activities = models.IntegerField(
        default=0,
        help_text=_('Number of completed activities')
    )
    completed_twitter_posts = models.IntegerField(
        default=0,
        help_text=_('Number of completed Twitter posts')
    )
    total_points_awarded = models.IntegerField(
        default=0,
        help_text=_('Total points awarded in this campaign')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['campaign_type']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save campaign and update statistics."""
        # If update_fields is specified, skip statistics update (just save)
        if 'update_fields' in kwargs:
            super().save(*args, **kwargs)
            return

        # Save first to get ID for many-to-many relationships
        super().save(*args, **kwargs)

        # Update statistics after saving
        self.update_statistics()

        # Save statistics fields only
        super().save(update_fields=['current_members', 'completed_activities', 'completed_twitter_posts'])

    def update_statistics(self):
        """Update denormalized statistics."""
        from apps.tasks.models import TaskAssignment
        from .models import CampaignVolunteer

        # Update current members count
        self.current_members = self.volunteers.count()

        # Update completed activities count
        completed_assignments = TaskAssignment.objects.filter(
            task__campaign=self,
            status=TaskAssignment.Status.COMPLETED
        ).count()
        self.completed_activities = completed_assignments

        # Update Twitter posts count (for Twitter storm campaigns)
        if self.campaign_type in [self.CampaignType.TWITTER_STORM, self.CampaignType.HYBRID]:
            twitter_completed = TaskAssignment.objects.filter(
                task__campaign=self,
                task__task_type='twitter_post',
                status=TaskAssignment.Status.COMPLETED
            ).count()
            self.completed_twitter_posts = twitter_completed

    def progress_percentage(self):
        """Calculate overall progress percentage."""
        total_target = 0
        total_completed = 0

        # Members progress
        if self.target_members > 0:
            total_target += self.target_members
            total_completed += min(self.current_members, self.target_members)

        # Activities progress
        if self.target_activities > 0:
            total_target += self.target_activities
            total_completed += min(self.completed_activities, self.target_activities)

        # Twitter posts progress
        if self.target_twitter_posts > 0:
            total_target += self.target_twitter_posts
            total_completed += min(self.completed_twitter_posts, self.target_twitter_posts)

        if total_target == 0:
            return 0
        return (total_completed / total_target) * 100

    def is_active(self):
        return self.status == self.Status.ACTIVE

    def is_twitter_storm(self):
        return self.campaign_type in [self.CampaignType.TWITTER_STORM, self.CampaignType.HYBRID]


class CampaignVolunteer(models.Model):
    """
    Through model for Campaign volunteers with additional data.
    """
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
        BANNED = 'banned', _('Banned')

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    points_earned = models.IntegerField(default=0)

    class Meta:
        unique_together = [('campaign', 'volunteer')]
        verbose_name = _('Campaign Volunteer')
        verbose_name_plural = _('Campaign Volunteers')

    def __str__(self):
        return f'{self.volunteer.username} - {self.campaign.name}'


class CampaignUpdate(models.Model):
    """
    Updates and announcements for a campaign.
    """
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='updates'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    sent_to_telegram = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-created_at']
        verbose_name = _('Campaign Update')
        verbose_name_plural = _('Campaign Updates')

    def __str__(self):
        return self.title
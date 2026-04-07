"""
Task models for PFP Campaign Manager.
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.campaigns.models import Campaign

User = get_user_model()


class Task(models.Model):
    """
    Task model representing a social media action or other campaign activity.
    """
    class TaskType(models.TextChoices):
        TWITTER_POST = 'twitter_post', _('Twitter Post')
        TWITTER_RETWEET = 'twitter_retweet', _('Twitter Retweet')
        TWITTER_COMMENT = 'twitter_comment', _('Twitter Comment')
        TWITTER_LIKE = 'twitter_like', _('Twitter Like')
        TELEGRAM_SHARE = 'telegram_share', _('Telegram Share')
        TELEGRAM_INVITE = 'telegram_invite', _('Telegram Invite')
        CONTENT_CREATION = 'content_creation', _('Content Creation')
        PETITION = 'petition', _('Petition')
        MASS_EMAIL = 'mass_email', _('Mass Email')

    class AssignmentType(models.TextChoices):
        FIRST_COME = 'first_come', _('First Come, First Served')
        MANUAL = 'manual', _('Manual Assignment')
        AUTOMATIC = 'automatic', _('Automatic Assignment')

    # Basic information
    title = models.CharField(
        max_length=200,
        help_text=_('Task title (English)')
    )
    title_fa = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text=_('Task title (Farsi)')
    )
    title_ar = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text=_('Task title (Arabic)')
    )
    description = models.TextField(
        help_text=_('Detailed task description (English)')
    )
    description_fa = models.TextField(
        blank=True,
        default='',
        help_text=_('Detailed task description (Farsi)')
    )
    description_ar = models.TextField(
        blank=True,
        default='',
        help_text=_('Detailed task description (Arabic)')
    )
    instructions = models.TextField(
        help_text=_('Step-by-step instructions for volunteers')
    )
    instructions_fa = models.TextField(
        blank=True,
        default='',
        help_text=_('Instructions (Farsi)')
    )
    instructions_ar = models.TextField(
        blank=True,
        default='',
        help_text=_('Instructions (Arabic)')
    )

    def localized_title(self, lang: str = 'en') -> str:
        """Return title in the requested language, falling back to English."""
        if lang == 'fa' and self.title_fa:
            return self.title_fa
        if lang == 'ar' and self.title_ar:
            return self.title_ar
        return self.title

    def localized_description(self, lang: str = 'en') -> str:
        """Return description in the requested language, falling back to English."""
        if lang == 'fa' and self.description_fa:
            return self.description_fa
        if lang == 'ar' and self.description_ar:
            return self.description_ar
        return self.description

    def localized_instructions(self, lang: str = 'en') -> str:
        """Return instructions in the requested language, falling back to English."""
        if lang == 'fa' and self.instructions_fa:
            return self.instructions_fa
        if lang == 'ar' and self.instructions_ar:
            return self.instructions_ar
        return self.instructions

    # Task type and assignment
    task_type = models.CharField(
        max_length=50,
        choices=TaskType.choices,
        help_text=_('Type of task')
    )
    assignment_type = models.CharField(
        max_length=20,
        choices=AssignmentType.choices,
        default=AssignmentType.FIRST_COME,
        help_text=_('How tasks are assigned to volunteers')
    )

    # Campaign relationship
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text=_('Campaign this task belongs to')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        help_text=_('User who created the task')
    )

    # Task requirements and rewards
    points = models.IntegerField(
        default=10,
        help_text=_('Points awarded for completing this task')
    )
    estimated_time = models.IntegerField(
        default=15,
        help_text=_('Estimated time to complete in minutes')
    )
    max_assignments = models.IntegerField(
        default=1,
        help_text=_('Maximum number of volunteers who can complete this task')
    )
    current_assignments = models.IntegerField(
        default=0,
        help_text=_('Number of volunteers currently assigned')
    )
    completed_assignments = models.IntegerField(
        default=0,
        help_text=_('Number of volunteers who completed this task')
    )

    # Task URLs and resources
    target_url = models.URLField(
        blank=True,
        help_text=_('URL for the task (e.g., tweet to retweet)')
    )
    hashtags = models.CharField(
        max_length=500,
        blank=True,
        help_text=_('Comma-separated list of hashtags')
    )
    mentions = models.CharField(
        max_length=500,
        blank=True,
        help_text=_('Comma-separated list of accounts to mention')
    )
    image_url = models.URLField(
        blank=True,
        help_text=_('URL of image to use (if applicable)')
    )

    # Status and availability
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether the task is available for assignment')
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Whether the task has been verified by a manager')
    )
    available_from = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Date/time when task becomes available')
    )
    available_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Date/time when task is no longer available')
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['available_from', 'available_until']),
        ]

    def __str__(self):
        return f'{self.title} ({self.campaign.name})'

    def is_available(self):
        """Check if task is available for assignment."""
        if not self.is_active or not self.is_verified:
            return False

        if self.available_from and timezone.now() < self.available_from:
            return False

        if self.available_until and timezone.now() > self.available_until:
            return False

        if self.current_assignments >= self.max_assignments:
            return False

        return True

    def available_slots(self):
        """Calculate number of available slots."""
        return max(0, self.max_assignments - self.current_assignments)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_is_active = None
        
        if not hasattr(self, '_changed_fields'):
            self._changed_fields = set()
            
        if not is_new:
            try:
                old_instance = Task.objects.get(pk=self.pk)
                old_is_active = old_instance.is_active
                if old_is_active != self.is_active:
                    self._changed_fields.add('is_active')
            except Task.DoesNotExist:
                pass
                
        super().save(*args, **kwargs)


class KeyTweet(models.Model):
    """
    A curated tweet from a key figure that volunteers should comment on.
    Used primarily for twitter_comment tasks.
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='key_tweets',
        help_text=_('Task this key tweet belongs to')
    )
    tweet_url = models.URLField(
        help_text=_('URL of the tweet to comment on')
    )
    author_name = models.CharField(
        max_length=200,
        help_text=_('Display name of the tweet author (e.g. "United Nations")')
    )
    author_handle = models.CharField(
        max_length=100,
        help_text=_('Twitter handle of the author (e.g. "@UN")')
    )
    description = models.TextField(
        blank=True,
        help_text=_('Brief description of the tweet content or why it matters')
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text=_('Display order (lower numbers shown first)')
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this key tweet is currently active')
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Key Tweet')
        verbose_name_plural = _('Key Tweets')
        ordering = ['order', '-created_at']

    def __str__(self):
        return f'{self.author_handle}: {self.tweet_url}'


class TaskAssignment(models.Model):
    """
    Assignment of a task to a volunteer.
    """
    class Status(models.TextChoices):
        ASSIGNED = 'assigned', _('Assigned')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        VERIFIED = 'verified', _('Verified')
        REJECTED = 'rejected', _('Rejected')
        CANCELLED = 'cancelled', _('Cancelled')

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task_assignments'
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='task_assignments'
    )

    # Assignment details
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ASSIGNED
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    # Completion details
    proof_url = models.URLField(
        blank=True,
        help_text=_('URL proof of completion (e.g., tweet link)')
    )
    proof_text = models.TextField(
        blank=True,
        help_text=_('Text proof of completion')
    )
    proof_image = models.URLField(
        blank=True,
        help_text=_('Image proof of completion')
    )
    completion_notes = models.TextField(
        blank=True,
        help_text=_('Volunteer notes about completion')
    )
    verification_notes = models.TextField(
        blank=True,
        help_text=_('Manager notes about verification')
    )

    # Points and rewards
    points_awarded = models.IntegerField(
        default=0,
        help_text=_('Points awarded for this assignment')
    )
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_tasks'
    )

    # Timestamps
    assigned_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Task Assignment')
        verbose_name_plural = _('Task Assignments')
        unique_together = [('task', 'volunteer')]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['volunteer', 'status']),
            models.Index(fields=['assigned_at']),
        ]

    def __str__(self):
        return f'{self.volunteer.username} - {self.task.title}'

    def save(self, *args, **kwargs):
        """Update task statistics when assignment status changes."""
        is_new = self.pk is None
        old_status = None
        
        if not hasattr(self, '_changed_fields'):
            self._changed_fields = set()
            
        if not is_new:
            try:
                old_instance = TaskAssignment.objects.get(pk=self.pk)
                old_status = old_instance.status
                if old_status != self.status:
                    self._changed_fields.add('status')
            except TaskAssignment.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Update task statistics
        if is_new or old_status != self.status:
            self.update_task_statistics()

        # Update volunteer points if completed and verified
        if self.status == self.Status.VERIFIED and old_status != self.Status.VERIFIED:
            self.award_points()

    def update_task_statistics(self):
        """Update task assignment counts."""
        task = self.task
        task.current_assignments = task.assignments.filter(
            status__in=[self.Status.ASSIGNED, self.Status.IN_PROGRESS]
        ).count()
        task.completed_assignments = task.assignments.filter(
            status__in=[self.Status.COMPLETED, self.Status.VERIFIED]
        ).count()
        task.save(update_fields=['current_assignments', 'completed_assignments'])

    def award_points(self):
        """Award points to volunteer."""
        if self.points_awarded <= 0:
            self.points_awarded = self.task.points
            self.save(update_fields=['points_awarded'])

        self.volunteer.points += self.points_awarded
        self.volunteer.save(update_fields=['points'])
        self.volunteer.update_level()

        # Update campaign total points
        self.campaign.total_points_awarded += self.points_awarded
        self.campaign.save(update_fields=['total_points_awarded'])

        # Update campaign volunteer points
        from apps.campaigns.models import CampaignVolunteer
        try:
            campaign_volunteer = CampaignVolunteer.objects.get(
                campaign=self.campaign,
                volunteer=self.volunteer
            )
            campaign_volunteer.points_earned += self.points_awarded
            campaign_volunteer.save(update_fields=['points_earned'])
        except CampaignVolunteer.DoesNotExist:
            pass
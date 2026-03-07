"""
Admin configuration for Campaigns app.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Campaign, CampaignVolunteer, CampaignUpdate, TwitterStorm, StormParticipant


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """Admin interface for Campaign model."""

    list_display = (
        'name', 'campaign_type', 'status', 'created_by',
        'current_members', 'completed_activities', 'progress_percentage',
        'created_at'
    )
    list_filter = ('campaign_type', 'status', 'created_at', 'start_date')
    search_fields = ('name', 'description', 'created_by__username')
    readonly_fields = (
        'current_members', 'completed_activities', 'completed_twitter_posts',
        'total_points_awarded', 'created_at', 'updated_at'
    )
    filter_horizontal = ('managers', 'volunteers')
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'short_description')
        }),
        (_('Type & Status'), {
            'fields': ('campaign_type', 'status')
        }),
        (_('Goals'), {
            'fields': (
                'target_members', 'target_activities', 'target_twitter_posts'
            )
        }),
        (_('Twitter Storm'), {
            'fields': (
                'twitter_hashtags', 'twitter_accounts', 'twitter_storm_schedule'
            ),
            'classes': ('collapse',)
        }),
        (_('Telegram Integration'), {
            'fields': ('telegram_channel_id', 'telegram_group_id'),
            'classes': ('collapse',)
        }),
        (_('Ownership'), {
            'fields': ('created_by', 'managers')
        }),
        (_('Timelines'), {
            'fields': (
                'start_date', 'end_date',
                'actual_start_date', 'actual_end_date'
            )
        }),
        (_('Statistics'), {
            'fields': (
                'current_members', 'completed_activities',
                'completed_twitter_posts', 'total_points_awarded'
            )
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def progress_percentage(self, obj):
        """Display progress percentage in admin list."""
        return f'{obj.progress_percentage():.1f}%'
    progress_percentage.short_description = _('Progress')

    def save_model(self, request, obj, form, change):
        """Set created_by if not set."""
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CampaignVolunteer)
class CampaignVolunteerAdmin(admin.ModelAdmin):
    """Admin interface for CampaignVolunteer model."""

    list_display = ('campaign', 'volunteer', 'status', 'points_earned', 'joined_at')
    list_filter = ('status', 'campaign', 'joined_at')
    search_fields = ('campaign__name', 'volunteer__username')
    readonly_fields = ('joined_at', 'last_active')


@admin.register(CampaignUpdate)
class CampaignUpdateAdmin(admin.ModelAdmin):
    """Admin interface for CampaignUpdate model."""

    list_display = ('title', 'campaign', 'created_by', 'is_pinned', 'created_at')
    list_filter = ('is_pinned', 'campaign', 'created_at')
    search_fields = ('title', 'content', 'campaign__name')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        """Set created_by if not set."""
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class StormParticipantInline(admin.TabularInline):
    """Inline for viewing storm participants."""
    model = StormParticipant
    extra = 0
    readonly_fields = ('volunteer', 'status', 'tweet_url', 'posted_at', 'created_at')


@admin.register(TwitterStorm)
class TwitterStormAdmin(admin.ModelAdmin):
    """Admin interface for TwitterStorm model."""

    list_display = (
        'title', 'campaign', 'status', 'scheduled_at',
        'participants_notified', 'tweets_posted', 'created_by'
    )
    list_filter = ('status', 'campaign', 'scheduled_at')
    search_fields = ('title', 'description', 'campaign__name')
    readonly_fields = (
        'participants_notified', 'tweets_posted', 'celery_task_ids',
        'activated_at', 'completed_at', 'created_at', 'updated_at'
    )
    inlines = [StormParticipantInline]

    fieldsets = (
        (None, {
            'fields': ('campaign', 'title', 'description', 'created_by')
        }),
        (_('Schedule'), {
            'fields': ('scheduled_at', 'duration_minutes', 'status')
        }),
        (_('Content'), {
            'fields': ('tweet_templates', 'hashtags', 'mentions')
        }),
        (_('Notifications'), {
            'fields': ('notify_1h', 'notify_15m', 'notify_5m')
        }),
        (_('Statistics'), {
            'fields': (
                'participants_notified', 'tweets_posted',
                'celery_task_ids'
            )
        }),
        (_('Timestamps'), {
            'fields': ('activated_at', 'completed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Set created_by and schedule notifications on creation."""
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

        # Auto-schedule notifications when storm is saved with scheduled status
        if obj.status == TwitterStorm.Status.SCHEDULED:
            from .tasks import schedule_storm_notifications
            schedule_storm_notifications.delay(obj.id)
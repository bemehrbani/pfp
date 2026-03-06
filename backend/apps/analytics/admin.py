"""
Admin configuration for Analytics app.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ActivityLog, AnalyticsSnapshot


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """Admin interface for ActivityLog model."""

    list_display = ('action_type', 'user', 'description', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('user__username', 'description', 'metadata')
    readonly_fields = ('created_at', 'content_type', 'object_id', 'metadata')
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('user', 'action_type', 'description')
        }),
        (_('Related Object'), {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('metadata', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        (_('Timestamp'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Activity logs are created automatically."""
        return False

    def has_change_permission(self, request, obj=None):
        """Activity logs should not be edited."""
        return False


@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    """Admin interface for AnalyticsSnapshot model."""

    list_display = (
        'snapshot_type', 'snapshot_date',
        'total_users', 'active_users',
        'total_campaigns', 'completed_tasks',
        'created_at'
    )
    list_filter = ('snapshot_type', 'snapshot_date')
    readonly_fields = ('created_at',)
    date_hierarchy = 'snapshot_date'

    fieldsets = (
        (None, {
            'fields': ('snapshot_type', 'snapshot_date')
        }),
        (_('User Metrics'), {
            'fields': ('total_users', 'new_users', 'active_users'),
            'classes': ('collapse',)
        }),
        (_('Campaign Metrics'), {
            'fields': ('total_campaigns', 'active_campaigns', 'completed_campaigns'),
            'classes': ('collapse',)
        }),
        (_('Task Metrics'), {
            'fields': ('total_tasks', 'completed_tasks', 'verification_rate'),
            'classes': ('collapse',)
        }),
        (_('Engagement Metrics'), {
            'fields': ('total_points_awarded', 'avg_points_per_user', 'avg_tasks_per_user'),
            'classes': ('collapse',)
        }),
        (_('Timestamp'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def has_change_permission(self, request, obj=None):
        """Analytics snapshots should not be edited."""
        return False
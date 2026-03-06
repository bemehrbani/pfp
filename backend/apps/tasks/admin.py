"""
Admin configuration for Tasks app.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Task, TaskAssignment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for Task model."""

    list_display = (
        'title', 'campaign', 'task_type', 'assignment_type',
        'points', 'is_active', 'is_verified',
        'current_assignments', 'completed_assignments',
        'created_at'
    )
    list_filter = ('task_type', 'assignment_type', 'is_active', 'is_verified', 'created_at')
    search_fields = ('title', 'description', 'campaign__name', 'created_by__username')
    readonly_fields = (
        'current_assignments', 'completed_assignments',
        'created_at', 'updated_at'
    )
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'instructions')
        }),
        (_('Type & Assignment'), {
            'fields': ('task_type', 'assignment_type')
        }),
        (_('Campaign'), {
            'fields': ('campaign', 'created_by')
        }),
        (_('Requirements & Rewards'), {
            'fields': (
                'points', 'estimated_time',
                'max_assignments', 'current_assignments', 'completed_assignments'
            )
        }),
        (_('Resources'), {
            'fields': ('target_url', 'hashtags', 'mentions', 'image_url'),
            'classes': ('collapse',)
        }),
        (_('Availability'), {
            'fields': (
                'is_active', 'is_verified',
                'available_from', 'available_until'
            )
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Set created_by if not set."""
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    """Admin interface for TaskAssignment model."""

    list_display = (
        'task', 'volunteer', 'status', 'points_awarded',
        'assigned_at', 'completed_at', 'verified_at'
    )
    list_filter = ('status', 'task__campaign', 'assigned_at')
    search_fields = (
        'task__title', 'volunteer__username',
        'proof_url', 'proof_text'
    )
    readonly_fields = (
        'assigned_at', 'started_at', 'completed_at', 'verified_at',
        'updated_at'
    )
    date_hierarchy = 'assigned_at'

    fieldsets = (
        (None, {
            'fields': ('task', 'volunteer', 'campaign', 'assigned_by')
        }),
        (_('Status'), {
            'fields': ('status',)
        }),
        (_('Completion Proof'), {
            'fields': ('proof_url', 'proof_text', 'proof_image', 'completion_notes'),
            'classes': ('collapse',)
        }),
        (_('Verification'), {
            'fields': ('verification_notes', 'verified_by', 'points_awarded'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': (
                'assigned_at', 'started_at', 'completed_at',
                'verified_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Set assigned_by if not set."""
        if not obj.pk and not obj.assigned_by:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)
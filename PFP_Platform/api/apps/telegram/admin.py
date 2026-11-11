"""
Admin configuration for Telegram app.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import TelegramSession, TelegramMessageLog, ContactSubmission


@admin.register(TelegramSession)
class TelegramSessionAdmin(admin.ModelAdmin):
    """Admin interface for TelegramSession model."""

    list_display = (
        'telegram_id', 'telegram_username', 'user',
        'state', 'total_messages', 'last_interaction'
    )
    list_filter = ('state', 'created_at', 'last_interaction')
    search_fields = ('telegram_id', 'telegram_username', 'user__username')
    readonly_fields = (
        'telegram_id', 'telegram_chat_id',
        'total_messages', 'commands_used',
        'created_at', 'updated_at', 'last_interaction'
    )
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('telegram_id', 'telegram_username', 'telegram_chat_id', 'user')
        }),
        (_('Conversation State'), {
            'fields': ('state', 'state_data', 'temp_data')
        }),
        (_('Interaction Tracking'), {
            'fields': ('total_messages', 'commands_used', 'last_interaction'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TelegramMessageLog)
class TelegramMessageLogAdmin(admin.ModelAdmin):
    """Admin interface for TelegramMessageLog model."""

    list_display = ('message_id', 'session', 'message_type', 'created_at')
    list_filter = ('message_type', 'created_at')
    search_fields = ('content', 'from_user', 'bot_response')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('session', 'message_id', 'chat_id')
        }),
        (_('Message Details'), {
            'fields': ('from_user', 'message_type', 'content', 'bot_response')
        }),
        (_('Timestamp'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Message logs are created automatically."""
        return False

    def has_change_permission(self, request, obj=None):
        """Message logs should not be edited."""
        return False


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin interface for ContactSubmission model."""

    list_display = (
        'id', 'name', 'email', 'role', 'status',
        'telegram_sent', 'created_at'
    )
    list_filter = ('status', 'telegram_sent', 'created_at')
    search_fields = ('name', 'email', 'role', 'message', 'notes')
    list_editable = ('status',)
    actions = ('export_as_csv',)
    readonly_fields = (
        'created_at', 'updated_at', 'ip_address',
        'user_agent', 'telegram_sent', 'telegram_error'
    )
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'role', 'roles', 'status')
        }),
        (_('Submission Content'), {
            'fields': ('message',)
        }),
        (_('Admin Management'), {
            'fields': ('notes',)
        }),
        (_('Telegram Dispatch Info'), {
            'fields': ('telegram_sent', 'telegram_error'),
            'classes': ('collapse',)
        }),
        (_('Technical Metadata'), {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description=_('Export selected submissions to CSV'))
    def export_as_csv(self, request, queryset):
        """Export selected ContactSubmission records as UTF-8 CSV."""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="contact_submissions.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'id', 'created_at', 'name', 'email', 'status',
            'role_summary', 'selected_roles', 'notes', 'message', 'telegram_sent'
        ])
        for sub in queryset:
            selected_roles = ' ; '.join(sub.roles) if isinstance(sub.roles, list) else ''
            writer.writerow([
                sub.id,
                sub.created_at.isoformat() if sub.created_at else '',
                sub.name,
                sub.email,
                sub.status,
                sub.role,
                selected_roles,
                sub.notes,
                sub.message,
                sub.telegram_sent,
            ])
        return response
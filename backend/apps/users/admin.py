"""
Admin configuration for Users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""

    list_display = ('username', 'email', 'role', 'telegram_username', 'points', 'level', 'is_active')
    list_filter = ('role', 'is_active', 'email_verified', 'phone_verified')
    search_fields = ('username', 'email', 'telegram_username', 'telegram_id')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Telegram info'), {'fields': ('telegram_id', 'telegram_username', 'telegram_chat_id')}),
        (_('Verification'), {'fields': ('email_verified', 'phone_verified')}),
        (_('Role & Points'), {'fields': ('role', 'points', 'level')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        """Make telegram_id readonly after creation."""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj:  # editing an existing object
            readonly_fields.append('telegram_id')
        return readonly_fields
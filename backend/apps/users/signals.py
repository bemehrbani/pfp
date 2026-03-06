"""
Signals for Users app.
"""
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.analytics.models import ActivityLog

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_created_or_updated(sender, instance, created, **kwargs):
    """Log user creation and updates."""
    if created:
        # Log user registration
        ActivityLog.objects.create(
            user=instance,
            action_type=ActivityLog.ActionType.USER_REGISTER,
            description=f'User {instance.username} registered',
            content_object=instance
        )
        logger.info(f'New user registered: {instance.username}')
    else:
        # Log profile updates (simplified - could be more detailed)
        ActivityLog.objects.create(
            user=instance,
            action_type=ActivityLog.ActionType.USER_UPDATE,
            description=f'User {instance.username} profile updated',
            content_object=instance
        )


@receiver(post_save, sender=User)
def link_telegram_account(sender, instance, **kwargs):
    """Handle Telegram account linking."""
    if instance.telegram_id and hasattr(instance, '_telegram_linked'):
        ActivityLog.objects.create(
            user=instance,
            action_type=ActivityLog.ActionType.TELEGRAM_LINK,
            description=f'User {instance.username} linked Telegram account',
            content_object=instance,
            metadata={
                'telegram_id': instance.telegram_id,
                'telegram_username': instance.telegram_username
            }
        )
        logger.info(f'User {instance.username} linked Telegram account {instance.telegram_id}')


@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    """Log user deletion."""
    # Note: We can't create ActivityLog with the user as foreign key
    # since it's being deleted. Log to system logger instead.
    logger.info(f'User deleted: {instance.username} (id: {instance.id})')


def user_logged_in(sender, request, user, **kwargs):
    """Signal receiver for user login."""
    ActivityLog.objects.create(
        user=user,
        action_type=ActivityLog.ActionType.USER_LOGIN,
        description=f'User {user.username} logged in',
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    logger.info(f'User {user.username} logged in from {request.META.get("REMOTE_ADDR")}')


def user_logged_out(sender, request, user, **kwargs):
    """Signal receiver for user logout."""
    if user and user.is_authenticated:
        ActivityLog.objects.create(
            user=user,
            action_type=ActivityLog.ActionType.USER_LOGOUT,
            description=f'User {user.username} logged out',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        logger.info(f'User {user.username} logged out')
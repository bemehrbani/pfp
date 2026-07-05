"""
Django integration utilities for Telegram bot.
Provides functions to access Django models and setup Django environment.
"""
import os
import sys
import logging
from typing import Optional, Any
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

# Flag to track if Django has been set up
_django_setup_done = False


def setup_django():
    """
    Set up Django environment for the bot.
    This must be called before accessing any Django models.
    """
    global _django_setup_done

    if _django_setup_done:
        return

    # Add the backend directory to Python path
    backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backend')
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

    try:
        import django
        django.setup()
        _django_setup_done = True
        logger.info("Django setup completed successfully")
    except Exception as e:
        logger.error(f"Failed to setup Django: {e}")
        raise


def get_django_model(model_name: str):
    """
    Get a Django model by name.

    Args:
        model_name: Name of the model in format 'app.ModelName'

    Returns:
        Django model class

    Raises:
        ImportError: If Django is not set up or model not found
    """
    if not _django_setup_done:
        setup_django()

    try:
        # Split app and model name
        app_label, model_class = model_name.split('.')

        # Import the model
        from django.apps import apps
        model = apps.get_model(app_label, model_class)
        return model
    except (ValueError, LookupError) as e:
        logger.error(f"Failed to get model {model_name}: {e}")
        raise ImportError(f"Model {model_name} not found")


def get_user_by_telegram_id(telegram_id: int):
    """
    Get Django User by Telegram ID.

    Args:
        telegram_id: Telegram user ID

    Returns:
        User object or None if not found
    """
    if not _django_setup_done:
        setup_django()

    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.get(telegram_id=telegram_id)
    except Exception as e:
        logger.debug(f"User not found for telegram_id {telegram_id}: {e}")
        return None


def create_or_update_telegram_session(telegram_id: int, telegram_username: str,
                                      telegram_chat_id: int, user=None):
    """
    Create or update Telegram session for a user.

    Args:
        telegram_id: Telegram user ID
        telegram_username: Telegram username
        telegram_chat_id: Telegram chat ID
        user: Django User object (optional)

    Returns:
        Tuple of (TelegramSession object, created boolean)
    """
    if not _django_setup_done:
        setup_django()

    try:
        from apps.telegram.models import TelegramSession

        # Try to get existing session
        try:
            session = TelegramSession.objects.get(telegram_id=telegram_id)
            session.telegram_username = telegram_username
            session.telegram_chat_id = telegram_chat_id
            if user:
                session.user = user
            session.save(update_fields=['telegram_username', 'telegram_chat_id', 'user', 'updated_at'])
            return session, False
        except TelegramSession.DoesNotExist:
            # Create new session
            session = TelegramSession.objects.create(
                telegram_id=telegram_id,
                telegram_username=telegram_username,
                telegram_chat_id=telegram_chat_id,
                user=user
            )
            return session, True
    except Exception as e:
        logger.error(f"Failed to create/update Telegram session: {e}")
        raise


def log_telegram_message(session, message_id: int, chat_id: int,
                         from_user: dict, message_type: str,
                         content: str, bot_response: Optional[str] = None):
    """
    Log a Telegram message to the database.

    Args:
        session: TelegramSession object
        message_id: Telegram message ID
        chat_id: Telegram chat ID
        from_user: User information dict from Telegram
        message_type: Type of message ('text', 'command', 'callback_query', etc.)
        content: Message content
        bot_response: Bot's response (optional)
    """
    if not _django_setup_done:
        setup_django()

    try:
        from apps.telegram.models import TelegramMessageLog

        TelegramMessageLog.objects.create(
            session=session,
            message_id=message_id,
            chat_id=chat_id,
            from_user=from_user,
            message_type=message_type,
            content=content,
            bot_response=bot_response
        )
    except Exception as e:
        logger.error(f"Failed to log Telegram message: {e}")


def get_active_campaigns_for_user(user):
    """
    Get active campaigns for a user.

    Args:
        user: Django User object

    Returns:
        QuerySet of Campaign objects
    """
    if not _django_setup_done:
        setup_django()

    try:
        from apps.campaigns.models import Campaign, CampaignVolunteer

        # Get campaigns where user is a volunteer
        campaign_ids = CampaignVolunteer.objects.filter(
            user=user,
            campaign__status=Campaign.Status.ACTIVE
        ).values_list('campaign_id', flat=True)

        return Campaign.objects.filter(id__in=campaign_ids, status=Campaign.Status.ACTIVE)
    except Exception as e:
        logger.error(f"Failed to get active campaigns for user: {e}")
        raise


def get_available_tasks_for_user(user):
    """
    Get available tasks for a user (from their active campaigns).

    Args:
        user: Django User object

    Returns:
        QuerySet of Task objects
    """
    if not _django_setup_done:
        setup_django()

    try:
        from apps.campaigns.models import CampaignVolunteer
        from apps.tasks.models import Task

        # Get user's active campaigns
        campaign_ids = CampaignVolunteer.objects.filter(
            user=user,
            campaign__status='active'
        ).values_list('campaign_id', flat=True)

        if not campaign_ids:
            return Task.objects.none()

        # Get available tasks from those campaigns
        tasks = Task.objects.filter(
            campaign_id__in=campaign_ids,
            current_assignments__lt=models.F('max_assignments')
        ).exclude(
            assignments__user=user
        ).order_by('-points', 'created_at')

        return tasks
    except Exception as e:
        logger.error(f"Failed to get available tasks for user: {e}")
        raise


def is_django_available() -> bool:
    """
    Check if Django is available and set up.

    Returns:
        True if Django is available, False otherwise
    """
    try:
        if not _django_setup_done:
            setup_django()
        return True
    except Exception:
        return False
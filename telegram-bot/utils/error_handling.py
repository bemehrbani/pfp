"""
Error handling utilities for Telegram bot.
Provides graceful error handling and user-friendly error messages.
"""
import logging
import traceback
from typing import Optional, Callable, Any
from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext

from .django_integration import is_django_available

logger = logging.getLogger(__name__)


class BotError(Exception):
    """Base exception for bot errors with user-friendly messages."""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message)
        self.user_message = user_message or message


class DjangoUnavailableError(BotError):
    """Raised when Django is not available."""
    pass


class UserNotRegisteredError(BotError):
    """Raised when a user is not registered."""
    pass


class CampaignNotFoundError(BotError):
    """Raised when a campaign is not found."""
    pass


class TaskNotFoundError(BotError):
    """Raised when a task is not found."""
    pass


class PermissionDeniedError(BotError):
    """Raised when a user doesn't have permission."""
    pass


def error_handler(func: Callable) -> Callable:
    """
    Decorator for handling errors in bot handlers.

    Args:
        func: The handler function to wrap

    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            await handle_error(update, context, e)
            # Re-raise the exception for logging
            raise

    return wrapper


async def handle_error(update: Update, context: CallbackContext, error: Exception):
    """
    Handle an error that occurred in a bot handler.

    Args:
        update: Telegram Update object
        context: CallbackContext object
        error: The exception that was raised
    """
    # Log the error
    logger.error(f"Error in handler: {error}", exc_info=True)

    # Get user-friendly error message
    user_message = get_user_friendly_error(error)

    # Send error message to user
    try:
        if update and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user_message,
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Failed to send error message to user: {e}")

    # Log to Django if available
    if is_django_available():
        try:
            log_error_to_django(update, error)
        except Exception as e:
            logger.error(f"Failed to log error to Django: {e}")


def get_user_friendly_error(error: Exception) -> str:
    """
    Convert an exception to a user-friendly error message.

    Args:
        error: The exception

    Returns:
        User-friendly error message
    """
    if isinstance(error, BotError):
        return f"❌ *Error:* {error.user_message or str(error)}"

    # Handle specific exception types
    if isinstance(error, ValueError):
        return "❌ *Invalid input.* Please check your command and try again."

    if isinstance(error, KeyError):
        return "❌ *Missing information.* Please try the command again from the beginning."

    if isinstance(error, TimeoutError):
        return "⏰ *Request timed out.* Please try again in a moment."

    if isinstance(error, ConnectionError):
        return "🔌 *Connection error.* Please check your internet connection and try again."

    # Generic error message
    return "❌ *Something went wrong.* Our team has been notified. Please try again later."


def log_error_to_django(update: Optional[Update], error: Exception):
    """
    Log error to Django database if available.

    Args:
        update: Telegram Update object (optional)
        error: The exception
    """
    if not is_django_available():
        return

    try:
        from apps.analytics.models import ActivityLog

        # Get user info from update if available
        user_info = {}
        if update and update.effective_user:
            user_info = {
                'id': update.effective_user.id,
                'username': update.effective_user.username,
                'first_name': update.effective_user.first_name,
                'last_name': update.effective_user.last_name,
            }

        # Create error log entry
        ActivityLog.objects.create(
            action_type='bot_error',
            user_info=user_info,
            details={
                'error_type': error.__class__.__name__,
                'error_message': str(error),
                'traceback': traceback.format_exc(),
                'update': str(update) if update else None,
            }
        )
    except Exception as e:
        logger.error(f"Failed to create Django error log: {e}")


def require_django(func: Callable) -> Callable:
    """
    Decorator to ensure Django is available before executing a function.

    Args:
        func: The function to wrap

    Returns:
        Wrapped function that checks Django availability
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not is_django_available():
            raise DjangoUnavailableError(
                "Django is not available",
                "❌ *System temporarily unavailable.* Please try again in a few moments."
            )
        return await func(*args, **kwargs)

    return wrapper


def require_registration(func: Callable) -> Callable:
    """
    Decorator to ensure user is registered before executing a handler.

    Args:
        func: The handler function to wrap

    Returns:
        Wrapped function that checks user registration
    """
    @wraps(func)
    @error_handler
    @require_django
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        from .django_integration import get_user_by_telegram_id

        user = update.effective_user
        db_user = get_user_by_telegram_id(user.id)

        if not db_user:
            raise UserNotRegisteredError(
                f"User {user.id} not registered",
                "⚠️ *You need to register first!*\n\n"
                "Use `/start` to begin registration and create your account."
            )

        # Add user to context for convenience
        context.user_data['db_user'] = db_user
        return await func(update, context, *args, **kwargs)

    return wrapper


def with_fallback(fallback_func: Callable) -> Callable:
    """
    Decorator to provide a fallback function when the main function fails.

    Args:
        fallback_func: The fallback function to call

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
            try:
                return await func(update, context, *args, **kwargs)
            except Exception as e:
                logger.warning(f"Function {func.__name__} failed, using fallback: {e}")
                return await fallback_func(update, context, *args, **kwargs)

        return wrapper

    return decorator


async def fallback_simple_response(update: Update, context: CallbackContext):
    """
    Simple fallback response when a handler fails.

    Args:
        update: Telegram Update object
        context: CallbackContext object
    """
    await update.message.reply_text(
        "⚠️ *This feature is temporarily unavailable.*\n\n"
        "Please try again later or use another command.",
        parse_mode='Markdown'
    )


def validate_command_args(expected_args: int, error_message: Optional[str] = None):
    """
    Decorator to validate command arguments.

    Args:
        expected_args: Number of expected arguments
        error_message: Custom error message (optional)

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
            if len(context.args) < expected_args:
                default_message = (
                    f"❌ *Incorrect usage.*\n\n"
                    f"Expected {expected_args} argument{'s' if expected_args > 1 else ''}, "
                    f"got {len(context.args)}.\n\n"
                    f"Use `/help` for command usage instructions."
                )
                await update.message.reply_text(
                    error_message or default_message,
                    parse_mode='Markdown'
                )
                return

            return await func(update, context, *args, **kwargs)

        return wrapper

    return decorator


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on failure.

    Args:
        max_retries: Maximum number of retries
        delay: Delay between retries in seconds

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import asyncio

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise  # Last attempt, re-raise the exception
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    await asyncio.sleep(delay)

            # This should never be reached due to the raise above
            raise Exception(f"Failed after {max_retries} attempts")

        return wrapper

    return decorator
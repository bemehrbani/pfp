"""
State management utilities for Telegram bot conversations.
Manages conversation states using TelegramSession model.

All Django ORM calls are wrapped with sync_to_async for safe
usage in python-telegram-bot's async handlers.
"""
import logging
from typing import Optional, Dict, Any
from telegram import Update
from telegram.ext import CallbackContext
from asgiref.sync import sync_to_async

from .django_integration import setup_django

logger = logging.getLogger(__name__)


class ConversationStateManager:
    """
    Manages conversation states for Telegram bot using Django models.
    All database operations are wrapped with sync_to_async.
    """

    def __init__(self):
        setup_django()
        from apps.telegram.models import TelegramSession
        self.TelegramSession = TelegramSession

    async def get_or_create_session(self, update: Update, context: CallbackContext):
        """Get or create Telegram session for the current user."""
        user = update.effective_user
        chat_id = update.effective_chat.id

        @sync_to_async
        def _db_get_or_create(telegram_id, telegram_username, telegram_chat_id):
            from apps.telegram.models import TelegramSession
            from django.contrib.auth import get_user_model
            User = get_user_model()

            try:
                session = TelegramSession.objects.select_related('user').get(
                    telegram_id=telegram_id
                )
                session.telegram_username = telegram_username
                session.telegram_chat_id = telegram_chat_id
                update_fields = ['telegram_username', 'telegram_chat_id', 'updated_at']

                # Auto-repair: link orphaned session to existing user
                if not session.user:
                    try:
                        db_user = User.objects.get(telegram_id=telegram_id)
                        session.user = db_user
                        update_fields.append('user')
                    except User.DoesNotExist:
                        pass

                session.save(update_fields=update_fields)
                session.increment_message_count()
                return session, False
            except TelegramSession.DoesNotExist:
                db_user = None
                try:
                    db_user = User.objects.get(telegram_id=telegram_id)
                except User.DoesNotExist:
                    pass

                session = TelegramSession.objects.create(
                    telegram_id=telegram_id,
                    telegram_username=telegram_username,
                    telegram_chat_id=telegram_chat_id,
                    user=db_user
                )
                session.increment_message_count()
                return session, True

        return await _db_get_or_create(user.id, user.username, chat_id)

    async def update_state(self, session, new_state: str, state_data: Optional[Dict] = None):
        """Update conversation state for a session."""
        @sync_to_async
        def _db_update_state():
            session.update_state(new_state, state_data)

        try:
            await _db_update_state()
            logger.debug(f"Updated state for session {session.id} to {new_state}")
        except Exception as exc:
            logger.error(f"Failed to update state for session {session.id}: {exc}")
            raise

    async def get_state(self, telegram_id: int) -> Optional[str]:
        """Get current conversation state for a user."""
        @sync_to_async
        def _db_get():
            try:
                s = self.TelegramSession.objects.get(telegram_id=telegram_id)
                return s.state
            except self.TelegramSession.DoesNotExist:
                return None

        try:
            return await _db_get()
        except Exception as exc:
            logger.error(f"Failed to get state for telegram_id {telegram_id}: {exc}")
            return None

    async def get_state_data(self, telegram_id: int) -> Dict[str, Any]:
        """Get state data for a user."""
        @sync_to_async
        def _db_get():
            try:
                s = self.TelegramSession.objects.get(telegram_id=telegram_id)
                return s.state_data or {}
            except self.TelegramSession.DoesNotExist:
                return {}

        try:
            return await _db_get()
        except Exception as exc:
            logger.error(f"Failed to get state data for telegram_id {telegram_id}: {exc}")
            return {}

    async def set_state_data(self, session, data: Dict[str, Any]):
        """Set state data for a session."""
        @sync_to_async
        def _db_save():
            session.state_data = data
            session.save(update_fields=['state_data', 'updated_at'])

        try:
            await _db_save()
            logger.debug(f"Updated state data for session {session.id}")
        except Exception as exc:
            logger.error(f"Failed to set state data for session {session.id}: {exc}")
            raise

    async def get_temp_data(self, telegram_id: int) -> Dict[str, Any]:
        """Get temporary data for a user."""
        @sync_to_async
        def _db_get():
            try:
                s = self.TelegramSession.objects.get(telegram_id=telegram_id)
                return s.temp_data or {}
            except self.TelegramSession.DoesNotExist:
                return {}

        try:
            return await _db_get()
        except Exception as exc:
            logger.error(f"Failed to get temp data for telegram_id {telegram_id}: {exc}")
            return {}

    async def set_temp_data(self, session, data: Dict[str, Any]):
        """Set temporary data for a session."""
        @sync_to_async
        def _db_save():
            session.temp_data = data
            session.save(update_fields=['temp_data', 'updated_at'])

        try:
            await _db_save()
            logger.debug(f"Updated temp data for session {session.id}")
        except Exception as exc:
            logger.error(f"Failed to set temp data for session {session.id}: {exc}")
            raise

    async def clear_state(self, session):
        """Clear conversation state (set to IDLE)."""
        @sync_to_async
        def _db_clear():
            session.update_state(self.TelegramSession.State.IDLE)

        try:
            await _db_clear()
            logger.debug(f"Cleared state for session {session.id}")
        except Exception as exc:
            logger.error(f"Failed to clear state for session {session.id}: {exc}")
            raise

    async def record_command(self, session, command: str):
        """Record usage of a command."""
        @sync_to_async
        def _db_record():
            session.record_command(command)

        try:
            await _db_record()
            logger.debug(f"Recorded command {command} for session {session.id}")
        except Exception as exc:
            logger.error(f"Failed to record command {command} for session {session.id}: {exc}")

    async def handle_registration_flow(self, update: Update, context: CallbackContext, session):
        """Handle registration flow based on current state."""
        from apps.telegram.models import TelegramSession

        if session.state == TelegramSession.State.AWAITING_EMAIL:
            return await self._handle_email_input(update, context, session)
        elif session.state == TelegramSession.State.AWAITING_NAME:
            return await self._handle_name_input(update, context, session)
        elif session.state == TelegramSession.State.AWAITING_CONFIRMATION:
            return await self._handle_confirmation(update, context, session)

        return False

    async def _handle_email_input(self, update: Update, context: CallbackContext, session):
        """Handle email input during registration."""
        email = update.message.text.strip()

        # Validate email
        if '@' not in email or '.' not in email.split('@')[-1]:
            await update.message.reply_text(
                "❌ Please enter a valid email address.\n"
                "Example: user@example.com"
            )
            return False

        # Check if email already exists
        @sync_to_async
        def _check_email(em):
            from django.contrib.auth import get_user_model
            User = get_user_model()
            return User.objects.filter(email=em).exists()

        if await _check_email(email):
            await update.message.reply_text(
                "❌ This email is already registered.\n"
                "Please use a different email or contact support."
            )
            return False

        # Store email in temp data and ask for name
        @sync_to_async
        def _save_email():
            from apps.telegram.models import TelegramSession as TS
            session.temp_data = session.temp_data or {}
            session.temp_data['registration_email'] = email
            session.update_state(TS.State.AWAITING_NAME)

        await _save_email()

        await update.message.reply_text(
            "📝 Great! Now please enter your full name:"
        )
        return False

    async def _handle_name_input(self, update: Update, context: CallbackContext, session):
        """Handle name input during registration."""
        name = update.message.text.strip()

        if len(name) < 2:
            await update.message.reply_text(
                "❌ Please enter a valid name (at least 2 characters)."
            )
            return False

        # Create user account
        @sync_to_async
        def _create_user():
            from django.contrib.auth import get_user_model
            from apps.telegram.models import TelegramSession as TS
            User = get_user_model()

            reg_email = (session.temp_data or {}).get('registration_email', '')
            user = User.objects.create_user(
                username=reg_email.split('@')[0] if reg_email else f'user_{session.telegram_id}',
                email=reg_email,
                first_name=name,
                telegram_id=session.telegram_id,
                telegram_username=session.telegram_username,
                role='volunteer'
            )

            # Link user to session and persist ALL fields in one save
            session.user = user
            session.state = TS.State.IDLE
            session.temp_data = {}
            session.save(update_fields=['user', 'state', 'temp_data', 'state_data', 'updated_at'])

            return user

        try:
            user = await _create_user()

            await update.message.reply_text(
                f"🎉 *Registration Complete!*\n\n"
                f"Welcome to People for Peace, {name}!\n\n"
                f"*Your account details:*\n"
                f"• Email: {user.email}\n"
                f"• Role: Volunteer\n"
                f"• Telegram: @{session.telegram_username or 'Not set'}\n\n"
                f"*Next steps:*\n"
                f"1. Use `/campaigns` to browse available campaigns\n"
                f"2. Join a campaign to start earning points\n"
                f"3. Use `/help` for a list of commands",
                parse_mode='Markdown'
            )

            return True

        except Exception as exc:
            logger.error(f"Failed to create user: {exc}")
            await update.message.reply_text(
                "❌ Failed to create account. Please try again or contact support."
            )
            return False

    async def _handle_confirmation(self, update: Update, context: CallbackContext, session):
        """Handle confirmation step (placeholder for future use)."""
        return False


# Global state manager instance
state_manager = ConversationStateManager()
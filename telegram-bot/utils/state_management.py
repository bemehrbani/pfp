"""
State management utilities for Telegram bot conversations.
Manages conversation states using TelegramSession model.
"""
import logging
from typing import Optional, Dict, Any
from telegram import Update
from telegram.ext import CallbackContext

from .django_integration import setup_django, create_or_update_telegram_session

logger = logging.getLogger(__name__)


class ConversationStateManager:
    """
    Manages conversation states for Telegram bot using Django models.
    """

    def __init__(self):
        setup_django()
        from apps.telegram.models import TelegramSession
        self.TelegramSession = TelegramSession

    async def get_or_create_session(self, update: Update, context: CallbackContext):
        """
        Get or create Telegram session for the current user.

        Args:
            update: Telegram Update object
            context: CallbackContext object

        Returns:
            Tuple of (TelegramSession object, created boolean)
        """
        user = update.effective_user
        chat_id = update.effective_chat.id

        # Get or create session
        session, created = create_or_update_telegram_session(
            telegram_id=user.id,
            telegram_username=user.username,
            telegram_chat_id=chat_id
        )

        # Update last interaction
        session.increment_message_count()

        return session, created

    async def update_state(self, session, new_state: str, state_data: Optional[Dict] = None):
        """
        Update conversation state for a session.

        Args:
            session: TelegramSession object
            new_state: New state value
            state_data: Optional data to store with the state
        """
        try:
            session.update_state(new_state, state_data)
            logger.debug(f"Updated state for session {session.id} to {new_state}")
        except Exception as e:
            logger.error(f"Failed to update state for session {session.id}: {e}")
            raise

    async def get_state(self, telegram_id: int) -> Optional[str]:
        """
        Get current conversation state for a user.

        Args:
            telegram_id: Telegram user ID

        Returns:
            Current state or None if session not found
        """
        try:
            session = self.TelegramSession.objects.get(telegram_id=telegram_id)
            return session.state
        except self.TelegramSession.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Failed to get state for telegram_id {telegram_id}: {e}")
            return None

    async def get_state_data(self, telegram_id: int) -> Dict[str, Any]:
        """
        Get state data for a user.

        Args:
            telegram_id: Telegram user ID

        Returns:
            State data dictionary (empty dict if not found)
        """
        try:
            session = self.TelegramSession.objects.get(telegram_id=telegram_id)
            return session.state_data or {}
        except self.TelegramSession.DoesNotExist:
            return {}
        except Exception as e:
            logger.error(f"Failed to get state data for telegram_id {telegram_id}: {e}")
            return {}

    async def set_state_data(self, session, data: Dict[str, Any]):
        """
        Set state data for a session.

        Args:
            session: TelegramSession object
            data: State data dictionary
        """
        try:
            session.state_data = data
            session.save(update_fields=['state_data', 'updated_at'])
            logger.debug(f"Updated state data for session {session.id}")
        except Exception as e:
            logger.error(f"Failed to set state data for session {session.id}: {e}")
            raise

    async def get_temp_data(self, telegram_id: int) -> Dict[str, Any]:
        """
        Get temporary data for a user.

        Args:
            telegram_id: Telegram user ID

        Returns:
            Temporary data dictionary (empty dict if not found)
        """
        try:
            session = self.TelegramSession.objects.get(telegram_id=telegram_id)
            return session.temp_data or {}
        except self.TelegramSession.DoesNotExist:
            return {}
        except Exception as e:
            logger.error(f"Failed to get temp data for telegram_id {telegram_id}: {e}")
            return {}

    async def set_temp_data(self, session, data: Dict[str, Any]):
        """
        Set temporary data for a session.

        Args:
            session: TelegramSession object
            data: Temporary data dictionary
        """
        try:
            session.temp_data = data
            session.save(update_fields=['temp_data', 'updated_at'])
            logger.debug(f"Updated temp data for session {session.id}")
        except Exception as e:
            logger.error(f"Failed to set temp data for session {session.id}: {e}")
            raise

    async def clear_state(self, session):
        """
        Clear conversation state (set to IDLE).

        Args:
            session: TelegramSession object
        """
        try:
            session.update_state(self.TelegramSession.State.IDLE)
            logger.debug(f"Cleared state for session {session.id}")
        except Exception as e:
            logger.error(f"Failed to clear state for session {session.id}: {e}")
            raise

    async def record_command(self, session, command: str):
        """
        Record usage of a command.

        Args:
            session: TelegramSession object
            command: Command name (without slash)
        """
        try:
            session.record_command(command)
            logger.debug(f"Recorded command {command} for session {session.id}")
        except Exception as e:
            logger.error(f"Failed to record command {command} for session {session.id}: {e}")

    async def handle_registration_flow(self, update: Update, context: CallbackContext, session):
        """
        Handle registration flow based on current state.

        Args:
            update: Telegram Update object
            context: CallbackContext object
            session: TelegramSession object

        Returns:
            Boolean indicating if registration is complete
        """
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
        from django.contrib.auth import get_user_model
        from apps.telegram.models import TelegramSession

        email = update.message.text.strip()

        # Validate email
        if '@' not in email or '.' not in email.split('@')[-1]:
            await update.message.reply_text(
                "❌ Please enter a valid email address.\n"
                "Example: user@example.com"
            )
            return False

        # Check if email already exists
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            await update.message.reply_text(
                "❌ This email is already registered.\n"
                "Please use a different email or contact support."
            )
            return False

        # Store email in temp data and ask for name
        session.temp_data['registration_email'] = email
        session.update_state(TelegramSession.State.AWAITING_NAME)

        await update.message.reply_text(
            "📝 Great! Now please enter your full name:"
        )
        return False

    async def _handle_name_input(self, update: Update, context: CallbackContext, session):
        """Handle name input during registration."""
        from django.contrib.auth import get_user_model
        from apps.telegram.models import TelegramSession

        name = update.message.text.strip()

        if len(name) < 2:
            await update.message.reply_text(
                "❌ Please enter a valid name (at least 2 characters)."
            )
            return False

        # Create user account
        User = get_user_model()
        try:
            user = User.objects.create_user(
                username=session.temp_data['registration_email'].split('@')[0],
                email=session.temp_data['registration_email'],
                first_name=name,
                telegram_id=session.telegram_id,
                telegram_username=session.telegram_username,
                role='volunteer'
            )

            # Link user to session
            session.user = user
            session.update_state(TelegramSession.State.IDLE)
            session.temp_data = {}

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

        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            await update.message.reply_text(
                "❌ Failed to create account. Please try again or contact support."
            )
            return False

    async def _handle_confirmation(self, update: Update, context: CallbackContext, session):
        """Handle confirmation step (placeholder for future use)."""
        # This can be extended for various confirmation flows
        return False


# Global state manager instance
state_manager = ConversationStateManager()
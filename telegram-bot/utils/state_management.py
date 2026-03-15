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

        if session.state == TelegramSession.State.AWAITING_NAME:
            return await self._handle_name_input(update, context, session)
        elif session.state == TelegramSession.State.AWAITING_CONFIRMATION:
            return await self._handle_confirmation(update, context, session)

        return False

    async def register_user_automatically(self, update: Update, context: CallbackContext, session, lang: str):
        """Automatically register user using their Telegram name."""
        from utils.translations import t
        from telegram import ReplyKeyboardMarkup
        
        user_info = update.effective_user
        first_name = user_info.first_name or ''
        last_name = user_info.last_name or ''
        full_name = f"{first_name} {last_name}".strip() or "Volunteer"

        # Read deep-link campaign ID
        @sync_to_async
        def _read_deeplink():
            session.refresh_from_db(fields=['temp_data'])
            return (session.temp_data or {}).get('deeplink_campaign_id')

        deeplink_campaign_id = await _read_deeplink()

        # Create user account
        @sync_to_async
        def _create_user():
            from django.contrib.auth import get_user_model
            from apps.telegram.models import TelegramSession as TS
            User = get_user_model()

            user = User.objects.create_user(
                username=f'user_{session.telegram_id}',
                email='',
                first_name=full_name,
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

            # Translated success message
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=t('register_success', lang).format(name=first_name or full_name),
                parse_mode='Markdown'
            )

            # Re-send inline menu so the user has navigation buttons
            from utils.translations import get_main_menu_inline
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⬇️",
                reply_markup=get_main_menu_inline(lang),
            )

            # Auto-join campaign from deep-link (if present)
            if deeplink_campaign_id:
                await self._auto_join_campaign(
                    update, context, session, user, deeplink_campaign_id, lang
                )

            return True

        except Exception as exc:
            logger.error(f"Failed to create user automatically: {exc}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=t('register_error', lang)
            )
            return False

    async def _handle_name_input(self, update: Update, context: CallbackContext, session):
        """Handle name input during registration."""
        from utils.translations import t, get_keyboard_buttons
        from telegram import ReplyKeyboardMarkup

        name = update.message.text.strip()
        lang = getattr(session, 'language', 'en') or 'en'

        if len(name) < 2:
            await update.message.reply_text(t('register_name_invalid', lang))
            return False

        # Read deep-link campaign ID BEFORE clearing temp_data
        @sync_to_async
        def _read_deeplink():
            session.refresh_from_db(fields=['temp_data'])
            return (session.temp_data or {}).get('deeplink_campaign_id')

        deeplink_campaign_id = await _read_deeplink()

        # Create user account (no email needed — Telegram ID is the identifier)
        @sync_to_async
        def _create_user():
            from django.contrib.auth import get_user_model
            from apps.telegram.models import TelegramSession as TS
            User = get_user_model()

            user = User.objects.create_user(
                username=f'user_{session.telegram_id}',
                email='',
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

            # Translated success message
            await update.message.reply_text(
                t('register_success', lang).format(name=name),
                parse_mode='Markdown'
            )

            # Re-send inline menu so the user has navigation buttons
            from utils.translations import get_main_menu_inline
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⬇️",
                reply_markup=get_main_menu_inline(lang),
            )

            # Auto-join campaign from deep-link (if present)
            if deeplink_campaign_id:
                await self._auto_join_campaign(
                    update, context, session, user, deeplink_campaign_id, lang
                )

            return True

        except Exception as exc:
            logger.error(f"Failed to create user: {exc}")
            await update.message.reply_text(t('register_error', lang))
            return False

    async def _auto_join_campaign(self, update, context, session, user, campaign_id, lang):
        """Auto-join a campaign after registration and show its tasks."""
        from utils.translations import t
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        from handlers.campaigns import (
            _get_campaign, _is_volunteer, _join_campaign, _get_task_count
        )

        campaign = await _get_campaign(campaign_id)
        if not campaign:
            return

        already_joined = await _is_volunteer(campaign, user)
        if already_joined:
            return

        member_count = await _join_campaign(campaign, user)
        task_count = await _get_task_count(campaign)

        # Get tasks for inline buttons
        @sync_to_async
        def _get_tasks(cid):
            from apps.tasks.models import Task
            return list(Task.objects.filter(
                campaign_id=cid, is_active=True,
            ).order_by('-points')[:10])

        tasks = await _get_tasks(campaign_id)

        # Build message with task buttons
        text = t('auto_joined_campaign', lang).format(
            name=campaign.localized_name(lang),
            members=member_count,
            tasks=task_count,
        )

        keyboard = []
        type_icons = {
            'twitter_post': '🐦', 'twitter_retweet': '🔁', 'twitter_comment': '💬',
            'twitter_like': '❤️', 'telegram_share': '📢', 'telegram_invite': '👥',
            'content_creation': '✍️', 'other': '📌',
        }
        for task in tasks:
            icon = type_icons.get(task.task_type, '📌')
            keyboard.append([
                InlineKeyboardButton(
                    f"{icon} {task.localized_title(lang)[:35]}",
                    callback_data=f"task_claim_{task.id}"
                )
            ])

        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

        logger.info(f"Auto-joined user {user.username} to campaign {campaign_id}")

    async def _handle_confirmation(self, update: Update, context: CallbackContext, session):
        """Handle confirmation step (placeholder for future use)."""
        return False


# Global state manager instance
state_manager = ConversationStateManager()
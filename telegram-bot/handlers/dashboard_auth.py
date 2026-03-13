"""
Dashboard authentication handler.
Generates OTP codes for campaign managers to log into the web dashboard.
"""
import logging
import secrets
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import CallbackContext

from utils.django_integration import setup_django
from utils.state_management import state_manager
from utils.translations import t

logger = logging.getLogger(__name__)

setup_django()


def _generate_otp() -> str:
    """Generate a 6-digit numeric OTP code."""
    return f"{secrets.randbelow(900000) + 100000}"


async def dashboard_command(update: Update, context: CallbackContext) -> None:
    """Handle /dashboard command — generate OTP for web dashboard login."""
    session, _ = await state_manager.get_or_create_session(update, context)

    @sync_to_async
    def _get_user_and_generate_otp():
        from django.contrib.auth import get_user_model
        from django.core.cache import cache

        User = get_user_model()

        if not session.user_id:
            return None, None, 'not_registered'

        try:
            user = User.objects.get(pk=session.user_id)
        except User.DoesNotExist:
            return None, None, 'not_registered'

        # Only admin and campaign_manager can access dashboard
        if user.role not in ('admin', 'campaign_manager'):
            return user, None, 'not_authorized'

        # Generate OTP and store in Redis cache (5 min TTL)
        otp_code = _generate_otp()
        cache_key = f"otp:{user.telegram_id}"
        cache.set(cache_key, {
            'code': otp_code,
            'user_id': user.pk,
        }, timeout=300)

        # Determine display name for login
        login_name = user.telegram_username or f"user_{user.telegram_id}"

        return user, otp_code, login_name

    user, otp_code, result = await _get_user_and_generate_otp()

    lang = getattr(session, 'language', 'en') or 'en'

    if result == 'not_registered':
        await update.message.reply_text(
            t('register_need_first', lang),
            parse_mode='Markdown'
        )
        return

    if result == 'not_authorized':
        await update.message.reply_text(
            t('dashboard_not_authorized', lang),
            parse_mode='Markdown'
        )
        return

    # Success — send OTP code
    await update.message.reply_text(
        t('dashboard_otp_sent', lang).format(
            code=otp_code,
            username=result,
        ),
        parse_mode='Markdown'
    )

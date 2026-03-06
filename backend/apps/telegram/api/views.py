"""
API views for Telegram app.
"""
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import telegram
from telegram import Update
from telegram.ext import Application, ContextTypes

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):
    """Handle Telegram bot webhook updates."""

    def post(self, request, *args, **kwargs):
        """Process incoming Telegram update."""
        try:
            # Parse update from request body
            body = json.loads(request.body.decode('utf-8'))
            update = Update.de_json(body, bot=None)  # Bot will be set in handler

            # Process update asynchronously
            self._process_update_async(update)

            return HttpResponse('OK')
        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON in webhook: {e}')
            return HttpResponse('Invalid JSON', status=400)
        except Exception as e:
            logger.error(f'Error processing webhook: {e}')
            return HttpResponse('Server Error', status=500)

    def _process_update_async(self, update: Update):
        """Process update asynchronously (in background)."""
        # TODO: Implement async processing with Celery or Django Channels
        # For now, just log the update
        if update.message:
            logger.info(f'Message from {update.message.from_user.id}: {update.message.text}')
        elif update.callback_query:
            logger.info(f'Callback from {update.callback_query.from_user.id}: {update.callback_query.data}')


class TelegramBotStatusView(APIView):
    """Get Telegram bot status and information."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """Return bot status information."""
        bot_token = settings.TELEGRAM_BOT_TOKEN

        if not bot_token:
            return Response({
                'status': 'not_configured',
                'message': 'Telegram bot token not configured'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            # Initialize bot
            bot = telegram.Bot(token=bot_token)

            # Get bot info
            bot_info = bot.get_me()

            # Get webhook info
            webhook_info = bot.get_webhook_info()

            return Response({
                'status': 'active',
                'bot': {
                    'id': bot_info.id,
                    'username': bot_info.username,
                    'first_name': bot_info.first_name,
                    'can_join_groups': bot_info.can_join_groups,
                    'can_read_all_group_messages': bot_info.can_read_all_group_messages,
                    'supports_inline_queries': bot_info.supports_inline_queries,
                },
                'webhook': {
                    'url': webhook_info.url,
                    'has_custom_certificate': webhook_info.has_custom_certificate,
                    'pending_update_count': webhook_info.pending_update_count,
                    'last_error_date': webhook_info.last_error_date,
                    'last_error_message': webhook_info.last_error_message,
                    'max_connections': webhook_info.max_connections,
                    'allowed_updates': webhook_info.allowed_updates,
                }
            })
        except telegram.error.InvalidToken:
            return Response({
                'status': 'invalid_token',
                'message': 'Invalid Telegram bot token'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error getting bot status: {e}')
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetTelegramWebhookView(APIView):
    """Set or update Telegram webhook URL."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """Set webhook URL for Telegram bot."""
        bot_token = settings.TELEGRAM_BOT_TOKEN
        webhook_url = settings.TELEGRAM_WEBHOOK_URL

        if not bot_token:
            return Response({
                'error': 'Telegram bot token not configured'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not webhook_url:
            return Response({
                'error': 'Webhook URL not configured'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            bot = telegram.Bot(token=bot_token)

            # Set webhook
            success = bot.set_webhook(
                url=f'{webhook_url}/webhook/telegram/{bot_token}/',
                certificate=None,  # Add certificate if using self-signed SSL
                max_connections=40,
                allowed_updates=['message', 'callback_query', 'chat_member']
            )

            if success:
                logger.info(f'Webhook set successfully: {webhook_url}')
                return Response({
                    'status': 'success',
                    'message': 'Webhook set successfully',
                    'webhook_url': webhook_url
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'Failed to set webhook'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f'Error setting webhook: {e}')
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteTelegramWebhookView(APIView):
    """Delete Telegram webhook."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """Delete webhook (switch to polling mode)."""
        bot_token = settings.TELEGRAM_BOT_TOKEN

        if not bot_token:
            return Response({
                'error': 'Telegram bot token not configured'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            bot = telegram.Bot(token=bot_token)
            success = bot.delete_webhook()

            if success:
                logger.info('Webhook deleted successfully')
                return Response({
                    'status': 'success',
                    'message': 'Webhook deleted successfully (switched to polling)'
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'Failed to delete webhook'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f'Error deleting webhook: {e}')
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendTelegramMessageView(APIView):
    """Send message to Telegram user or chat (admin only)."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """Send message to specified Telegram chat."""
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = request.data.get('chat_id')
        message = request.data.get('message')

        if not bot_token:
            return Response({
                'error': 'Telegram bot token not configured'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not chat_id or not message:
            return Response({
                'error': 'chat_id and message are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            bot = telegram.Bot(token=bot_token)
            sent_message = bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML'
            )

            return Response({
                'status': 'success',
                'message_id': sent_message.message_id,
                'chat_id': sent_message.chat.id,
                'date': sent_message.date.isoformat() if sent_message.date else None
            })

        except telegram.error.BadRequest as e:
            logger.error(f'Bad request sending message: {e}')
            return Response({
                'status': 'error',
                'message': f'Invalid chat_id or message: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error sending message: {e}')
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
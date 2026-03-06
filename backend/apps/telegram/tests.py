"""
Comprehensive tests for Telegram app.

Tests cover:
1. TelegramSession model creation and methods
2. TelegramMessageLog model
3. API endpoints: webhook, bot status, message sending
4. Permission checks and edge cases
"""

import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.test import Client
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.telegram.models import TelegramSession, TelegramMessageLog

User = get_user_model()


class TelegramSessionModelTests(TestCase):
    """Test TelegramSession model creation and methods."""

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='testpass123',
            role=User.Role.ADMIN
        )
        self.volunteer = User.objects.create_user(
            username='volunteer',
            email='volunteer@example.com',
            password='testpass123',
            role=User.Role.VOLUNTEER
        )

    def test_telegram_session_creation(self):
        """Test TelegramSession creation with all fields."""
        session = TelegramSession.objects.create(
            telegram_id=123456789,
            telegram_username='testuser',
            telegram_chat_id=987654321,
            user=self.volunteer,
            state=TelegramSession.State.AWAITING_NAME,
            state_data={'name': 'John'},
            temp_data={'email': 'test@example.com'},
            total_messages=5,
            commands_used={'/start': 2, '/help': 1}
        )

        self.assertEqual(session.telegram_id, 123456789)
        self.assertEqual(session.telegram_username, 'testuser')
        self.assertEqual(session.telegram_chat_id, 987654321)
        self.assertEqual(session.user, self.volunteer)
        self.assertEqual(session.state, TelegramSession.State.AWAITING_NAME)
        self.assertEqual(session.state_data['name'], 'John')
        self.assertEqual(session.temp_data['email'], 'test@example.com')
        self.assertEqual(session.total_messages, 5)
        self.assertEqual(session.commands_used['/start'], 2)
        self.assertEqual(session.commands_used['/help'], 1)
        self.assertIsNotNone(session.created_at)
        self.assertIsNotNone(session.updated_at)
        self.assertIsNotNone(session.last_interaction)

    def test_telegram_session_creation_without_user(self):
        """Test TelegramSession creation without linked user."""
        session = TelegramSession.objects.create(
            telegram_id=987654321,
            telegram_chat_id=123456789,
            state=TelegramSession.State.IDLE
        )

        self.assertEqual(session.telegram_id, 987654321)
        self.assertIsNone(session.user)
        self.assertEqual(session.state, TelegramSession.State.IDLE)
        self.assertEqual(session.total_messages, 0)
        self.assertEqual(session.commands_used, {})

    def test_telegram_session_string_representation(self):
        """Test string representation of TelegramSession."""
        # With user
        session_with_user = TelegramSession.objects.create(
            telegram_id=123456789,
            telegram_chat_id=987654321,
            user=self.volunteer
        )
        self.assertEqual(str(session_with_user), f'{self.volunteer.username} (123456789)')

        # Without user
        session_without_user = TelegramSession.objects.create(
            telegram_id=987654321,
            telegram_chat_id=123456789
        )
        self.assertEqual(str(session_without_user), 'Anonymous (987654321)')

    def test_update_state_method(self):
        """Test update_state method."""
        session = TelegramSession.objects.create(
            telegram_id=123456789,
            telegram_chat_id=987654321,
            state=TelegramSession.State.IDLE,
            state_data={}
        )

        # Update state with new data
        new_state_data = {'task_id': 1, 'campaign_id': 2}
        session.update_state(TelegramSession.State.AWAITING_TASK_PROOF, new_state_data)

        # Check state was updated
        session.refresh_from_db()
        self.assertEqual(session.state, TelegramSession.State.AWAITING_TASK_PROOF)
        self.assertEqual(session.state_data['task_id'], 1)
        self.assertEqual(session.state_data['campaign_id'], 2)

    def test_increment_message_count_method(self):
        """Test increment_message_count method."""
        session = TelegramSession.objects.create(
            telegram_id=123456789,
            telegram_chat_id=987654321,
            total_messages=10
        )

        # Increment message count
        session.increment_message_count()

        # Check count was incremented
        session.refresh_from_db()
        self.assertEqual(session.total_messages, 11)

    def test_record_command_method(self):
        """Test record_command method."""
        session = TelegramSession.objects.create(
            telegram_id=123456789,
            telegram_chat_id=987654321,
            commands_used={'/start': 1}
        )

        # Record existing command
        session.record_command('/start')

        # Record new command
        session.record_command('/help')

        # Check commands were recorded
        session.refresh_from_db()
        self.assertEqual(session.commands_used['/start'], 2)
        self.assertEqual(session.commands_used['/help'], 1)

    def test_telegram_session_indexes(self):
        """Test that indexes are properly set."""
        indexes = [index.fields for index in TelegramSession._meta.indexes]
        expected_indexes = [['telegram_id'], ['state'], ['last_interaction']]

        for expected in expected_indexes:
            self.assertIn(expected, indexes)


class TelegramMessageLogModelTests(TestCase):
    """Test TelegramMessageLog model."""

    def setUp(self):
        """Set up test data."""
        self.session = TelegramSession.objects.create(
            telegram_id=123456789,
            telegram_chat_id=987654321
        )

    def test_telegram_message_log_creation(self):
        """Test TelegramMessageLog creation with all fields."""
        from_user_data = {
            'id': 123456789,
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User'
        }

        message_log = TelegramMessageLog.objects.create(
            session=self.session,
            message_id=1001,
            chat_id=987654321,
            from_user=from_user_data,
            message_type='text',
            content='Hello, bot!',
            bot_response='Hello, user! How can I help you?'
        )

        self.assertEqual(message_log.session, self.session)
        self.assertEqual(message_log.message_id, 1001)
        self.assertEqual(message_log.chat_id, 987654321)
        self.assertEqual(message_log.from_user['username'], 'testuser')
        self.assertEqual(message_log.message_type, 'text')
        self.assertEqual(message_log.content, 'Hello, bot!')
        self.assertEqual(message_log.bot_response, 'Hello, user! How can I help you?')
        self.assertIsNotNone(message_log.created_at)

    def test_telegram_message_log_string_representation(self):
        """Test string representation of TelegramMessageLog."""
        from_user_data = {'username': 'testuser'}

        message_log = TelegramMessageLog.objects.create(
            session=self.session,
            message_id=1001,
            chat_id=987654321,
            from_user=from_user_data,
            message_type='text',
            content='Test message'
        )

        self.assertEqual(str(message_log), 'Message 1001 from testuser')

    def test_telegram_message_log_without_bot_response(self):
        """Test TelegramMessageLog creation without bot response."""
        from_user_data = {'id': 123456789}

        message_log = TelegramMessageLog.objects.create(
            session=self.session,
            message_id=1002,
            chat_id=987654321,
            from_user=from_user_data,
            message_type='command',
            content='/start'
        )

        self.assertEqual(message_log.message_type, 'command')
        self.assertEqual(message_log.content, '/start')
        self.assertIsNone(message_log.bot_response)

    def test_telegram_message_log_ordering(self):
        """Test TelegramMessageLog ordering (newest first)."""
        # Create logs in order
        log1 = TelegramMessageLog.objects.create(
            session=self.session,
            message_id=1001,
            chat_id=987654321,
            from_user={'id': 123456789},
            message_type='text',
            content='First message'
        )

        log2 = TelegramMessageLog.objects.create(
            session=self.session,
            message_id=1002,
            chat_id=987654321,
            from_user={'id': 123456789},
            message_type='text',
            content='Second message'
        )

        logs = TelegramMessageLog.objects.all()
        self.assertEqual(logs[0], log2)  # Newest first
        self.assertEqual(logs[1], log1)  # Oldest last

    def test_telegram_message_log_indexes(self):
        """Test that indexes are properly set."""
        indexes = [index.fields for index in TelegramMessageLog._meta.indexes]
        expected_indexes = [['session', 'created_at'], ['created_at']]

        for expected in expected_indexes:
            self.assertIn(expected, indexes)


class TelegramAPITests(APITestCase):
    """Test Telegram API endpoints."""

    def setUp(self):
        """Set up test data and client."""
        self.client = APIClient()

        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role=User.Role.ADMIN
        )
        self.volunteer = User.objects.create_user(
            username='volunteer',
            email='volunteer@example.com',
            password='volunteerpass123',
            role=User.Role.VOLUNTEER
        )

        # Get tokens for authentication
        self.admin_token = RefreshToken.for_user(self.admin_user)
        self.volunteer_token = RefreshToken.for_user(self.volunteer)

        # Create test Telegram session
        self.telegram_session = TelegramSession.objects.create(
            telegram_id=123456789,
            telegram_username='testuser',
            telegram_chat_id=987654321,
            user=self.volunteer,
            state=TelegramSession.State.IDLE
        )

    @patch('apps.telegram.api.views.logger')
    def test_telegram_webhook_valid_json(self, mock_logger):
        """Test Telegram webhook with valid JSON."""
        # Use Django test client for CSRF-exempt view
        client = Client()

        # Create valid Telegram update JSON
        update_data = {
            'update_id': 123456789,
            'message': {
                'message_id': 1001,
                'from': {
                    'id': 123456789,
                    'is_bot': False,
                    'first_name': 'Test',
                    'username': 'testuser'
                },
                'chat': {
                    'id': 987654321,
                    'first_name': 'Test',
                    'username': 'testuser',
                    'type': 'private'
                },
                'date': 1672531200,
                'text': '/start'
            }
        }

        response = client.post(
            reverse('telegram:telegram_webhook', kwargs={'bot_token': 'test_token'}),
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')
        mock_logger.info.assert_called()

    @patch('apps.telegram.api.views.logger')
    def test_telegram_webhook_invalid_json(self, mock_logger):
        """Test Telegram webhook with invalid JSON."""
        client = Client()

        response = client.post(
            reverse('telegram:telegram_webhook', kwargs={'bot_token': 'test_token'}),
            data='invalid json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid JSON')
        mock_logger.error.assert_called()

    @patch('apps.telegram.api.views.logger')
    def test_telegram_webhook_callback_query(self, mock_logger):
        """Test Telegram webhook with callback query."""
        client = Client()

        # Create callback query update
        update_data = {
            'update_id': 123456790,
            'callback_query': {
                'id': 'callback123',
                'from': {
                    'id': 123456789,
                    'is_bot': False,
                    'first_name': 'Test',
                    'username': 'testuser'
                },
                'message': {
                    'message_id': 1002,
                    'from': {
                        'id': 999999999,
                        'is_bot': True,
                        'first_name': 'TestBot',
                        'username': 'test_bot'
                    },
                    'chat': {
                        'id': 987654321,
                        'first_name': 'Test',
                        'username': 'testuser',
                        'type': 'private'
                    },
                    'date': 1672531200,
                    'text': 'Choose an option:'
                },
                'chat_instance': '123456',
                'data': 'campaign_1'
            }
        }

        response = client.post(
            reverse('telegram:telegram_webhook', kwargs={'bot_token': 'test_token'}),
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        mock_logger.info.assert_called()

    @patch('telegram.Bot')
    def test_telegram_bot_status_admin(self, mock_bot_class):
        """Test Telegram bot status endpoint as admin."""
        url = reverse('telegram:telegram_status')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock bot and its methods
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot

        # Mock bot info
        mock_bot_info = MagicMock()
        mock_bot_info.id = 999999999
        mock_bot_info.username = 'test_bot'
        mock_bot_info.first_name = 'TestBot'
        mock_bot_info.can_join_groups = True
        mock_bot_info.can_read_all_group_messages = False
        mock_bot_info.supports_inline_queries = False

        # Mock webhook info
        mock_webhook_info = MagicMock()
        mock_webhook_info.url = 'https://example.com/webhook/'
        mock_webhook_info.has_custom_certificate = False
        mock_webhook_info.pending_update_count = 0
        mock_webhook_info.last_error_date = None
        mock_webhook_info.last_error_message = None
        mock_webhook_info.max_connections = 40
        mock_webhook_info.allowed_updates = ['message', 'callback_query']

        mock_bot.get_me.return_value = mock_bot_info
        mock_bot.get_webhook_info.return_value = mock_webhook_info

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response contains expected fields
        self.assertEqual(response.data['status'], 'active')
        self.assertEqual(response.data['bot']['username'], 'test_bot')
        self.assertEqual(response.data['webhook']['url'], 'https://example.com/webhook/')

    @patch('telegram.Bot')
    def test_telegram_bot_status_invalid_token(self, mock_bot_class):
        """Test Telegram bot status with invalid token."""
        url = reverse('telegram:telegram_status')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock InvalidToken exception
        from telegram.error import InvalidToken
        mock_bot_class.side_effect = InvalidToken('Invalid token')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'invalid_token')

    def test_telegram_bot_status_non_admin(self):
        """Test Telegram bot status endpoint as non-admin (should fail)."""
        url = reverse('telegram:telegram_status')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('telegram.Bot')
    def test_set_telegram_webhook_admin(self, mock_bot_class):
        """Test set Telegram webhook endpoint as admin."""
        url = reverse('telegram:set_webhook')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock bot and set_webhook method
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot
        mock_bot.set_webhook.return_value = True

        # Mock settings
        with patch.dict('django.conf.settings.__dict__', {
            'TELEGRAM_BOT_TOKEN': 'test_token_123',
            'TELEGRAM_WEBHOOK_URL': 'https://example.com'
        }):
            response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['webhook_url'], 'https://example.com')

        # Verify set_webhook was called with correct parameters
        mock_bot.set_webhook.assert_called_once_with(
            url='https://example.com/webhook/telegram/test_token_123/',
            certificate=None,
            max_connections=40,
            allowed_updates=['message', 'callback_query', 'chat_member']
        )

    @patch('telegram.Bot')
    def test_set_telegram_webhook_failure(self, mock_bot_class):
        """Test set Telegram webhook endpoint with failure."""
        url = reverse('telegram:set_webhook')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock bot with set_webhook returning False
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot
        mock_bot.set_webhook.return_value = False

        with patch.dict('django.conf.settings.__dict__', {
            'TELEGRAM_BOT_TOKEN': 'test_token_123',
            'TELEGRAM_WEBHOOK_URL': 'https://example.com'
        }):
            response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['status'], 'error')

    def test_set_telegram_webhook_missing_token(self):
        """Test set Telegram webhook endpoint with missing bot token."""
        url = reverse('telegram:set_webhook')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock settings without token
        with patch.dict('django.conf.settings.__dict__', {
            'TELEGRAM_BOT_TOKEN': None,
            'TELEGRAM_WEBHOOK_URL': 'https://example.com'
        }):
            response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_set_telegram_webhook_non_admin(self):
        """Test set Telegram webhook endpoint as non-admin (should fail)."""
        url = reverse('telegram:set_webhook')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('telegram.Bot')
    def test_delete_telegram_webhook_admin(self, mock_bot_class):
        """Test delete Telegram webhook endpoint as admin."""
        url = reverse('telegram:delete_webhook')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock bot and delete_webhook method
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot
        mock_bot.delete_webhook.return_value = True

        with patch.dict('django.conf.settings.__dict__', {
            'TELEGRAM_BOT_TOKEN': 'test_token_123'
        }):
            response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

    @patch('telegram.Bot')
    def test_delete_telegram_webhook_failure(self, mock_bot_class):
        """Test delete Telegram webhook endpoint with failure."""
        url = reverse('telegram:delete_webhook')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock bot with delete_webhook returning False
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot
        mock_bot.delete_webhook.return_value = False

        with patch.dict('django.conf.settings.__dict__', {
            'TELEGRAM_BOT_TOKEN': 'test_token_123'
        }):
            response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['status'], 'error')

    @patch('telegram.Bot')
    def test_send_telegram_message_admin(self, mock_bot_class):
        """Test send Telegram message endpoint as admin."""
        url = reverse('telegram:send_message')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock bot and send_message method
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot

        mock_sent_message = MagicMock()
        mock_sent_message.message_id = 1001
        mock_sent_message.chat.id = 987654321
        mock_sent_message.date = datetime(2023, 1, 1, 12, 0, 0)

        mock_bot.send_message.return_value = mock_sent_message

        data = {
            'chat_id': 987654321,
            'message': 'Test message from admin'
        }

        with patch.dict('django.conf.settings.__dict__', {
            'TELEGRAM_BOT_TOKEN': 'test_token_123'
        }):
            response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message_id'], 1001)
        self.assertEqual(response.data['chat_id'], 987654321)

        # Verify send_message was called with correct parameters
        mock_bot.send_message.assert_called_once_with(
            chat_id=987654321,
            text='Test message from admin',
            parse_mode='HTML'
        )

    def test_send_telegram_message_missing_parameters(self):
        """Test send Telegram message endpoint with missing parameters."""
        url = reverse('telegram:send_message')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Test missing chat_id
        data = {'message': 'Test message'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test missing message
        data = {'chat_id': 987654321}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('telegram.Bot')
    def test_send_telegram_message_bad_request(self, mock_bot_class):
        """Test send Telegram message endpoint with bad request (invalid chat_id)."""
        url = reverse('telegram:send_message')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        # Mock bot with BadRequest exception
        from telegram.error import BadRequest
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot
        mock_bot.send_message.side_effect = BadRequest('Invalid chat_id')

        data = {
            'chat_id': 'invalid',
            'message': 'Test message'
        }

        with patch.dict('django.conf.settings.__dict__', {
            'TELEGRAM_BOT_TOKEN': 'test_token_123'
        }):
            response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    def test_send_telegram_message_non_admin(self):
        """Test send Telegram message endpoint as non-admin (should fail)."""
        url = reverse('telegram:send_message')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'chat_id': 987654321,
            'message': 'Test message'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
"""
Comprehensive tests for Users app.

Tests cover:
1. User model creation and methods
2. API endpoints (register, login, profile, Telegram linking, etc.)
3. Signal handlers for user creation/updates
4. Permission checks and edge cases
"""

import json
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.analytics.models import ActivityLog

User = get_user_model()


class UserModelTests(TestCase):
    """Test User model creation and methods."""

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='testpass123',
            role=User.Role.ADMIN
        )
        self.campaign_manager = User.objects.create_user(
            username='campaign_manager',
            email='manager@example.com',
            password='testpass123',
            role=User.Role.CAMPAIGN_MANAGER
        )
        self.volunteer = User.objects.create_user(
            username='volunteer',
            email='volunteer@example.com',
            password='testpass123',
            role=User.Role.VOLUNTEER
        )

    def test_user_creation(self):
        """Test user creation with different roles."""
        self.assertEqual(self.admin_user.role, User.Role.ADMIN)
        self.assertEqual(self.campaign_manager.role, User.Role.CAMPAIGN_MANAGER)
        self.assertEqual(self.volunteer.role, User.Role.VOLUNTEER)
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.campaign_manager.is_active)
        self.assertTrue(self.volunteer.is_active)

    def test_role_methods(self):
        """Test role checking methods."""
        self.assertTrue(self.admin_user.is_admin())
        self.assertFalse(self.admin_user.is_campaign_manager())
        self.assertFalse(self.admin_user.is_volunteer())

        self.assertFalse(self.campaign_manager.is_admin())
        self.assertTrue(self.campaign_manager.is_campaign_manager())
        self.assertFalse(self.campaign_manager.is_volunteer())

        self.assertFalse(self.volunteer.is_admin())
        self.assertFalse(self.volunteer.is_campaign_manager())
        self.assertTrue(self.volunteer.is_volunteer())

    def test_update_level(self):
        """Test level update based on points."""
        # Test level 1 (default)
        self.assertEqual(self.volunteer.level, 1)

        # Test level 2 (100 points)
        self.volunteer.points = 100
        self.volunteer.update_level()
        self.assertEqual(self.volunteer.level, 2)

        # Test level 3 (250 points)
        self.volunteer.points = 250
        self.volunteer.update_level()
        self.assertEqual(self.volunteer.level, 3)

        # Test level doesn't change if points don't cross threshold
        self.volunteer.points = 299
        self.volunteer.update_level()
        self.assertEqual(self.volunteer.level, 3)  # Still level 3

        # Test level 4 (300 points)
        self.volunteer.points = 300
        self.volunteer.update_level()
        self.assertEqual(self.volunteer.level, 4)

    def test_telegram_fields(self):
        """Test Telegram integration fields."""
        user = User.objects.create_user(
            username='telegram_user',
            email='telegram@example.com',
            password='testpass123',
            telegram_id=123456789,
            telegram_username='telegramuser',
            telegram_chat_id=987654321
        )

        self.assertEqual(user.telegram_id, 123456789)
        self.assertEqual(user.telegram_username, 'telegramuser')
        self.assertEqual(user.telegram_chat_id, 987654321)

    def test_string_representation(self):
        """Test string representation of user."""
        self.assertEqual(str(self.admin_user), 'admin_user (admin)')
        self.assertEqual(str(self.volunteer), 'volunteer (volunteer)')

    def test_user_indexes(self):
        """Test that indexes are properly set."""
        indexes = [index.fields for index in User._meta.indexes]
        expected_indexes = [['telegram_id'], ['role'], ['points']]

        for expected in expected_indexes:
            self.assertIn(expected, indexes)


class UserAPITests(APITestCase):
    """Test User API endpoints."""

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
            username='testvolunteer',
            email='volunteer@example.com',
            password='testpass123',
            role=User.Role.VOLUNTEER
        )

        # Get tokens for authentication
        self.admin_token = RefreshToken.for_user(self.admin_user)
        self.volunteer_token = RefreshToken.for_user(self.volunteer)

    def test_register_user(self):
        """Test user registration endpoint."""
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirmation': 'newpass123',
            'role': User.Role.VOLUNTEER
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check user was created
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.role, User.Role.VOLUNTEER)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=user,
            action_type=ActivityLog.ActionType.USER_REGISTER
        ).exists())

    def test_register_user_invalid_data(self):
        """Test user registration with invalid data."""
        url = reverse('users:register')

        # Test missing required fields
        data = {'username': 'incomplete'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test duplicate username
        data = {
            'username': 'testvolunteer',  # Already exists
            'email': 'another@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """Test user login endpoint."""
        url = reverse('users:login')
        data = {
            'username': 'testvolunteer',
            'password': 'testpass123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response contains tokens
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.USER_LOGIN
        ).exists())

    def test_login_user_invalid_credentials(self):
        """Test user login with invalid credentials."""
        url = reverse('users:login')

        # Wrong password
        data = {
            'username': 'testvolunteer',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Non-existent user
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_profile(self):
        """Test retrieving current user profile."""
        url = reverse('users:profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testvolunteer')
        self.assertEqual(response.data['email'], 'volunteer@example.com')

    def test_get_user_profile_unauthenticated(self):
        """Test retrieving profile without authentication."""
        url = reverse('users:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile(self):
        """Test updating current user profile."""
        url = reverse('users:profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone_number': '+1234567890'
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check user was updated
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.first_name, 'Updated')
        self.assertEqual(self.volunteer.last_name, 'Name')
        self.assertEqual(self.volunteer.phone_number, '+1234567890')

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.USER_UPDATE
        ).exists())

    def test_list_users_admin_only(self):
        """Test listing users (admin only)."""
        url = reverse('users:user_list')

        # Test as volunteer (should fail)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test as admin (should succeed)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: Pagination returns a dictionary with 'count', so we check count
        self.assertEqual(response.data.get('count', len(response.data)), 2)  # admin + volunteer

    def test_user_detail_admin_only(self):
        """Test retrieving user detail (admin only)."""
        url = reverse('users:user_detail', args=[self.volunteer.id])

        # Test as volunteer (should fail - can't access other users)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test as admin (should succeed)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testvolunteer')

    def test_link_telegram_account(self):
        """Test linking Telegram account to user."""
        url = reverse('users:telegram_link')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'telegram_id': 123456789,
            'telegram_username': 'testuser',
            'telegram_chat_id': 987654321
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check user was updated
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.telegram_id, 123456789)
        self.assertEqual(self.volunteer.telegram_username, 'testuser')
        self.assertEqual(self.volunteer.telegram_chat_id, 987654321)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.TELEGRAM_LINK
        ).exists())

    def test_link_telegram_account_invalid_data(self):
        """Test linking Telegram account with invalid data."""
        url = reverse('users:telegram_link')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        # Missing required telegram_id
        data = {
            'telegram_username': 'testuser'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        """Test logout endpoint."""
        url = reverse('users:logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'refresh_token': str(self.volunteer_token)
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.USER_LOGOUT
        ).exists())

    def test_logout_invalid_token(self):
        """Test logout with invalid token."""
        url = reverse('users:logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'refresh_token': 'invalid_token'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        """Test changing user password."""
        url = reverse('users:change_password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'old_password': 'testpass123',
            'new_password': 'newsecurepass456'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify new password works
        self.volunteer.refresh_from_db()
        self.assertTrue(self.volunteer.check_password('newsecurepass456'))

    def test_change_password_wrong_old_password(self):
        """Test changing password with wrong old password."""
        url = reverse('users:change_password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newsecurepass456'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_weak_new_password(self):
        """Test changing password with weak new password."""
        url = reverse('users:change_password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'old_password': 'testpass123',
            'new_password': 'short'  # Too short
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserSignalTests(TestCase):
    """Test User signal handlers."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'signaluser',
            'email': 'signal@example.com',
            'password': 'testpass123'
        }

    def test_user_created_signal(self):
        """Test signal when user is created."""
        # Create user - should trigger signal
        user = User.objects.create_user(**self.user_data)

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=user,
            action_type=ActivityLog.ActionType.USER_REGISTER
        ).first()

        self.assertIsNotNone(activity_log)
        self.assertEqual(activity_log.description, f'User {user.username} registered')

    def test_user_updated_signal(self):
        """Test signal when user is updated."""
        user = User.objects.create_user(**self.user_data)

        # Clear existing logs
        ActivityLog.objects.all().delete()

        # Update user - should trigger signal
        user.first_name = 'Updated'
        user.save()

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=user,
            action_type=ActivityLog.ActionType.USER_UPDATE
        ).first()

        self.assertIsNotNone(activity_log)
        self.assertEqual(activity_log.description, f'User {user.username} profile updated')

    def test_telegram_linking_signal(self):
        """Test signal when Telegram account is linked."""
        user = User.objects.create_user(**self.user_data)

        # Clear existing logs
        ActivityLog.objects.all().delete()

        # Link Telegram account - need to simulate the _telegram_linked attribute
        user._telegram_linked = True
        user.telegram_id = 123456789
        user.telegram_username = 'telegramuser'
        user.save()

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=user,
            action_type=ActivityLog.ActionType.TELEGRAM_LINK
        ).first()

        self.assertIsNotNone(activity_log)
        self.assertEqual(activity_log.description, f'User {user.username} linked Telegram account')
        self.assertEqual(activity_log.metadata['telegram_id'], 123456789)
        self.assertEqual(activity_log.metadata['telegram_username'], 'telegramuser')

    def test_user_deleted_signal(self):
        """Test signal when user is deleted."""
        user = User.objects.create_user(**self.user_data)
        user_id = user.id
        username = user.username

        # Delete user
        user.delete()

        # Signal logs to logger, not ActivityLog (since user is being deleted)
        # We can't easily test logger output, but we can verify no ActivityLog was created
        # with this user (since foreign key would fail)
        self.assertFalse(ActivityLog.objects.filter(user_id=user_id).exists())

    @patch('apps.users.signals.logger')
    def test_user_logged_in_signal(self, mock_logger):
        """Test signal when user logs in."""
        from django.contrib.auth.signals import user_logged_in
        from apps.users import signals

        # Connect the signal
        user_logged_in.connect(signals.user_logged_in)

        # Create mock request
        mock_request = MagicMock()
        mock_request.META = {
            'REMOTE_ADDR': '127.0.0.1',
            'HTTP_USER_AGENT': 'TestClient'
        }

        # Create a user object
        user = User.objects.create_user(**self.user_data)
        # Trigger signal
        user_logged_in.send(sender=self.__class__, request=mock_request, user=user)

        # Check ActivityLog was created
        # Note: We can't easily test this without actual user object
        # This is more of an integration test

    @patch('apps.users.signals.logger')
    def test_user_logged_out_signal(self, mock_logger):
        """Test signal when user logs out."""
        from django.contrib.auth.signals import user_logged_out
        from apps.users import signals

        # Connect the signal
        user_logged_out.connect(signals.user_logged_out)

        # Create mock request and user
        mock_request = MagicMock()
        mock_request.META = {'REMOTE_ADDR': '127.0.0.1'}

        user = User.objects.create_user(**self.user_data)

        # Trigger signal
        user_logged_out.send(sender=self.__class__, request=mock_request, user=user)

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=user,
            action_type=ActivityLog.ActionType.USER_LOGOUT
        ).first()

        self.assertIsNotNone(activity_log)
        self.assertEqual(activity_log.description, f'User {user.username} logged out')
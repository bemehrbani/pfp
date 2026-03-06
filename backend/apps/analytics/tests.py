"""
Comprehensive tests for Analytics app.

Tests cover:
1. ActivityLog model with different action types
2. AnalyticsSnapshot model
3. API endpoints: dashboard stats, campaign analytics, system analytics
4. Permission checks and edge cases
"""

import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.analytics.models import ActivityLog, AnalyticsSnapshot
from apps.campaigns.models import Campaign, CampaignVolunteer
from apps.tasks.models import Task, TaskAssignment

User = get_user_model()


class ActivityLogModelTests(TestCase):
    """Test ActivityLog model creation and methods."""

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

        # Create test campaign for content object
        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            description='A test campaign',
            short_description='Test',
            created_by=self.admin_user
        )

    def test_activity_log_creation(self):
        """Test ActivityLog creation with all fields."""
        # Get content type for campaign
        content_type = ContentType.objects.get_for_model(self.campaign)

        activity_log = ActivityLog.objects.create(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.CAMPAIGN_CREATE,
            description='Campaign "Test Campaign" created',
            content_type=content_type,
            object_id=self.campaign.id,
            metadata={'campaign_id': self.campaign.id, 'action': 'create'},
            ip_address='127.0.0.1',
            user_agent='TestClient/1.0'
        )

        self.assertEqual(activity_log.user, self.admin_user)
        self.assertEqual(activity_log.action_type, ActivityLog.ActionType.CAMPAIGN_CREATE)
        self.assertEqual(activity_log.description, 'Campaign "Test Campaign" created')
        self.assertEqual(activity_log.content_object, self.campaign)
        self.assertEqual(activity_log.metadata['campaign_id'], self.campaign.id)
        self.assertEqual(activity_log.ip_address, '127.0.0.1')
        self.assertEqual(activity_log.user_agent, 'TestClient/1.0')
        self.assertIsNotNone(activity_log.created_at)

    def test_activity_log_string_representation(self):
        """Test string representation of ActivityLog."""
        activity_log = ActivityLog.objects.create(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.USER_LOGIN,
            description='User admin_user logged in'
        )

        expected_str = f'{ActivityLog.ActionType.USER_LOGIN} by {self.admin_user} at {activity_log.created_at}'
        self.assertEqual(str(activity_log), expected_str)

    def test_activity_log_without_user(self):
        """Test ActivityLog creation without a user (anonymous actions)."""
        activity_log = ActivityLog.objects.create(
            user=None,
            action_type=ActivityLog.ActionType.USER_REGISTER,
            description='New user registered',
            ip_address='192.168.1.1'
        )

        self.assertIsNone(activity_log.user)
        self.assertEqual(activity_log.action_type, ActivityLog.ActionType.USER_REGISTER)
        self.assertIsNotNone(activity_log.created_at)

    def test_activity_log_without_content_object(self):
        """Test ActivityLog creation without a content object."""
        activity_log = ActivityLog.objects.create(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.USER_LOGIN,
            description='User volunteer logged in'
        )

        self.assertEqual(activity_log.user, self.volunteer)
        self.assertIsNone(activity_log.content_type)
        self.assertIsNone(activity_log.object_id)
        self.assertIsNone(activity_log.content_object)

    def test_activity_log_indexes(self):
        """Test that indexes are properly set."""
        indexes = [index.fields for index in ActivityLog._meta.indexes]
        expected_indexes = [['action_type'], ['user', 'created_at'], ['created_at']]

        for expected in expected_indexes:
            self.assertIn(expected, indexes)

    def test_activity_log_ordering(self):
        """Test ActivityLog ordering (newest first)."""
        # Create logs in order
        log1 = ActivityLog.objects.create(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.USER_LOGIN,
            description='First login'
        )

        log2 = ActivityLog.objects.create(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.USER_LOGIN,
            description='Second login'
        )

        logs = ActivityLog.objects.all()
        self.assertEqual(logs[0], log2)  # Newest first
        self.assertEqual(logs[1], log1)  # Oldest last


class AnalyticsSnapshotModelTests(TestCase):
    """Test AnalyticsSnapshot model."""

    def setUp(self):
        """Set up test data."""
        self.today = timezone.now().date()

    def test_analytics_snapshot_creation(self):
        """Test AnalyticsSnapshot creation with all fields."""
        snapshot = AnalyticsSnapshot.objects.create(
            snapshot_type='daily',
            snapshot_date=self.today,
            total_users=100,
            new_users=5,
            active_users=75,
            total_campaigns=10,
            active_campaigns=3,
            completed_campaigns=2,
            total_tasks=50,
            completed_tasks=30,
            verification_rate=60.0,
            total_points_awarded=1500,
            avg_points_per_user=15.0,
            avg_tasks_per_user=0.5
        )

        self.assertEqual(snapshot.snapshot_type, 'daily')
        self.assertEqual(snapshot.snapshot_date, self.today)
        self.assertEqual(snapshot.total_users, 100)
        self.assertEqual(snapshot.new_users, 5)
        self.assertEqual(snapshot.active_users, 75)
        self.assertEqual(snapshot.total_campaigns, 10)
        self.assertEqual(snapshot.active_campaigns, 3)
        self.assertEqual(snapshot.completed_campaigns, 2)
        self.assertEqual(snapshot.total_tasks, 50)
        self.assertEqual(snapshot.completed_tasks, 30)
        self.assertEqual(snapshot.verification_rate, 60.0)
        self.assertEqual(snapshot.total_points_awarded, 1500)
        self.assertEqual(snapshot.avg_points_per_user, 15.0)
        self.assertEqual(snapshot.avg_tasks_per_user, 0.5)
        self.assertIsNotNone(snapshot.created_at)

    def test_analytics_snapshot_string_representation(self):
        """Test string representation of AnalyticsSnapshot."""
        snapshot = AnalyticsSnapshot.objects.create(
            snapshot_type='weekly',
            snapshot_date=self.today
        )

        expected_str = f'weekly snapshot for {self.today}'
        self.assertEqual(str(snapshot), expected_str)

    def test_analytics_snapshot_unique_together(self):
        """Test unique_together constraint for snapshot_type and snapshot_date."""
        # Create first snapshot
        AnalyticsSnapshot.objects.create(
            snapshot_type='daily',
            snapshot_date=self.today
        )

        # Try to create another snapshot with same type and date
        with self.assertRaises(Exception):
            AnalyticsSnapshot.objects.create(
                snapshot_type='daily',
                snapshot_date=self.today
            )

        # Should allow different type for same date
        AnalyticsSnapshot.objects.create(
            snapshot_type='weekly',
            snapshot_date=self.today
        )

        # Should allow same type for different date
        yesterday = self.today - timedelta(days=1)
        AnalyticsSnapshot.objects.create(
            snapshot_type='daily',
            snapshot_date=yesterday
        )

    def test_analytics_snapshot_ordering(self):
        """Test AnalyticsSnapshot ordering."""
        # Create snapshots in different order
        snapshot1 = AnalyticsSnapshot.objects.create(
            snapshot_type='daily',
            snapshot_date=self.today - timedelta(days=2)
        )

        snapshot2 = AnalyticsSnapshot.objects.create(
            snapshot_type='weekly',
            snapshot_date=self.today - timedelta(days=1)
        )

        snapshot3 = AnalyticsSnapshot.objects.create(
            snapshot_type='daily',
            snapshot_date=self.today - timedelta(days=1)
        )

        snapshot4 = AnalyticsSnapshot.objects.create(
            snapshot_type='daily',
            snapshot_date=self.today
        )

        snapshots = AnalyticsSnapshot.objects.all()
        # Should be ordered by snapshot_date descending, then snapshot_type
        self.assertEqual(snapshots[0], snapshot4)  # Today daily
        self.assertEqual(snapshots[1], snapshot3)  # Yesterday daily
        self.assertEqual(snapshots[2], snapshot2)  # Yesterday weekly
        self.assertEqual(snapshots[3], snapshot1)  # Day before yesterday daily


class AnalyticsAPITests(APITestCase):
    """Test Analytics API endpoints."""

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
        self.campaign_manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123',
            role=User.Role.CAMPAIGN_MANAGER
        )
        self.volunteer = User.objects.create_user(
            username='volunteer',
            email='volunteer@example.com',
            password='volunteerpass123',
            role=User.Role.VOLUNTEER
        )

        # Get tokens for authentication
        self.admin_token = RefreshToken.for_user(self.admin_user)
        self.manager_token = RefreshToken.for_user(self.campaign_manager)
        self.volunteer_token = RefreshToken.for_user(self.volunteer)

        # Create test campaigns
        self.campaign1 = Campaign.objects.create(
            name='Admin Campaign',
            description='Campaign created by admin',
            short_description='Admin campaign',
            campaign_type=Campaign.CampaignType.REGULAR,
            status=Campaign.Status.ACTIVE,
            created_by=self.admin_user,
            target_members=100,
            target_activities=50
        )

        self.campaign2 = Campaign.objects.create(
            name='Manager Campaign',
            description='Campaign managed by manager',
            short_description='Manager campaign',
            campaign_type=Campaign.CampaignType.REGULAR,
            status=Campaign.Status.DRAFT,
            created_by=self.admin_user,
            target_members=50,
            target_activities=25
        )
        self.campaign2.managers.add(self.campaign_manager)

        # Add volunteer to campaign1
        CampaignVolunteer.objects.create(
            campaign=self.campaign1,
            volunteer=self.volunteer,
            status=CampaignVolunteer.Status.ACTIVE
        )

        # Create test tasks and assignments
        self.task1 = Task.objects.create(
            title='Task 1',
            description='Task in admin campaign',
            instructions='Complete this task',
            task_type=Task.TaskType.TWITTER_POST,
            campaign=self.campaign1,
            created_by=self.admin_user,
            points=10
        )

        self.task2 = Task.objects.create(
            title='Task 2',
            description='Task in manager campaign',
            instructions='Complete this task',
            task_type=Task.TaskType.TWITTER_RETWEET,
            campaign=self.campaign2,
            created_by=self.admin_user,
            points=15
        )

        # Create completed task assignment for volunteer
        self.assignment = TaskAssignment.objects.create(
            task=self.task1,
            volunteer=self.volunteer,
            campaign=self.campaign1,
            status=TaskAssignment.Status.VERIFIED,
            points_awarded=10,
            verified_by=self.admin_user
        )

        # Create some activity logs
        ActivityLog.objects.create(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.CAMPAIGN_CREATE,
            description='Campaign "Admin Campaign" created',
            content_object=self.campaign1
        )

        ActivityLog.objects.create(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.USER_LOGIN,
            description='User volunteer logged in'
        )

        # Update user last_login for active users calculation
        self.volunteer.last_login = timezone.now()
        self.volunteer.save()

    def test_dashboard_stats_admin(self):
        """Test dashboard statistics for admin."""
        url = reverse('analytics:dashboard-stats')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response contains expected fields
        self.assertIn('active_campaigns', response.data)
        self.assertIn('total_campaigns', response.data)
        self.assertIn('my_tasks', response.data)
        self.assertIn('points_earned', response.data)
        self.assertIn('total_volunteers', response.data)
        self.assertIn('active_volunteers', response.data)
        self.assertIn('recent_activity', response.data)

        # Admin should see all campaigns
        self.assertEqual(response.data['total_campaigns'], 2)
        self.assertEqual(response.data['active_campaigns'], 1)  # Only campaign1 is active

    def test_dashboard_stats_manager(self):
        """Test dashboard statistics for campaign manager."""
        url = reverse('analytics:dashboard-stats')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Manager should only see managed campaigns
        self.assertEqual(response.data['total_campaigns'], 1)  # Only campaign2
        self.assertEqual(response.data['active_campaigns'], 0)  # campaign2 is draft

    def test_dashboard_stats_volunteer(self):
        """Test dashboard statistics for volunteer."""
        url = reverse('analytics:dashboard-stats')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Volunteer should only see joined campaigns
        self.assertEqual(response.data['total_campaigns'], 1)  # Only campaign1
        self.assertEqual(response.data['active_campaigns'], 1)  # campaign1 is active
        self.assertEqual(response.data['points_earned'], 10)  # From verified assignment
        self.assertEqual(response.data['my_tasks'], 0)  # No assigned/in-progress tasks

        # Check recent activity
        self.assertGreater(len(response.data['recent_activity']), 0)

    def test_campaign_analytics_admin(self):
        """Test campaign analytics for admin (should have access)."""
        url = reverse('analytics:campaign-analytics', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response contains expected fields
        self.assertIn('campaign', response.data)
        self.assertIn('progress', response.data)
        self.assertIn('task_types', response.data)
        self.assertIn('top_volunteers', response.data)
        self.assertIn('recent_activity', response.data)

        # Check campaign data
        self.assertEqual(response.data['campaign']['id'], self.campaign1.id)
        self.assertEqual(response.data['campaign']['name'], 'Admin Campaign')

        # Check progress data
        self.assertIn('members', response.data['progress'])
        self.assertIn('activities', response.data['progress'])
        self.assertIn('twitter_posts', response.data['progress'])

    def test_campaign_analytics_manager(self):
        """Test campaign analytics for manager (should have access to managed campaign)."""
        url = reverse('analytics:campaign-analytics', args=[self.campaign2.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Manager should have access to managed campaign
        self.assertEqual(response.data['campaign']['id'], self.campaign2.id)

    def test_campaign_analytics_manager_unauthorized(self):
        """Test campaign analytics for manager (should NOT have access to unmanaged campaign)."""
        url = reverse('analytics:campaign-analytics', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_campaign_analytics_volunteer(self):
        """Test campaign analytics for volunteer (should NOT have access)."""
        url = reverse('analytics:campaign-analytics', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_campaign_analytics_not_found(self):
        """Test campaign analytics for non-existent campaign."""
        url = reverse('analytics:campaign-analytics', args=[999])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_system_analytics_admin(self):
        """Test system analytics for admin (should have access)."""
        url = reverse('analytics:system-analytics')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response contains expected fields
        self.assertIn('users', response.data)
        self.assertIn('campaigns', response.data)
        self.assertIn('tasks', response.data)
        self.assertIn('points', response.data)
        self.assertIn('daily_activity', response.data)

        # Check user statistics
        self.assertEqual(response.data['users']['total'], 3)  # admin, manager, volunteer
        self.assertIn('new_week', response.data['users'])
        self.assertIn('new_month', response.data['users'])
        self.assertIn('active_week', response.data['users'])

        # Check campaign statistics
        self.assertEqual(response.data['campaigns']['total'], 2)
        self.assertEqual(response.data['campaigns']['active'], 1)
        self.assertEqual(response.data['campaigns']['completed'], 0)

        # Check task statistics
        self.assertEqual(response.data['tasks']['total'], 2)
        self.assertEqual(response.data['tasks']['completed'], 1)  # One verified assignment

    def test_system_analytics_non_admin(self):
        """Test system analytics for non-admin (should NOT have access)."""
        url = reverse('analytics:system-analytics')

        # Test as campaign manager
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test as volunteer
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_time_ago_helper_method(self):
        """Test the _time_ago helper method."""
        from apps.analytics.api.views import DashboardStatsView

        view = DashboardStatsView()
        now = timezone.now()

        # Test just now
        self.assertEqual(view._time_ago(now), 'just now')

        # Test minutes ago
        two_minutes_ago = now - timedelta(minutes=2)
        self.assertEqual(view._time_ago(two_minutes_ago), '2 minutes ago')

        # Test hours ago
        three_hours_ago = now - timedelta(hours=3)
        self.assertEqual(view._time_ago(three_hours_ago), '3 hours ago')

        # Test days ago
        five_days_ago = now - timedelta(days=5)
        self.assertEqual(view._time_ago(five_days_ago), '5 days ago')

        # Test months ago
        two_months_ago = now - timedelta(days=65)
        self.assertEqual(view._time_ago(two_months_ago), '2 months ago')

        # Test years ago
        three_years_ago = now - timedelta(days=1100)
        self.assertEqual(view._time_ago(three_years_ago), '3 years ago')

    def test_campaign_analytics_time_ago_helper(self):
        """Test the _time_ago helper method in CampaignAnalyticsView."""
        from apps.analytics.api.views import CampaignAnalyticsView

        view = CampaignAnalyticsView()
        now = timezone.now()

        # Test just now
        self.assertEqual(view._time_ago(now), 'just now')

        # Test minutes ago
        two_minutes_ago = now - timedelta(minutes=2)
        self.assertEqual(view._time_ago(two_minutes_ago), '2m ago')

        # Test hours ago
        three_hours_ago = now - timedelta(hours=3)
        self.assertEqual(view._time_ago(three_hours_ago), '3h ago')

        # Test days ago
        five_days_ago = now - timedelta(days=5)
        self.assertEqual(view._time_ago(five_days_ago), '5d ago')

    def test_dashboard_stats_with_no_activity(self):
        """Test dashboard statistics when user has no recent activity."""
        # Create a new user with no activity
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpass123',
            role=User.Role.VOLUNTEER
        )

        new_user_token = RefreshToken.for_user(new_user)

        url = reverse('analytics:dashboard-stats')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_user_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # New user should have 0 for most stats
        self.assertEqual(response.data['total_campaigns'], 0)
        self.assertEqual(response.data['active_campaigns'], 0)
        self.assertEqual(response.data['points_earned'], 0)
        self.assertEqual(response.data['my_tasks'], 0)

        # Recent activity should be empty list
        self.assertEqual(len(response.data['recent_activity']), 0)
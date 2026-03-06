"""
Comprehensive tests for Campaigns app.

Tests cover:
1. Campaign model creation and methods
2. CampaignVolunteer and CampaignUpdate models
3. API endpoints (CRUD, join, volunteers, updates, stats)
4. Signal handlers for campaign creation and volunteer joining
5. Permission checks and edge cases
"""

import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.campaigns.models import Campaign, CampaignVolunteer, CampaignUpdate
from apps.analytics.models import ActivityLog
from apps.tasks.models import Task, TaskAssignment

User = get_user_model()


class CampaignModelTests(TestCase):
    """Test Campaign model creation and methods."""

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

        # Create test campaign
        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            description='A test campaign for peace',
            short_description='Test campaign',
            campaign_type=Campaign.CampaignType.REGULAR,
            status=Campaign.Status.DRAFT,
            created_by=self.admin_user,
            target_members=100,
            target_activities=50,
            target_twitter_posts=0
        )
        self.campaign.managers.add(self.campaign_manager)

    def test_campaign_creation(self):
        """Test campaign creation with all fields."""
        self.assertEqual(self.campaign.name, 'Test Campaign')
        self.assertEqual(self.campaign.description, 'A test campaign for peace')
        self.assertEqual(self.campaign.campaign_type, Campaign.CampaignType.REGULAR)
        self.assertEqual(self.campaign.status, Campaign.Status.DRAFT)
        self.assertEqual(self.campaign.created_by, self.admin_user)
        self.assertEqual(self.campaign.target_members, 100)
        self.assertEqual(self.campaign.target_activities, 50)
        self.assertEqual(self.campaign.target_twitter_posts, 0)
        self.assertIn(self.campaign_manager, self.campaign.managers.all())

    def test_campaign_string_representation(self):
        """Test string representation of campaign."""
        self.assertEqual(str(self.campaign), 'Test Campaign')

    def test_campaign_progress_percentage(self):
        """Test progress percentage calculation."""
        # Test with no progress
        self.assertEqual(self.campaign.progress_percentage(), 0)

        # Test with some progress
        self.campaign.current_members = 50
        self.campaign.completed_activities = 25
        progress = self.campaign.progress_percentage()
        expected = ((50 + 25) / (100 + 50)) * 100
        self.assertEqual(progress, expected)

        # Test with Twitter posts
        twitter_campaign = Campaign.objects.create(
            name='Twitter Campaign',
            description='Twitter storm campaign',
            short_description='Twitter campaign',
            campaign_type=Campaign.CampaignType.TWITTER_STORM,
            status=Campaign.Status.ACTIVE,
            created_by=self.admin_user,
            target_members=0,
            target_activities=0,
            target_twitter_posts=100
        )
        twitter_campaign.completed_twitter_posts = 75
        progress = twitter_campaign.progress_percentage()
        self.assertEqual(progress, 75)  # 75/100 = 75%

        # Test with all zeros (no targets)
        no_target_campaign = Campaign.objects.create(
            name='No Target Campaign',
            description='Campaign with no targets',
            short_description='No targets',
            campaign_type=Campaign.CampaignType.REGULAR,
            status=Campaign.Status.DRAFT,
            created_by=self.admin_user,
            target_members=0,
            target_activities=0,
            target_twitter_posts=0
        )
        self.assertEqual(no_target_campaign.progress_percentage(), 0)

    def test_is_active_method(self):
        """Test is_active method."""
        self.assertFalse(self.campaign.is_active())

        self.campaign.status = Campaign.Status.ACTIVE
        self.assertTrue(self.campaign.is_active())

        self.campaign.status = Campaign.Status.PAUSED
        self.assertFalse(self.campaign.is_active())

    def test_is_twitter_storm_method(self):
        """Test is_twitter_storm method."""
        self.assertFalse(self.campaign.is_twitter_storm())

        # Test Twitter storm campaign
        twitter_campaign = Campaign.objects.create(
            name='Twitter Storm',
            description='Twitter storm campaign',
            short_description='Twitter storm',
            campaign_type=Campaign.CampaignType.TWITTER_STORM,
            status=Campaign.Status.ACTIVE,
            created_by=self.admin_user
        )
        self.assertTrue(twitter_campaign.is_twitter_storm())

        # Test hybrid campaign
        hybrid_campaign = Campaign.objects.create(
            name='Hybrid Campaign',
            description='Hybrid campaign',
            short_description='Hybrid',
            campaign_type=Campaign.CampaignType.HYBRID,
            status=Campaign.Status.ACTIVE,
            created_by=self.admin_user
        )
        self.assertTrue(hybrid_campaign.is_twitter_storm())

    def test_update_statistics_method(self):
        """Test update_statistics method."""
        # Add volunteers
        self.campaign.volunteers.add(self.volunteer)

        # Create a task and assignment for this campaign
        task = Task.objects.create(
            campaign=self.campaign,
            title='Test Task',
            description='Test task description',
            task_type='social_media_post',
            points=10,
            max_assignments=5
        )

        # Create a completed assignment
        assignment = TaskAssignment.objects.create(
            task=task,
            volunteer=self.volunteer,
            status=TaskAssignment.Status.COMPLETED
        )

        # Update statistics
        self.campaign.update_statistics()

        # Check statistics
        self.assertEqual(self.campaign.current_members, 1)
        self.assertEqual(self.campaign.completed_activities, 1)
        self.assertEqual(self.campaign.completed_twitter_posts, 0)  # Not a Twitter task

    def test_campaign_indexes(self):
        """Test that indexes are properly set."""
        indexes = [index.fields for index in Campaign._meta.indexes]
        expected_indexes = [['status'], ['campaign_type'], ['start_date', 'end_date']]

        for expected in expected_indexes:
            self.assertIn(expected, indexes)


class CampaignVolunteerModelTests(TestCase):
    """Test CampaignVolunteer model."""

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

        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            description='A test campaign',
            short_description='Test',
            created_by=self.admin_user
        )

    def test_campaign_volunteer_creation(self):
        """Test CampaignVolunteer creation."""
        campaign_volunteer = CampaignVolunteer.objects.create(
            campaign=self.campaign,
            volunteer=self.volunteer,
            status=CampaignVolunteer.Status.ACTIVE
        )

        self.assertEqual(campaign_volunteer.campaign, self.campaign)
        self.assertEqual(campaign_volunteer.volunteer, self.volunteer)
        self.assertEqual(campaign_volunteer.status, CampaignVolunteer.Status.ACTIVE)
        self.assertEqual(campaign_volunteer.points_earned, 0)
        self.assertIsNotNone(campaign_volunteer.joined_at)
        self.assertIsNotNone(campaign_volunteer.last_active)

    def test_campaign_volunteer_string_representation(self):
        """Test string representation of CampaignVolunteer."""
        campaign_volunteer = CampaignVolunteer.objects.create(
            campaign=self.campaign,
            volunteer=self.volunteer
        )
        self.assertEqual(str(campaign_volunteer), f'{self.volunteer.username} - {self.campaign.name}')

    def test_unique_together_constraint(self):
        """Test that a volunteer can only join a campaign once."""
        CampaignVolunteer.objects.create(
            campaign=self.campaign,
            volunteer=self.volunteer
        )

        # Try to create another record with same campaign and volunteer
        with self.assertRaises(Exception):
            CampaignVolunteer.objects.create(
                campaign=self.campaign,
                volunteer=self.volunteer
            )


class CampaignUpdateModelTests(TestCase):
    """Test CampaignUpdate model."""

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='testpass123',
            role=User.Role.ADMIN
        )

        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            description='A test campaign',
            short_description='Test',
            created_by=self.admin_user
        )

    def test_campaign_update_creation(self):
        """Test CampaignUpdate creation."""
        update = CampaignUpdate.objects.create(
            campaign=self.campaign,
            title='Important Update',
            content='This is an important update about the campaign.',
            created_by=self.admin_user,
            is_pinned=True
        )

        self.assertEqual(update.campaign, self.campaign)
        self.assertEqual(update.title, 'Important Update')
        self.assertEqual(update.content, 'This is an important update about the campaign.')
        self.assertEqual(update.created_by, self.admin_user)
        self.assertTrue(update.is_pinned)
        self.assertFalse(update.sent_to_telegram)
        self.assertIsNotNone(update.created_at)
        self.assertIsNotNone(update.updated_at)

    def test_campaign_update_string_representation(self):
        """Test string representation of CampaignUpdate."""
        update = CampaignUpdate.objects.create(
            campaign=self.campaign,
            title='Test Update',
            content='Test content',
            created_by=self.admin_user
        )
        self.assertEqual(str(update), 'Test Update')

    def test_campaign_update_ordering(self):
        """Test CampaignUpdate ordering (pinned first, then by creation date)."""
        # Create updates in reverse order
        update1 = CampaignUpdate.objects.create(
            campaign=self.campaign,
            title='Update 1',
            content='Content 1',
            created_by=self.admin_user,
            is_pinned=False
        )

        update2 = CampaignUpdate.objects.create(
            campaign=self.campaign,
            title='Update 2',
            content='Content 2',
            created_by=self.admin_user,
            is_pinned=True  # This should appear first
        )

        update3 = CampaignUpdate.objects.create(
            campaign=self.campaign,
            title='Update 3',
            content='Content 3',
            created_by=self.admin_user,
            is_pinned=False
        )

        updates = CampaignUpdate.objects.all()
        self.assertEqual(updates[0], update2)  # Pinned first
        self.assertEqual(updates[1], update3)  # Most recent non-pinned
        self.assertEqual(updates[2], update1)  # Oldest non-pinned


class CampaignAPITests(APITestCase):
    """Test Campaign API endpoints."""

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
            campaign_type=Campaign.CampaignType.TWITTER_STORM,
            status=Campaign.Status.DRAFT,
            created_by=self.admin_user,
            target_members=50,
            target_activities=25,
            target_twitter_posts=100
        )
        self.campaign2.managers.add(self.campaign_manager)

        # Add volunteer to campaign1
        CampaignVolunteer.objects.create(
            campaign=self.campaign1,
            volunteer=self.volunteer,
            status=CampaignVolunteer.Status.ACTIVE
        )

    def test_list_campaigns_admin(self):
        """Test listing campaigns as admin (should see all)."""
        url = reverse('campaigns:campaign-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should see both campaigns

    def test_list_campaigns_manager(self):
        """Test listing campaigns as campaign manager (should see managed campaigns)."""
        url = reverse('campaigns:campaign-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see campaign2
        self.assertEqual(response.data[0]['name'], 'Manager Campaign')

    def test_list_campaigns_volunteer(self):
        """Test listing campaigns as volunteer (should see joined campaigns)."""
        url = reverse('campaigns:campaign-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see campaign1
        self.assertEqual(response.data[0]['name'], 'Admin Campaign')

    def test_create_campaign_admin(self):
        """Test creating a campaign as admin."""
        url = reverse('campaigns:campaign-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        data = {
            'name': 'New Campaign',
            'description': 'A new campaign for peace',
            'short_description': 'New campaign',
            'campaign_type': Campaign.CampaignType.REGULAR,
            'status': Campaign.Status.DRAFT,
            'target_members': 200,
            'target_activities': 100,
            'managers': [self.campaign_manager.id]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check campaign was created
        campaign = Campaign.objects.get(name='New Campaign')
        self.assertEqual(campaign.description, 'A new campaign for peace')
        self.assertEqual(campaign.created_by, self.admin_user)
        self.assertIn(self.campaign_manager, campaign.managers.all())

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.CAMPAIGN_CREATE,
            description=f'Campaign "New Campaign" created'
        ).exists())

    def test_create_campaign_non_admin(self):
        """Test creating a campaign as non-admin (should fail)."""
        url = reverse('campaigns:campaign-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        data = {
            'name': 'Unauthorized Campaign',
            'description': 'Should not be allowed',
            'short_description': 'Unauthorized',
            'campaign_type': Campaign.CampaignType.REGULAR
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_campaign_detail_admin(self):
        """Test retrieving campaign detail as admin."""
        url = reverse('campaigns:campaign-detail', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Admin Campaign')

    def test_retrieve_campaign_detail_manager(self):
        """Test retrieving campaign detail as manager (should succeed for managed campaign)."""
        url = reverse('campaigns:campaign-detail', args=[self.campaign2.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Manager Campaign')

    def test_retrieve_campaign_detail_manager_unauthorized(self):
        """Test retrieving campaign detail as manager for unmanaged campaign (should fail)."""
        url = reverse('campaigns:campaign-detail', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_campaign_admin(self):
        """Test updating a campaign as admin."""
        url = reverse('campaigns:campaign-detail', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        data = {
            'name': 'Updated Campaign Name',
            'description': 'Updated description',
            'status': Campaign.Status.ACTIVE
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check campaign was updated
        self.campaign1.refresh_from_db()
        self.assertEqual(self.campaign1.name, 'Updated Campaign Name')
        self.assertEqual(self.campaign1.status, Campaign.Status.ACTIVE)

        # Check ActivityLog was created for status change
        self.assertTrue(ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.CAMPAIGN_UPDATE,
            description=f'Campaign "Updated Campaign Name" status changed to active'
        ).exists())

    def test_delete_campaign_admin(self):
        """Test deleting a campaign as admin."""
        url = reverse('campaigns:campaign-detail', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check campaign was deleted
        self.assertFalse(Campaign.objects.filter(id=self.campaign1.id).exists())

    def test_join_campaign(self):
        """Test joining a campaign as a volunteer."""
        url = reverse('campaigns:campaign-join', args=[self.campaign2.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check volunteer was added
        self.assertTrue(self.campaign2.volunteers.filter(id=self.volunteer.id).exists())

        # Check CampaignVolunteer was created
        campaign_volunteer = CampaignVolunteer.objects.get(
            campaign=self.campaign2,
            volunteer=self.volunteer
        )
        self.assertEqual(campaign_volunteer.status, CampaignVolunteer.Status.ACTIVE)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.CAMPAIGN_JOIN,
            description=f'User {self.volunteer.username} joined campaign "{self.campaign2.name}"'
        ).exists())

    def test_join_campaign_already_member(self):
        """Test joining a campaign when already a member."""
        url = reverse('campaigns:campaign-join', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_join_campaign_not_found(self):
        """Test joining a non-existent campaign."""
        url = reverse('campaigns:campaign-join', args=[999])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_campaign_stats(self):
        """Test retrieving campaign statistics."""
        url = reverse('campaigns:campaign-stats', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response contains expected fields
        self.assertIn('progress_percentage', response.data)
        self.assertIn('current_members', response.data)
        self.assertIn('completed_activities', response.data)

    def test_campaign_updates_list(self):
        """Test listing campaign updates."""
        # Create some updates
        CampaignUpdate.objects.create(
            campaign=self.campaign1,
            title='Update 1',
            content='Content 1',
            created_by=self.admin_user
        )
        CampaignUpdate.objects.create(
            campaign=self.campaign1,
            title='Update 2',
            content='Content 2',
            created_by=self.admin_user,
            is_pinned=True
        )

        url = reverse('campaigns:campaign-update-list', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_campaign_update(self):
        """Test creating a campaign update."""
        url = reverse('campaigns:campaign-update-list', args=[self.campaign1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        data = {
            'title': 'Important Announcement',
            'content': 'This is an important announcement for all volunteers.',
            'is_pinned': True
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check update was created
        update = CampaignUpdate.objects.get(title='Important Announcement')
        self.assertEqual(update.campaign, self.campaign1)
        self.assertEqual(update.created_by, self.admin_user)
        self.assertTrue(update.is_pinned)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.CAMPAIGN_UPDATE,
            description=f'Update "Important Announcement" created for campaign "{self.campaign1.name}"'
        ).exists())


class CampaignSignalTests(TestCase):
    """Test Campaign signal handlers."""

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

    def test_campaign_created_signal(self):
        """Test signal when campaign is created."""
        # Create campaign - should trigger signal
        campaign = Campaign.objects.create(
            name='Signal Campaign',
            description='Campaign for signal testing',
            short_description='Signal test',
            created_by=self.admin_user
        )

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.CAMPAIGN_CREATE,
            description=f'Campaign "Signal Campaign" created'
        ).first()

        self.assertIsNotNone(activity_log)

    def test_campaign_updated_signal_status_change(self):
        """Test signal when campaign status is updated."""
        campaign = Campaign.objects.create(
            name='Status Change Campaign',
            description='Campaign for status change testing',
            short_description='Status test',
            created_by=self.admin_user,
            status=Campaign.Status.DRAFT
        )

        # Clear existing logs
        ActivityLog.objects.all().delete()

        # Update status - should trigger signal
        campaign.status = Campaign.Status.ACTIVE
        campaign.save()

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.CAMPAIGN_UPDATE,
            description=f'Campaign "Status Change Campaign" status changed to active'
        ).first()

        self.assertIsNotNone(activity_log)
        self.assertEqual(activity_log.metadata['new_status'], 'active')

    def test_volunteer_joined_campaign_signal(self):
        """Test signal when volunteer joins a campaign."""
        campaign = Campaign.objects.create(
            name='Join Test Campaign',
            description='Campaign for join testing',
            short_description='Join test',
            created_by=self.admin_user
        )

        # Clear existing logs
        ActivityLog.objects.all().delete()

        # Create CampaignVolunteer - should trigger signal
        campaign_volunteer = CampaignVolunteer.objects.create(
            campaign=campaign,
            volunteer=self.volunteer,
            status=CampaignVolunteer.Status.ACTIVE
        )

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.CAMPAIGN_JOIN,
            description=f'User {self.volunteer.username} joined campaign "{campaign.name}"'
        ).first()

        self.assertIsNotNone(activity_log)

    def test_campaign_update_created_signal(self):
        """Test signal when campaign update is created."""
        campaign = Campaign.objects.create(
            name='Update Test Campaign',
            description='Campaign for update testing',
            short_description='Update test',
            created_by=self.admin_user
        )

        # Clear existing logs
        ActivityLog.objects.all().delete()

        # Create CampaignUpdate - should trigger signal
        update = CampaignUpdate.objects.create(
            campaign=campaign,
            title='Test Update',
            content='Test content',
            created_by=self.admin_user
        )

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.CAMPAIGN_UPDATE,
            description=f'Update "Test Update" created for campaign "{campaign.name}"'
        ).first()

        self.assertIsNotNone(activity_log)
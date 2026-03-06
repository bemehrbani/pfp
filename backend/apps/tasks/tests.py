"""
Comprehensive tests for Tasks app.

Tests cover:
1. Task model creation and methods (is_available(), available_slots())
2. TaskAssignment model with status transitions and points awarding
3. API endpoints (task CRUD, assignments, completion, verification)
4. Signal handlers for task assignment status changes
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
from apps.tasks.models import Task, TaskAssignment
from apps.campaigns.models import Campaign, CampaignVolunteer
from apps.analytics.models import ActivityLog

User = get_user_model()


class TaskModelTests(TestCase):
    """Test Task model creation and methods."""

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
            status=Campaign.Status.ACTIVE,
            created_by=self.admin_user
        )
        self.campaign.managers.add(self.campaign_manager)

        # Add volunteer to campaign
        CampaignVolunteer.objects.create(
            campaign=self.campaign,
            volunteer=self.volunteer,
            status=CampaignVolunteer.Status.ACTIVE
        )

        # Create test task
        self.task = Task.objects.create(
            title='Test Task',
            description='A test task for volunteers',
            instructions='1. Do this\n2. Then do that\n3. Submit proof',
            task_type=Task.TaskType.TWITTER_POST,
            assignment_type=Task.AssignmentType.FIRST_COME,
            campaign=self.campaign,
            created_by=self.admin_user,
            points=10,
            estimated_time=15,
            max_assignments=5,
            is_active=True,
            is_verified=True,
            target_url='https://twitter.com/test/tweet/123',
            hashtags='#peace,#test',
            mentions='@testuser'
        )

    def test_task_creation(self):
        """Test task creation with all fields."""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'A test task for volunteers')
        self.assertEqual(self.task.task_type, Task.TaskType.TWITTER_POST)
        self.assertEqual(self.task.assignment_type, Task.AssignmentType.FIRST_COME)
        self.assertEqual(self.task.campaign, self.campaign)
        self.assertEqual(self.task.created_by, self.admin_user)
        self.assertEqual(self.task.points, 10)
        self.assertEqual(self.task.max_assignments, 5)
        self.assertEqual(self.task.current_assignments, 0)
        self.assertEqual(self.task.completed_assignments, 0)
        self.assertTrue(self.task.is_active)
        self.assertTrue(self.task.is_verified)
        self.assertEqual(self.task.target_url, 'https://twitter.com/test/tweet/123')
        self.assertEqual(self.task.hashtags, '#peace,#test')
        self.assertEqual(self.task.mentions, '@testuser')

    def test_task_string_representation(self):
        """Test string representation of task."""
        self.assertEqual(str(self.task), 'Test Task (Test Campaign)')

    def test_is_available_method(self):
        """Test is_available method."""
        # Task should be available initially
        self.assertTrue(self.task.is_available())

        # Test when not active
        self.task.is_active = False
        self.assertFalse(self.task.is_available())
        self.task.is_active = True

        # Test when not verified
        self.task.is_verified = False
        self.assertFalse(self.task.is_available())
        self.task.is_verified = True

        # Test when max assignments reached
        self.task.current_assignments = 5
        self.assertFalse(self.task.is_available())
        self.task.current_assignments = 0

        # Test with availability window
        now = timezone.now()
        self.task.available_from = now + timedelta(hours=1)
        self.assertFalse(self.task.is_available())

        self.task.available_from = now - timedelta(hours=1)
        self.task.available_until = now - timedelta(minutes=30)
        self.assertFalse(self.task.is_available())

        self.task.available_until = now + timedelta(hours=1)
        self.assertTrue(self.task.is_available())

        # Clear availability window
        self.task.available_from = None
        self.task.available_until = None
        self.assertTrue(self.task.is_available())

    def test_available_slots_method(self):
        """Test available_slots method."""
        # Test with no assignments
        self.assertEqual(self.task.available_slots(), 5)

        # Test with some assignments
        self.task.current_assignments = 3
        self.assertEqual(self.task.available_slots(), 2)

        # Test with max assignments
        self.task.current_assignments = 5
        self.assertEqual(self.task.available_slots(), 0)

        # Test with more than max (shouldn't happen, but test edge case)
        self.task.current_assignments = 7
        self.assertEqual(self.task.available_slots(), 0)

    def test_task_indexes(self):
        """Test that indexes are properly set."""
        indexes = [index.fields for index in Task._meta.indexes]
        expected_indexes = [['task_type'], ['is_active'], ['available_from', 'available_until']]

        for expected in expected_indexes:
            self.assertIn(expected, indexes)


class TaskAssignmentModelTests(TestCase):
    """Test TaskAssignment model."""

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

        # Create test campaign
        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            description='A test campaign',
            short_description='Test',
            created_by=self.admin_user
        )

        # Create test task
        self.task = Task.objects.create(
            title='Test Task',
            description='Test task',
            instructions='Test instructions',
            task_type=Task.TaskType.TWITTER_POST,
            campaign=self.campaign,
            created_by=self.admin_user,
            points=10
        )

    def test_task_assignment_creation(self):
        """Test TaskAssignment creation."""
        assignment = TaskAssignment.objects.create(
            task=self.task,
            volunteer=self.volunteer,
            campaign=self.campaign,
            status=TaskAssignment.Status.ASSIGNED,
            assigned_by=self.admin_user
        )

        self.assertEqual(assignment.task, self.task)
        self.assertEqual(assignment.volunteer, self.volunteer)
        self.assertEqual(assignment.campaign, self.campaign)
        self.assertEqual(assignment.status, TaskAssignment.Status.ASSIGNED)
        self.assertEqual(assignment.assigned_by, self.admin_user)
        self.assertEqual(assignment.points_awarded, 0)
        self.assertIsNotNone(assignment.assigned_at)

    def test_task_assignment_status_transitions(self):
        """Test TaskAssignment status transitions."""
        assignment = TaskAssignment.objects.create(
            task=self.task,
            volunteer=self.volunteer,
            campaign=self.campaign
        )

        # Test status transitions
        assignment.status = TaskAssignment.Status.IN_PROGRESS
        assignment.save()

        assignment.status = TaskAssignment.Status.COMPLETED
        assignment.proof_url = 'https://twitter.com/user/status/123'
        assignment.proof_text = 'Completed the task as requested'
        assignment.save()

        assignment.status = TaskAssignment.Status.VERIFIED
        assignment.verified_by = self.admin_user
        assignment.points_awarded = self.task.points
        assignment.verification_notes = 'Good work!'
        assignment.save()

        # Check that points were awarded
        self.assertEqual(assignment.points_awarded, 10)

        # Check that volunteer points were updated
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.points, 10)

    def test_task_assignment_string_representation(self):
        """Test string representation of TaskAssignment."""
        assignment = TaskAssignment.objects.create(
            task=self.task,
            volunteer=self.volunteer,
            campaign=self.campaign
        )
        self.assertEqual(str(assignment), f'{self.volunteer.username} - {self.task.title}')


class TaskAPITests(APITestCase):
    """Test Task API endpoints."""

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
            created_by=self.admin_user
        )

        self.campaign2 = Campaign.objects.create(
            name='Manager Campaign',
            description='Campaign managed by manager',
            short_description='Manager campaign',
            campaign_type=Campaign.CampaignType.REGULAR,
            status=Campaign.Status.ACTIVE,
            created_by=self.admin_user
        )
        self.campaign2.managers.add(self.campaign_manager)

        # Add volunteer to campaign1
        CampaignVolunteer.objects.create(
            campaign=self.campaign1,
            volunteer=self.volunteer,
            status=CampaignVolunteer.Status.ACTIVE
        )

        # Create test tasks
        self.task1 = Task.objects.create(
            title='Admin Task',
            description='Task in admin campaign',
            instructions='Complete this task',
            task_type=Task.TaskType.TWITTER_POST,
            campaign=self.campaign1,
            created_by=self.admin_user,
            points=10,
            max_assignments=3,
            is_active=True,
            is_verified=True
        )

        self.task2 = Task.objects.create(
            title='Manager Task',
            description='Task in manager campaign',
            instructions='Complete this task',
            task_type=Task.TaskType.TWITTER_RETWEET,
            campaign=self.campaign2,
            created_by=self.admin_user,
            points=15,
            max_assignments=2,
            is_active=True,
            is_verified=True
        )

    def test_list_tasks_admin(self):
        """Test listing tasks as admin (should see all)."""
        url = reverse('tasks:task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should see both tasks

    def test_list_tasks_manager(self):
        """Test listing tasks as campaign manager (should see managed campaign tasks)."""
        url = reverse('tasks:task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see task2
        self.assertEqual(response.data[0]['title'], 'Manager Task')

    def test_list_tasks_volunteer(self):
        """Test listing tasks as volunteer (should see joined campaign tasks)."""
        url = reverse('tasks:task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see task1
        self.assertEqual(response.data[0]['title'], 'Admin Task')

    def test_create_task_admin(self):
        """Test creating a task as admin."""
        url = reverse('tasks:task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        data = {
            'title': 'New Task',
            'description': 'A new task for volunteers',
            'instructions': 'Complete the following steps',
            'task_type': Task.TaskType.TELEGRAM_SHARE,
            'campaign': self.campaign1.id,
            'points': 20,
            'estimated_time': 30,
            'max_assignments': 5,
            'target_url': 'https://t.me/testchannel',
            'hashtags': '#peace,#unity',
            'mentions': '@testchannel'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check task was created
        task = Task.objects.get(title='New Task')
        self.assertEqual(task.description, 'A new task for volunteers')
        self.assertEqual(task.created_by, self.admin_user)
        self.assertEqual(task.points, 20)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.TASK_CREATE,
            description=f'Task "New Task" created for campaign "{self.campaign1.name}"'
        ).exists())

    def test_create_task_non_admin(self):
        """Test creating a task as non-admin (should fail)."""
        url = reverse('tasks:task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        data = {
            'title': 'Unauthorized Task',
            'description': 'Should not be allowed',
            'task_type': Task.TaskType.TWITTER_POST,
            'campaign': self.campaign2.id,
            'points': 10
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_task_detail_admin(self):
        """Test retrieving task detail as admin."""
        url = reverse('tasks:task-detail', args=[self.task1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Admin Task')

    def test_retrieve_task_detail_manager(self):
        """Test retrieving task detail as manager (should succeed for managed campaign task)."""
        url = reverse('tasks:task-detail', args=[self.task2.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Manager Task')

    def test_retrieve_task_detail_manager_unauthorized(self):
        """Test retrieving task detail as manager for unmanaged campaign task (should fail)."""
        url = reverse('tasks:task-detail', args=[self.task1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task_admin(self):
        """Test updating a task as admin."""
        url = reverse('tasks:task-detail', args=[self.task1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        data = {
            'title': 'Updated Task Title',
            'description': 'Updated description',
            'points': 25
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check task was updated
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task Title')
        self.assertEqual(self.task1.points, 25)

    def test_delete_task_admin(self):
        """Test deleting a task as admin."""
        url = reverse('tasks:task-detail', args=[self.task1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check task was deleted
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_available_tasks_volunteer(self):
        """Test listing available tasks for a volunteer."""
        url = reverse('tasks:available-tasks')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should see task1
        self.assertEqual(response.data[0]['title'], 'Admin Task')

    def test_available_tasks_non_volunteer(self):
        """Test listing available tasks as non-volunteer (should return empty)."""
        url = reverse('tasks:available-tasks')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Admin is not a volunteer

    def test_assign_task(self):
        """Test assigning a task to a volunteer."""
        url = reverse('tasks:task-assign', args=[self.task1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check assignment was created
        assignment = TaskAssignment.objects.get(task=self.task1, volunteer=self.volunteer)
        self.assertEqual(assignment.status, TaskAssignment.Status.ASSIGNED)
        self.assertEqual(assignment.campaign, self.campaign1)

        # Check task current_assignments was updated
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.current_assignments, 1)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.TASK_ASSIGN,
            description=f'Task "Admin Task" assigned to {self.volunteer.username}'
        ).exists())

    def test_assign_task_already_assigned(self):
        """Test assigning a task when already assigned."""
        # First assignment
        url = reverse('tasks:task-assign', args=[self.task1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')
        self.client.post(url)

        # Try to assign again
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assign_task_max_assignments_reached(self):
        """Test assigning a task when max assignments reached."""
        # Create max assignments
        for i in range(3):
            volunteer = User.objects.create_user(
                username=f'volunteer{i}',
                email=f'volunteer{i}@example.com',
                password='testpass123',
                role=User.Role.VOLUNTEER
            )
            CampaignVolunteer.objects.create(
                campaign=self.campaign1,
                volunteer=volunteer,
                status=CampaignVolunteer.Status.ACTIVE
            )
            TaskAssignment.objects.create(
                task=self.task1,
                volunteer=volunteer,
                campaign=self.campaign1
            )

        # Try to assign to our test volunteer
        url = reverse('tasks:task-assign', args=[self.task1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complete_task(self):
        """Test completing a task assignment."""
        # First assign the task
        assignment = TaskAssignment.objects.create(
            task=self.task1,
            volunteer=self.volunteer,
            campaign=self.campaign1,
            status=TaskAssignment.Status.ASSIGNED
        )

        url = reverse('tasks:task-complete', args=[assignment.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.volunteer_token.access_token}')

        data = {
            'proof_url': 'https://twitter.com/user/status/123456',
            'proof_text': 'I completed the task as requested',
            'completion_notes': 'Task was straightforward'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check assignment was updated
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, TaskAssignment.Status.COMPLETED)
        self.assertEqual(assignment.proof_url, 'https://twitter.com/user/status/123456')
        self.assertEqual(assignment.proof_text, 'I completed the task as requested')

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.TASK_COMPLETE,
            description=f'Task "Admin Task" completed by {self.volunteer.username}'
        ).exists())

    def test_verify_task(self):
        """Test verifying a completed task."""
        # Create a completed assignment
        assignment = TaskAssignment.objects.create(
            task=self.task1,
            volunteer=self.volunteer,
            campaign=self.campaign1,
            status=TaskAssignment.Status.COMPLETED,
            proof_url='https://twitter.com/user/status/123456',
            proof_text='Completed task'
        )

        url = reverse('tasks:task-verify', args=[assignment.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        data = {
            'status': TaskAssignment.Status.VERIFIED,
            'verification_notes': 'Good work! Verified.',
            'points_awarded': self.task1.points
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check assignment was updated
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, TaskAssignment.Status.VERIFIED)
        self.assertEqual(assignment.verified_by, self.admin_user)
        self.assertEqual(assignment.points_awarded, 10)
        self.assertEqual(assignment.verification_notes, 'Good work! Verified.')

        # Check volunteer points were updated
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.points, 10)

        # Check task completed_assignments was updated
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.completed_assignments, 1)

        # Check ActivityLog was created
        self.assertTrue(ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.TASK_VERIFY,
            description=f'Task "Admin Task" verified by {self.volunteer.username}'
        ).exists())

    def test_reject_task(self):
        """Test rejecting a completed task."""
        # Create a completed assignment
        assignment = TaskAssignment.objects.create(
            task=self.task1,
            volunteer=self.volunteer,
            campaign=self.campaign1,
            status=TaskAssignment.Status.COMPLETED,
            proof_url='https://twitter.com/user/status/123456'
        )

        url = reverse('tasks:task-verify', args=[assignment.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')

        data = {
            'status': TaskAssignment.Status.REJECTED,
            'verification_notes': 'Proof does not meet requirements.',
            'points_awarded': 0
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check assignment was updated
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, TaskAssignment.Status.REJECTED)
        self.assertEqual(assignment.verified_by, self.admin_user)
        self.assertEqual(assignment.points_awarded, 0)

        # Check volunteer points were NOT updated
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.points, 0)


class TaskSignalTests(TestCase):
    """Test Task signal handlers."""

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

        # Create test campaign
        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            description='A test campaign',
            short_description='Test',
            created_by=self.admin_user
        )

    def test_task_created_signal(self):
        """Test signal when task is created."""
        # Create task - should trigger signal
        task = Task.objects.create(
            title='Signal Task',
            description='Task for signal testing',
            instructions='Test instructions',
            task_type=Task.TaskType.TWITTER_POST,
            campaign=self.campaign,
            created_by=self.admin_user,
            points=10
        )

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.TASK_CREATE,
            description=f'Task "Signal Task" created for campaign "{self.campaign.name}"'
        ).first()

        self.assertIsNotNone(activity_log)

    def test_task_updated_signal_activation(self):
        """Test signal when task is activated/deactivated."""
        task = Task.objects.create(
            title='Activation Test Task',
            description='Task for activation testing',
            instructions='Test',
            task_type=Task.TaskType.TWITTER_POST,
            campaign=self.campaign,
            created_by=self.admin_user,
            points=10,
            is_active=False
        )

        # Clear existing logs
        ActivityLog.objects.all().delete()

        # Activate task - should trigger signal
        task.is_active = True
        task.save()

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.TASK_UPDATE,
            description=f'Task "Activation Test Task" activated'
        ).first()

        self.assertIsNotNone(activity_log)

    def test_task_assignment_created_signal(self):
        """Test signal when task assignment is created."""
        task = Task.objects.create(
            title='Assignment Test Task',
            description='Task for assignment testing',
            instructions='Test',
            task_type=Task.TaskType.TWITTER_POST,
            campaign=self.campaign,
            created_by=self.admin_user,
            points=10
        )

        # Clear existing logs
        ActivityLog.objects.all().delete()

        # Create TaskAssignment - should trigger signal
        assignment = TaskAssignment.objects.create(
            task=task,
            volunteer=self.volunteer,
            campaign=self.campaign
        )

        # Check ActivityLog was created
        activity_log = ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.TASK_ASSIGN,
            description=f'Task "Assignment Test Task" assigned to {self.volunteer.username}'
        ).first()

        self.assertIsNotNone(activity_log)

    def test_task_assignment_status_change_signal(self):
        """Test signal when task assignment status changes."""
        task = Task.objects.create(
            title='Status Change Task',
            description='Task for status change testing',
            instructions='Test',
            task_type=Task.TaskType.TWITTER_POST,
            campaign=self.campaign,
            created_by=self.admin_user,
            points=10
        )

        assignment = TaskAssignment.objects.create(
            task=task,
            volunteer=self.volunteer,
            campaign=self.campaign,
            status=TaskAssignment.Status.ASSIGNED
        )

        # Clear existing logs
        ActivityLog.objects.all().delete()

        # Change status to COMPLETED - should trigger signal
        assignment.status = TaskAssignment.Status.COMPLETED
        assignment.proof_url = 'https://twitter.com/test/123'
        assignment.save()

        # Check ActivityLog was created for completion
        activity_log = ActivityLog.objects.filter(
            user=self.volunteer,
            action_type=ActivityLog.ActionType.TASK_COMPLETE,
            description=f'Task "Status Change Task" completed by {self.volunteer.username}'
        ).first()

        self.assertIsNotNone(activity_log)

        # Change status to VERIFIED - should trigger signal
        assignment.status = TaskAssignment.Status.VERIFIED
        assignment.verified_by = self.admin_user
        assignment.points_awarded = task.points
        assignment.save()

        # Check ActivityLog was created for verification
        activity_log = ActivityLog.objects.filter(
            user=self.admin_user,
            action_type=ActivityLog.ActionType.TASK_VERIFY,
            description=f'Task "Status Change Task" verified by {self.volunteer.username}'
        ).first()

        self.assertIsNotNone(activity_log)
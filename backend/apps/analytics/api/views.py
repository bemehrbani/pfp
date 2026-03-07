"""
API views for Analytics app.
"""
from datetime import datetime, timedelta
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count, Sum, Avg, Q
from django.utils.translation import gettext_lazy as _
from ..models import ActivityLog, AnalyticsSnapshot
from apps.campaigns.models import Campaign
from apps.tasks.models import Task, TaskAssignment
from apps.users.models import User


class DashboardStatsView(APIView):
    """Get dashboard statistics for the current user."""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get dashboard statistics for the current user",
        responses={200: openapi.Response('Dashboard statistics including campaigns, tasks, points, and recent activity')}
    )
    def get(self, request):
        user = request.user
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        # Base query based on user role
        if user.is_admin():
            campaigns = Campaign.objects.all()
            tasks = Task.objects.all()
            volunteers = User.objects.filter(role=User.Role.VOLUNTEER)
        elif user.is_campaign_manager():
            campaigns = Campaign.objects.filter(managers=user)
            tasks = Task.objects.filter(campaign__managers=user)
            volunteers = User.objects.filter(
                volunteered_campaigns__managers=user
            ).distinct()
        else:
            campaigns = Campaign.objects.filter(volunteers=user)
            tasks = Task.objects.filter(campaign__volunteers=user)
            volunteers = User.objects.filter(pk=user.pk)

        # Campaign statistics
        active_campaigns = campaigns.filter(status=Campaign.Status.ACTIVE).count()
        total_campaigns = campaigns.count()

        # Task statistics
        my_tasks = TaskAssignment.objects.filter(
            volunteer=user,
            status__in=[
                TaskAssignment.Status.ASSIGNED,
                TaskAssignment.Status.IN_PROGRESS
            ]
        ).count()

        # Points earned
        points_earned = TaskAssignment.objects.filter(
            volunteer=user,
            status=TaskAssignment.Status.VERIFIED
        ).aggregate(total=Sum('points_awarded'))['total'] or 0

        # Volunteer statistics
        total_volunteers = volunteers.count()
        active_volunteers = User.objects.filter(
            last_login__gte=thirty_days_ago,
            role=User.Role.VOLUNTEER
        ).count()

        # Recent activity
        recent_activity = ActivityLog.objects.filter(
            user=user
        ).order_by('-created_at')[:5].values('action_type', 'description', 'created_at')

        stats = {
            'active_campaigns': active_campaigns,
            'total_campaigns': total_campaigns,
            'my_tasks': my_tasks,
            'points_earned': points_earned,
            'total_volunteers': total_volunteers,
            'active_volunteers': active_volunteers,
            'recent_activity': [
                {
                    'action': log['action_type'].replace('_', ' ').title(),
                    'description': log['description'],
                    'time': self._time_ago(log['created_at'])
                }
                for log in recent_activity
            ]
        }

        return Response(stats)

    def _time_ago(self, dt):
        """Convert datetime to human-readable time ago."""
        now = timezone.now()
        diff = now - dt

        if diff.days > 365:
            years = diff.days // 365
            return f'{years} year{"s" if years > 1 else ""} ago'
        elif diff.days > 30:
            months = diff.days // 30
            return f'{months} month{"s" if months > 1 else ""} ago'
        elif diff.days > 0:
            return f'{diff.days} day{"s" if diff.days > 1 else ""} ago'
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f'{hours} hour{"s" if hours > 1 else ""} ago'
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
        else:
            return 'just now'


class CampaignAnalyticsView(APIView):
    """Get analytics for a specific campaign."""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get analytics for a specific campaign",
        responses={
            200: openapi.Response('Campaign analytics data'),
            404: openapi.Response('Campaign not found'),
        }
    )
    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(pk=campaign_id)
        except Campaign.DoesNotExist:
            return Response(
                {'error': _('Campaign not found.')},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check permissions
        if not (request.user.is_admin() or campaign.managers.filter(pk=request.user.pk).exists()):
            return Response(
                {'error': _('You do not have permission to view these analytics.')},
                status=status.HTTP_403_FORBIDDEN
            )

        # Campaign progress
        progress_data = {
            'members': {
                'current': campaign.current_members,
                'target': campaign.target_members,
                'percentage': min(100, (campaign.current_members / campaign.target_members * 100) if campaign.target_members > 0 else 0)
            },
            'activities': {
                'current': campaign.completed_activities,
                'target': campaign.target_activities,
                'percentage': min(100, (campaign.completed_activities / campaign.target_activities * 100) if campaign.target_activities > 0 else 0)
            },
            'twitter_posts': {
                'current': campaign.completed_twitter_posts,
                'target': campaign.target_twitter_posts,
                'percentage': min(100, (campaign.completed_twitter_posts / campaign.target_twitter_posts * 100) if campaign.target_twitter_posts > 0 else 0)
            }
        }

        # Task type distribution
        task_types = Task.objects.filter(campaign=campaign).values(
            'task_type'
        ).annotate(
            count=Count('id'),
            completed=Count('assignments', filter=Q(assignments__status=TaskAssignment.Status.VERIFIED))
        ).order_by('-count')

        # Volunteer engagement
        volunteer_stats = campaign.volunteers.annotate(
            tasks_completed=Count(
                'task_assignments',
                filter=Q(task_assignments__status=TaskAssignment.Status.VERIFIED)
            ),
            points_earned=Sum(
                'task_assignments__points_awarded',
                filter=Q(task_assignments__status=TaskAssignment.Status.VERIFIED)
            )
        ).values('username', 'tasks_completed', 'points_earned').order_by('-points_earned')[:10]

        # Recent activity
        recent_activity = ActivityLog.objects.filter(
            content_type__model='campaign',
            object_id=campaign_id
        ).select_related('user').order_by('-created_at')[:10].values(
            'user__username',
            'action_type',
            'description',
            'created_at'
        )

        analytics = {
            'campaign': {
                'id': campaign.id,
                'name': campaign.name,
                'progress_percentage': campaign.progress_percentage(),
                'total_points_awarded': campaign.total_points_awarded,
            },
            'progress': progress_data,
            'task_types': [
                {
                    'name': tt['task_type'].replace('_', ' ').title(),
                    'count': tt['count'],
                    'completed': tt['completed'],
                    'completion_rate': (tt['completed'] / tt['count'] * 100) if tt['count'] > 0 else 0
                }
                for tt in task_types
            ],
            'top_volunteers': list(volunteer_stats),
            'recent_activity': [
                {
                    'volunteer_name': ra['user__username'],
                    'action': ra['action_type'].replace('_', ' ').title(),
                    'description': ra['description'],
                    'time_ago': self._time_ago(ra['created_at'])
                }
                for ra in recent_activity
            ]
        }

        return Response(analytics)

    def _time_ago(self, dt):
        """Convert datetime to human-readable time ago."""
        now = timezone.now()
        diff = now - dt
        if diff.days > 0:
            return f'{diff.days}d ago'
        elif diff.seconds > 3600:
            return f'{diff.seconds // 3600}h ago'
        elif diff.seconds > 60:
            return f'{diff.seconds // 60}m ago'
        else:
            return 'just now'


class SystemAnalyticsView(APIView):
    """Get system-wide analytics (admin only)."""
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Get system-wide analytics (admin only)",
        responses={200: openapi.Response('System analytics data including users, campaigns, tasks, and daily activity')}
    )
    def get(self, request):
        # Time ranges
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        # User statistics
        total_users = User.objects.count()
        new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
        new_users_month = User.objects.filter(date_joined__gte=month_ago).count()
        active_users_week = User.objects.filter(last_login__gte=week_ago).count()

        # Campaign statistics
        total_campaigns = Campaign.objects.count()
        active_campaigns = Campaign.objects.filter(status=Campaign.Status.ACTIVE).count()
        completed_campaigns = Campaign.objects.filter(status=Campaign.Status.COMPLETED).count()

        # Task statistics
        total_tasks = Task.objects.count()
        completed_tasks = TaskAssignment.objects.filter(
            status=TaskAssignment.Status.VERIFIED
        ).count()
        verification_rate = (
            (completed_tasks / TaskAssignment.objects.count() * 100)
            if TaskAssignment.objects.count() > 0 else 0
        )

        # Points statistics
        total_points_awarded = TaskAssignment.objects.filter(
            status=TaskAssignment.Status.VERIFIED
        ).aggregate(total=Sum('points_awarded'))['total'] or 0
        avg_points_per_user = (
            total_points_awarded / User.objects.filter(role=User.Role.VOLUNTEER).count()
            if User.objects.filter(role=User.Role.VOLUNTEER).exists() else 0
        )

        # Daily activity
        daily_activity = ActivityLog.objects.filter(
            created_at__gte=month_ago
        ).extra(
            {'date': "DATE(created_at)"}
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        analytics = {
            'users': {
                'total': total_users,
                'new_week': new_users_week,
                'new_month': new_users_month,
                'active_week': active_users_week,
            },
            'campaigns': {
                'total': total_campaigns,
                'active': active_campaigns,
                'completed': completed_campaigns,
            },
            'tasks': {
                'total': total_tasks,
                'completed': completed_tasks,
                'verification_rate': verification_rate,
            },
            'points': {
                'total_awarded': total_points_awarded,
                'avg_per_user': avg_points_per_user,
            },
            'daily_activity': [
                {
                    'date': str(day['date']),
                    'count': day['count']
                }
                for day in daily_activity
            ]
        }

        return Response(analytics)
"""
API views for Analytics app.
"""
from datetime import datetime, timedelta
import hashlib
from django.conf import settings
from django.db.models.functions import TruncDate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count, Sum, Avg, Q
from django.utils.translation import gettext_lazy as _
from ..models import ActivityLog, AnalyticsSnapshot, PageViewEvent
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


from apps.users.permissions import IsAdminUser

class SystemAnalyticsView(APIView):
    """Get system-wide analytics (admin only)."""
    permission_classes = [IsAdminUser]

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


class RecordPageViewView(APIView):
    """
    Lightweight, cookie-free first-party web analytics beacon endpoint.
    Computes a daily salted SHA-256 hash so visitor IPs are never stored in analytics.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="Record a first-party pageview, PDF download, or Vow modal interaction.",
        responses={201: openapi.Response('Event recorded')}
    )
    def post(self, request):
        raw_path = (request.data.get('path') or '/').strip()
        if not raw_path.startswith('/'):
            raw_path = '/' + raw_path
        path = raw_path[:255]

        valid_events = {choice[0] for choice in PageViewEvent.EventType.choices}
        event_type = (request.data.get('event_type') or PageViewEvent.EventType.PAGEVIEW).strip()
        if event_type not in valid_events:
            event_type = PageViewEvent.EventType.PAGEVIEW

        referrer = (request.data.get('referrer') or request.META.get('HTTP_REFERER') or '').strip()[:500]
        lang = (request.data.get('lang') or '').strip()[:16]
        country = (request.META.get('HTTP_CF_IPCOUNTRY') or '').strip().upper()[:8]

        screen_width = request.data.get('screen_width')
        try:
            screen_width = int(screen_width) if screen_width is not None else None
            if screen_width is not None and (screen_width <= 0 or screen_width > 16384):
                screen_width = None
        except (ValueError, TypeError):
            screen_width = None

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else (request.META.get('REMOTE_ADDR') or '')
        user_agent = request.META.get('HTTP_USER_AGENT') or ''
        day_str = timezone.now().date().isoformat()
        visitor_hash = hashlib.sha256(
            f"{day_str}:{ip_address}:{user_agent}:{settings.SECRET_KEY}".encode('utf-8')
        ).hexdigest()[:16]

        PageViewEvent.objects.create(
            path=path,
            event_type=event_type,
            referrer=referrer,
            country=country,
            lang=lang,
            screen_width=screen_width,
            visitor_hash=visitor_hash,
        )

        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)


class WebAnalyticsSummaryView(APIView):
    """Aggregate first-party web analytics and Accountability Vow statistics (admin only)."""
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Get aggregated website traffic, top pages, countries, PDF downloads, and Vow signers.",
        responses={200: openapi.Response('Web analytics summary')}
    )
    def get(self, request):
        from apps.telegram.models import ContactSubmission
        from apps.telegram.api.views import get_vow_signatory_count

        days = int(request.query_params.get('days', 30))
        since = timezone.now() - timedelta(days=max(1, min(days, 365)))

        events = PageViewEvent.objects.filter(created_at__gte=since)
        pageviews = events.filter(event_type=PageViewEvent.EventType.PAGEVIEW)

        total_pageviews = pageviews.count()
        unique_visitors = events.exclude(visitor_hash='').values('visitor_hash').distinct().count()
        pdf_downloads = events.filter(event_type=PageViewEvent.EventType.PDF_DOWNLOAD).count()
        vow_opens = events.filter(event_type=PageViewEvent.EventType.VOW_OPEN).count()

        top_pages = list(
            pageviews.values('path')
            .annotate(views=Count('id'), uniques=Count('visitor_hash', distinct=True))
            .order_by('-views')[:25]
        )

        top_pdfs = list(
            events.filter(event_type=PageViewEvent.EventType.PDF_DOWNLOAD)
            .values('path')
            .annotate(downloads=Count('id'))
            .order_by('-downloads')[:15]
        )

        top_countries = list(
            pageviews.exclude(country='')
            .values('country')
            .annotate(views=Count('id'), uniques=Count('visitor_hash', distinct=True))
            .order_by('-views')[:20]
        )

        daily_pageviews = [
            {
                'date': str(row['day']),
                'pageviews': row['views'],
                'uniques': row['uniques'],
            }
            for row in pageviews.annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(views=Count('id'), uniques=Count('visitor_hash', distinct=True))
            .order_by('day')
        ]

        vow_signers_count = get_vow_signatory_count()
        total_contacts = ContactSubmission.objects.count()

        return Response({
            'period_days': days,
            'total_pageviews': total_pageviews,
            'unique_visitors': unique_visitors,
            'pdf_downloads': pdf_downloads,
            'vow_modal_opens': vow_opens,
            'vow_signers_count': vow_signers_count,
            'vow_badge_visible': vow_signers_count >= 100,
            'contact_submissions_count': total_contacts,
            'top_pages': top_pages,
            'top_pdfs': top_pdfs,
            'top_countries': top_countries,
            'daily_pageviews': daily_pageviews,
        }, status=status.HTTP_200_OK)

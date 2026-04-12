"""
API views for Campaigns app.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.db.models import Count, Sum, Q
from ..models import Campaign, CampaignVolunteer, CampaignUpdate, TwitterStorm, ProtestEvent
from apps.tasks.models import Task, TaskAssignment
from apps.analytics.models import ActivityLog
from ..serializers import (
    CampaignSerializer, CampaignCreateSerializer,
    CampaignVolunteerSerializer, CampaignUpdateSerializer,
    CampaignStatsSerializer, ProtestEventSerializer
)
from apps.users.models import User
from apps.users.permissions import IsAdminUser


class IsAdminOrCampaignManager(permissions.BasePermission):
    """Permission check for admin or campaign manager."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        if request.user.is_campaign_manager() and obj.managers.filter(id=request.user.id).exists():
            return True
        return False


class CampaignListView(generics.ListCreateAPIView):
    """List campaigns or create a new campaign."""
    queryset = Campaign.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['campaign_type', 'status', 'created_by']
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'current_members']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CampaignCreateSerializer
        return CampaignSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Filter campaigns based on user role."""
        user = self.request.user
        if user.is_admin():
            return Campaign.objects.all()
        elif user.is_campaign_manager():
            return Campaign.objects.filter(managers=user)
        else:
            # Volunteers can only see campaigns they're part of
            return Campaign.objects.filter(volunteers=user)

    def perform_create(self, serializer):
        """Set created_by to the authenticated user."""
        serializer.save(created_by=self.request.user)


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a campaign."""
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCampaignManager]

    def perform_update(self, serializer):
        """Update campaign with proper permissions."""
        instance = serializer.save()
        # Update statistics after save
        instance.update_statistics()


class CampaignJoinView(APIView):
    """Allow a volunteer to join a campaign."""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Join a campaign as a volunteer",
        responses={200: openapi.Response('Successfully joined'), 404: openapi.Response('Campaign not found')}
    )
    def post(self, request, pk):
        try:
            campaign = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response(
                {'error': _('Campaign not found.')},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user is already a volunteer
        if campaign.volunteers.filter(id=request.user.id).exists():
            return Response(
                {'error': _('You are already a volunteer for this campaign.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add volunteer to campaign
        CampaignVolunteer.objects.create(
            campaign=campaign,
            volunteer=request.user,
            status=CampaignVolunteer.Status.ACTIVE
        )

        # Update campaign statistics
        campaign.update_statistics()

        return Response(
            {'message': _('Successfully joined the campaign.')},
            status=status.HTTP_200_OK
        )


class CampaignVolunteersView(generics.ListAPIView):
    """List volunteers for a campaign."""
    serializer_class = CampaignVolunteerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCampaignManager]

    def get_queryset(self):
        campaign_id = self.kwargs['pk']
        return CampaignVolunteer.objects.filter(campaign_id=campaign_id)


class CampaignUpdatesView(generics.ListCreateAPIView):
    """List or create updates for a campaign."""
    serializer_class = CampaignUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        campaign_id = self.kwargs['pk']
        return CampaignUpdate.objects.filter(campaign_id=campaign_id)

    def perform_create(self, serializer):
        campaign_id = self.kwargs['pk']
        campaign = Campaign.objects.get(pk=campaign_id)
        serializer.save(campaign=campaign, created_by=self.request.user)


class CampaignStatsView(APIView):
    """Get campaign statistics."""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get campaign statistics",
        responses={200: openapi.Response('Campaign statistics'), 404: openapi.Response('Campaign not found')}
    )
    def get(self, request, pk):
        try:
            campaign = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response(
                {'error': _('Campaign not found.')},
                status=status.HTTP_404_NOT_FOUND
            )

        stats = {
            'total_campaigns': Campaign.objects.count(),
            'active_campaigns': Campaign.objects.filter(status=Campaign.Status.ACTIVE).count(),
            'total_volunteers': campaign.volunteers.count(),
            'total_points_awarded': campaign.total_points_awarded,
            'completion_rate': campaign.progress_percentage(),
        }

        serializer = CampaignStatsSerializer(stats)
        return Response(serializer.data)


class MyCampaignsView(generics.ListAPIView):
    """List campaigns for the current user."""
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin() or user.is_campaign_manager():
            # Return campaigns they created or manage
            return Campaign.objects.filter(
                models.Q(created_by=user) | models.Q(managers=user)
            ).distinct()
        else:
            # Return campaigns they volunteer for
            return Campaign.objects.filter(volunteers=user)


class CampaignSearchView(generics.ListAPIView):
    """Search campaigns by name or description."""
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'short_description']

    def get_queryset(self):
        """Return campaigns visible to the user."""
        user = self.request.user
        if user.is_admin():
            return Campaign.objects.all()
        elif user.is_campaign_manager():
            return Campaign.objects.filter(managers=user)
        else:
            return Campaign.objects.filter(volunteers=user)


class PublicCampaignStatsView(APIView):
    """Public campaign stats — no authentication required.

    Returns aggregate data only. Volunteer names are anonymized.
    Designed for the live dashboard at /dashboard-live.html.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def _anonymize_name(self, name: str) -> str:
        """Show first character + asterisks for privacy."""
        if not name:
            return '***'
        return name[0] + '*' * min(len(name) - 1, 5)

    def _time_ago(self, dt) -> str:
        """Convert datetime to human-readable time ago."""
        if not dt:
            return ''
        diff = timezone.now() - dt
        seconds = diff.total_seconds()
        if seconds < 60:
            return 'just now'
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f'{minutes}m ago'
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f'{hours}h ago'
        else:
            days = int(seconds / 86400)
            return f'{days}d ago'

    @swagger_auto_schema(
        operation_description="Get public campaign statistics (no auth required)",
        responses={
            200: openapi.Response('Public campaign statistics'),
            404: openapi.Response('Campaign not found'),
        }
    )
    def get(self, request, pk):
        try:
            campaign = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response(
                {'error': 'Campaign not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Members progress
        members_data = {
            'current': campaign.current_members,
            'target': campaign.target_members,
            'percentage': min(100, round(
                (campaign.current_members / campaign.target_members * 100)
                if campaign.target_members > 0 else 0
            )),
        }

        # Task stats
        total_tasks = Task.objects.filter(campaign=campaign).count()
        completed_assignments = TaskAssignment.objects.filter(
            task__campaign=campaign,
            status=TaskAssignment.Status.VERIFIED
        ).count()
        total_assignments = TaskAssignment.objects.filter(
            task__campaign=campaign
        ).count()
        verification_rate = round(
            (completed_assignments / total_assignments * 100)
            if total_assignments > 0 else 0
        )

        # Task type distribution
        task_types = Task.objects.filter(campaign=campaign).values(
            'task_type'
        ).annotate(
            count=Count('id'),
            completed=Count(
                'assignments',
                filter=Q(assignments__status=TaskAssignment.Status.VERIFIED)
            )
        ).order_by('-count')

        # Top volunteers (anonymized)
        top_volunteers = campaign.volunteers.annotate(
            tasks_completed=Count(
                'task_assignments',
                filter=Q(
                    task_assignments__status=TaskAssignment.Status.VERIFIED,
                    task_assignments__task__campaign=campaign
                )
            ),
            points_earned=Sum(
                'task_assignments__points_awarded',
                filter=Q(
                    task_assignments__status=TaskAssignment.Status.VERIFIED,
                    task_assignments__task__campaign=campaign
                )
            )
        ).filter(tasks_completed__gt=0).order_by('-points_earned')[:10]

        # Recent activity
        recent_activity = ActivityLog.objects.filter(
            content_type__model='campaign',
            object_id=campaign.id
        ).select_related('user').order_by('-created_at')[:10]

        # Storm info
        upcoming_storms = TwitterStorm.objects.filter(
            campaign=campaign,
            status__in=[
                TwitterStorm.Status.SCHEDULED,
                TwitterStorm.Status.COUNTDOWN
            ],
            scheduled_at__gte=timezone.now()
        ).order_by('scheduled_at')

        next_storm = None
        if upcoming_storms.exists():
            storm = upcoming_storms.first()
            next_storm = {
                'title': storm.title,
                'scheduled_at': storm.scheduled_at.isoformat(),
                'hashtags': storm.get_hashtags(),
                'status': storm.status,
                'participants_ready': storm.participants.filter(
                    is_ready=True
                ).count() if hasattr(storm, 'participants') else 0,
            }

        completed_storms = TwitterStorm.objects.filter(
            campaign=campaign,
            status=TwitterStorm.Status.COMPLETED
        ).count()

        data = {
            'campaign': {
                'name': campaign.name,
                'status': campaign.status,
                'progress_percentage': campaign.progress_percentage(),
                'total_points_awarded': campaign.total_points_awarded,
            },
            'members': members_data,
            'tasks': {
                'total': total_tasks,
                'completed_assignments': completed_assignments,
                'total_assignments': total_assignments,
                'verification_rate': verification_rate,
            },
            'task_types': [
                {
                    'name': tt['task_type'].replace('_', ' ').title(),
                    'count': tt['count'],
                    'completed': tt['completed'],
                }
                for tt in task_types
            ],
            'top_volunteers': [
                {
                    'name': self._anonymize_name(v.username or v.first_name),
                    'tasks_completed': v.tasks_completed,
                    'points': v.points_earned or 0,
                }
                for v in top_volunteers
            ],
            'recent_activity': [
                {
                    'action': ra.action_type.replace('_', ' ').title(),
                    'description': ra.description,
                    'time_ago': self._time_ago(ra.created_at),
                }
                for ra in recent_activity
            ],
            'storms': {
                'next': next_storm,
                'completed': completed_storms,
                'upcoming_count': upcoming_storms.count(),
            },
            'updated_at': timezone.now().isoformat(),
        }

        response = Response(data)
        response['Access-Control-Allow-Origin'] = '*'
        return response

class ProtestEventListView(generics.ListAPIView):
    """List verified upcoming protest events."""
    serializer_class = ProtestEventSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    
    def get_queryset(self):
        """Return upcoming verified protests ordered by date."""
        return ProtestEvent.objects.filter(
            is_verified=True,
            date_time__gte=timezone.now() - timezone.timedelta(days=1)
        ).order_by('date_time')
"""
API views for Twitter Storm management.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ..models import Campaign, TwitterStorm, StormParticipant
from ..serializers import (
    TwitterStormSerializer, TwitterStormCreateSerializer,
    StormParticipantSerializer
)


class IsAdminOrCampaignManager(permissions.BasePermission):
    """Permission check: user must be admin or a manager of the storm's campaign."""

    def has_object_permission(self, request, view, obj):
        storm = obj if isinstance(obj, TwitterStorm) else getattr(obj, 'storm', None)
        campaign = storm.campaign if storm else None
        if not campaign:
            return False
        if request.user.is_admin():
            return True
        return campaign.managers.filter(id=request.user.id).exists()


class StormListCreateView(generics.ListCreateAPIView):
    """
    List storms for a campaign or schedule a new storm.

    GET /api/campaigns/{campaign_pk}/storms/
    POST /api/campaigns/{campaign_pk}/storms/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TwitterStormCreateSerializer
        return TwitterStormSerializer

    def get_queryset(self):
        campaign_pk = self.kwargs['campaign_pk']
        return TwitterStorm.objects.filter(campaign_id=campaign_pk)

    def perform_create(self, serializer):
        """Create storm and optionally trigger scheduling."""
        campaign_pk = self.kwargs['campaign_pk']
        campaign = Campaign.objects.get(pk=campaign_pk)
        storm = serializer.save(
            campaign=campaign,
            created_by=self.request.user
        )

        # If scheduled_at is in the future, auto-schedule notifications
        if storm.scheduled_at > timezone.now():
            storm.status = TwitterStorm.Status.SCHEDULED
            storm.save(update_fields=['status'])
            from ..tasks import schedule_storm_notifications
            schedule_storm_notifications.delay(storm.id)


class StormDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a storm.

    GET /api/storms/{pk}/
    PATCH /api/storms/{pk}/
    """
    queryset = TwitterStorm.objects.all()
    serializer_class = TwitterStormSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCampaignManager]


class StormActivateView(APIView):
    """
    Manually activate a storm (trigger the blast immediately).

    POST /api/storms/{pk}/activate/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            storm = TwitterStorm.objects.get(pk=pk)
        except TwitterStorm.DoesNotExist:
            return Response(
                {'error': _('Storm not found.')},
                status=status.HTTP_404_NOT_FOUND
            )

        if storm.status in ['active', 'completed', 'cancelled']:
            return Response(
                {'error': _(f'Storm is already {storm.status}.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Trigger blast immediately
        from ..tasks import send_storm_blast
        send_storm_blast.delay(storm.id)

        return Response({'message': _('Storm blast triggered!')})


class StormCancelView(APIView):
    """
    Cancel a scheduled storm.

    POST /api/storms/{pk}/cancel/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            storm = TwitterStorm.objects.get(pk=pk)
        except TwitterStorm.DoesNotExist:
            return Response(
                {'error': _('Storm not found.')},
                status=status.HTTP_404_NOT_FOUND
            )

        if storm.status in ['completed', 'cancelled']:
            return Response(
                {'error': _(f'Storm is already {storm.status}.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Revoke queued Celery tasks
        from django.conf import settings
        from config.celery import app as celery_app
        for task_id in storm.celery_task_ids:
            celery_app.control.revoke(task_id, terminate=False)

        storm.status = TwitterStorm.Status.CANCELLED
        storm.save(update_fields=['status', 'updated_at'])

        return Response({'message': _('Storm cancelled.')})


class StormParticipantsView(generics.ListAPIView):
    """
    List participants for a storm.

    GET /api/storms/{pk}/participants/
    """
    serializer_class = StormParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StormParticipant.objects.filter(storm_id=self.kwargs['pk'])

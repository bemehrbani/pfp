"""
API views for Campaigns app.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from ..models import Campaign, CampaignVolunteer, CampaignUpdate
from django.db import models
from ..serializers import (
    CampaignSerializer, CampaignCreateSerializer,
    CampaignVolunteerSerializer, CampaignUpdateSerializer,
    CampaignStatsSerializer
)
from apps.users.models import User


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
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
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
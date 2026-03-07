"""
API views for Tasks app.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from ..models import Task, TaskAssignment
from ..serializers import (
    TaskSerializer, TaskCreateSerializer,
    TaskAssignmentSerializer, TaskAssignmentCreateSerializer,
    TaskCompletionSerializer, TaskVerificationSerializer,
    AvailableTaskSerializer
)
from apps.campaigns.models import Campaign
from apps.users.models import User


class IsAdminOrCampaignManager(permissions.BasePermission):
    """Permission check for admin or campaign manager."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        if request.user.is_campaign_manager() and obj.campaign.managers.filter(id=request.user.id).exists():
            return True
        return False


class TaskListView(generics.ListCreateAPIView):
    """List tasks or create a new task."""
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['task_type', 'assignment_type', 'is_active', 'campaign']
    search_fields = ['title', 'description', 'instructions']
    ordering_fields = ['created_at', 'points', 'estimated_time']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Filter tasks based on user role."""
        user = self.request.user
        if user.is_admin():
            return Task.objects.all()
        elif user.is_campaign_manager():
            # Campaign managers can see tasks for campaigns they manage
            return Task.objects.filter(campaign__managers=user)
        else:
            # Volunteers can see tasks for campaigns they're part of
            return Task.objects.filter(campaign__volunteers=user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a task."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCampaignManager]


class AvailableTasksView(generics.ListAPIView):
    """List tasks available for the current volunteer."""
    serializer_class = AvailableTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get tasks that are available for the current volunteer."""
        user = self.request.user
        if not user.is_volunteer():
            return Task.objects.none()

        # Get campaigns the volunteer is part of
        volunteer_campaigns = Campaign.objects.filter(volunteers=user)

        # Get available tasks
        return Task.objects.filter(
            campaign__in=volunteer_campaigns,
            is_active=True,
            is_verified=True,
            current_assignments__lt=models.F('max_assignments')
        ).filter(
            models.Q(available_from__isnull=True) | models.Q(available_from__lte=timezone.now())
        ).filter(
            models.Q(available_until__isnull=True) | models.Q(available_until__gte=timezone.now())
        ).exclude(
            assignments__volunteer=user
        ).order_by('-created_at')


class TaskAssignmentView(generics.CreateAPIView):
    """Assign a task to a volunteer."""
    serializer_class = TaskAssignmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = serializer.validated_data['task']
        volunteer = serializer.validated_data.get('volunteer', request.user)

        # Check permissions
        if volunteer != request.user and not request.user.is_admin():
            return Response(
                {'error': _('Only admins can assign tasks to other users.')},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if task is available
        if not task.is_available():
            return Response(
                {'error': _('This task is not available for assignment.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if volunteer is part of the campaign
        if not task.campaign.volunteers.filter(id=volunteer.id).exists():
            return Response(
                {'error': _('Volunteer is not part of this campaign.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if volunteer already has this task assigned
        if TaskAssignment.objects.filter(task=task, volunteer=volunteer).exists():
            return Response(
                {'error': _('Volunteer already has this task assigned.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create assignment
        assignment = TaskAssignment.objects.create(
            task=task,
            volunteer=volunteer,
            campaign=task.campaign,
            assigned_by=request.user if request.user != volunteer else None,
            status=TaskAssignment.Status.ASSIGNED
        )

        return Response(
            TaskAssignmentSerializer(assignment).data,
            status=status.HTTP_201_CREATED
        )


class MyTaskAssignmentsView(generics.ListAPIView):
    """List task assignments for the current user."""
    serializer_class = TaskAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get('status', None)

        queryset = TaskAssignment.objects.filter(volunteer=user)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-assigned_at')


class TaskCompletionView(APIView):
    """Mark a task assignment as completed."""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Submit proof and mark a task assignment as completed",
        request_body=TaskCompletionSerializer,
        responses={200: openapi.Response('Task completed'), 404: openapi.Response('Assignment not found')}
    )
    def post(self, request, assignment_id):
        try:
            assignment = TaskAssignment.objects.get(
                id=assignment_id,
                volunteer=request.user
            )
        except TaskAssignment.DoesNotExist:
            return Response(
                {'error': _('Task assignment not found.')},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if assignment can be completed
        if assignment.status not in [
            TaskAssignment.Status.ASSIGNED,
            TaskAssignment.Status.IN_PROGRESS
        ]:
            return Response(
                {'error': _('This task assignment cannot be completed.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskCompletionSerializer(data=request.data)
        if serializer.is_valid():
            assignment.proof_url = serializer.validated_data.get('proof_url', '')
            assignment.proof_text = serializer.validated_data.get('proof_text', '')
            assignment.proof_image = serializer.validated_data.get('proof_image', '')
            assignment.completion_notes = serializer.validated_data.get('completion_notes', '')
            assignment.status = TaskAssignment.Status.COMPLETED
            assignment.completed_at = timezone.now()
            assignment.save()

            return Response(
                TaskAssignmentSerializer(assignment).data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskVerificationView(APIView):
    """Verify or reject a completed task."""
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCampaignManager]

    @swagger_auto_schema(
        operation_description="Verify or reject a completed task assignment",
        request_body=TaskVerificationSerializer,
        responses={200: openapi.Response('Task verified/rejected'), 404: openapi.Response('Assignment not found')}
    )
    def post(self, request, assignment_id):
        try:
            assignment = TaskAssignment.objects.get(id=assignment_id)
        except TaskAssignment.DoesNotExist:
            return Response(
                {'error': _('Task assignment not found.')},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if assignment can be verified
        if assignment.status != TaskAssignment.Status.COMPLETED:
            return Response(
                {'error': _('Only completed tasks can be verified.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskVerificationSerializer(data=request.data)
        if serializer.is_valid():
            assignment.verification_notes = serializer.validated_data.get('verification_notes', '')
            assignment.verified_by = request.user
            assignment.verified_at = timezone.now()

            if serializer.validated_data['status'] == 'verified':
                assignment.status = TaskAssignment.Status.VERIFIED
                assignment.points_awarded = serializer.validated_data.get(
                    'points_awarded',
                    assignment.task.points
                )
            else:
                assignment.status = TaskAssignment.Status.REJECTED

            assignment.save()

            return Response(
                TaskAssignmentSerializer(assignment).data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
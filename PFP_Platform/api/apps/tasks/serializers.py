"""
Serializers for Tasks app.
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Task, TaskAssignment, KeyTweet
from apps.campaigns.serializers import CampaignSerializer
from apps.users.serializers import UserSerializer
from apps.users.models import User


class KeyTweetSerializer(serializers.ModelSerializer):
    """Serializer for KeyTweet model."""
    class Meta:
        model = KeyTweet
        fields = (
            'id', 'tweet_url', 'author_name', 'author_handle',
            'description', 'order', 'is_active',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    campaign = CampaignSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    key_tweets = KeyTweetSerializer(many=True, read_only=True)
    is_available = serializers.SerializerMethodField()
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'instructions',
            'task_type', 'assignment_type',
            'campaign', 'created_by',
            'points', 'estimated_time',
            'max_assignments', 'current_assignments', 'completed_assignments',
            'target_url', 'hashtags', 'mentions', 'image_url',
            'key_tweets',
            'is_active', 'is_verified', 'is_available',
            'available_from', 'available_until',
            'available_slots',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'created_by', 'current_assignments', 'completed_assignments',
            'created_at', 'updated_at'
        )

    def get_is_available(self, obj):
        """Check if task is available for assignment."""
        return obj.is_available()

    def get_available_slots(self, obj):
        """Calculate available slots."""
        return obj.available_slots()

    def create(self, validated_data):
        """Create a new task."""
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks."""
    key_tweets = KeyTweetSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = (
            'title', 'description', 'instructions',
            'task_type', 'assignment_type',
            'campaign', 'points', 'estimated_time',
            'max_assignments', 'target_url',
            'hashtags', 'mentions', 'image_url',
            'key_tweets',
            'is_active', 'is_verified',
            'available_from', 'available_until'
        )

    def create(self, validated_data):
        """Create task with nested key tweets."""
        key_tweets_data = validated_data.pop('key_tweets', [])
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
        task = Task.objects.create(**validated_data)
        for tweet_data in key_tweets_data:
            KeyTweet.objects.create(task=task, **tweet_data)
        return task


class TaskAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for TaskAssignment model."""
    task = TaskSerializer(read_only=True)
    volunteer = UserSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)

    class Meta:
        model = TaskAssignment
        fields = (
            'id', 'task', 'volunteer', 'campaign',
            'status', 'assigned_by',
            'proof_url', 'proof_text', 'proof_image', 'completion_notes',
            'verification_notes', 'points_awarded', 'verified_by',
            'assigned_at', 'started_at', 'completed_at', 'verified_at',
            'updated_at'
        )
        read_only_fields = (
            'id', 'task', 'volunteer', 'campaign', 'assigned_by',
            'points_awarded', 'verified_by',
            'assigned_at', 'started_at', 'completed_at', 'verified_at',
            'updated_at'
        )


class TaskAssignmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating task assignments."""
    volunteer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = TaskAssignment
        fields = ('task', 'volunteer')


class TaskCompletionSerializer(serializers.Serializer):
    """Serializer for completing a task."""
    proof_url = serializers.URLField(required=False, allow_blank=True)
    proof_text = serializers.CharField(required=False, allow_blank=True)
    proof_image = serializers.URLField(required=False, allow_blank=True)
    completion_notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        """Validate that at least one proof is provided."""
        if not any([data.get('proof_url'), data.get('proof_text'), data.get('proof_image')]):
            raise serializers.ValidationError(
                _('At least one proof (URL, text, or image) is required.')
            )
        return data


class TaskVerificationSerializer(serializers.Serializer):
    """Serializer for verifying a task assignment."""
    status = serializers.ChoiceField(
        choices=['verified', 'rejected']
    )
    verification_notes = serializers.CharField(required=False, allow_blank=True)
    points_awarded = serializers.IntegerField(min_value=0, required=False)

    def validate(self, data):
        """Validate points if status is verified."""
        if data['status'] == 'verified' and 'points_awarded' not in data:
            # Default points will be set from task
            pass
        return data


class AvailableTaskSerializer(serializers.ModelSerializer):
    """Serializer for available tasks (simplified for volunteers)."""
    campaign_name = serializers.CharField(source='campaign.name')
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'task_type',
            'points', 'estimated_time',
            'campaign_name', 'available_slots'
        )

    def get_available_slots(self, obj):
        return obj.available_slots()
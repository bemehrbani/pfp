"""
Serializers for Campaigns app.
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Campaign, CampaignVolunteer, CampaignUpdate, TwitterStorm, StormParticipant
from apps.users.serializers import UserSerializer


class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for Campaign model."""
    created_by = UserSerializer(read_only=True)
    managers = UserSerializer(many=True, read_only=True)
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = (
            'id', 'name', 'description', 'short_description',
            'campaign_type', 'status',
            'target_members', 'target_activities', 'target_twitter_posts',
            'twitter_hashtags', 'twitter_accounts', 'twitter_storm_schedule',
            'telegram_channel_id', 'telegram_group_id',
            'created_by', 'managers',
            'start_date', 'end_date', 'actual_start_date', 'actual_end_date',
            'current_members', 'completed_activities', 'completed_twitter_posts',
            'total_points_awarded',
            'progress_percentage',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'created_by', 'current_members', 'completed_activities',
            'completed_twitter_posts', 'total_points_awarded',
            'created_at', 'updated_at'
        )

    def get_progress_percentage(self, obj):
        """Calculate progress percentage."""
        return obj.progress_percentage()

    def create(self, validated_data):
        """Create a new campaign."""
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class CampaignCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating campaigns."""
    class Meta:
        model = Campaign
        fields = (
            'name', 'description', 'short_description',
            'campaign_type', 'status',
            'target_members', 'target_activities', 'target_twitter_posts',
            'twitter_hashtags', 'twitter_accounts',
            'telegram_channel_id', 'telegram_group_id',
            'start_date', 'end_date'
        )


class CampaignVolunteerSerializer(serializers.ModelSerializer):
    """Serializer for CampaignVolunteer model."""
    volunteer = UserSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)

    class Meta:
        model = CampaignVolunteer
        fields = (
            'id', 'campaign', 'volunteer', 'status',
            'points_earned', 'joined_at', 'last_active'
        )
        read_only_fields = ('id', 'campaign', 'volunteer', 'points_earned', 'joined_at', 'last_active')


class CampaignUpdateSerializer(serializers.ModelSerializer):
    """Serializer for CampaignUpdate model."""
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = CampaignUpdate
        fields = (
            'id', 'campaign', 'title', 'content',
            'created_by', 'is_pinned', 'sent_to_telegram',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_by', 'sent_to_telegram', 'created_at', 'updated_at')


class CampaignStatsSerializer(serializers.Serializer):
    """Serializer for campaign statistics."""
    total_campaigns = serializers.IntegerField()
    active_campaigns = serializers.IntegerField()
    total_volunteers = serializers.IntegerField()
    total_points_awarded = serializers.IntegerField()
    completion_rate = serializers.FloatField()


class TwitterStormScheduleSerializer(serializers.Serializer):
    """Serializer for Twitter storm schedule."""
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    posts_per_hour = serializers.IntegerField(min_value=1, max_value=60)
    assigned_volunteers = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )


class StormParticipantSerializer(serializers.ModelSerializer):
    """Serializer for StormParticipant model."""
    volunteer = UserSerializer(read_only=True)

    class Meta:
        model = StormParticipant
        fields = (
            'id', 'storm', 'volunteer', 'status',
            'tweet_text', 'tweet_url', 'posted_at', 'created_at'
        )
        read_only_fields = ('id', 'storm', 'volunteer', 'created_at')


class TwitterStormSerializer(serializers.ModelSerializer):
    """Serializer for TwitterStorm model (read)."""
    created_by = UserSerializer(read_only=True)
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = TwitterStorm
        fields = (
            'id', 'campaign', 'created_by', 'title', 'description',
            'scheduled_at', 'duration_minutes', 'status',
            'tweet_templates', 'hashtags', 'mentions',
            'notify_1h', 'notify_15m', 'notify_5m',
            'participants_notified', 'tweets_posted',
            'participants_count',
            'activated_at', 'completed_at', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'created_by', 'status',
            'participants_notified', 'tweets_posted',
            'activated_at', 'completed_at', 'created_at', 'updated_at'
        )

    def get_participants_count(self, obj):
        """Count storm participants."""
        return obj.participants.count()


class TwitterStormCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/scheduling a TwitterStorm."""

    class Meta:
        model = TwitterStorm
        fields = (
            'title', 'description', 'scheduled_at', 'duration_minutes',
            'tweet_templates', 'hashtags', 'mentions',
            'notify_1h', 'notify_15m', 'notify_5m'
        )
"""
Utility to wrap synchronous Django ORM calls for use in async Telegram handlers.

Django's ORM is synchronous. python-telegram-bot v20+ uses async handlers.
This module provides the bridge using Django's sync_to_async.
"""
from asgiref.sync import sync_to_async


def db_sync(func):
    """
    Decorator to wrap a synchronous function (containing Django ORM calls)
    for use in async contexts.

    Usage:
        @db_sync
        def get_user(telegram_id):
            return User.objects.get(telegram_id=telegram_id)

        # In async handler:
        user = await get_user(telegram_id)
    """
    return sync_to_async(func, thread_sensitive=True)


# Common database operations as async-safe functions

@db_sync
def get_session(telegram_id):
    """Get TelegramSession by telegram_id."""
    from apps.telegram.models import TelegramSession
    try:
        return TelegramSession.objects.select_related('user').get(telegram_id=telegram_id)
    except TelegramSession.DoesNotExist:
        return None


@db_sync
def get_session_language(telegram_id):
    """Get language preference for a telegram user. Returns 'en' as default."""
    from apps.telegram.models import TelegramSession
    try:
        return TelegramSession.objects.values_list('language', flat=True).get(telegram_id=telegram_id)
    except TelegramSession.DoesNotExist:
        return 'en'


@db_sync
def get_user_by_telegram_id(telegram_id):
    """Get User by telegram_id field."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None


@db_sync
def get_active_campaigns():
    """Get all active campaigns."""
    from apps.campaigns.models import Campaign
    return list(Campaign.objects.filter(status=Campaign.Status.ACTIVE))


@db_sync
def get_campaign(campaign_id):
    """Get a campaign by ID."""
    from apps.campaigns.models import Campaign
    try:
        return Campaign.objects.get(id=campaign_id, status=Campaign.Status.ACTIVE)
    except Campaign.DoesNotExist:
        return None


@db_sync
def is_volunteer(campaign, user):
    """Check if user is a volunteer for a campaign."""
    from apps.campaigns.models import CampaignVolunteer
    return CampaignVolunteer.objects.filter(campaign=campaign, volunteer=user).exists()


@db_sync
def join_campaign(campaign, user):
    """Add user as volunteer to campaign."""
    from apps.campaigns.models import CampaignVolunteer
    cv, created = CampaignVolunteer.objects.get_or_create(
        campaign=campaign,
        volunteer=user,
        defaults={'status': 'active'}
    )
    if created:
        campaign.current_members = campaign.volunteers.count()
        campaign.save(update_fields=['current_members'])
    return created


@db_sync
def get_available_tasks(campaign_ids):
    """Get available tasks for given campaign IDs."""
    from apps.tasks.models import Task
    # Only show Twitter storm tasks for now — remove task_type filter to show all
    return list(Task.objects.filter(
        campaign_id__in=campaign_ids,
        status='active',
        task_type__in=['twitter_post', 'twitter_retweet']
    ).select_related('campaign'))


@db_sync
def get_task(task_id):
    """Get a task by ID."""
    from apps.tasks.models import Task
    try:
        return Task.objects.select_related('campaign').get(id=task_id)
    except Task.DoesNotExist:
        return None


@db_sync
def get_user_task_assignments(user, status=None):
    """Get task assignments for a user."""
    from apps.tasks.models import TaskAssignment
    qs = TaskAssignment.objects.filter(volunteer=user).select_related('task', 'task__campaign')
    if status:
        qs = qs.filter(status=status)
    return list(qs)


@db_sync
def create_task_assignment(task, user):
    """Create a task assignment."""
    from apps.tasks.models import TaskAssignment
    if TaskAssignment.objects.filter(task=task, volunteer=user).exists():
        return None
    return TaskAssignment.objects.create(
        task=task,
        campaign=task.campaign,
        volunteer=user,
        status='in_progress'
    )


@db_sync
def get_task_assignment(assignment_id, user=None):
    """Get a task assignment by ID."""
    from apps.tasks.models import TaskAssignment
    try:
        qs = TaskAssignment.objects.select_related('task', 'task__campaign')
        if user:
            return qs.get(id=assignment_id, volunteer=user)
        return qs.get(id=assignment_id)
    except TaskAssignment.DoesNotExist:
        return None


@db_sync
def submit_task_proof(assignment, proof_url, proof_text=''):
    """Submit proof for a task assignment."""
    from django.utils import timezone
    assignment.proof_url = proof_url
    assignment.proof_text = proof_text
    assignment.status = 'submitted'
    assignment.submitted_at = timezone.now()
    assignment.save()
    return assignment


@db_sync
def get_user_campaigns(user):
    """Get campaign IDs the user is a volunteer for."""
    from apps.campaigns.models import CampaignVolunteer
    return list(CampaignVolunteer.objects.filter(
        volunteer=user,
        status='active'
    ).values_list('campaign_id', flat=True))


@db_sync
def get_leaderboard_users(campaign_id=None, limit=10):
    """Get leaderboard data."""
    from django.contrib.auth import get_user_model
    from apps.campaigns.models import CampaignVolunteer
    User = get_user_model()

    qs = User.objects.filter(role='volunteer', is_active=True)
    if campaign_id:
        user_ids = CampaignVolunteer.objects.filter(
            campaign_id=campaign_id, status='active'
        ).values_list('volunteer_id', flat=True)
        qs = qs.filter(id__in=user_ids)
    return list(qs.order_by('-total_points')[:limit])


@db_sync
def get_user_profile(user):
    """Get user profile data with stats."""
    from apps.tasks.models import TaskAssignment
    from apps.campaigns.models import CampaignVolunteer
    from django.db.models import Count, Q

    task_stats = TaskAssignment.objects.filter(volunteer=user).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='completed')),
        in_progress=Count('id', filter=Q(status='in_progress')),
    )
    campaign_count = CampaignVolunteer.objects.filter(
        volunteer=user, status='active'
    ).count()

    return {
        'task_stats': task_stats,
        'campaign_count': campaign_count,
    }


@db_sync
def create_or_get_session(telegram_id, telegram_chat_id, user=None, **extra):
    """Create or get a TelegramSession."""
    from apps.telegram.models import TelegramSession
    session, created = TelegramSession.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'telegram_chat_id': telegram_chat_id,
            'user': user,
            **extra,
        }
    )
    return session, created


@db_sync
def update_session_user(session, user):
    """Link a user to a session."""
    session.user = user
    session.save(update_fields=['user'])
    return session


@db_sync
def create_user(**kwargs):
    """Create a new user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.create_user(**kwargs)
    return user


@db_sync
def user_exists_by_email(email):
    """Check if a user with this email exists."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.filter(email=email).exists()


@db_sync
def get_storms_for_user(user):
    """Get upcoming storms for a user's campaigns."""
    from apps.campaigns.models import TwitterStorm, CampaignVolunteer

    campaign_ids = CampaignVolunteer.objects.filter(
        volunteer=user,
        status='active'
    ).values_list('campaign_id', flat=True)

    return list(TwitterStorm.objects.filter(
        campaign_id__in=campaign_ids,
        status__in=['scheduled', 'countdown', 'active']
    ).order_by('scheduled_at')[:5])


@db_sync
def get_storm(storm_id):
    """Get a storm by ID."""
    from apps.campaigns.models import TwitterStorm
    try:
        return TwitterStorm.objects.get(id=storm_id)
    except TwitterStorm.DoesNotExist:
        return None


@db_sync
def mark_storm_participant_ready(storm_id, user):
    """Mark a user as ready for a storm."""
    from apps.campaigns.models import StormParticipant
    sp, created = StormParticipant.objects.update_or_create(
        storm_id=storm_id,
        volunteer=user,
        defaults={'status': 'ready'}
    )
    return sp

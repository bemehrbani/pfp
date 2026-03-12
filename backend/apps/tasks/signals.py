"""
Signals for Tasks app.
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Task, TaskAssignment
from apps.analytics.models import ActivityLog

logger = logging.getLogger(__name__)

# Milestone thresholds to trigger channel broadcasts
MILESTONE_THRESHOLDS = [10, 25, 50, 75, 100]


def _check_and_broadcast_milestone(assignment):
    """
    Check if a task completion crosses a milestone threshold for the campaign.
    Uses Django cache to prevent duplicate broadcasts.
    """
    from django.core.cache import cache

    campaign = assignment.task.campaign
    if not campaign or not campaign.target_activities:
        return

    current = campaign.completed_activities + 1  # +1 for the one just completed
    target = campaign.target_activities
    percentage = int((current / target) * 100)

    for threshold in MILESTONE_THRESHOLDS:
        if percentage >= threshold:
            cache_key = f'milestone_{campaign.id}_{threshold}'
            if cache.get(cache_key):
                continue  # Already broadcasted this milestone

            # Mark milestone as broadcasted (24h TTL)
            cache.set(cache_key, True, timeout=86400)

            from apps.campaigns.tasks import broadcast_milestone
            broadcast_milestone.delay(
                campaign_id=campaign.id,
                metric='activities',
                current=current,
                target=target,
                percentage=threshold,
            )
            logger.info(f'Milestone {threshold}% triggered for campaign {campaign.id}')


@receiver(post_save, sender=Task)
def task_created_or_updated(sender, instance, created, **kwargs):
    """Log task creation and updates."""
    if created:
        ActivityLog.objects.create(
            user=instance.created_by,
            action_type=ActivityLog.ActionType.TASK_CREATE,
            description=f'Task "{instance.title}" created for campaign "{instance.campaign.name}"',
            content_object=instance
        )
        logger.info(f'Task created: {instance.title} (id: {instance.id})')
    else:
        # Log important updates
        changed_fields = getattr(instance, '_changed_fields', set())
        if instance.is_active and 'is_active' in changed_fields:
            ActivityLog.objects.create(
                user=instance.created_by,
                action_type=ActivityLog.ActionType.TASK_UPDATE,
                description=f'Task "{instance.title}" {"activated" if instance.is_active else "deactivated"}',
                content_object=instance
            )
            logger.info(f'Task {instance.title} {"activated" if instance.is_active else "deactivated"}')


@receiver(post_save, sender=TaskAssignment)
def task_assignment_created_or_updated(sender, instance, created, **kwargs):
    """Log task assignment creation and status changes."""
    if created:
        ActivityLog.objects.create(
            user=instance.volunteer,
            action_type=ActivityLog.ActionType.TASK_ASSIGN,
            description=f'Task "{instance.task.title}" assigned to {instance.volunteer.username}',
            content_object=instance.task
        )
        logger.info(f'Task {instance.task.title} assigned to {instance.volunteer.username}')

    else:
        # Check for status changes
        changed_fields = getattr(instance, '_changed_fields', set())
        if 'status' in changed_fields:
            # Map status to action type
            status_actions = {
                TaskAssignment.Status.IN_PROGRESS: 'started',
                TaskAssignment.Status.COMPLETED: ActivityLog.ActionType.TASK_COMPLETE,
                TaskAssignment.Status.VERIFIED: ActivityLog.ActionType.TASK_VERIFY,
                TaskAssignment.Status.REJECTED: 'rejected',
            }

            if instance.status in status_actions:
                action = status_actions[instance.status]
                if isinstance(action, str):
                    # Simple string action
                    description = f'Task "{instance.task.title}" {action} by {instance.volunteer.username}'
                    action_type = ActivityLog.ActionType.TASK_UPDATE
                else:
                    # Full action type enum
                    action_type = action
                    description = f'Task "{instance.task.title}" {instance.status} by {instance.volunteer.username}'

                # Log the activity
                ActivityLog.objects.create(
                    user=instance.volunteer if instance.status in ['completed', 'in_progress'] else instance.verified_by,
                    action_type=action_type,
                    description=description,
                    content_object=instance.task,
                    metadata={
                        'task_id': instance.task.id,
                        'assignment_id': instance.id,
                        'new_status': instance.status,
                        'points_awarded': instance.points_awarded if instance.status == 'verified' else 0
                    }
                )

                logger.info(f'Task {instance.task.title} status changed to {instance.status}')

            # Update campaign statistics when task is verified
            if instance.status == TaskAssignment.Status.VERIFIED:
                instance.campaign.update_statistics()

            # ── Milestone detection on completion ──
            if instance.status in (TaskAssignment.Status.COMPLETED, TaskAssignment.Status.VERIFIED):
                _check_and_broadcast_milestone(instance)


@receiver(post_save, sender=TaskAssignment)
def update_user_points(sender, instance, **kwargs):
    """Update user points when task is verified."""
    if instance.status == TaskAssignment.Status.VERIFIED:
        # Points are awarded in the model's save method
        # This signal is for additional processing if needed
        pass


@receiver(post_save, sender=TaskAssignment)
def send_notification_on_completion(sender, instance, **kwargs):
    """Send notification when task is completed and needs verification."""
    if instance.status == TaskAssignment.Status.COMPLETED:
        # TODO: Send notification to campaign managers
        # This could be implemented with Django Channels or Celery
        logger.info(f'Task {instance.task.title} completed, waiting verification')

        # Create activity log for completion
        ActivityLog.objects.create(
            user=instance.volunteer,
            action_type=ActivityLog.ActionType.TASK_COMPLETE,
            description=f'Task "{instance.task.title}" completed by {instance.volunteer.username}',
            content_object=instance.task,
            metadata={
                'proof_url': instance.proof_url,
                'proof_text': instance.proof_text[:100] if instance.proof_text else None
            }
        )
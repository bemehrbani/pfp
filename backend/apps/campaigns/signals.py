"""
Signals for Campaigns app.
"""
import logging
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from .models import Campaign, CampaignVolunteer, CampaignUpdate
from apps.analytics.models import ActivityLog

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Campaign)
def campaign_created_or_updated(sender, instance, created, **kwargs):
    """Log campaign creation and updates."""
    if created:
        ActivityLog.objects.create(
            user=instance.created_by,
            action_type=ActivityLog.ActionType.CAMPAIGN_CREATE,
            description=f'Campaign "{instance.name}" created',
            content_object=instance
        )
        logger.info(f'Campaign created: {instance.name} (id: {instance.id})')
    else:
        # Check if status changed
        if 'status' in instance._changed_fields:
            ActivityLog.objects.create(
                user=instance.created_by,
                action_type=ActivityLog.ActionType.CAMPAIGN_UPDATE,
                description=f'Campaign "{instance.name}" status changed to {instance.status}',
                content_object=instance,
                metadata={'new_status': instance.status}
            )
            logger.info(f'Campaign {instance.name} status changed to {instance.status}')


@receiver(post_save, sender=CampaignVolunteer)
def volunteer_joined_campaign(sender, instance, created, **kwargs):
    """Log volunteer joining a campaign."""
    if created:
        ActivityLog.objects.create(
            user=instance.volunteer,
            action_type=ActivityLog.ActionType.CAMPAIGN_JOIN,
            description=f'User {instance.volunteer.username} joined campaign "{instance.campaign.name}"',
            content_object=instance.campaign
        )
        logger.info(f'User {instance.volunteer.username} joined campaign {instance.campaign.name}')

        # Update campaign statistics
        instance.campaign.update_statistics()


@receiver(m2m_changed, sender=Campaign.managers.through)
def campaign_managers_changed(sender, instance, action, pk_set, **kwargs):
    """Log changes to campaign managers."""
    if action == 'post_add':
        from apps.users.models import User
        added_managers = User.objects.filter(pk__in=pk_set)
        for manager in added_managers:
            ActivityLog.objects.create(
                user=manager,
                action_type=ActivityLog.ActionType.CAMPAIGN_UPDATE,
                description=f'User {manager.username} added as manager to campaign "{instance.name}"',
                content_object=instance
            )
            logger.info(f'User {manager.username} added as manager to campaign {instance.name}')
    elif action == 'post_remove':
        from apps.users.models import User
        removed_managers = User.objects.filter(pk__in=pk_set)
        for manager in removed_managers:
            ActivityLog.objects.create(
                user=instance.created_by if instance.created_by else manager,
                action_type=ActivityLog.ActionType.CAMPAIGN_UPDATE,
                description=f'User {manager.username} removed as manager from campaign "{instance.name}"',
                content_object=instance
            )
            logger.info(f'User {manager.username} removed as manager from campaign {instance.name}')


@receiver(post_save, sender=CampaignUpdate)
def campaign_update_created(sender, instance, created, **kwargs):
    """Log campaign update creation."""
    if created:
        ActivityLog.objects.create(
            user=instance.created_by,
            action_type=ActivityLog.ActionType.CAMPAIGN_UPDATE,
            description=f'Update "{instance.title}" created for campaign "{instance.campaign.name}"',
            content_object=instance.campaign
        )
        logger.info(f'Campaign update created: {instance.title} for campaign {instance.campaign.name}')


@receiver(post_save, sender=Campaign)
def update_campaign_statistics(sender, instance, **kwargs):
    """Update campaign statistics after save."""
    # This is called from the model's save method, but we keep it as a signal
    # for other related updates
    pass